#!/usr/bin/env python3
"""Build client approval packet from business profile data."""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    """Load JSON file or return empty dict if missing."""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def get_value(field: dict) -> str:
    """Extract value from field with possible confidence wrapper."""
    if isinstance(field, str):
        return field
    if isinstance(field, dict) and "value" in field:
        return field["value"]
    return str(field) if field else ""


def format_list(items: list, key: str = "name") -> list:
    """Format list of items for display."""
    if not items:
        return []
    result = []
    for item in items:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            val = item.get(key) or item.get("value") or item.get("question", "")
            result.append(val)
    return result


def get_field_fact_type(field) -> str:
    """Extract fact type from field."""
    if isinstance(field, dict):
        return field.get("factType", "unknown")
    return "direct"


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/build_approval_packet.py businesses/<customer-slug>")
        sys.exit(1)

    business_path = Path(sys.argv[1])
    customer_slug = business_path.name

    profile = load_json(business_path / "profile.json")
    sources = load_json(business_path / "sources.json")
    registry = load_json(business_path / "registry-entry.json")

    legal_name = get_value(profile.get("legalName", {}))
    brand_name = get_value(profile.get("brandName", {}))
    domain = profile.get("domain", "")
    short_desc = get_value(profile.get("shortDescription", {}))
    full_desc = get_value(profile.get("description", {}))
    business_category = get_value(profile.get("businessCategory", {}))

    services = format_list(profile.get("services", []), "name")
    products = format_list(profile.get("products", []), "name")
    locations = format_list(profile.get("locations", []), "name")
    service_areas = format_list(profile.get("serviceAreas", []), "value")
    industries = format_list(profile.get("industriesServed", []), "value")
    faqs = profile.get("faqs", [])

    source_map = {s["id"]: s for s in sources.get("sources", [])}

    claims = []
    source_backed = []

    for key, label in [
        ("legalName", "Legal Name"),
        ("brandName", "Brand Name"),
        ("shortDescription", "Short Description"),
        ("description", "Full Description"),
        ("businessCategory", "Business Category"),
    ]:
        if key in profile:
            field = profile[key]
            source_ids = field.get("sourceIds", [])
            fact_type = field.get("factType", "unknown")
            confidence = field.get("confidence", 0.0)

            source_names = [source_map.get(sid, {}).get("title", sid) for sid in source_ids]

            claim = f"- **{label}**: {get_value(field)} ({fact_type})"
            claims.append(claim)

            if source_ids:
                source_backed.append(f"- {label}: \"{get_value(field)}\" — Source: {', '.join(source_names)}")

    missing = []
    if not legal_name:
        missing.append("Legal Name")
    if not short_desc:
        missing.append("Short Description")
    if not full_desc:
        missing.append("Full Description")
    if not services:
        missing.append("Services")
    if not products:
        missing.append("Products")
    if not locations:
        missing.append("Locations")
    if not industries:
        missing.append("Industries Served")

    today = datetime.now().strftime("%Y-%m-%d")

    output = []
    output.append(f"# Client Approval Packet")
    output.append(f"")
    output.append(f"**Customer**: {brand_name or customer_slug}")
    output.append(f"**Domain**: {domain}")
    output.append(f"**Generated**: {today}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Business Overview")
    output.append(f"")
    output.append(f"### Proposed Short Description")
    output.append(f"")
    output.append(f"> {short_desc}")
    output.append(f"")
    output.append(f"### Proposed Full Description")
    output.append(f"")
    output.append(f"> {full_desc}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Services")
    output.append(f"")
    for svc in services:
        output.append(f"- {svc}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Products")
    output.append(f"")
    for prod in products:
        output.append(f"- {prod}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Locations")
    output.append(f"")
    for loc in locations:
        output.append(f"- {loc}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Service Areas")
    output.append(f"")
    for area in service_areas:
        output.append(f"- {area}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Industries Served")
    output.append(f"")
    for ind in industries:
        output.append(f"- {ind}")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## FAQs")
    output.append(f"")
    for faq in faqs:
        output.append(f"**Q: {faq.get('question', '')}**")
        output.append(f"A: {faq.get('answer', '')}")
        output.append(f"")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Claims Requiring Approval")
    output.append(f"")
    for claim in claims:
        output.append(claim)
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Source-Backed Claims")
    output.append(f"")
    if source_backed:
        for claim in source_backed:
            output.append(claim)
    else:
        output.append(f"_No source-backed claims available._")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Missing Information")
    output.append(f"")
    if missing:
        for m in missing:
            output.append(f"- {m}")
    else:
        output.append(f"_All key information appears to be present._")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Registry Entry Preview")
    output.append(f"")
    if registry:
        output.append(f"```json")
        output.append(json.dumps(registry, indent=2))
        output.append(f"```")
    else:
        output.append(f"_No registry entry available._")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"## Approval Checklist")
    output.append(f"")
    output.append(f"Please review and approve the following:")
    output.append(f"")
    output.append(f"- [ ] Business name and domain are correct")
    output.append(f"- [ ] Short description is accurate")
    output.append(f"- [ ] Full description is accurate")
    output.append(f"- [ ] Services are correctly listed")
    output.append(f"- [ ] Products are correctly listed")
    output.append(f"- [ ] Locations are correct")
    output.append(f"- [ ] Service areas are correct")
    output.append(f"- [ ] Industries served are correct")
    output.append(f"- [ ] FAQs are accurate")
    output.append(f"- [ ] All claims are verified")
    output.append(f"")
    output.append(f"---")
    output.append(f"")
    output.append(f"_Please respond with your approval or requested changes._")
    output.append(f"")

    output_path = business_path / "approval-packet.md"
    output_path.write_text("\n".join(output), encoding="utf-8")
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
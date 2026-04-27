#!/usr/bin/env python3
"""
Build a lightweight public registry entry from a rich customer profile.

Usage:
  python scripts/build_registry_entry.py businesses/example-co
"""

import json
import sys
from pathlib import Path


def claim_value(item: object, fallback: str = "") -> str:
    if isinstance(item, dict):
        value = item.get("value")
        if isinstance(value, str):
            return value
    if isinstance(item, str):
        return item
    return fallback


def to_simple_strings(items: object) -> list[str]:
    values: list[str] = []
    if not isinstance(items, list):
        return values
    for item in items:
        if isinstance(item, str):
            values.append(item)
        elif isinstance(item, dict):
            name = item.get("name")
            value = item.get("value")
            if isinstance(name, str):
                values.append(name)
            elif isinstance(value, str):
                values.append(value)
    return values


def to_location_strings(locations: object) -> list[str]:
    values: list[str] = []
    if not isinstance(locations, list):
        return values
    for loc in locations:
        if not isinstance(loc, dict):
            continue
        name = loc.get("name")
        city = loc.get("city")
        region = loc.get("region")
        country = loc.get("country")
        parts = [p for p in [city, region, country] if isinstance(p, str) and p.strip()]
        location_text = ", ".join(parts)
        if isinstance(name, str) and name.strip():
            values.append(f"{name} ({location_text})" if location_text else name)
        elif location_text:
            values.append(location_text)
    return values


def build_verification_summary(profile: dict) -> dict:
    approval = profile.get("approval", {})
    if not isinstance(approval, dict):
        approval = {}
    return {
        "verificationStatus": profile.get("verificationStatus"),
        "confidenceScore": profile.get("confidenceScore"),
        "approvalStatus": approval.get("status"),
        "approvedAt": approval.get("approvedAt"),
    }


def build_entry(slug: str, profile: dict) -> dict:
    domain = profile.get("domain", "")
    if isinstance(domain, str) and domain:
        source_website = f"https://{domain}"
    else:
        source_website = None

    return {
        "vizaiId": profile.get("vizaiId", slug),
        "businessName": claim_value(profile.get("brandName"), slug),
        "legalName": claim_value(profile.get("legalName"), ""),
        "domain": domain,
        "shortDescription": claim_value(profile.get("shortDescription"), ""),
        "businessCategory": claim_value(profile.get("businessCategory"), ""),
        "services": to_simple_strings(profile.get("services")),
        "products": to_simple_strings(profile.get("products")),
        "industriesServed": to_simple_strings(profile.get("industriesServed")),
        "locations": to_location_strings(profile.get("locations")),
        "serviceAreas": to_simple_strings(profile.get("serviceAreas")),
        "profileUrl": f"https://raw.githubusercontent.com/{{ORG}}/{{REPO}}/main/businesses/{slug}/profile.json",
        "jsonLdUrl": f"https://raw.githubusercontent.com/{{ORG}}/{{REPO}}/main/businesses/{slug}/profile.jsonld",
        "sourceWebsite": source_website,
        "lastVerified": profile.get("lastReviewed"),
        "lastUpdated": profile.get("lastUpdated"),
        "status": profile.get("status"),
        "verificationSummary": build_verification_summary(profile),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/build_registry_entry.py businesses/<customer-slug>")
        return 1

    repo_root = Path(__file__).parent.parent
    customer_dir = (repo_root / sys.argv[1]).resolve()
    if not customer_dir.exists() or not customer_dir.is_dir():
        print(f"Customer directory not found: {sys.argv[1]}")
        return 1

    profile_path = customer_dir / "profile.json"
    if not profile_path.exists():
        print(f"Missing profile.json: {profile_path}")
        return 1

    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    slug = customer_dir.name
    entry = build_entry(slug, profile)
    out_path = customer_dir / "registry-entry.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

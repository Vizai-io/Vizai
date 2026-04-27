#!/usr/bin/env python3
"""Export registry entry for publication to business-registry repo."""

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    """Load JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def validate_against_schema(entry: dict, schema: dict) -> tuple[bool, list[str]]:
    """Validate entry against schema."""
    errors = []

    for field in schema.get("required", []):
        if field not in entry:
            errors.append(f"Missing required field: {field}")

    props = schema.get("properties", {})
    for field, spec in props.items():
        if field in entry:
            val = entry[field]
            if spec.get("type") == "string" and not isinstance(val, str):
                errors.append(f"Field '{field}' must be a string")
            if spec.get("type") == "array" and not isinstance(val, list):
                errors.append(f"Field '{field}' must be an array")

    return len(errors) == 0, errors


def infer_country_region_city(entry: dict) -> tuple[str, str, str]:
    """Infer country, region, city from location data."""
    locations = entry.get("locations", [])

    for loc in locations:
        if isinstance(loc, str):
            loc_lower = loc.lower()
            if "san francisco" in loc_lower or "ca" in loc_lower:
                return "US", "CA", "San Francisco"
            if "new york" in loc_lower or "ny" in loc_lower:
                return "US", "NY", "New York"
            if "london" in loc_lower:
                return "GB", "LDN", "London"

    return "US", "CA", "Unknown"


def clean_entry(entry: dict) -> dict:
    """Transform full registry entry to lightweight discovery format."""
    slug = entry.get("vizaiId") or entry.get("slug", "")
    name = entry.get("businessName") or entry.get("name", "")
    domain = entry.get("domain", "")
    short_desc = entry.get("shortDescription", "")
    category = entry.get("businessCategory", "")
    services = entry.get("services", [])
    products = entry.get("products", [])

    country, region, city = infer_country_region_city(entry)

    clean = {
        "slug": slug,
        "name": name,
        "domain": domain,
        "shortDescription": short_desc,
        "profileUrl": entry.get("profileUrl", ""),
        "industry": entry.get("industriesServed", []),
        "services": services,
        "products": products,
        "location": {
            "country": country,
            "region": region,
            "city": city
        },
        "updatedAt": entry.get("lastUpdated") or entry.get("updatedAt", ""),
        "status": entry.get("status", "draft")
    }

    return {k: v for k, v in clean.items() if v}


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/export_registry_entry.py businesses/<customer-slug>")
        sys.exit(1)

    business_path = Path(sys.argv[1])
    customer_slug = business_path.name

    schema_path = Path("schema/registry-entry.schema.json")
    registry_path = business_path / "registry-entry.json"

    if not registry_path.exists():
        print(f"Error: {registry_path} not found")
        sys.exit(1)

    schema = load_json(schema_path)
    entry = load_json(registry_path)

    valid, errors = validate_against_schema(entry, schema)
    if not valid:
        print("Validation warnings:")
        for err in errors:
            print(f"  - {err}")

    clean = clean_entry(entry)

    output_dir = Path("registry")
    country = clean.get("location", {}).get("country", "US")
    region = clean.get("location", {}).get("region", "XX")
    city = clean.get("location", {}).get("city", "Unknown")

    output_dir = output_dir / country / region / city
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{customer_slug}.json"
    output_path.write_text(json.dumps(clean, indent=2), encoding="utf-8")

    suggested_path = f"registry/{country}/{region}/{city}/{customer_slug}.json"
    print(f"Exported: {output_path}")
    print(f"Suggested copy path: {suggested_path}")
    print(f"Status: {clean.get('status', 'draft')}")


if __name__ == "__main__":
    main()
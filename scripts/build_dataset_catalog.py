#!/usr/bin/env python3
"""
Build dataset-catalog.json from active customer profiles.
"""

import json
from datetime import date
from pathlib import Path

CATALOG_NAME = "VizAI AI Data Hub"
CATALOG_URL = "https://github.com/vizai-io/vizai"
SCHEMA_REFS = {
    "businessProfile": "schema/business-profile.schema.json",
    "service": "schema/service.schema.json",
    "product": "schema/product.schema.json",
    "location": "schema/location.schema.json",
    "source": "schema/source.schema.json",
    "approval": "schema/approval.schema.json",
    "registryEntry": "schema/registry-entry.schema.json",
}


def read_json(path: Path) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        return None
    return None


def claim_value(value: object) -> str:
    if isinstance(value, dict):
        inner = value.get("value")
        if isinstance(inner, str):
            return inner
    if isinstance(value, str):
        return value
    return ""


def is_active_profile(profile: dict) -> bool:
    status = profile.get("status")
    return isinstance(status, str) and status != "archived"


def build_dataset_item(slug: str, profile: dict, customer_dir: Path) -> dict:
    profile_rel = f"businesses/{slug}/profile.json"
    registry_rel = f"businesses/{slug}/registry-entry.json"
    profile_ld_rel = f"businesses/{slug}/profile.jsonld"
    return {
        "@type": "Dataset",
        "name": f"{claim_value(profile.get('brandName')) or slug} Dataset",
        "description": claim_value(profile.get("shortDescription")),
        "identifier": profile.get("vizaiId", slug),
        "status": profile.get("status"),
        "dateModified": profile.get("lastUpdated"),
        "profilePath": profile_rel,
        "profileJsonLdPath": profile_ld_rel if (customer_dir / "profile.jsonld").exists() else None,
        "registryEntryPath": registry_rel if (customer_dir / "registry-entry.json").exists() else None,
    }


def main() -> int:
    repo_root = Path(__file__).parent.parent
    businesses_dir = repo_root / "businesses"
    datasets = []

    if not businesses_dir.exists():
        print("No businesses directory found.")
        return 1

    for customer_dir in sorted(businesses_dir.iterdir()):
        if not customer_dir.is_dir() or customer_dir.name.startswith("."):
            continue
        slug = customer_dir.name
        profile_path = customer_dir / "profile.json"
        if not profile_path.exists():
            continue
        profile = read_json(profile_path)
        if not profile:
            print(f"Skipping {slug}: invalid profile.json")
            continue
        if not is_active_profile(profile):
            continue
        datasets.append(build_dataset_item(slug, profile, customer_dir))

    catalog = {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "name": CATALOG_NAME,
        "url": CATALOG_URL,
        "dateModified": date.today().isoformat(),
        "businessCount": len(datasets),
        "schemaReferences": SCHEMA_REFS,
        "dataset": datasets,
    }

    out_path = repo_root / "dataset-catalog.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

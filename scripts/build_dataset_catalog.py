#!/usr/bin/env python3
"""
Build dataset-catalog.json from customer profile manifests.
"""

import json
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).parent.parent
    businesses_dir = repo_root / "businesses"
    datasets = []

    for customer_dir in sorted(businesses_dir.iterdir()):
        if not customer_dir.is_dir() or customer_dir.name.startswith("."):
            continue
        slug = customer_dir.name
        profile_path = customer_dir / "profile.json"
        if not profile_path.exists():
            continue
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        manifest_url = f"https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/{slug}/manifest.json"
        datasets.append(
            {
                "@type": "Dataset",
                "name": f"{profile.get('name', slug)} Dataset",
                "description": profile.get("description", ""),
                "url": manifest_url,
                "dateModified": profile.get("updatedAt", ""),
            }
        )

    catalog = {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "name": "VizAI AI Data Hub",
        "url": "https://github.com/vizai-io/vizai",
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

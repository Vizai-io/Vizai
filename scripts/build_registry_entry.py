#!/usr/bin/env python3
"""
Build lightweight registry entries from rich customer profiles.
"""

import json
from pathlib import Path


def build_entry(slug: str, profile: dict) -> dict:
    return {
        "slug": slug,
        "name": profile.get("name", slug),
        "profileUrl": f"https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/{slug}/profile.json",
        "industry": profile.get("industries", []),
        "updatedAt": profile.get("updatedAt"),
    }


def main() -> int:
    repo_root = Path(__file__).parent.parent
    businesses_dir = repo_root / "businesses"
    out_path = repo_root / "registry-entries.json"
    entries = []

    for customer_dir in sorted(businesses_dir.iterdir()):
        if not customer_dir.is_dir() or customer_dir.name.startswith("."):
            continue
        profile_path = customer_dir / "profile.json"
        if not profile_path.exists():
            continue
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        entries.append(build_entry(customer_dir.name, profile))

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"entries": entries}, f, indent=2)
        f.write("\n")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

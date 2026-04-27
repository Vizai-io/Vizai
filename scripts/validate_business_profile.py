#!/usr/bin/env python3
"""
Validate business profile packages under businesses/{slug}.
"""

import json
import sys
from pathlib import Path

REQUIRED_FILES = [
    "profile.json",
    "profile.jsonld",
    "company.md",
    "services.md",
    "products.md",
    "locations.md",
    "industries.md",
    "faqs.md",
    "proof-points.md",
    "sources.json",
    "approval.json",
    "changelog.md",
]


def validate_json(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
    return errors


def validate_customer_dir(customer_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        file_path = customer_dir / name
        if not file_path.exists():
            errors.append(f"{customer_dir.name}: missing required file {name}")

    for json_name in ["profile.json", "profile.jsonld", "sources.json", "approval.json"]:
        file_path = customer_dir / json_name
        if file_path.exists():
            errors.extend(validate_json(file_path))

    profile_path = customer_dir / "profile.json"
    if profile_path.exists():
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        if "isSample" not in profile:
            errors.append(f"{customer_dir.name}: profile.json should include isSample")
    return errors


def main() -> int:
    repo_root = Path(__file__).parent.parent
    businesses_dir = repo_root / "businesses"
    if not businesses_dir.exists():
        print("No businesses directory found.")
        return 1

    all_errors: list[str] = []
    for child in businesses_dir.iterdir():
        if child.is_dir() and not child.name.startswith("."):
            all_errors.extend(validate_customer_dir(child))

    if all_errors:
        print("Business profile validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Business profile validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

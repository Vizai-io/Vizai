#!/usr/bin/env python3
"""
Validate customer profile packages under businesses/{customer-slug}.

Checks:
1) Required files exist
2) profile.json is valid JSON and validates against schema/business-profile.schema.json
3) sourceIds referenced in profile.json exist in sources.json
4) approval.json exists and includes required status fields
5) profile.jsonld is valid JSON

Usage:
  python scripts/validate_business_profile.py businesses/example-co
  python scripts/validate_business_profile.py               # validate all customers
"""

import json
import sys
import copy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

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


def load_json(path: Path) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), errors
    except Exception as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
        return None, errors


def collect_source_ids(node: Any) -> set[str]:
    """Recursively collect all sourceIds arrays from profile data."""
    found: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "sourceIds":
                if isinstance(value, list):
                    for entry in value:
                        if isinstance(entry, str) and entry.strip():
                            found.add(entry.strip())
                continue
            found.update(collect_source_ids(value))
    elif isinstance(node, list):
        for item in node:
            found.update(collect_source_ids(item))
    return found


def validate_schema(profile: dict, schema_path: Path) -> list[str]:
    errors: list[str] = []
    schema_data, schema_load_errors = load_json(schema_path)
    if schema_load_errors:
        return schema_load_errors
    assert isinstance(schema_data, dict)

    schema_dir = schema_path.parent
    refs_map: dict[str, Any] = {}
    referenced_files = [
        "service.schema.json",
        "product.schema.json",
        "location.schema.json",
        "approval.schema.json",
    ]
    for filename in referenced_files:
        ref_path = schema_dir / filename
        ref_data, ref_errors = load_json(ref_path)
        if ref_errors:
            errors.extend(ref_errors)
            continue
        if isinstance(ref_data, dict):
            refs_map[filename] = ref_data

    def inline_external_refs(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node and isinstance(node["$ref"], str):
                ref = node["$ref"]
                if ref in refs_map:
                    # Inline referenced local schema to avoid remote/network resolution.
                    return inline_external_refs(copy.deepcopy(refs_map[ref]))
            return {key: inline_external_refs(value) for key, value in node.items()}
        if isinstance(node, list):
            return [inline_external_refs(item) for item in node]
        return node

    normalized_schema = inline_external_refs(copy.deepcopy(schema_data))
    validator = Draft202012Validator(normalized_schema)
    validation_errors = sorted(validator.iter_errors(profile), key=lambda e: list(e.path))
    for err in validation_errors:
        path = ".".join(str(part) for part in err.path) or "<root>"
        errors.append(f"profile.json schema error at {path}: {err.message}")
    return errors


def validate_customer_dir(customer_dir: Path, schema_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED_FILES:
        file_path = customer_dir / name
        if not file_path.exists():
            errors.append(f"{customer_dir.name}: missing required file {name}")

    # Validate profile.json
    profile_path = customer_dir / "profile.json"
    profile_data: dict[str, Any] | None = None
    if profile_path.exists():
        profile_raw, profile_errors = load_json(profile_path)
        errors.extend(profile_errors)
        if isinstance(profile_raw, dict):
            profile_data = profile_raw
            errors.extend(validate_schema(profile_data, schema_path))
        elif profile_raw is not None:
            errors.append(f"{profile_path}: expected a JSON object at root.")

    # Validate sources.json and sourceIds references.
    sources_path = customer_dir / "sources.json"
    if sources_path.exists():
        sources_raw, source_errors = load_json(sources_path)
        errors.extend(source_errors)
        available_source_ids: set[str] = set()
        if isinstance(sources_raw, dict):
            sources_list = sources_raw.get("sources", [])
            if isinstance(sources_list, list):
                for entry in sources_list:
                    if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                        available_source_ids.add(entry["id"])
            else:
                errors.append(f"{sources_path}: field 'sources' must be an array.")

            if profile_data is not None:
                referenced = collect_source_ids(profile_data)
                missing = sorted(source_id for source_id in referenced if source_id not in available_source_ids)
                for source_id in missing:
                    errors.append(
                        f"{customer_dir.name}: profile.json references sourceId '{source_id}' not found in sources.json"
                    )
        elif sources_raw is not None:
            errors.append(f"{sources_path}: expected a JSON object at root.")

    # Validate approval.json status fields.
    approval_path = customer_dir / "approval.json"
    if approval_path.exists():
        approval_raw, approval_errors = load_json(approval_path)
        errors.extend(approval_errors)
        if isinstance(approval_raw, dict):
            for field in ["status", "submittedAt"]:
                if field not in approval_raw:
                    errors.append(f"{approval_path}: missing required field '{field}'")
            if "verificationStatus" not in approval_raw:
                warnings.append(
                    f"{approval_path}: recommended field 'verificationStatus' is missing"
                )
        elif approval_raw is not None:
            errors.append(f"{approval_path}: expected a JSON object at root.")

    # Validate profile.jsonld JSON syntax only.
    profile_jsonld_path = customer_dir / "profile.jsonld"
    if profile_jsonld_path.exists():
        _, jsonld_errors = load_json(profile_jsonld_path)
        errors.extend(jsonld_errors)

    if not errors:
        warnings.append(f"{customer_dir.name}: all checks passed")

    return errors, warnings


def resolve_targets(repo_root: Path, arg_path: str | None) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    businesses_dir = repo_root / "businesses"
    if arg_path:
        candidate = (repo_root / arg_path).resolve()
        if not candidate.exists() or not candidate.is_dir():
            errors.append(f"Target path does not exist or is not a folder: {arg_path}")
            return [], errors
        return [candidate], errors

    if not businesses_dir.exists():
        errors.append("No businesses directory found.")
        return [], errors
    targets = [child for child in businesses_dir.iterdir() if child.is_dir() and not child.name.startswith(".")]
    if not targets:
        errors.append("No customer folders found under businesses/.")
    return targets, errors


def print_report(results: list[tuple[str, list[str], list[str]]]) -> None:
    print("\nVizAI Customer Profile Validation Report")
    print("=" * 40)
    for name, errors, warnings in results:
        if errors:
            print(f"\n[FAIL] {name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"\n[PASS] {name}")
            for msg in warnings:
                print(f"  - {msg}")


def main() -> int:
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / "schema" / "business-profile.schema.json"
    if not schema_path.exists():
        print(f"Missing schema file: {schema_path}")
        return 1

    target_arg = sys.argv[1] if len(sys.argv) > 1 else None
    targets, target_errors = resolve_targets(repo_root, target_arg)
    if target_errors:
        for err in target_errors:
            print(err)
        return 1

    results: list[tuple[str, list[str], list[str]]] = []
    has_errors = False
    for customer_dir in targets:
        errors, warnings = validate_customer_dir(customer_dir, schema_path)
        if errors:
            has_errors = True
        results.append((customer_dir.name, errors, warnings))

    print_report(results)
    if has_errors:
        print("\nValidation failed.")
        return 1
    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

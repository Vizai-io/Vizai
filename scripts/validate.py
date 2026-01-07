#!/usr/bin/env python3
"""
VizAI AI Data Hub Validator

Validates the repository structure and content:
1. JSON validity for all .json and .jsonld files
2. Required files exist in each business folder
3. Manifest references all artifacts listed in distribution
4. Dataset catalog references valid manifests
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Tuple

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def validate_json_file(file_path: Path) -> Tuple[bool, str]:
    """Validate that a file contains valid JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON decode error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def validate_manifest_artifacts(manifest_path: Path) -> Tuple[bool, List[str]]:
    """Validate that all artifacts referenced in manifest.json exist."""
    errors = []

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # Check distribution array
        if 'distribution' not in manifest:
            errors.append(f"{manifest_path}: Missing 'distribution' field")
            return False, errors

        distributions = manifest['distribution']
        if not isinstance(distributions, list):
            distributions = [distributions]

        business_dir = manifest_path.parent

        for dist in distributions:
            if 'contentUrl' not in dist:
                errors.append(f"{manifest_path}: Distribution missing 'contentUrl'")
                continue

            # Extract filename from GitHub raw URL
            content_url = dist['contentUrl']
            if 'raw.githubusercontent.com' in content_url:
                # Extract path after /main/
                parts = content_url.split('/main/')
                if len(parts) == 2:
                    rel_path = parts[1]
                    # Get the part relative to the business directory
                    if rel_path.startswith('businesses/'):
                        business_rel_path = '/'.join(rel_path.split('/')[2:])
                        artifact_path = business_dir / business_rel_path

                        if not artifact_path.exists():
                            errors.append(f"{manifest_path}: Referenced artifact does not exist: {artifact_path}")

        return len(errors) == 0, errors

    except Exception as e:
        errors.append(f"{manifest_path}: Error validating manifest: {e}")
        return False, errors

def main():
    """Main validation function."""
    repo_root = Path(__file__).parent.parent
    errors = []
    warnings = []
    success_count = 0

    print(f"\n{YELLOW}VizAI AI Data Hub Validator{RESET}")
    print(f"Repository: {repo_root}\n")

    # 1. Validate all JSON/JSONLD files
    print("Validating JSON files...")
    json_files = list(repo_root.glob('**/*.json')) + list(repo_root.glob('**/*.jsonld'))

    for json_file in json_files:
        # Skip files in .git directory
        if '.git' in json_file.parts:
            continue

        valid, error = validate_json_file(json_file)
        if valid:
            success_count += 1
            print(f"  {GREEN}✓{RESET} {json_file.relative_to(repo_root)}")
        else:
            errors.append(f"{json_file.relative_to(repo_root)}: {error}")
            print(f"  {RED}✗{RESET} {json_file.relative_to(repo_root)}: {error}")

    # 2. Validate business folders
    print("\nValidating business folders...")
    businesses_dir = repo_root / 'businesses'

    if businesses_dir.exists():
        for business_dir in businesses_dir.iterdir():
            if not business_dir.is_dir() or business_dir.name.startswith('.'):
                continue

            # Check required files
            manifest_path = business_dir / 'manifest.json'
            org_path = business_dir / 'organization.jsonld'

            if not manifest_path.exists():
                errors.append(f"{business_dir.name}: Missing manifest.json")
                print(f"  {RED}✗{RESET} {business_dir.name}: Missing manifest.json")
            elif not org_path.exists():
                errors.append(f"{business_dir.name}: Missing organization.jsonld")
                print(f"  {RED}✗{RESET} {business_dir.name}: Missing organization.jsonld")
            else:
                # Validate manifest artifact references
                valid, artifact_errors = validate_manifest_artifacts(manifest_path)
                if valid:
                    print(f"  {GREEN}✓{RESET} {business_dir.name}: All required files present")
                    success_count += 1
                else:
                    errors.extend(artifact_errors)
                    for err in artifact_errors:
                        print(f"  {RED}✗{RESET} {err}")
    else:
        warnings.append("No businesses/ directory found")

    # 3. Validate dataset catalog
    print("\nValidating dataset catalog...")
    catalog_path = repo_root / 'dataset-catalog.json'

    if catalog_path.exists():
        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                catalog = json.load(f)

            if 'dataset' in catalog:
                datasets = catalog['dataset']
                if not isinstance(datasets, list):
                    datasets = [datasets]

                print(f"  {GREEN}✓{RESET} Found {len(datasets)} dataset(s) in catalog")
                success_count += 1
            else:
                warnings.append("dataset-catalog.json: No 'dataset' field found")
        except Exception as e:
            errors.append(f"dataset-catalog.json: {e}")
    else:
        warnings.append("No dataset-catalog.json found")

    # 4. Check for sitemap.xml
    print("\nValidating sitemap...")
    sitemap_path = repo_root / 'sitemap.xml'

    if sitemap_path.exists():
        print(f"  {GREEN}✓{RESET} sitemap.xml exists")
        success_count += 1
    else:
        warnings.append("No sitemap.xml found")

    # Print summary
    print(f"\n{YELLOW}Validation Summary{RESET}")
    print(f"  Successes: {GREEN}{success_count}{RESET}")

    if warnings:
        print(f"  Warnings: {YELLOW}{len(warnings)}{RESET}")
        for warning in warnings:
            print(f"    {YELLOW}⚠{RESET} {warning}")

    if errors:
        print(f"  Errors: {RED}{len(errors)}{RESET}")
        for error in errors:
            print(f"    {RED}✗{RESET} {error}")
        print(f"\n{RED}Validation FAILED{RESET}\n")
        sys.exit(1)
    else:
        print(f"\n{GREEN}Validation PASSED{RESET}\n")
        sys.exit(0)

if __name__ == '__main__':
    main()

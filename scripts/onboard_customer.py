#!/usr/bin/env python3
"""
Safe customer onboarding setup script.

Usage:
  python scripts/onboard_customer.py --name "Example Co" --domain "https://example.com" --country CA --region ON --city Perth
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("Unable to generate slug from name.")
    return slug


def normalize_domain(domain: str) -> tuple[str, str]:
    cleaned = domain.strip().rstrip("/")
    cleaned = re.sub(r"^https?://", "", cleaned, flags=re.IGNORECASE)
    if not cleaned:
        raise ValueError("Domain cannot be empty.")
    return cleaned, f"https://{cleaned}"


def replace_placeholders(root: Path, values: dict[str, str]) -> None:
    text_extensions = {".md", ".json", ".jsonld", ".txt"}
    for file_path in root.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in text_extensions:
            continue
        original = file_path.read_text(encoding="utf-8")
        updated = original
        for placeholder, value in values.items():
            updated = updated.replace(placeholder, value)
        if updated != original:
            file_path.write_text(updated, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_profile(slug: str, name: str, domain_host: str, country: str, region: str, city: str) -> dict:
    today = date.today().isoformat()
    return {
        "vizaiId": slug,
        "isSample": False,
        "status": "draft",
        "legalName": {
            "value": name,
            "sourceIds": ["src-client-001"],
            "factType": "customer_provided",
            "confidence": 0.8,
            "notes": "Replace with exact legal entity name after intake validation."
        },
        "brandName": {
            "value": name,
            "sourceIds": ["src-web-001"],
            "factType": "website_extracted",
            "confidence": 0.8
        },
        "domain": domain_host,
        "description": {
            "value": f"{name} profile draft created by onboarding setup.",
            "sourceIds": ["src-client-001"],
            "factType": "customer_provided",
            "confidence": 0.6
        },
        "shortDescription": {
            "value": f"{name} business profile draft.",
            "sourceIds": ["src-client-001"],
            "factType": "customer_provided",
            "confidence": 0.6
        },
        "businessCategory": {
            "value": "TBD",
            "sourceIds": ["src-client-001"],
            "factType": "customer_provided",
            "confidence": 0.5
        },
        "naicsCodes": [],
        "services": [],
        "products": [],
        "industriesServed": [],
        "locations": [
            {
                "name": f"{city} Office",
                "type": "Headquarters",
                "city": city,
                "region": region,
                "country": country,
                "sourceIds": ["src-client-001"],
                "factType": "customer_provided",
                "confidence": 0.7
            }
        ],
        "serviceAreas": [],
        "certifications": [],
        "differentiators": [],
        "faqs": [],
        "sameAs": [],
        "contactPoints": [],
        "lastReviewed": today,
        "lastUpdated": today,
        "approval": {
            "customerSlug": slug,
            "status": "pending",
            "approvedBy": None,
            "approvedAt": None,
            "submittedAt": today,
            "scope": ["profile.json", "profile.jsonld", "sources.json"],
            "notes": "Initial onboarding scaffold generated.",
            "confidenceScore": 0.6,
            "verificationStatus": "unverified"
        },
        "confidenceScore": 0.6,
        "verificationStatus": "unverified",
        "version": "1.0.0"
    }


def build_sources(slug: str, name: str, website_url: str) -> dict:
    today = date.today().isoformat()
    return {
        "customerSlug": slug,
        "sources": [
            {
                "id": "src-client-001",
                "title": f"{name} intake questionnaire",
                "url": "https://example.com/internal/intake",
                "type": "document",
                "capturedAt": today,
                "notes": "Replace with approved intake source location.",
                "factType": "customer_provided"
            },
            {
                "id": "src-web-001",
                "title": f"{name} website",
                "url": website_url,
                "type": "website",
                "capturedAt": today,
                "notes": "Public website source.",
                "factType": "website_extracted"
            }
        ]
    }


def build_approval(slug: str) -> dict:
    today = date.today().isoformat()
    return {
        "customerSlug": slug,
        "status": "pending",
        "approvedBy": None,
        "approvedAt": None,
        "submittedAt": today,
        "scope": ["profile.json", "profile.jsonld", "sources.json"],
        "notes": "Starter approval record created by onboarding setup.",
        "confidenceScore": 0.6,
        "verificationStatus": "unverified"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a safe starter customer package from template.")
    parser.add_argument("--name", required=True, help="Customer display/legal name")
    parser.add_argument("--domain", required=True, help="Customer domain or URL")
    parser.add_argument("--country", required=True, help="Country code (e.g. CA)")
    parser.add_argument("--region", required=True, help="Region or state (e.g. ON)")
    parser.add_argument("--city", required=True, help="City")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    template_dir = repo_root / "templates" / "customer-profile-template"
    businesses_dir = repo_root / "businesses"

    if not template_dir.exists():
        print(f"Template folder not found: {template_dir}")
        return 1

    slug = slugify(args.name)
    domain_host, website_url = normalize_domain(args.domain)
    customer_dir = businesses_dir / slug

    if customer_dir.exists():
        print(f"Customer folder already exists: {customer_dir}")
        return 1

    shutil.copytree(template_dir, customer_dir)

    today = date.today().isoformat()
    placeholders = {
        "{{CUSTOMER_SLUG}}": slug,
        "{{CUSTOMER_NAME}}": args.name,
        "{{CUSTOMER_LEGAL_NAME}}": args.name,
        "{{DOMAIN}}": domain_host,
        "{{CITY}}": args.city,
        "{{REGION_OR_STATE}}": args.region,
        "{{COUNTRY_CODE}}": args.country,
        "{{DATE_YYYY_MM_DD}}": today,
    }
    replace_placeholders(customer_dir, placeholders)

    write_json(
        customer_dir / "profile.json",
        build_profile(slug, args.name, domain_host, args.country, args.region, args.city),
    )
    write_json(customer_dir / "sources.json", build_sources(slug, args.name, website_url))
    write_json(customer_dir / "approval.json", build_approval(slug))

    print(f"Created customer package: {customer_dir}")
    print("\nNext steps:")
    print("1) Fill out markdown context files (company/services/products/locations/faqs/proof-points).")
    print("2) Complete profile.json with approved claims and sourceIds.")
    print(f"3) Validate package: python scripts/validate_business_profile.py businesses/{slug}")
    print(f"4) Build registry entry: python scripts/build_registry_entry.py businesses/{slug}")
    print("5) Open a PR for human review and approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

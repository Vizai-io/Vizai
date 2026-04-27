#!/usr/bin/env python3
"""
Build sitemap.xml for key repository data assets.
"""

from pathlib import Path
from datetime import date

BASE_URL = "https://raw.githubusercontent.com/vizai-io/vizai/main"


def build_url(path: str) -> str:
    return f"{BASE_URL}/{path}"


def add_if_exists(url_paths: list[str], file_path: Path, relative_path: str) -> None:
    if file_path.exists():
        url_paths.append(build_url(relative_path))


def main() -> int:
    repo_root = Path(__file__).parent.parent
    businesses_dir = repo_root / "businesses"
    today = date.today().isoformat()

    if not businesses_dir.exists():
        print("No businesses directory found.")
        return 1

    url_paths = [
        build_url("README.ai.md"),
        build_url("dataset-catalog.json"),
        build_url("schema/business-profile.schema.json"),
        build_url("schema/registry-entry.schema.json"),
    ]

    for customer_dir in sorted(businesses_dir.iterdir()):
        if not customer_dir.is_dir() or customer_dir.name.startswith("."):
            continue
        slug = customer_dir.name
        base_rel = f"businesses/{slug}"
        add_if_exists(url_paths, customer_dir / "README.md", f"{base_rel}/README.md")
        add_if_exists(url_paths, customer_dir / "profile.json", f"{base_rel}/profile.json")
        add_if_exists(url_paths, customer_dir / "profile.jsonld", f"{base_rel}/profile.jsonld")
        add_if_exists(url_paths, customer_dir / "registry-entry.json", f"{base_rel}/registry-entry.json")
        add_if_exists(url_paths, customer_dir / "manifest.json", f"{base_rel}/manifest.json")
        add_if_exists(url_paths, customer_dir / "organization.jsonld", f"{base_rel}/organization.jsonld")
        add_if_exists(url_paths, customer_dir / "products.jsonld", f"{base_rel}/products.jsonld")
        add_if_exists(url_paths, customer_dir / "updates" / "feed.json", f"{base_rel}/updates/feed.json")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in sorted(set(url_paths)):
        lines.extend(
            [
                "  <url>",
                f"    <loc>{url}</loc>",
                f"    <lastmod>{today}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                "    <priority>0.8</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")

    out_path = repo_root / "sitemap.xml"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

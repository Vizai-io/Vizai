#!/usr/bin/env python3
"""
Build sitemap.xml for key repository data assets.
"""

from pathlib import Path
from datetime import date


def main() -> int:
    repo_root = Path(__file__).parent.parent
    businesses_dir = repo_root / "businesses"
    today = date.today().isoformat()

    urls = [
        "https://raw.githubusercontent.com/vizai-io/vizai/main/README.ai.md",
        "https://raw.githubusercontent.com/vizai-io/vizai/main/dataset-catalog.json",
    ]

    for customer_dir in sorted(businesses_dir.iterdir()):
        if not customer_dir.is_dir() or customer_dir.name.startswith("."):
            continue
        slug = customer_dir.name
        for file_name in ["manifest.json", "profile.json", "profile.jsonld", "organization.jsonld"]:
            path = customer_dir / file_name
            if path.exists():
                urls.append(
                    f"https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/{slug}/{file_name}"
                )

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
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

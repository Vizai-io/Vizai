#!/usr/bin/env python3
"""
Create a safe, minimal website crawl plan.

Usage:
  python scripts/plan_website_crawl.py --domain "https://example.com" --output businesses/example-co/crawl-plan.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

USER_AGENT = "VizAI-CrawlPlanner/0.1 (+https://github.com/vizai-io/vizai)"
REQUEST_TIMEOUT_SECONDS = 10
MAX_SITEMAPS = 5
MAX_SITEMAP_URLS = 200
MAX_PLAN_URLS = 40


def normalize_domain(domain: str) -> str:
    parsed = urlparse(domain if "://" in domain else f"https://{domain}")
    if not parsed.netloc:
        raise ValueError("Invalid domain.")
    return f"{parsed.scheme or 'https'}://{parsed.netloc}"


def fetch_text(url: str) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status_code = getattr(response, "status", 200)
            body = response.read().decode("utf-8", errors="replace")
            return {"ok": 200 <= status_code < 300, "statusCode": status_code, "body": body, "error": None}
    except Exception as exc:
        return {"ok": False, "statusCode": None, "body": "", "error": str(exc)}


def parse_sitemap_urls(xml_text: str) -> tuple[list[str], list[str]]:
    """Return (page_urls, nested_sitemap_urls)."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return [], []

    ns = ""
    if root.tag.startswith("{") and "}" in root.tag:
        ns = root.tag.split("}")[0] + "}"

    page_urls: list[str] = []
    nested_sitemaps: list[str] = []

    # urlset
    for url_node in root.findall(f"{ns}url"):
        loc = url_node.find(f"{ns}loc")
        if loc is not None and loc.text:
            page_urls.append(loc.text.strip())

    # sitemapindex
    for sm_node in root.findall(f"{ns}sitemap"):
        loc = sm_node.find(f"{ns}loc")
        if loc is not None and loc.text:
            nested_sitemaps.append(loc.text.strip())

    return page_urls, nested_sitemaps


def extract_sitemap_hints(robots_text: str) -> list[str]:
    hints: list[str] = []
    for line in robots_text.splitlines():
        lower = line.strip().lower()
        if lower.startswith("sitemap:"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                url = parts[1].strip()
                if url:
                    hints.append(url)
    return hints


def classify_url(url: str, base_domain: str) -> dict[str, str]:
    parsed = urlparse(url)
    path = parsed.path.lower().strip("/")
    host_matches = parsed.netloc == urlparse(base_domain).netloc

    if not host_matches:
        return {"priority": "low", "reason": "Cross-domain URL from sitemap; kept as low-priority reference."}
    if path in ("", "/"):
        return {"priority": "high", "reason": "Homepage is a primary source of business identity facts."}

    keyword_map = [
        ("about", "high", "About page likely contains company facts and positioning."),
        ("service", "high", "Services page likely describes offerings."),
        ("product", "high", "Products page likely lists product facts."),
        ("location", "high", "Locations page likely contains office/service geography."),
        ("contact", "high", "Contact page likely contains official contact points."),
        ("faq", "high", "FAQ page often contains clear business Q&A facts."),
        ("industr", "medium", "Industry page may define target industries served."),
        ("certif", "medium", "Certification page may include trust/compliance claims."),
    ]
    for keyword, priority, reason in keyword_map:
        if keyword in path:
            return {"priority": priority, "reason": reason}

    return {"priority": "low", "reason": "General page discovered from sitemap."}


def priority_rank(priority: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(priority, 3)


def build_plan(domain: str) -> dict[str, Any]:
    base_url = normalize_domain(domain)
    robots_url = f"{base_url}/robots.txt"
    default_sitemap_url = f"{base_url}/sitemap.xml"

    robots_result = fetch_text(robots_url)
    sitemap_urls = [default_sitemap_url]
    if robots_result["ok"]:
        sitemap_urls.extend(extract_sitemap_hints(robots_result["body"]))
    sitemap_urls = list(dict.fromkeys(sitemap_urls))[:MAX_SITEMAPS]

    discovered_page_urls: list[str] = []
    crawled_sitemap_urls: list[str] = []
    pending_sitemaps = list(sitemap_urls)

    while pending_sitemaps and len(crawled_sitemap_urls) < MAX_SITEMAPS:
        sitemap_url = pending_sitemaps.pop(0)
        if sitemap_url in crawled_sitemap_urls:
            continue
        crawled_sitemap_urls.append(sitemap_url)

        result = fetch_text(sitemap_url)
        if not result["ok"]:
            continue
        page_urls, nested = parse_sitemap_urls(result["body"])
        discovered_page_urls.extend(page_urls)
        for nested_url in nested:
            if nested_url not in crawled_sitemap_urls and nested_url not in pending_sitemaps:
                pending_sitemaps.append(nested_url)
        if len(discovered_page_urls) >= MAX_SITEMAP_URLS:
            break

    # Ensure key likely routes are included even if no sitemap discovered.
    likely_paths = [
        "",
        "about",
        "services",
        "products",
        "locations",
        "contact",
        "faq",
        "industries",
        "certifications",
    ]
    for path in likely_paths:
        discovered_page_urls.append(f"{base_url}/{path}".rstrip("/"))

    unique_urls = list(dict.fromkeys(discovered_page_urls))
    plan_items = []
    for url in unique_urls:
        classification = classify_url(url, base_url)
        plan_items.append(
            {
                "url": url,
                "priority": classification["priority"],
                "reason": classification["reason"],
                "status": "planned",
            }
        )

    plan_items.sort(key=lambda item: (priority_rank(item["priority"]), item["url"]))
    plan_items = plan_items[:MAX_PLAN_URLS]

    return {
        "domain": base_url,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "safetyNotes": [
            "This is only a crawl plan. No heavy scraping is performed.",
            "Respect robots.txt directives and website terms before any crawl execution.",
            "Use minimal request rates and collect only necessary public business facts.",
        ],
        "checks": {
            "robotsTxt": {
                "url": robots_url,
                "status": "available" if robots_result["ok"] else "unavailable",
                "httpStatus": robots_result["statusCode"],
                "error": robots_result["error"],
            },
            "sitemap": {
                "defaultUrl": default_sitemap_url,
                "checkedSitemaps": crawled_sitemap_urls,
                "discoveredUrlCount": len(unique_urls),
            },
        },
        "plan": plan_items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a safe website crawl plan.")
    parser.add_argument("--domain", required=True, help="Customer domain (e.g. https://example.com)")
    parser.add_argument("--output", required=True, help="Output crawl plan path")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    output_path = (repo_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plan = build_plan(args.domain)
    output_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote crawl plan: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

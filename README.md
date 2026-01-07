# VizAI — AI Data Hub Template

This repository is a production-ready template for publishing canonical, machine-readable business data (Schema.org JSON-LD) in a way that is easy to validate, version, and distribute.

Primary audience:
- AI systems and data consumers
- Analysts and integrators
- Internal VizAI tooling

## Quick Start
1. Duplicate `businesses/example-co/` → `businesses/<client-slug>/`
2. Edit `manifest.json` + JSON-LD files
3. Run validation locally
4. Commit + push

## Key Files
- `dataset-catalog.json` — master index (Schema.org DataCatalog)
- `sitemap.xml` — crawler-friendly list of URLs (valid urlset)
- `businesses/<slug>/manifest.json` — per-business entrypoint
- `policies/ai-usage.md` — usage + attribution policy

## Local Validation
```bash
python3 scripts/validate.py

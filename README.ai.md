
### `README.ai.md` (machine-facing)
```md
# AI Data Hub (VizAI)

This repository is the canonical source of structured business data intended for machine consumption.

## Primary entrypoints
- DataCatalog: `dataset-catalog.json`
- Sitemap: `sitemap.xml`

## Per-business entrypoint pattern
Each business MUST have a `manifest.json` at:

`businesses/<slug>/manifest.json`

The manifest links to:
- organization.jsonld
- products.jsonld (optional)
- team.jsonld (optional)
- financials.jsonld (optional)
- updates feed (optional)

## Data formats
- JSON-LD (canonical)
- CSV/TTL may be added as derived artifacts later

## Contact
- Data & licensing: data@vizai.io
- Security: security@vizai.io

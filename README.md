# VizAI — AI Data Hub Template

This repository is a production-ready template for publishing canonical, machine-readable business data (Schema.org JSON-LD) in a way that is easy to validate, version, and distribute.

## Overview

The VizAI AI Data Hub provides a standardized structure for publishing structured business information that can be consumed by AI systems, data analysts, and integrators. All data is published as valid Schema.org JSON-LD with comprehensive validation and version control via Git.

### Primary Audience
- AI systems and data consumers
- Analysts and integrators
- Internal VizAI tooling
- Researchers and developers

## Quick Start

1. **Fork this repository** or use it as a template
2. **Duplicate the example**: Copy `businesses/example-co/` → `businesses/<your-company-slug>/`
3. **Edit the files**: Update `manifest.json`, `organization.jsonld`, and other JSON-LD files with your business data
4. **Run validation**: Execute `python3 scripts/validate.py` to ensure all files are valid
5. **Commit and push**: Your data is now published and accessible via raw GitHub URLs

## Repository Structure

```
/
├── README.md                          # This file (human-facing overview)
├── README.ai.md                       # Machine-facing instructions
├── dataset-catalog.json               # Master index (Schema.org DataCatalog)
├── sitemap.xml                        # Valid XML sitemap for crawlers
│
├── policies/
│   └── ai-usage.md                    # Usage and attribution policy
│
├── businesses/
│   └── example-co/                    # Example company record
│       ├── manifest.json              # Per-company entrypoint
│       ├── organization.jsonld        # Schema.org Organization
│       ├── products.jsonld            # Schema.org ItemList (optional)
│       └── updates/
│           └── feed.json              # Schema.org DataFeed (optional)
│
├── templates/                         # Starter templates
│   ├── manifest.json
│   └── organization.jsonld
│
├── scripts/
│   └── validate.py                    # Local validation script
│
└── .github/
    └── workflows/
        └── validate.yml               # CI validation on push/PR
```

## Key Files

### Root Level
- **`dataset-catalog.json`**: Master index of all datasets (Schema.org DataCatalog)
- **`sitemap.xml`**: Crawler-friendly list of all data URLs (valid XML urlset)
- **`README.ai.md`**: Machine-facing instructions for AI systems

### Per-Business Structure
Each business has its own folder under `businesses/<slug>/`:

- **`manifest.json`** (required): Entrypoint listing all available data artifacts
- **`organization.jsonld`** (required): Schema.org Organization with business details
- **`products.jsonld`** (optional): Schema.org ItemList of products/services
- **`updates/feed.json`** (optional): Schema.org DataFeed with recent updates

## Validation

### Local Validation
Run the validation script before committing:

```bash
python3 scripts/validate.py
```

The script checks:
- JSON validity for all `.json` and `.jsonld` files
- Required files exist in each business folder
- Manifest references all artifacts listed in distribution
- Dataset catalog references valid manifests

### Continuous Integration
GitHub Actions automatically runs validation on all pushes and pull requests. See `.github/workflows/validate.yml` for details.

## Data Access

All data is accessible via raw GitHub URLs. For example:

- **Dataset Catalog**: `https://raw.githubusercontent.com/vizai-io/vizai/main/dataset-catalog.json`
- **Example Company Manifest**: `https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/example-co/manifest.json`
- **Example Organization**: `https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/example-co/organization.jsonld`

## Contributing

### Adding a New Company

1. **Copy the template**:
   ```bash
   cp -r templates businesses/your-company-slug
   ```

2. **Create required directory structure**:
   ```bash
   mkdir -p businesses/your-company-slug/updates
   ```

3. **Edit the files**:
   - Update `businesses/your-company-slug/manifest.json`:
     - Replace `YOUR_COMPANY_NAME`, `YOUR_SLUG`, and dates
     - Update `distribution` URLs to point to your slug
   - Update `businesses/your-company-slug/organization.jsonld`:
     - Replace all placeholder values (YOUR_COMPANY_NAME, YOUR_WEBSITE, etc.)
     - Fill in actual business information
   - Optionally create `products.jsonld` and `updates/feed.json`

4. **Add to dataset catalog**:
   - Edit `dataset-catalog.json`
   - Add a new entry to the `dataset` array referencing your manifest URL

5. **Add to sitemap**:
   - Edit `sitemap.xml`
   - Add `<url>` entries for your manifest and main artifacts

6. **Validate**:
   ```bash
   python3 scripts/validate.py
   ```

7. **Commit and push**:
   ```bash
   git add businesses/your-company-slug
   git commit -m "Add [Company Name] dataset"
   git push
   ```

### Guidelines

- Use lowercase, hyphenated slugs for company folders (e.g., `acme-corp`, `example-co`)
- Ensure all JSON files are valid (no trailing commas, comments, etc.)
- Use current dates in ISO format (YYYY-MM-DD)
- Include proper Schema.org `@context` and `@type` in all JSON-LD files
- Reference the actual raw GitHub URLs in manifests and catalogs

## Usage Policy

See `policies/ai-usage.md` for detailed information about:
- Permitted uses (AI training, analytics, integration, redistribution)
- Attribution requirements
- Data quality and warranties
- Licensing (CC BY 4.0 for data)
- Privacy and security guidelines

## Contact

- **Data licensing and partnerships**: data@vizai.io
- **Security issues**: security@vizai.io
- **General inquiries**: Open an issue in this repository

## License

- **Data**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Code** (validation scripts, templates): MIT License (see individual files)

---

**Version**: 1.0
**Last Updated**: 2026-01-06

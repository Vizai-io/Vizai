# AI Data Hub (VizAI)

**Machine-Readable Business Data Repository**

This repository is the canonical source of structured business data intended for machine consumption by AI systems, data analysts, and automated integrators.

## Primary Entrypoints

### 1. Dataset Catalog
**URL**: `https://raw.githubusercontent.com/vizai-io/vizai/main/dataset-catalog.json`

- **Type**: Schema.org DataCatalog
- **Purpose**: Master index of all available datasets in this repository
- **Format**: JSON-LD
- **Update Frequency**: Updated when new businesses are added

### 2. Sitemap
**URL**: `https://raw.githubusercontent.com/vizai-io/vizai/main/sitemap.xml`

- **Type**: XML Sitemap (standard sitemap protocol)
- **Purpose**: Crawler-friendly list of all data artifact URLs
- **Format**: XML (urlset)
- **Update Frequency**: Updated when new artifacts are published

## Per-Business Entrypoint Pattern

Each business MUST have a manifest file at:

```
https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/<slug>/manifest.json
```

### Manifest Structure

The manifest is a Schema.org Dataset that references all available data artifacts for that business via the `distribution` property.

**Required Fields**:
- `@context`: "https://schema.org"
- `@type`: "Dataset"
- `name`: Business dataset name
- `url`: URL to this manifest
- `distribution`: Array of DataDownload objects

### Standard Artifacts

Each business directory may contain:

1. **`organization.jsonld`** (required)
   - **Type**: Schema.org Organization
   - **Contains**: Business profile, contact info, address, social links

2. **`products.jsonld`** (optional)
   - **Type**: Schema.org ItemList
   - **Contains**: Products and services offered

3. **`updates/feed.json`** (optional)
   - **Type**: Schema.org DataFeed
   - **Contains**: Recent business updates, announcements, news

4. **Custom artifacts** (optional)
   - Additional JSON-LD files referenced in the manifest
   - Examples: team.jsonld, financials.jsonld, locations.jsonld

## Data Formats

### Primary Format: JSON-LD

All data is published as Schema.org JSON-LD with:
- Valid JSON syntax (no comments, trailing commas)
- Standard Schema.org vocabulary
- `@context` set to "https://schema.org"
- Appropriate `@type` for each entity

### Access Pattern

All files are accessible via GitHub raw URLs:
```
https://raw.githubusercontent.com/vizai-io/vizai/main/<path-to-file>
```

Example:
```
https://raw.githubusercontent.com/vizai-io/vizai/main/businesses/example-co/organization.jsonld
```

## Schema.org Types Used

### Primary Types
- **DataCatalog**: Root catalog (dataset-catalog.json)
- **Dataset**: Per-business manifest files
- **Organization**: Business entity profiles
- **ItemList**: Product/service catalogs
- **DataFeed**: Update feeds

### Supporting Types
- **DataDownload**: Distribution references in manifests
- **Person**: Founders, team members
- **PostalAddress**: Physical locations
- **ContactPoint**: Contact information
- **Product**: Individual products
- **Service**: Individual services
- **Article**: News items in feeds

## Discovery and Crawling

### Recommended Discovery Flow

1. **Start** at `dataset-catalog.json`
2. **Iterate** through the `dataset` array
3. **Fetch** each manifest URL
4. **Parse** the `distribution` array in each manifest
5. **Retrieve** individual artifacts via their `contentUrl`

### Alternative Discovery

- Parse `sitemap.xml` for all available artifact URLs
- Directly access known business manifests if slug is known

## Validation

All data in this repository is automatically validated on push/PR via:
- JSON syntax validation
- Required file checks
- Manifest-artifact reference verification
- Schema.org structure validation (planned)

Validation script: `scripts/validate.py`

## Versioning

- All data is versioned via Git commits
- Each file includes `datePublished` and `dateModified` fields
- Breaking changes will be tagged as releases
- Consumers should monitor the repository for updates

## Attribution and Usage

### License
- Data: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Code: MIT License

### Required Attribution
When using this data:
1. Credit "VizAI AI Data Hub"
2. Include link to repository: https://github.com/vizai-io/vizai
3. Preserve Schema.org metadata

See `policies/ai-usage.md` for complete usage policy.

## Contact

- **Data inquiries and partnerships**: data@vizai.io
- **Security issues**: security@vizai.io
- **Technical issues**: Open an issue on GitHub

## API Endpoints

**Note**: This is a static data repository. There are no dynamic API endpoints. All data is accessed via static GitHub raw URLs.

For programmatic access:
- Use GitHub API to list repository contents
- Fetch raw file contents via documented URLs
- Monitor repository commits/releases for updates

## Example: Fetching Business Data

```python
import requests

# 1. Fetch the catalog
catalog = requests.get(
    'https://raw.githubusercontent.com/vizai-io/vizai/main/dataset-catalog.json'
).json()

# 2. Get first business manifest URL
manifest_url = catalog['dataset'][0]['url']

# 3. Fetch manifest
manifest = requests.get(manifest_url).json()

# 4. Get organization data URL
org_url = next(
    d['contentUrl'] for d in manifest['distribution']
    if 'organization' in d['contentUrl']
)

# 5. Fetch organization data
org_data = requests.get(org_url).json()

print(f"Business: {org_data['name']}")
print(f"Website: {org_data['url']}")
```

## Changelog

- **2026-01-06**: Initial release (v1.0)
  - Dataset catalog
  - Example company (example-co)
  - Validation infrastructure
  - Template files

---

**Repository**: https://github.com/vizai-io/vizai
**Version**: 1.0
**Last Updated**: 2026-01-06

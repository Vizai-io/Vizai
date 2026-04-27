# VizAI to Business Registry Sync

This document describes the design for synchronizing approved customer profiles from VizAI to the separate business-registry repository.

## Overview

| Repository | Purpose | Content |
|------------|---------|---------|
| **VizAI** | Rich source of truth | Complete profiles, sources, approvals |
| **business-registry** | Lightweight discovery | Minimal cards for lookup |

## Architecture

```
VizAI Repository                    business-registry Repository
┌─────────────────────────┐         ┌─────────────────────────┐
│ businesses/{slug}/      │         │ registry/{country}/      │
│  - profile.json          │   ──►   │    {region}/{city}/     │
│  - profile.jsonld       │         │     {slug}.json          │
│  - sources.json         │                               
│  - registry-entry.json│                               
│  - approval.json       │                               
└─────────────────────────┘         └─────────────────────────┘
```

## Data Flow

1. **Profile Creation** - Customer profile built in VizAI with sources and approvals
2. **Approval Complete** - Status set to `approved` in `approval.json`
3. **Export** - Run `scripts/export_registry_entry.py` to generate light entry
4. **Manual Review** - Human reviews exported entry before copying
5. **Copy** - Manually copy to business-registry repo
6. **Publish** - Merge in business-registry repo

## Why Manual Review?

- Registry entries are public discovery cards
- Mistakes are visible to all users
- Requires human judgment on phrasing
- Opportunity to catch edge cases
- No automatic push protects against errors

## Export Script

```bash
# Export approved registry entry
python scripts/export_registry_entry.py businesses/<customer-slug>
```

Output:
- Validated JSON
- Lightweight format
- Suggested path: `registry/{country}/{region}/{city}/{slug}.json`

## Registry Entry Format

```json
{
  "slug": "customer-slug",
  "name": "Customer Name",
  "domain": "customer.com",
  "shortDescription": "One-line description",
  "profileUrl": "https://viz.ai/data/customer-slug",
  "industry": ["Industry A", "Industry B"],
  "services": ["Service A", "Service B"],
  "location": {
    "country": "US",
    "region": "CA",
    "city": "San Francisco"
  },
  "updatedAt": "2026-04-27",
  "status": "approved"
}
```

## Field Mapping

| VizAI (profile.json) | Registry Entry |
|---------------------|----------------|
| vizaiId / customerSlug | slug |
| businessName / brandName | name |
| domain | domain |
| shortDescription | shortDescription |
| profileUrl (computed) | profileUrl |
| industriesServed | industry |
| services | services |
| locations (inferred) | location |
| lastUpdated | updatedAt |
| approval.status | status |

## Validation

Before export:
1. Check `approval.json` status is `approved`
2. Validate against `schema/registry-entry.schema.json`
3. Verify required fields present

## What Gets Copied

Approved fields only:
- Business name and domain
- Short description
- Industry categories
- Services/products (summary)
- Location (city-level)
- Profile link

## What Stays in VizAI

Not copied to registry:
- Full descriptions
- Source metadata
- Contact details (unless approved)
- Raw scraped content
- Internal notes

## Path Structure

Registry entries organized by geography:
```
registry/
└── US/
    ├── CA/
    │   └── San Francisco/
    │       └── customer-slug.json
    ├── NY/
    │   └── New York/
    │       └── customer-slug.json
    └── TX/
        └── Austin/
            └── customer-slug.json
└── GB/
    └── LDN/
        └── London/
            └── customer-slug.json
```

## Publication Checklist

Before copying to business-registry:

- [ ] Profile approved in VizAI
- [ ] Registry entry validated
- [ ] Short description reviewed
- [ ] Location verified
- [ ] Status set to `approved`
- [ ] Manual review complete

## Future Automation

Once manual process is proven:
1. Add validation to PR checks
2. Consider bot-assisted review
3. Track sync status in VizAI
4. Add metadata to registry entry (source, syncedAt)
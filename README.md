# VizAI Data Hub

VizAI helps businesses become accurately understood by AI systems by creating verified, structured, source-backed business profiles.

This repository is the VizAI Data Hub template and customer profile structure. It stores rich AI-readable business truth files, Schema.org JSON-LD, source attribution, approval metadata, and validation tooling.

---

## What This Repository Contains

```
vizai/
├── businesses/           # Customer profile packages
│   └── {customer-slug}/ # Per-customer rich data
│       ├── profile.json       # Structured business profile
│       ├── profile.jsonld # Schema.org Organization
│       ├── sources.json   # Source attribution
│       ├── approval.json  # Approval metadata
│       └── registry-entry.json
├── schema/              # JSON schemas for validation
├── templates/            # Customer onboarding templates
├── scripts/             # Build, validation, and export tools
├── policies/            # Data governance rules
├── docs/                # Design documentation
└── registry/            # Exported registry entries (ready to copy)
```

---

## Customer Profile Structure

Each customer has a dedicated folder under `businesses/{customer-slug}/`:

| File | Purpose |
|------|---------|
| `profile.json` | Full structured profile with facts, confidence, sources |
| `profile.jsonld` | Schema.org representation |
| `sources.json` | Source URLs with metadata |
| `approval.json` | Approval status and scope |
| `registry-entry.json` | Lightweight entry for discovery |
| `*.md` | Human-readable supporting docs |

See `businesses/example-co/` for a complete example.

---

## How Validation Works

Run validation before any publication:

```bash
# Validate all profiles
python scripts/validate.py

# Validate specific profile
python scripts/validate_business_profile.py businesses/example-co
```

Validation checks:
- JSON schema compliance
- Required fields present
- Source attribution links
- Approval status

---

## How to Onboard a Customer

1. **Create customer folder** from template:
   ```bash
   cp -r templates/customer-profile-template businesses/{customer-slug}
   ```

2. **Gather data** - Review public website, collect customer questionnaire

3. **Build profile** - Populate `profile.json` with facts and sources

4. **Generate approval packet**:
   ```bash
   python scripts/build_approval_packet.py businesses/{customer-slug}
   ```

5. **Submit for approval** - Send `approval-packet.md` to customer

6. **Record approval** - Update `approval.json` with status

7. **Generate registry entry**:
   ```bash
   python scripts/build_registry_entry.py businesses/{customer-slug}
   ```

8. **Validate and publish** - Run validation, commit changes

---

## How the Business Registry Connects

This repo (VizAI) stores rich profiles. A separate `business-registry` repo stores lightweight discovery cards.

**VizAI → Rich source of truth** (full profiles, all metadata)

**business-registry → Lightweight discovery** (name, domain, short description, profile link)

To export a registry entry:

```bash
python scripts/export_registry_entry.py businesses/{customer-slug}
```

Output goes to `registry/{country}/{region}/{city}/{slug}.json` — ready to copy to business-registry after manual review.

See `docs/business-registry-sync.md` for the full sync design.

---

## What Should Not Be Published

Data governance rules in `policies/`:

- **Never publish**: Private questionnaire answers, raw scrape text, confidential contacts, pricing, contracts, internal notes
- **Publish only**: Approved customer profiles, source-backed public facts, lightweight registry entries
- **AI-generated content**: Must be reviewed by a human before publication

See `PUBLICATION_RULES.md` for the complete rules.

---

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Validate all data
python scripts/validate.py

# Build artifacts
python scripts/build_dataset_catalog.py
python scripts/build_sitemap.py
python scripts/build_registry_entry.py businesses/{customer-slug}

# Generate approval packet
python scripts/build_approval_packet.py businesses/{customer-slug}

# Export for business-registry
python scripts/export_registry_entry.py businesses/{customer-slug}
```

---

## Current Status

**Early MVP / Active Development**

This repository is in active development. Features:
- Rich profile structure with source attribution
- Approval workflow
- Registry entry export
- Validation tooling
- Data governance policies

planned:
- Enhanced validation rules
- Automated sync to business-registry
- Monitoring for drift and changes

---

## Resources

- `docs/onboarding-workflow.md` — End-to-end onboarding process
- `docs/business-registry-sync.md` — Sync design to business-registry
- `docs/customer-data-model.md` — Data model reference
- `PUBLICATION_RULES.md` — Publication guardrails
- `policies/*.md` — All governance policies

---

## License

- **Data**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Code**: MIT License
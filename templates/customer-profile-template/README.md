# Customer Profile Template

Copy this folder to `businesses/{{CUSTOMER_SLUG}}/` when onboarding a new VizAI customer.

## Usage

1. Copy all files in this template folder.
2. Replace placeholders like `{{CUSTOMER_NAME}}`, `{{DOMAIN}}`, `{{CITY}}`, and `{{DATE_YYYY_MM_DD}}`.
3. Keep claims conservative and factual.
4. Ensure every important claim is either:
   - client-approved, or
   - source-backed using `sourceIds`.

## Included Files

- `profile.json` (core structured customer profile, schema-aligned)
- `profile.jsonld` (Schema.org-style JSON-LD representation)
- `company.md` (human/AI narrative context)
- `services.md`
- `products.md`
- `locations.md`
- `industries.md`
- `faqs.md`
- `proof-points.md`
- `sources.json` (source catalog referenced by `sourceIds`)
- `approval.json` (approval workflow state)
- `changelog.md` (data updates over time)

## Data Quality Reminder

Do not publish unsupported claims. If a claim cannot be source-backed yet, mark it clearly as pending approval and keep it out of approved outputs.

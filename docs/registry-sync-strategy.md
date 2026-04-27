# Registry Sync Strategy

VizAI keeps rich profile data in this repository and publishes a lightweight index to a separate business-registry repository.

## Sync Principles
- Rich source of truth remains in `Vizai`.
- Registry receives minimal discovery fields only.
- Registry entries are generated from approved customer profile data.

## Suggested Flow
1. Validate customer profile package.
2. Ensure approval status is suitable for publication.
3. Build lightweight registry card with:
   - `python scripts/build_registry_entry.py businesses/{customer-slug}`
   - Output: `businesses/{customer-slug}/registry-entry.json`
4. Sync generated output to business-registry through controlled automation.

## Registry Entry Contract (Lightweight)

`registry-entry.json` is a public discovery card and should not include private intake/questionnaire data or raw scrape output.

Expected fields:
- `vizaiId`
- `businessName`
- `legalName`
- `domain`
- `shortDescription`
- `businessCategory`
- `services` (simple strings)
- `products` (simple strings)
- `industriesServed` (simple strings)
- `locations` (lightweight strings)
- `serviceAreas` (simple strings)
- `profileUrl` (placeholder URL pattern)
- `jsonLdUrl` (placeholder URL pattern)
- `sourceWebsite`
- `lastVerified`
- `lastUpdated`
- `status`
- `verificationSummary`

## Notes

- The builder flattens rich profile claim objects into lightweight strings for registry use.
- Keep the registry output intentionally small and public-safe.

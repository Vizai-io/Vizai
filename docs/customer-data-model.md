# Customer Data Model

Each customer package under `businesses/{slug}/` has a core structured profile in `profile.json`.

## What the main profile captures

The core profile supports:
- Identity: `vizaiId`, `legalName`, `brandName`, `domain`
- Publishing lifecycle: `status`, `lastReviewed`, `lastUpdated`, `approval`
- Business summary: `description`, `shortDescription`, `businessCategory`, `naicsCodes`
- Offerings and coverage: `services`, `products`, `industriesServed`, `locations`, `serviceAreas`
- Trust signals: `certifications`, `differentiators`, `faqs`, `sameAs`, `contactPoints`
- Data quality: `confidenceScore`, `verificationStatus`

## Claim provenance model (important)

Important business facts use a claim wrapper:
- `value`: the actual claim text/value
- `sourceIds`: one or more source IDs that support the claim
- `factType`: where the fact came from

`factType` is an enum with:
- `customer_provided`
- `website_extracted`
- `human_approved`

This keeps provenance practical and consistent across top-level fields and nested arrays.

## Approval and verification

The profile includes approval metadata directly in `approval`:
- workflow status (`pending`, `in_review`, `approved`, etc.)
- submission/approval dates
- review scope and notes
- verification state (`unverified`, `partially_verified`, `verified`, `disputed`)
- confidence score (0 to 1)

## Related files in each customer folder

- `profile.json`: primary structured record used by tooling
- `profile.jsonld`: linked-data representation for schema consumers
- `sources.json`: source catalog keyed by source ID
- `approval.json`: optional standalone approval record for workflow handoff
- markdown context files for human review (`company.md`, `services.md`, etc.)

## Practical guidance

- Use source IDs on all meaningful claims.
- Keep `status`, `verificationStatus`, and `confidenceScore` current.
- Mark sample customers clearly with `isSample: true`.

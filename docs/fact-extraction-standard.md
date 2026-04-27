# Fact Extraction Standard

## Purpose

This standard defines how future agents should record extracted business facts before approval.

Use:
- `schema/extracted-facts.schema.json` as the validation contract
- `templates/extracted-facts-template.json` as a starter file

## Core Rule

Extracted facts are **candidate facts**, not approved truth.

They are used for review, conflict resolution, and approval workflows before being promoted into `profile.json`.

## Required Fact Fields

Each extracted fact entry supports:
- `factId`
- `claim`
- `category`
- `normalizedValue`
- `sourceUrl`
- `sourceSnippet`
- `sourceType` (`website`, `questionnaire`, `manual`, `third-party`)
- `confidence` (0.0 to 1.0)
- `extractedAt` (ISO datetime)
- `requiresApproval` (boolean)
- `approvalStatus`
- `suggestedProfileField`
- `notes` (optional)

## Mandatory Safety and Quality Rules

- AI must **not invent facts**.
- Uncertain claims must be flagged with lower confidence and `approvalStatus: "needs_review"` or `pending`.
- Extracted facts are **not approved facts**.
- Approved facts are what become `profile.json` content.
- Every claim needs evidence (`sourceUrl` + `sourceSnippet`) or explicit client approval before publication.

## Suggested Workflow

1. Agent extracts candidate claims from allowed sources.
2. Agent records each claim in extracted-facts format with evidence.
3. Human or approval workflow reviews `approvalStatus`.
4. Only approved claims are mapped into `profile.json` and related public artifacts.

## Mapping Guidance

Use `suggestedProfileField` to indicate where approved claims should land, for example:
- `brandName.value`
- `legalName.value`
- `businessCategory.value`
- `services[0].name`
- `locations[0]`

This keeps extraction output actionable without bypassing approval controls.

# Publication Rules

These rules govern what data can be published from the VizAI Data Hub to external systems.

## Core Principles

1. **Privacy First** - Never publish private customer data without explicit approval
2. **Source-Back Everything** - Every major claim should have source attribution
3. **Human Review Required** - AI-generated content must be reviewed before publication
4. **Lightweight Registry** - Registry entries are discovery cards, not full profiles
5. **Rich Profiles Stay Here** - Full profiles live in VizAI Data Hub

## What NOT to Publish

| Category | Examples |
|----------|----------|
| Private data | Questionnaire answers, internal notes |
| Raw content | Full website scrape text, complete page dumps |
| Confidential | Contacts (unapproved), pricing, contracts, credentials |
| Unapproved | Draft content, rejected claims, speculative facts |
| Internal | Reviewer comments, discussion threads, credentials |

## What TO Publish

| Category | Examples |
|----------|----------|
| Approved facts | Customer-approved descriptions, services, products |
| Source-backed | Public website facts with attribution |
| Discovery data | Registry entry cards (name, domain, category, short desc) |
| Public announcements | Publicly known locations, industries served |

## Publication Workflow

1. **Extract** - Pull approved fields from `profile.json`
2. **Validate** - Verify `approval.json` status is `approved`
3. **Transform** - Transform to lightweight registry format
4. **Validate** - Run schema validation
5. **Publish** - Commit to registry repository

## Registry Entry Format

Registry entries should be minimal:
```json
{
  "vizaiId": "customer-slug",
  "businessName": "Customer Name",
  "domain": "customer.com",
  "shortDescription": "One-line description",
  "services": ["Service A", "Service B"],
  "profileUrl": "https://viz.ai/data/customer-slug"
}
```

## AI Content Rules

- AI-generated descriptions must be reviewed by a human
- Mark with `factType: "ai_generated"` until approved
- After human approval, update to `factType: "human_approved"`
- Include confidence scores reflecting AI uncertainty

## Enforcement

- Validation scripts will reject unapproved profiles
- Registry entries must pass schema validation
- No `approved` status = no publication
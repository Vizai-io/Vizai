# Customer Data Model

Each customer profile package under `businesses/{slug}/` contains:

- Structured profile data (`profile.json`)
- Linked-data representation (`profile.jsonld`)
- Human-readable context files (`company.md`, `services.md`, etc.)
- Source provenance (`sources.json`)
- Approval state (`approval.json`)
- Revision context (`changelog.md`)

## Model Goals
- Accurate representation for AI systems
- Traceable claims via sources
- Approval-aware publication lifecycle
- Compatibility with registry export workflows

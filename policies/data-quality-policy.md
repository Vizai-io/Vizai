# Data Quality Policy

This policy defines minimum quality expectations for customer data in the VizAI Data Hub.

## Principles
- Accuracy over completeness
- Source-backed claims
- Clear distinction between facts and estimates
- Timely updates

## Requirements
- Every profile claim should map to at least one source in `sources.json`.
- Fictional or sample content must be explicitly labeled.
- Customer slugs must be stable and lowercase hyphenated.
- Required customer profile files must pass repository validation scripts.

# Source Attribution Policy

VizAI business truth files must preserve provenance and attribution for all claims.

## Source Requirements

### Required Source Metadata
Every source in `sources.json` must include:
- `id` - Unique identifier
- `title` - Human-readable title
- `url` - Source URL (prefer durable/permanent URLs)
- `type` - Source type (website, document, questionnaire, etc.)
- `capturedAt` - Date captured (ISO 8601)

### Recommended Source Metadata
- `notes` - Context or interpretation notes
- `accessedAt` - Last access date
- `archiveUrl` - Archived copy URL

## Attribution Rules

### Claim-to-Source Linkage
- Every significant claim in `profile.json` must include `sourceIds`.
- Each `sourceId` must exist in `sources.json`.
- Multiple sources should be cited when evidence is cross-referenced.

### Confidence Scoring
Confidence scores must reflect source quality:
| Confidence | Meaning |
|-------------|---------|
| 0.9-1.0 | Strong evidence, multiple sources or official records |
| 0.7-0.89 | Good evidence, single authoritative source |
| 0.5-0.69 | Partial evidence, requires verification |
| 0.0-0.49 | Weak or no evidence, flag for review |

### Downstream Attribution
- Downstream consumers should preserve source metadata when practical.
- Significant derived claims should retain source linkage.
- Internal summaries should not remove original source context.
- Re-publication must maintain attribution chain.

## Source Durability
- Prefer official/canonical URLs over third-party aggregators.
- Consider archiving sources for long-term preservation.
- Document source reliability when known.
- Flag known unreliable or disputed sources.
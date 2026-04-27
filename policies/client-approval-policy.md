# Client Approval Policy

All publishable customer profile data must be approved before external use or publication.

## Approval Steps
1. **Prepare package** - Generate approval packet using `build_approval_packet.py`
2. **Gather evidence** - Attach source evidence for all key claims
3. **Submit for review** - Send approval packet to customer
4. **Record decision** - Update `approval.json` with status
5. **Publish scope** - Only publish items explicitly approved

## Approval States
| Status | Description |
|--------|-------------|
| `draft` | Initial draft, not submitted |
| `pending` | Submitted for customer review |
| `in_review` | Currently being reviewed |
| `approved` | Approved for publication |
| `rejected` | Not approved - revisions needed |
| `superseded` | New version replaces this entry |

## Required Approval Metadata
```json
{
  "status": "approved",
  "submittedAt": "2026-04-27",
  "approvedBy": "customer@example.com",
  "approvedAt": "2026-04-28",
  "scope": ["profile.json", "profile.jsonld"]
}
```

## Scope Rules
- Approval scope must explicitly list all files approved for publication.
- New files added after approval require re-approval.
- Major changes (new services, locations, descriptions) require re-approval.

## Human Review Requirements
- AI-generated content (descriptions, summaries) MUST be reviewed by a human before approval.
- Automated fact extraction requires human verification.
- Customer-provided claims should still be spot-checked against public sources.

## Re-Approval Triggers
Re-approval is required when:
- Business category changes
- New service or product lines added
- Location additions or closures
- Brand name or legal name changes
- More than 30% of profile fields change
- Annual review cycle completes
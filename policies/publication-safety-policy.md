# Publication Safety Policy

This policy defines what may and may not be published from the VizAI Data Hub.

## Publication Boundaries

### Never Publish
- Private customer questionnaire answers not explicitly approved
- Raw full website scrape text or complete page dumps
- Confidential contacts, pricing, contracts, or credentials
- Internal reviewer notes or non-public discussion
- AI-generated content that has not been human-approved
- Claims marked as speculative or unverified
- Draft or pending approval content
- Credentials, API keys, or authentication tokens

### Publish Only When Approved
- Source-backed facts from public websites
- Customer-approved business descriptions
- Listed services, products, and offerings
- Publicly announced locations
- Industries served (publicly known)
- Contact information explicitly approved for publication
- Registry entry cards (lightweight discovery format)

### Source-Backed Facts Only
- Facts must be verifiable from public sources OR explicitly approved by customer.
- Each published claim should have clear provenance.
- AI-generated descriptions require human review before any publication.

## File Publication Rules

### Rich Profiles (`businesses/{slug}/`)
Rich profiles live in the VizAI Data Hub and contain complete information:
- `profile.json` - Full structured profile
- `profile.jsonld` - Schema.org representation
- `sources.json` - Source metadata
- Supporting `.md` files

These files are NOT the public registry - they are internal/customer-facing.

### Registry Entries (`business-registry/`)
Registry entries are lightweight discovery cards:
- Basic business info (name, domain, category)
- Short description
- Services/products summary
- Link to full profile in VizAI Data Hub

Registry entries should NOT contain:
- Full scraped content
- Internal notes
- Unapproved claims
- Source raw text

### Approval Requirement
No profile should be published as "approved" without:
1. Human-reviewed approval packet
2. Explicit approval in `approval.json`
3. Verification status set to appropriate value

## AI-Generated Content
- All AI-generated descriptions must be marked with `factType: "ai_generated"`
- Must receive human approval before publication
- Must cite source prompt if derived from specific input
- Should include confidence scores reflecting AI uncertainty
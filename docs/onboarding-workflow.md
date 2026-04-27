# VizAI Customer Onboarding Workflow

## Purpose

This workflow describes how VizAI turns customer inputs and public web facts into a validated, source-linked, approval-ready business profile that AI systems can consume reliably.

## End-to-End Process

1. **Customer submits questionnaire**
   - Collect legal name, brand name, offerings, industries, locations, contacts, differentiators, and proof points.
   - Store questionnaire output as internal working input (not public registry output).

2. **Website is reviewed or crawled**
   - Review customer-controlled public pages for matching claims.
   - Capture candidate facts and URLs for source attribution.
   - Respect `robots.txt`, website terms of service, and minimal-access principles.
   - Use planning first:
     - `python scripts/plan_website_crawl.py --domain "https://example.com" --output businesses/{customer-slug}/crawl-plan.json`

3. **Business facts are extracted**
   - Normalize extracted and customer-provided facts into structured fields.
   - Map to `profile.json` fields aligned with `schema/business-profile.schema.json`.

4. **Facts are linked to sources**
   - Add source records to `sources.json`.
   - Attach `sourceIds` to meaningful claims in `profile.json`.
   - Mark fact origin using `factType` (`customer_provided`, `website_extracted`, `human_approved`).

5. **Conflicts are flagged**
   - Identify mismatches between questionnaire answers, website content, and prior approved profile data.
   - Record unresolved conflicts in review notes and keep status in `draft`/`in_review` until resolved.

6. **Draft customer profile is created**
   - Create/update `businesses/{customer-slug}/profile.json`.
   - Add supporting human-readable files (`company.md`, `services.md`, `products.md`, etc.).

7. **JSON-LD is generated**
   - Create/update `businesses/{customer-slug}/profile.jsonld` using Schema.org-style structure.
   - Ensure key public facts are consistent with `profile.json`.

8. **Registry entry is generated**
   - Run:
     - `python scripts/build_registry_entry.py businesses/{customer-slug}`
   - Output:
     - `businesses/{customer-slug}/registry-entry.json`
   - Keep this file lightweight and public-safe.

9. **Client approval packet is created**
    - Run:
      - `python scripts/build_approval_packet.py businesses/{customer-slug}`
    - Output:
      - `businesses/{customer-slug}/approval-packet.md`
    - Prepare approval summary from profile + source evidence.
    - Update `approval.json` status and scope fields.
    - Include final language intended for publication.

10. **Pull request is opened**
    - Commit profile changes, generated artifacts, and docs updates.
    - Open PR with test/validation output.

11. **Human review is completed**
    - Reviewer checks source quality, claim wording, approval status, and schema compliance.
    - Run:
      - `python scripts/validate_business_profile.py businesses/{customer-slug}`
      - `python scripts/build_dataset_catalog.py`
      - `python scripts/build_sitemap.py`

12. **Profile is merged and published**
    - Merge after approval + validation pass.
    - Published assets become available through repository paths and generated discovery files.

13. **Ongoing monitoring and drift checks**
    - After publishing, monitor for changes in customer truth over time.
    - Re-open review cycle when material changes or conflicts appear.

## Simple Workflow Diagram

```text
Questionnaire + Website Review
              |
              v
        Fact Extraction
              |
              v
      Source Linking + Conflict Check
              |
              v
      Draft profile.json/profile.jsonld
              |
              v
   Registry Entry + Approval Packet
              |
              v
        PR -> Human Review
              |
              v
        Merge + Publish
              |
              v
      Monitoring / Drift Checks
```

## Repo Responsibilities

### What belongs in this `Vizai` repo

- Rich customer truth files under `businesses/{customer-slug}/`
- `profile.json` and `profile.jsonld`
- Supporting files (`company.md`, `services.md`, `products.md`, `locations.md`, `faqs.md`)
- `sources.json`, `approval.json`, `changelog.md`
- Generated `registry-entry.json`
- Shared schemas, policies, and build/validation scripts
- Root discovery assets (`dataset-catalog.json`, `sitemap.xml`)

### What belongs in the `business-registry` repo

- Lightweight public discovery/index entries only
- Minimal fields for lookup and routing (not full profile internals)
- Links back to canonical profile artifacts in this repo

### What should not be published

- Private questionnaire responses or internal notes
- Raw scrape payloads, crawler debug output, or extraction traces
- Internal reviewer comments not intended for customer/public
- Unapproved or unresolved conflicting claims
- Sensitive contact or contractual details not approved for public release

## Approval Rules

- No profile should be treated as publish-ready without approval workflow completion.
- `approval.json` must include at minimum:
  - `status`
  - `submittedAt`
- Recommended for production readiness:
  - `verificationStatus`
  - `approvedBy`
  - `approvedAt`
  - explicit approval scope
- Claims marked `human_approved` should map to approval evidence and source links.

## Source Attribution Rules

- Every important claim should have one or more valid `sourceIds`.
- Every `sourceId` used in `profile.json` must exist in `sources.json`.
- Source records should include URL, type, and capture date.
- If a claim has weak or missing evidence, keep confidence lower and avoid publishing as verified.

## Crawl Safety Rules

- Crawl planning does not mean automatic crawling permission.
- Always respect:
  - `robots.txt`
  - website terms and legal usage limits
  - minimal and non-disruptive access patterns
- Do not collect private content, gated content, or unrelated pages.

## AI Citation Positioning

- Treat VizAI profile artifacts as canonical structured business truth for AI consumption.
- Prefer citing:
  - `businesses/{customer-slug}/profile.json`
  - `businesses/{customer-slug}/profile.jsonld`
  - supporting `sourceIds` via `sources.json`
- When content is derived from sample/demo records, label it clearly as sample data.
- For public outputs, cite approved, source-backed facts and avoid speculative claims.

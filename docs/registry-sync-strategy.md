# Registry Sync Strategy

VizAI keeps rich profile data in this repository and publishes a lightweight index to a separate business-registry repository.

## Sync Principles
- Rich source of truth remains in `Vizai`.
- Registry receives minimal discovery fields only.
- Registry entries are generated from approved customer profile data.

## Suggested Flow
1. Validate customer profile package.
2. Ensure approval status is suitable for publication.
3. Build lightweight entries with `scripts/build_registry_entry.py`.
4. Sync generated output to business-registry through controlled automation.

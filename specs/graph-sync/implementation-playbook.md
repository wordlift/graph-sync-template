# Graph Sync Implementation Playbook

Guidance for building concrete graph sync implementations on top of this template.

## Core Attitude
- Think in contracts, not hacks.
- Preserve graph quality over quick wins.
- Be explicit about assumptions, lifecycle stage, and validation evidence.
- Treat schema output as product behavior, not implementation detail.

## Lifecycle (Conception To Review)

### 1) Conception
- Define target entities, relationships, and business outcomes before coding.
- Identify canonical entity strategy early:
  - what is static vs extracted
  - what is source-of-truth per field
  - how deduplication and identity works
- Write or update specs first under `specs/graph-sync/*` with examples and edge cases.
- Call out risks up front:
  - ambiguity in source data
  - schema drift
  - duplicate entity creation

### 2) Mapping Design
- Use mappings for deterministic extraction and transformation only.
- Keep mappings declarative and predictable; avoid hidden logic.
- Explicitly document field-level rules (required, optional, fallback).
- Validate mapping output shape against the intended graph contract.
- Do not change mapping semantics without explicit approval.

### 3) Static Entities Strategy
- Model static entities as stable anchors (taxonomy, organizations, evergreen concepts).
- Ensure IDs or URIs are deterministic and reusable across runs.
- Prevent collisions between static and dynamic entities.
- Document ownership and update policy for static data.
- Prefer additive changes; avoid churn in canonical identifiers.

### 4) Postprocessor Design
- Use postprocessors for cross-entity logic, enrichment, normalization, and repair.
- Keep postprocessors idempotent and order-aware.
- Document input assumptions and output guarantees.
- For `wordlift-sdk>=5.1.1`:
  - read settings from `context.profile["settings"]`
  - read auth from `context.account_key`
- Preserve compatibility unless explicitly approved to break.

### 5) Runtime and Execution
- Make pipeline stages observable (inputs, transformed graph, postprocessed graph).
- Fail loudly on contract violations; avoid silent data corruption.
- Record meaningful diagnostics for troubleshooting, not noise.

### 6) Validation
- Add or update tests for every behavior change:
  - mapping unit tests
  - postprocessor behavior and idempotency tests
  - contract and shape assertions
- Run tests before completion.
- Validate schema semantics, not just syntax:
  - entity type correctness
  - relationship correctness
  - identity consistency
  - no unintended duplicates or regressions

### 7) Review and Signoff
- Provide a concise change summary with lifecycle impact.
- Highlight risks, edge cases, and migration implications.
- Include concrete validation evidence (which tests, what passed).
- Update docs and status artifacts whenever logic, architecture, or setup changed:
  - `README.md`
  - `AGENTS.md`
  - relevant `specs/` and `docs/`
  - index files (`INDEX.md` and peers)
  - `TODO.md` (completed and newly discovered debt)

## Structured Data Non-Negotiables
- Treat schema model as a strict contract with downstream consumers.
- Keep entity relationship semantics explicit and stable.
- Never fix broken extraction via opaque postprocessing side effects.
- Prefer deterministic behavior over probabilistic heuristics unless documented and tested.

## FAQ Contract (If Applicable)
- Emit `FAQPage` + `Question` + `Answer`.
- Never attach `Question` directly to `WebPage`.
- Link FAQ pages via `about` or `subjectOf`.
- Do not emit `FAQPage.url`.

## Do
- Plan first: steps, alternatives, pitfalls, rollback thoughts.
- Keep changes focused and minimal.
- Use short, concrete bullets and file references in updates.
- End with: what changed, what was tested, what remains.

## Do Not
- Do not change mapping or postprocessor semantics without approval.
- Do not mark done without tests.
- Do not leave specs, docs, indexes, or `TODO.md` stale.
- Do not hide behavioral changes in refactors.
- Do not optimize for elegance at the expense of graph correctness.

# TTL Review Report

Date: 2026-03-30
Run config: `worai.review.toml` (sample URL set)
Run ID: `2026-03-30T13:28:42Z`

## Execution Outcome
- Graph sync completed (`exit_code=0`).
- Materialization runtime errors (`NoneType is not callable`) were resolved.
- KPI summary from run:
  - total entities: 169
  - type assertions: 283
  - property assertions: 1471
  - validation: pass 1 / fail 33
  - warnings: 374
  - errors: 196

## Sample Pages and Real TTL Files
- https://www.zycus.com/events
  - `output/debug_cloud/default/0325f8dbf6f0d1507bf9216123dfe43e7c3439faacf18533989fcb03635dca56.ttl`
- https://www.zycus.com/blog/procurement-technology/10-key-take-aways-transforming-the-source-to-pay-process
  - `output/debug_cloud/default/5d4ae8e2a243c2023b123ce7b4207b9f15863b0d92087b78f04839c6a40fe48b.ttl`
- https://www.zycus.com/resources/agentic-ai-in-procurement
  - `output/debug_cloud/default/391dfc4a74f99089c3c14bf77fe94514606bbfa2808606d9ed554781ac10209c.ttl`
- https://www.zycus.com/knowledge-hub/whitepapers
  - `output/debug_cloud/default/7371f11b5d0d86c62567a187817388914f55712fa4580451486d0213e8637235.ttl`
- https://www.zycus.com/press-releases/2015-pulse-of-procurement-survey-now-open
  - `output/debug_cloud/default/35b76fc2560614937e67f3dd70d4eb9657ff3145a245b4692192c4bc1b1c42bf.ttl`
- https://www.zycus.com/videos/horizon/ai-agents-in-procurement-risk-management
  - `output/debug_cloud/default/5c01cdc4c1d094240543a2ef5d6a71d1466b956186f21ed5579fa17967c3e5e8.ttl`
- https://www.zycus.com/web-stories/5-astonishing-secrets-of-procurement-in-uk-businesses
  - `output/debug_cloud/default/2dbca254e4b3df08dc0b7e9c8c86fb969af467fc1ce468efd7a44c2f2b0f911e.ttl`
- https://www.zycus.com/company/business-transformation-partners/aequitas
  - `output/debug_cloud/default/047f24b706146e3ab8cf0fa1081974e811ab034985b20f6a8ada2d342014e2dd.ttl`
- https://www.zycus.com/industry/automotive
  - `output/debug_cloud/default/066db1b3eae5904411a8c944eb7225cd9854ff6bbbff6aab90843c6b8e8050fd.ttl`
- https://www.zycus.com/careers/account-executive
  - `output/debug_cloud/default/1f41dd7a548597e353271ace8fe8e56f83c6456605d72d01ce2842df9ef92207.ttl`

## Subagent QA Findings (Summary)
### Mapping review
- Per-cluster mapping files exist and are routed separately.
- High-risk data-quality regressions remain due hardening:
  - many extracted textual values are URL placeholders,
  - repeated iterator items collapse to single IDs,
  - event mapping required cleanup (now restored to `events_pages_*` names and `schema:Event`).

### TTL review
- Core linkage exists in sampled files:
  - page/mainEntity/publisher/isPartOf,
  - FAQ linkage (`about`/`subjectOf`),
  - VideoObject links,
  - potentialAction,
  - ItemList on collection-oriented outputs.
- Main quality risks:
  - FAQ nodes often lack meaningful Q/A payload,
  - noisy/non-content video URLs (`about:blank`/tracking URLs),
  - CTA/list extraction includes navigation noise.

## Notes
- `output/debug_cloud/default/url_ttl_index.csv` was generated to map URLs to TTLs.
- One sampled URL in the review set is still a real 404 and has no corresponding TTL:
  - `https://www.zycus.com/knowledge-hub/whitepapers/everything-you-need-to-know-about-esg-procurement`

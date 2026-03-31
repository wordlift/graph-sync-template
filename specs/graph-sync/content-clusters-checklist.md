# Content Clusters Checklist (zycus.com)

Status legend: `pending` | `in_progress` | `done`

Analysis basis:
- Source sitemap index: `https://www.zycus.com/sitemap_index.xml`
- Snapshot size: `3,306` unique URLs
- Clusters below are ordered and mutually exclusive (first match wins).

## Cluster List

1. `home_page.yarrrml` (`^/$`) — count `1` — semantic group: `WebPage` (homepage) — `done`
2. `search_page.yarrrml` (`^/search(?:/.*)?$`) — count `0` — semantic group: `SearchResultsPage` — `done`
3. `blog_hub_newsletter_utility.yarrrml` (`^/blog$|^/blog/newsletter(?:/.*)?$|^/blog/[^/]+$`) — count `6` — semantic group: `CollectionPage` / blog hub utility — `done`
4. `blog_articles.yarrrml` (`^/blog/(?!newsletter(?:/|$))[^/]+/.+$`) — count `1135` — semantic group: `BlogPosting` — `done`
5. `knowledge_hub_hub_pages.yarrrml` (`^/knowledge-hub(?:/[^/]+)?$`) — count `20` — semantic group: `CollectionPage` / resource hubs — `done`
6. `knowledge_hub_assets.yarrrml` (`^/knowledge-hub/[^/]+/.+$`) — count `698` — semantic group: `Article` / downloadable asset landing — `done`
7. `press_news_releases.yarrrml` (`^/press-releases(?:/.*)?$`) — count `492` — semantic group: `NewsArticle` / press — `done`
8. `videos_hub_pages.yarrrml` (`^/videos(?:/[^/]+)?$`) — count `20` — semantic group: `CollectionPage` / video hubs — `done`
9. `videos_detail_pages.yarrrml` (`^/videos/[^/]+/.+$`) — count `374` — semantic group: `VideoObject` + `WebPage` — `done`
10. `solution_pages.yarrrml` (`^/solution(?:/.*)?$`) — count `165` — semantic group: product/solution detail (`WebPage` + `SoftwareApplication`/`Service` where applicable) — `done`
11. `customers_success_story.yarrrml` (`^/customers/success-story(?:/.*)?$`) — count `61` — semantic group: case studies (`Article`) — `done`
12. `customers_other.yarrrml` (`^/customers(?:/.*)?$`) — count `13` — semantic group: customer directories/profiles (`CollectionPage` or `Organization`) — `done`
13. `company_partner_pages.yarrrml` (`^/company/(business-transformation-partners|technology-partners|consulting-partners|strategic-partners)(?:/.*)?$`) — count `48` — semantic group: partner program pages (`CollectionPage` / `Organization`) — `done`
14. `company_corporate_brand.yarrrml` (`^/company(?:/.*)?$`) — count `19` — semantic group: corporate pages (`AboutPage`, `ContactPage`, policy) — `done`
15. `resources_pages.yarrrml` (`^/resources(?:/.*)?$`) — count `50` — semantic group: tools/resources (`CollectionPage`/`WebPage`) — `done`
16. `web_stories.yarrrml` (`^/web-stories(?:/.*)?$`) — count `23` — semantic group: web stories (`Article`) — `done`
17. `industry_pages.yarrrml` (`^/(industry|industries)(?:/.*)?$`) — count `20` — semantic group: vertical landing pages (`CollectionPage`/`WebPage`) — `done`
18. `careers_pages.yarrrml` (`^/(careers|company/careers)(?:/.*)?$`) — count `31` — semantic group: jobs/careers (`JobPosting` where detail exists) — `done`
19. `role_pages.yarrrml` (`^/role(?:/.*)?$`) — count `3` — semantic group: persona landing pages (`WebPage`) — `done`
20. `compare_pages.yarrrml` (`^/compare(?:/.*)?$`) — count `14` — semantic group: comparison pages (`WebPage`) — `done`
21. `events_pages.yarrrml` (`^/events(?:/.*)?$|^/events-upcoming-webinars$`) — count `10` — semantic group: events/webinars (`Event`) — `done`
22. `horizon_event_pages.yarrrml` (`^/horizon(?:/.*)?$|^/horizon-us-2025-from-intake-to-outcomes$`) — count `4` — semantic group: event campaign pages (`Event`/`WebPage`) — `done`
23. `merlin_experience_center.yarrrml` (`^/merlin-experience-center(?:/.*)?$`) — count `6` — semantic group: product demo hub/detail (`CollectionPage`/`WebPage`) — `done`
24. `scale_implementation_framework.yarrrml` (`^/scale-implementation-framework(?:/.*)?$`) — count `8` — semantic group: framework pages (`HowTo`/`WebPage`) — `done`
25. `testimonials_pages.yarrrml` (`^/testimonial(?:/.*)?$`) — count `1` — semantic group: testimonial detail (`Article`) — `done`
26. `campaign_landing_misc.yarrrml` (`^/(campaigns|campaings)(?:/.*)?$|^/(campaign-lp-2026|ai-council|ap-automation-demo|aura-horizon-agent|anzgov|procurement-ai-world-tour-zycus-global|the-periodic-table-of-procurement|horizon-agent-portrait|merlin-experience-center-2025|merlin-experience-center-new-zycus|solution-e-invoicing-global-e-invoicing-compliance)$`) — count `22` — semantic group: campaign/LP pages (`WebPage`) — `done`
27. `single_level_detail_misc.yarrrml` (`^/(?!blog|knowledge-hub|press-releases|videos|solution|customers|resources|web-stories|industry|industries|role|company|careers|compare|campaigns|campaings|events|horizon|merlin-experience-center|scale-implementation-framework|testimonial$)[^/]+$`) — count `62` — semantic group: singleton landing pages (`WebPage`) — `done`
28. `default.yarrrml` (`.*`) — count `0` — semantic group: catch-all fallback — `done`

## High-Priority Cluster Samples

- `blog_articles.yarrrml`
  - `https://www.zycus.com/blog/procurement-technology/10-key-take-aways-transforming-the-source-to-pay-process`
  - `https://www.zycus.com/blog/ai-agents/agentic-ai-for-automated-po-generation`
  - `https://www.zycus.com/blog/source-to-pay/2026-gartner-magic-quadrant-zycus-leader`
- `knowledge_hub_assets.yarrrml`
  - `https://www.zycus.com/knowledge-hub/whitepapers/everything-you-need-to-know-about-esg-procurement`
  - `https://www.zycus.com/knowledge-hub/on-demand-webinar`
  - `https://www.zycus.com/knowledge-hub/ebooks`
- `press_news_releases.yarrrml`
  - `https://www.zycus.com/press-releases/zycus-named-a-leader-in-gartner-magic-quadrant-for-source-to-pay-suites`
- `videos_detail_pages.yarrrml`
  - `https://www.zycus.com/videos/horizon/ai-agents-in-procurement-risk-management`
  - `https://www.zycus.com/videos/procurement-stories/delta-airlines-ai-procurement-transformation`
- `solution_pages.yarrrml`
  - `https://www.zycus.com/solution/accounts-payable-automation-software`
  - `https://www.zycus.com/solution/intake-management`

## Validation Goals Per Cluster

- Keep primary semantic type homogeneous per cluster.
- Always include `schema:url` and `schema:name`.
- Scout Q/A blocks and emit connected `FAQPage` markup when applicable (except when FAQ itself is main entity).
- Prefer `CollectionPage` + list items with URL links on hub/index clusters.

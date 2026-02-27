# Agent Working Agreement

Internal operating rules learned from practical usage.

## URI Policy

- Use `http://schema.org` as the default vocabulary base URI.
- Use `https://schema.org` only when the user explicitly requires it.
- Assign the same `schema:url` to only one entity to prevent duplicate entities.

## Loader Selection Policy

- Unless the user specifies a loader, use this priority order:
  - `simple`
  - `playwright`
  - `proxy`
  - `web_scrape_api`
  - `premium_scraper`
- Before attempting the `playwright` loader, confirm the Playwright MCP integration is installed and available.

## Extraction Policy

- Inspect XHR/network traffic before finalizing extraction.
- If a structured upstream source exists, prefer it over HTML parsing.
- Be greedy in extraction coverage: collect all high-value content available from the page and related API calls that expose structured data.
- For YARRRML mappings, use relative XPath selectors and avoid absolute XPath paths.
- Ask for explicit user permission before using static fallback templates or static fallback extraction paths.
- Do not hardcode constants from sample web pages; treat sample pages as variable input and use reusable extraction/mapping rules that generalize across source pages.
- Do not use hard-coded fallbacks unless the user explicitly authorizes them.

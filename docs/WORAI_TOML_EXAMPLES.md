# worai.toml Examples

Practical, minimal, complete examples using fake data.

## 1. URLs Source (single profile)

```toml
[profiles._base]
overwrite = true
concurrency = 8
ingest_loader = "web_scrape_api"
ingest_timeout_ms = 120000
ingest_source = "urls"
urls = [
  "https://www.acme.example/insurance/home",
  "https://www.acme.example/insurance/auto"
]

[profiles.default]
api_key = "${WORDLIFT_API_KEY}"
```

## 2. Sitemap Source (single profile)

```toml
[profiles._base]
overwrite = true
concurrency = 8
ingest_loader = "web_scrape_api"
ingest_timeout_ms = 120000
ingest_source = "sitemap"
sitemap_url = "https://www.acme.example/sitemap.xml"
sitemap_url_pattern = "/insurance/.*"

[profiles.default]
api_key = "${WORDLIFT_API_KEY}"
```

## 3. Google Sheets Source (single profile)

```toml
[profiles._base]
overwrite = true
concurrency = 8
ingest_loader = "web_scrape_api"
ingest_timeout_ms = 120000
ingest_source = "sheets"
sheets_url = "https://docs.google.com/spreadsheets/d/1FAKE_SHEET_ID_ABC123"
sheets_name = "urls"
sheets_service_account = "${SHEETS_SERVICE_ACCOUNT}"

[profiles.default]
api_key = "${WORDLIFT_API_KEY}"
```

## 4. Multi-profile Setup (shared source config)

```toml
[profiles._base]
overwrite = true
concurrency = 4
ingest_loader = "web_scrape_api"
ingest_timeout_ms = 120000
ingest_source = "sitemap"
sitemap_url = "https://www.acme.example/sitemap.xml"

[profiles.retail]
api_key = "${WORDLIFT_API_KEY}"

[profiles.corporate]
api_key = "${WORDLIFT_API_KEY}"
```

## 5. Optional Runtime Knobs

```toml
[profiles._base]
overwrite = false
concurrency = 2
ingest_loader = "playwright"
ingest_timeout_ms = 45000
google_search_console = true
ingest_source = "urls"
urls = ["https://www.acme.example/"]

[profiles.default]
api_key = "${WORDLIFT_API_KEY}"
```

## .env Example

```bash
WORDLIFT_API_KEY=wlk_test_1234567890
SHEETS_SERVICE_ACCOUNT={"type":"service_account","project_id":"acme-dev"}
YOUTUBE_API_KEY=AIzaSy_FAKE_ONLY_FOR_EXAMPLE
```

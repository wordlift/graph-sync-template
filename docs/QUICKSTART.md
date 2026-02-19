# Quick Start Guide

## 1. Prerequisites

- Install `copier`
- Install `worai` (see https://docs.wordlift.io/worai/install/)

## 2. Generate Project

```bash
copier copy . ../my-graph-project
```

## 3. Setup

```bash
cd ../my-graph-project
uv sync
```

## 4. Configure Secrets

Copier creates `.env` automatically. Verify or update it:

```bash
WORDLIFT_API_KEY=your_api_key
SHEETS_SERVICE_ACCOUNT=.config/sa-key.json
YOUTUBE_API_KEY=your_youtube_api_key_optional
```

`SHEETS_SERVICE_ACCOUNT` is only needed when `source_type=google_sheets`.

## 5. Run Graph Sync

```bash
set -a && source .env && set +a
worai --config worai.toml graph sync --profile <default_profile>
```

With debug output:

```bash
worai --config worai.toml graph sync --profile <default_profile> --debug
```

## Static Template Quick Checks

- One subject node per static template file.
- No blank nodes in static templates.
- `schema:url` and `schema:sameAs` use URL literals.
- Template filenames are depth-prefixed (`20_*`, `40_*`, ...).

## Postprocessors

- Example template: `profiles/_base/postprocessors.example.toml`

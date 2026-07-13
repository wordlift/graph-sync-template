# Quick Start Guide

## Agent-Driven Approach (Recommended)

Ask Codex or Claude Code to run the graph-sync workflow end to end through the installed Graph Sync Agent Kit.

Codex prompt:

```text
Use the graph-sync-agent-kit:graph-sync-curator skill to start the graph-sync workflow for example.org.
```

Claude Code prompt:

```text
Use $graph-sync-curator to start the graph-sync workflow for example.org.
```

The graph-sync skills coordinate project setup, curation, implementation, credential checks, sync/audit validation, and publish handoff. Install and update commands live in `wordlift/graph-sync-agent-kit`.

## Manual Approach

Use this path when running a generated project without agent orchestration.

### 1. Create The Project

Install `uv` and use `pipx` to run Copier without a global install:

```bash
pipx run copier copy gh:wordlift/graph-sync-template my-graph-project
cd my-graph-project
uv sync
```

If `copier` is already installed, `copier copy gh:wordlift/graph-sync-template my-graph-project` is equivalent.

### 2. Configure Secrets

Copier creates `.env` automatically. Verify or update it:

```bash
WORDLIFT_API_KEY=your_api_key
SHEETS_SERVICE_ACCOUNT=.config/sa-key.json
YOUTUBE_API_KEY=your_youtube_api_key_optional
```

`SHEETS_SERVICE_ACCOUNT` is only needed when `source_type=google_sheets`.

### 3. Run Graph Sync

The GitHub workflow is the repeatable manual path because it pins the graph-sync action, which selects its compatible `worai` version. After each successful sync, it calculates and uploads a graph KPI snapshot by default; KPI failures remain warning-only unless the workflow is configured otherwise.

For a local run, use the command shape documented by the installed `worai` version. Current generated projects are compatible with:

```bash
set -a && source .env && set +a
worai --config worai.toml --profile <default_profile> graph sync run
```

With debug output:

```bash
worai --config worai.toml --profile <default_profile> graph sync run --debug
```

Without a global `worai` install, use `pipx`:

```bash
pipx run worai --config worai.toml --profile <default_profile> graph sync run
```

If your installed `worai` version exposes a different command shape, follow the official `worai` command documentation for that version.

# Lucidia

**The AI that remembers you.**

Lucidia is a conversational AI platform with persistent memory, multi-service orchestration, and a sovereign-first architecture. Built on FastAPI, it runs on your hardware — no cloud dependency, no data siphon.

## What It Does

- **Persistent Memory** — SQLite-backed key-value memory that persists across sessions. Every conversation builds on the last.
- **Agent System** — Chat with Lucidia, or call tools directly. Slack, Asana, Linear, Notion, GitHub, Jira — all accessible through a unified agent interface.
- **Local AI Completion** — Connect to any local LLM (llama.cpp, Ollama) for sovereign AI inference with zero external API calls.
- **Provider Registry** — Feature-flagged integrations. Enable services by setting environment variables — no code changes needed.
- **Health Monitoring** — Built-in health checks for fleet deployment across Raspberry Pi clusters.

## Architecture

```
┌─────────────────────────────────────────┐
│              FastAPI Server             │
├──────────┬──────────┬───────────────────┤
│  Memory  │  Agent   │   Completions     │
│  SQLite  │  Router  │   Local LLM       │
├──────────┴──────────┴───────────────────┤
│          Provider Registry              │
│  Slack · Asana · Linear · Notion · ...  │
└─────────────────────────────────────────┘
```

## Quickstart

```bash
# Clone
git clone https://github.com/blackboxprogramming/lucidia.git
cd lucidia

# Install
pip install fastapi pydantic uvicorn

# Configure integrations (optional)
export SLACK_BOT_TOKEN=xoxb-...
export LINEAR_API_KEY=lin_...
export GITHUB_TOKEN=ghp_...

# Run
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Status check |
| `/healthz` | GET | Health probe |
| `/memory/put` | POST | Store a memory `{key, value}` |
| `/memory/get?key=` | GET | Retrieve a memory by key |
| `/agent/capabilities` | GET | List enabled integrations |
| `/agent/chat` | POST | Chat or call a tool `{message, tool, args}` |
| `/agent/complete` | POST | Local LLM completion `{prompt, max_tokens}` |
| `/slack/say` | POST | Send a Slack message |
| `/asana/me` | GET | Asana user info |
| `/linear/me` | GET | Linear user info |

## Environment Variables

| Variable | Service |
|----------|---------|
| `SLACK_BOT_TOKEN` | Slack |
| `ASANA_ACCESS_TOKEN` | Asana |
| `LINEAR_API_KEY` | Linear |
| `NOTION_TOKEN` | Notion |
| `GITHUB_TOKEN` | GitHub |
| `JIRA_URL` + `JIRA_EMAIL` + `JIRA_API_TOKEN` | Jira |

## Ecosystem

- **[Lucidia CLI](https://github.com/blackboxprogramming/lucidia-cli)** — Sovereign coding assistant (explain, review, fix, copilot)
- **[Context Bridge](https://github.com/blackboxprogramming/context-bridge)** — Persistent memory layer for cross-session AI context
- **[Remember](https://github.com/blackboxprogramming/remember)** — AI-powered persistent memory for developers
- **[BlackRoad OS](https://github.com/blackboxprogramming/BlackRoad-Operating-System)** — The operating system for governed AI

## Infrastructure

Lucidia runs on the BlackRoad sovereign computing fleet:
- 5 Raspberry Pi 5 nodes (WireGuard mesh)
- 52 TOPS AI acceleration (2x Hailo-8)
- 108 local models via Ollama
- Zero cloud dependencies

## License

Copyright 2026 BlackRoad OS, Inc. — Alexa Amundson. All rights reserved.

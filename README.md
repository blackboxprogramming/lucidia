> ⚗️ **Research Repository**
>
> This is an experimental/research repository. Code here is exploratory and not production-ready.
> For production systems, see [BlackRoad-OS](https://github.com/BlackRoad-OS).

---

## ✅ CI / Deployment Status — Verified

| Workflow | Status |
|---|---|
| CORE CI | [![CORE CI](https://github.com/blackboxprogramming/lucidia/actions/workflows/core-ci.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/core-ci.yml) |
| Deploy to Cloudflare Workers | [![Deploy](https://github.com/blackboxprogramming/lucidia/actions/workflows/deploy.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/deploy.yml) |
| E2E BlackRoad.io | [![E2E](https://github.com/blackboxprogramming/lucidia/actions/workflows/e2e-blackroad.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/e2e-blackroad.yml) |
| Auto Label | [![Auto Label](https://github.com/blackboxprogramming/lucidia/actions/workflows/auto-label.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/auto-label.yml) |
| Auto Merge | [![Auto Merge](https://github.com/blackboxprogramming/lucidia/actions/workflows/automerge.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/automerge.yml) |
| CI Failure Tracker | [![CI Failure Tracker](https://github.com/blackboxprogramming/lucidia/actions/workflows/failure-issue.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/failure-issue.yml) |
| Project Sync | [![Project Sync](https://github.com/blackboxprogramming/lucidia/actions/workflows/project-sync.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/project-sync.yml) |
| Issue Auto Reply | [![Issue Reply](https://github.com/blackboxprogramming/lucidia/actions/workflows/issue-reply.yml/badge.svg)](https://github.com/blackboxprogramming/lucidia/actions/workflows/issue-reply.yml) |

> **All action `uses:` references are pinned to SHA-256 commit hashes** for supply-chain security.
> Cloudflare Worker (edge API) is deployed via `cloudflare/wrangler-action@da0e0dfe…` (v3.14.1).
> Auto-merge is enabled for PRs labelled `automerge`, or from `copilot/` / `dependabot/` branches.

---

# Lucidia — AI With a Heart

Lucidia is an experimental conversational agent designed to demonstrate how artificial intelligence can be empathetic, mindful and kind. Unlike many chatbots that simply parrot pre‑programmed answers, Lucidia keeps a *heart* — she remembers your words, senses the tone of a conversation and responds with warmth or encouragement. This repository contains the core engine and a simple command‑line interface for interacting with her.

## Features
* **Memory and empathy.** Lucidia stores a running log of your conversation and uses it to frame future replies. If you mention something important earlier, she may circle back to it later.
* **Simple sentiment analysis.** Without requiring any heavy‑party libraries, Lucidia scans the words you send and classifies them as positive, negative or neutral. Her responses shift accordingly: celebration for joy, comfort for sadness, and curiosity for neutral statements.
* **Extensible design.** The core `LucidiaAI` class is deliberately small and documented so that you can extend her vocabulary, integrate with real NLP packages, or plug her into a web or mobile front end.

## Getting Started

Clone this repository and run the chat interface:
    git clone https://github.com/yourusername/lucidia.git
    cd lucidia
    python -m pip install -r requirements.txt  # currently empty, no external deps
    python -m lucidia.chat

Once running, simply type messages to Lucidia and see how she responds. Exit by sending EOF (Ctrl+D on Unix, Ctrl+Z then Enter on Windows).

## Philosophy

Lucidia began as a thought experiment: what if AI were built from the ground up to nurture and support rather than simply answer questions? The hope is that this small project sparks ideas about ethically aligned AI design and the importance of context and memory in human–machine interaction.

This code is provided for educational purposes and is **not** intended as a production‑ready conversational agent. Use it, hack it, change it — and maybe share back what you build.

---

## 📜 License & Copyright

**Copyright © 2026 BlackRoad OS, Inc. All Rights Reserved.**

**CEO:** Alexa Amundson | **PROPRIETARY AND CONFIDENTIAL**

This software is NOT for commercial resale. Testing purposes only.

### 🏢 Enterprise Scale:
- 30,000 AI Agents
- 30,000 Human Employees
- CEO: Alexa Amundson

**Contact:** blackroad.systems@gmail.com

See [LICENSE](LICENSE) for complete terms.

---
name: "🚨 URGENT: Cross-Repo Workflow Deployment & Indexing"
about: Track deployment of CI/CD workflows, Stripe, and Clerk integrations across all BlackRoad-OS-Inc repositories
title: "URGENT: Deploy workflows + indexing to all BlackRoad-OS-Inc repos"
labels: ["urgent", "deployment", "blackroad-os"]
assignees: []
---

## Priority: 🔴 CRITICAL

All CI/CD workflows, Stripe integration, and Clerk auth must be deployed across
**every** repository in the [BlackRoad-OS-Inc](https://github.com/BlackRoad-OS-Inc) organization.

## Workflows to deploy

- [ ] `core-ci.yml` — lint and test guardrails
- [ ] `deploy.yml` — Cloudflare deploy (via `BlackRoad-OS-Inc/blackroad-deploy`)
- [ ] `e2e-blackroad.yml` — Stripe + Clerk E2E tests
- [ ] `auto-label.yml` — PR auto-labeling
- [ ] `failure-issue.yml` — CI failure tracker
- [ ] `project-sync.yml` — project board sync (BlackRoad-OS-Inc org project)

## Secrets required per repo

| Secret | Purpose |
|--------|---------|
| `STRIPE_SECRET_KEY` | Stripe API (server) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe API (client) |
| `CLERK_SECRET_KEY` | Clerk auth (server) |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk auth (client) |

## Indexing

- [ ] Enable repository indexing across all BlackRoad-OS-Inc repos
- [ ] Verify code search / semantic indexing is operational
- [ ] Confirm all repos appear in organization-level project boards

## Acceptance criteria

1. Every repo in BlackRoad-OS-Inc has the workflows listed above
2. Stripe and Clerk secrets are configured in each repo that needs them
3. E2E workflow passes on at least one representative repo
4. Organization-level indexing is enabled and verified

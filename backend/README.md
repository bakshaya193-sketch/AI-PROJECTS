---
title: AI Customer Support Backend
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# AI Customer Support Agent — Backend

FastAPI backend for the AI Customer Support Agent. Powers the chat (RAG over
uploaded documents), multilingual support, sentiment analysis, support tickets,
agent handoff, analytics, and role-based auth.

This Space runs as a **Docker** app on port **7860**.

## Required Secrets

Set these in the Space **Settings → Variables and secrets**:

| Name | Description |
|------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key (`sk-...`) |
| `SITE_PASSWORD` | Password for the site access gate |
| `SECRET_KEY` | Any long random string (JWT signing) |
| `FRONTEND_URL` | Your deployed frontend URL (for CORS), e.g. `https://your-app.vercel.app` |

## Endpoints

`/health`, `/chat`, `/upload`, `/tickets`, `/analytics`, `/agent/*`, `/auth/login`,
`/config`, `/verify-access`. Interactive docs at `/docs`.

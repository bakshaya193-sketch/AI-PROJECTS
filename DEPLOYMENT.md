# 🚀 Deployment Guide

This app has **two parts** that deploy separately:

| Part | Folder | Host | Why |
|------|--------|------|-----|
| Backend (FastAPI) | `backend/` | **Render** | Runs Python + ChromaDB + SQLite |
| Frontend (React) | `frontend/` | **Vercel** | Serves the static built site |

Both are **free** and **auto-deploy** from your GitHub repo (`bakshaya193-sketch/AI-PROJECTS`).

> Deploy the **backend first**, because the frontend needs the backend's URL.

---

## Part 1 — Deploy the Backend on Render

1. Go to **https://render.com** and sign up (use **"Sign in with GitHub"**).
2. Click **New +** → **Web Service**.
3. Connect your GitHub and select the **`AI-PROJECTS`** repo.
4. Fill in the settings:
   - **Name:** `ai-support-backend` (or anything)
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
5. Scroll to **Environment Variables** and add:
   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | your OpenAI key (`sk-...`) |
   | `SITE_PASSWORD` | a password for the site gate (e.g. `welcome123`) |
   | `SECRET_KEY` | any long random string |
   | `PYTHON_VERSION` | `3.11.9` |
   | `FRONTEND_URL` | *(leave blank for now — add after Part 2)* |
6. Click **Create Web Service**. The first build takes ~5–10 minutes.
7. When it's live, copy the URL at the top, e.g. **`https://ai-support-backend.onrender.com`**
8. Test it: open `https://your-backend-url.onrender.com/health` → you should see `{"status":"healthy"}`

---

## Part 2 — Deploy the Frontend on Vercel

1. Go to **https://vercel.com** and sign up with **GitHub**.
2. Click **Add New…** → **Project**, then import the **`AI-PROJECTS`** repo.
3. Configure:
   - **Root Directory:** click **Edit** → select **`frontend`**
   - **Framework Preset:** Vercel auto-detects **Vite** ✅
4. Expand **Environment Variables** and add:
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | your Render backend URL (e.g. `https://ai-support-backend.onrender.com`) |
5. Click **Deploy**. After ~1–2 minutes you'll get a URL like **`https://your-app.vercel.app`**

---

## Part 3 — Connect Them (CORS)

The backend must allow requests from your new frontend URL.

1. Go back to **Render** → your backend service → **Environment**.
2. Edit the **`FRONTEND_URL`** variable and set it to your Vercel URL, e.g. `https://your-app.vercel.app`
3. Save — Render redeploys automatically.

Now open your **Vercel URL** → you'll see the 🔒 password gate → enter your `SITE_PASSWORD` → the app works end-to-end! 🎉

---

## Default Logins (created automatically)

| Role | Username | Password |
|------|----------|----------|
| 👑 Admin | `admin` | `admin123` |
| 🧑‍💼 Agent | `agent` | `agent123` |
| 👤 Customer 1 | `customer1` | `customer123` |
| 👤 Customer 2 | `customer2` | `customer456` |

⚠️ **Change these for a real deployment** (edit `backend/database.py`).

---

## ⚠️ Important Caveats for the Free Tier

1. **Backend sleeps after 15 min idle.** Render's free tier spins down when unused, so the **first request after idle takes ~50 seconds** to wake up. The frontend may briefly show "Backend not connected" until it wakes.

2. **Data is not permanent.** The SQLite database and uploaded documents (ChromaDB) live on the server's temporary disk. On every redeploy or restart, **uploaded documents and chat history reset**. The default users are always recreated on startup, so logins keep working. For permanent storage you'd add a Render **persistent disk** (paid) or move to a hosted Postgres + vector DB.

3. **Sentiment analysis** downloads small NLTK data on first use — the very first chat may take a few extra seconds.

These are all fine for a **portfolio demo**. For production, upgrade to paid instances with persistent storage.

---

## Updating Your Deployed App

Both hosts auto-deploy when you push to GitHub:

```bash
git add -A
git commit -m "your changes"
git push
```

Render rebuilds the backend, Vercel rebuilds the frontend — automatically. ✅

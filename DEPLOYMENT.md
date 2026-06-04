# 🚀 Deployment Guide (Hugging Face + Vercel — 100% Free)

This app has **two parts** that deploy separately:

| Part | Folder | Host | Why |
|------|--------|------|-----|
| Backend (FastAPI) | `backend/` | **Hugging Face Spaces** (Docker) | Runs Python + ChromaDB + SQLite |
| Frontend (React) | `frontend/` | **Vercel** | Serves the static built site |

Both are **free**. Deploy the **backend first**, because the frontend needs the backend's URL.

---

## Part 1 — Deploy the Backend on Hugging Face Spaces

### 1.1 Create the Space
1. Sign up at **https://huggingface.co** (free).
2. Go to **https://huggingface.co/new-space**.
3. Fill in:
   - **Space name:** `ai-support-backend`
   - **License:** `mit` (or any)
   - **Select the SDK:** **Docker** → **Blank** template
   - **Hardware:** **CPU basic** (free)
   - **Visibility:** Public
4. Click **Create Space**. It will be at:
   `https://huggingface.co/spaces/<your-username>/ai-support-backend`

### 1.2 Add your secrets
In the Space, go to **Settings → Variables and secrets** → **New secret**, and add:

| Name | Value |
|------|-------|
| `OPENAI_API_KEY` | your OpenAI key (`sk-...`) |
| `SITE_PASSWORD` | a password for the site gate (e.g. `welcome123`) |
| `SECRET_KEY` | any long random string |
| `FRONTEND_URL` | *(leave blank for now — add after Part 2)* |

### 1.3 Get a Hugging Face access token
1. Go to **https://huggingface.co/settings/tokens** → **New token**.
2. Name it anything, role **Write**, click **Generate**.
3. Copy it (looks like `hf_xxxxx`). You'll use it as your **password** when pushing.

### 1.4 Push the backend code to the Space
The Space is its own git repo. We push **only the `backend/` folder** into it.
Run these in a terminal (replace `<USER>` with your HF username):

```bash
# Clone the empty Space repo next to your project
cd c:\Users\aksha
git clone https://huggingface.co/spaces/<USER>/ai-support-backend hf-space

# Copy all backend files into the cloned Space
xcopy /E /Y /I ai-customer-support-agent\backend\* hf-space\

# Commit and push
cd hf-space
git add -A
git commit -m "Deploy AI support backend"
git push
```

When prompted:
- **Username:** your Hugging Face username
- **Password:** paste the **`hf_...` token** (not your account password)

### 1.5 Wait for the build
On the Space page, the **Building** indicator runs for ~5–10 min (it builds the Docker image). When it shows **Running**, your backend is live at:
`https://<your-username>-ai-support-backend.hf.space`

Test it: open `https://<your-username>-ai-support-backend.hf.space/health` → you should see `{"status":"healthy"}`.

---

## Part 2 — Deploy the Frontend on Vercel

1. Go to **https://vercel.com** and sign up with **GitHub**.
2. Click **Add New… → Project**, import the **`AI-PROJECTS`** repo.
3. Configure:
   - **Root Directory:** click **Edit** → select **`frontend`**
   - **Framework Preset:** auto-detects **Vite** ✅
4. Expand **Environment Variables** and add:
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | your HF Space URL, e.g. `https://<your-username>-ai-support-backend.hf.space` |
5. Click **Deploy**. After ~1–2 min you get a URL like **`https://your-app.vercel.app`**

---

## Part 3 — Connect Them (CORS)

The backend must allow requests from your frontend URL.

1. Go back to the **Hugging Face Space → Settings → Variables and secrets**.
2. Edit **`FRONTEND_URL`** and set it to your Vercel URL, e.g. `https://your-app.vercel.app`
3. The Space restarts automatically.

Now open your **Vercel URL** → 🔒 password gate → enter your `SITE_PASSWORD` → the app works end-to-end! 🎉

---

## Default Logins (created automatically)

| Role | Username | Password |
|------|----------|----------|
| 👑 Admin | `admin` | `admin123` |
| 🧑‍💼 Agent | `agent` | `agent123` |
| 👤 Customer 1 | `customer1` | `customer123` |
| 👤 Customer 2 | `customer2` | `customer456` |

⚠️ Change these for a real deployment (edit `backend/database.py`).

---

## ⚠️ Free-Tier Caveats

1. **The Space sleeps after ~48h of no traffic** → the first visit after sleeping takes ~30s to wake.
2. **Data is not permanent.** SQLite + uploaded ChromaDB docs live on temporary disk and **reset on rebuild/restart**. Default users are always recreated on startup, so logins keep working. For permanent storage, add HF **persistent storage** (paid) or move to hosted Postgres + a vector DB.
3. **Sentiment analysis** downloads small NLTK data on first use — the first chat may take a few extra seconds.

Fine for a **portfolio demo**.

---

## Updating the Deployed App

- **Frontend (Vercel):** auto-deploys on every `git push` to GitHub.
- **Backend (HF Space):** re-run the copy + push from step 1.4 whenever you change backend code:
  ```bash
  xcopy /E /Y /I ai-customer-support-agent\backend\* hf-space\
  cd hf-space && git add -A && git commit -m "update" && git push
  ```

---

## Alternative: Render (also free)

Prefer Render instead of Hugging Face? A `render.yaml` blueprint is included in the repo root.
See the git history of this file for the Render-specific steps, or use Render's
"New → Blueprint" pointed at this repo with root directory `backend`.

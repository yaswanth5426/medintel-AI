# MedIntel AI — Deployment Guide (no Docker)

Two services, two hosts — both non-Docker:

| Service   | Stack            | Host                          | Cost |
|-----------|------------------|-------------------------------|------|
| Frontend  | React (Vite)     | **Vercel** (static)           | Free |
| Backend   | FastAPI + XGBoost + SHAP + RAG/Gemini | **Render** (native Python runtime) | Standard plan (RAG needs ~2GB RAM) |

> **Why not "all on Vercel"?** Vercel's Python functions cap at 250 MB and PyTorch
> alone is ~800 MB, so the ML/RAG backend can't run there. Vercel hosts the
> frontend; Render's native Python runtime hosts the API (no Dockerfile needed —
> it just runs `pip install` + `uvicorn`).

> **Memory note.** Full RAG loads PyTorch + the MiniLM model (~2 GB RAM), so the
> Render API needs the **Standard** plan. If you want it free, unset
> `GEMINI_API_KEY` (the app auto-falls back to an offline chat responder) and set
> the plan to `free`.

---

## Part 1 — Backend on Render (native Python, no Docker)

1. Commit & push these files:
   ```bash
   git add render.yaml render-build.sh backend/requirements.txt backend/main.py frontend/vercel.json
   git commit -m "Add no-Docker deployment (Render native Python + Vercel)"
   git push origin frontend-engineer
   ```
2. In Render: **New +  →  Blueprint** → pick the `medintel-AI` repo / `frontend-engineer` branch.
   Render reads `render.yaml` and creates `medintel-api` on the **Python** runtime.
3. Set the secrets (they're `sync: false`):
   - `GEMINI_API_KEY` — from https://aistudio.google.com/apikey (required for real chat)
   - `MONGODB_URI` — optional (persistent history)
4. **Apply.** The build runs `render-build.sh` (CPU PyTorch, xgboost, bakes the
   embedding model) — ~8–12 min the first time. When live, copy the URL, e.g.
   `https://medintel-api.onrender.com`.

*(No blueprint? Create a Web Service manually → Runtime **Python 3** →
Build `bash render-build.sh` → Start `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.)*

## Part 2 — Frontend on Vercel

1. In Vercel: **Add New → Project** → import the repo.
2. Set **Root Directory = `frontend`** (Vercel auto-detects Vite; `vercel.json`
   adds the SPA rewrite so React Router deep links work).
3. Add an env var **`VITE_API_BASE_URL`** = your Render backend URL
   (e.g. `https://medintel-api.onrender.com`).
4. **Deploy.** Open the Vercel URL — it talks to the Render API.

CORS already allows `*.vercel.app` (and `*.onrender.com`, `*.netlify.app`), so no
extra backend config is needed.

---

## Environment variables

| Variable            | Host   | Required | Purpose |
|---------------------|--------|----------|---------|
| `GEMINI_API_KEY`    | Render | for chat | Gemini model for RAG answers |
| `MONGODB_URI`       | Render | optional | Persistent prediction history |
| `CORS_ORIGINS`      | Render | optional | Extra allowed origins (comma-separated) |
| `VITE_API_BASE_URL` | Vercel | yes      | Backend URL, inlined at build time |

## Test locally first (optional)

```bash
# backend
bash render-build.sh                       # or: pip install -r backend/requirements.txt
uvicorn backend.main:app --reload          # http://localhost:8000/  -> {"status":"ok"}

# frontend
cd frontend && npm ci
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

## Alternatives (also no Docker)

- **Railway** — Nixpacks auto-detects Python; deploy the repo, add the env vars,
  set the start command to `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
- **Frontend** can equally go on **Netlify** or **Cloudflare Pages** (set the same
  `VITE_API_BASE_URL`).

## Troubleshooting

- **Backend OOM / restart on first chat** → RAG needs 2 GB; use Render Standard,
  or unset `GEMINI_API_KEY` for the lean offline chat.
- **Frontend calls `localhost:8000` in prod** → `VITE_API_BASE_URL` wasn't set on
  Vercel; add it and redeploy.
- **Model fails to unpickle** → keep `xgboost==3.3.0` (matches the saved models).

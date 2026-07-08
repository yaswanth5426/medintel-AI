# MedIntel AI

AI-powered clinical decision support system that predicts disease risk from
symptoms or uploaded lab reports, explains the prediction, answers medical
questions, and generates a lifestyle plan and downloadable report.

**Educational project only — not a certified medical diagnosis tool.**

This branch (`frontend-engineer`) covers Member 3's scope: `frontend/`,
`backend/pdf_processing/`, `backend/database/`, `backend/reports/`,
`backend/routers/`. The ML pipeline (`backend/ml/`) and RAG/chat pipeline
(`backend/rag/`) are owned by the other two team members.

## Status

- [x] React app running (Home, Chat, Upload Report, Dashboard pages + routing)
- [x] FastAPI running with `POST /predict` (dummy) and `POST /chat/`
- [x] Chat UI (message bubbles, typing indicator, source citations) wired to
      the backend, with an automatic dummy fallback when the real RAG +
      Gemini pipeline isn't configured locally
- [x] PDF upload component (drag/drop, validation) — no backend yet, by design
- [x] Dashboard with a Chart.js visualization over mock prediction history

## Running locally

### Frontend

```
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`. Copy `.env.example` to `.env` to point at a
non-default API URL.

### Backend

Run from the **project root** (not from inside `backend/`) — the real chat
router uses absolute `backend.*` imports:

```
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Runs at `http://localhost:8000`. Interactive API docs at
`http://localhost:8000/docs`. Copy `backend/.env.example` to `backend/.env`
as needed.

`POST /chat/` uses the real RAG + Gemini pipeline in `backend/rag/` when
`GEMINI_API_KEY` is set and the FAISS index has been built. Otherwise
`backend/main.py` automatically falls back to `backend/routers/chat_dummy.py`
so the frontend keeps working during local dev — check the server log for
which one is active.

## Folder structure

```
backend/
  ml/              # ML engineer's branch — not touched here
  rag/             # GenAI engineer's branch — not touched here
  models/          # shared pydantic schemas (e.g. ChatRequest/ChatResponse)
  pdf_processing/  # PDF parsing, OCR, lab value extraction (stubs for now)
  database/        # MongoDB schemas + connection (stubs for now)
  reports/         # PDF report generation via ReportLab (stub for now)
  routers/         # FastAPI route handlers
  main.py
  requirements.txt
frontend/
  src/
    api/           # axios client
    components/    # Navbar, ChatBubble, UploadBox, Disclaimer
    pages/         # Home, Chat, UploadReport, Dashboard
docs/
datasets/
```

## API contract so far

| Method | Path       | Body                                        | Notes |
|--------|-----------|-----------------------------------------------|-------|
| GET    | `/`        | —                                              | Health check |
| POST   | `/predict` | `{ input_type, disease_context, payload }`     | Dummy response until `backend/ml/` is wired in |
| POST   | `/chat/`   | `{ question }`                                 | Real RAG + Gemini answer, or dummy fallback — returns `{ answer, sources }` |

`POST /upload-report`, `POST /generate-report`, and `GET /history` are
planned for later days once `pdf_processing/`, `reports/`, and `database/`
are implemented.

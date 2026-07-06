# MedIntel AI

AI-powered clinical decision support system that predicts disease risk from
symptoms or uploaded lab reports, explains the prediction, answers medical
questions, and generates a lifestyle plan and downloadable report.

**Educational project only — not a certified medical diagnosis tool.**

This branch (`frontend-engineer`) covers Member 3's scope: `frontend/`,
`backend/pdf_processing/`, `backend/database/`, `backend/reports/`,
`backend/routers/`. The ML pipeline (`backend/ml/`) and RAG/chat pipeline
(`backend/rag/`) are owned by the other two team members on their own
branches.

## Status — Day 1 skeleton

- [x] React app running (Home, Chat, Upload Report, Dashboard pages + routing)
- [x] FastAPI running with dummy `POST /predict` and `POST /chat`
- [x] Chat UI (message bubbles, typing indicator) wired to the backend
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

```
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs at `http://localhost:8000`. Interactive API docs at
`http://localhost:8000/docs`. Copy `.env.example` to `.env` as needed.

## Folder structure

```
backend/
  ml/              # ML engineer's branch — not touched here
  rag/             # GenAI engineer's branch — not touched here
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

| Method | Path       | Body                                    | Notes |
|--------|-----------|------------------------------------------|-------|
| GET    | `/`        | —                                        | Health check |
| POST   | `/predict` | `{ input_type, disease_context, payload }` | Dummy response until `backend/ml/` lands |
| POST   | `/chat`    | `{ message, context }`                   | Dummy response until `backend/rag/` lands |

`POST /upload-report`, `POST /generate-report`, and `GET /history` are
planned for later days once `pdf_processing/`, `reports/`, and `database/`
are implemented.

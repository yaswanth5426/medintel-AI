"""
MedIntel AI — FastAPI entry point.

Owned by the Full Stack Engineer (Member 3). This file only wires together
routers and app-level config — actual business logic lives in each router
module and, in backend/ml/ (ML engineer) and backend/rag/ (GenAI engineer).

Run from the project root with:
    uvicorn backend.main:app --reload
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.chat import router as chat_router
from backend.routers.upload import router as upload_router
from backend.routers.history import router as history_router
from backend.routers.predict import router as predict_router


load_dotenv()

app = FastAPI(
    title="MedIntel AI",
    description="Educational clinical decision support API. Not a medical diagnosis tool.",
    version="0.1.0",
)

# Allow the Vite dev server (and any origin set via env) to call the API.
# CORS_ORIGINS can hold a comma-separated list for deployed environments.
default_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
extra_origins = os.getenv("CORS_ORIGINS", "")
allow_origins = default_origins + [o.strip() for o in extra_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
app.include_router(upload_router)
app.include_router(history_router)

# The real /chat router calls into the GenAI engineer's RAG + Gemini
# pipeline (backend/rag/). It needs GEMINI_API_KEY set in backend/.env and a
# built FAISS index to even import successfully. Until that's configured
# locally, fall back to a dummy /chat so the frontend can still be built and
# tested end to end.
try:
    from backend.routers.chat import router as chat_router
    print("[MedIntel] /chat: using the real RAG + Gemini pipeline.")
except Exception as exc:
    print(f"[MedIntel] /chat: real pipeline unavailable ({exc!r}) — using the dummy router.")
    from backend.routers.chat_dummy import router as chat_router

app.include_router(chat_router)



app.include_router(upload_router)
@app.get("/")
def health_check():
    """Simple liveness check used by the frontend and by deployment probes."""
    return {
        "status": "ok",
        "service": "MedIntel AI backend",
        "disclaimer": "Educational project — not a certified medical diagnosis tool.",
    }

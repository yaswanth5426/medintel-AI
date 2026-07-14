from fastapi import FastAPI

from backend.routers.chat import router as chat_router


app = FastAPI(
    title="MedIntel AI",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "MedIntel AI Backend Running"
    }


app.include_router(chat_router)
"""
MedIntel AI — FastAPI entry point.

Owned by the Full Stack Engineer (Member 3). This file only wires together
routers and app-level config — actual business logic lives in each router
module and, later, in backend/ml/ (ML engineer) and backend/rag/ (GenAI
engineer).

Run locally with:
    uvicorn main:app --reload
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# The real /chat router calls into the GenAI engineer's RAG + Gemini pipeline
# (backend/rag/). It needs GEMINI_API_KEY set and a built FAISS index to even
# import. Until that's configured locally, fall back to a dummy /chat so the
# frontend can still be built and tested end to end.
try:
    from backend.routers.chat import router as chat_router
    print("[MedIntel] /chat: using the real RAG + Gemini pipeline.")
except Exception as exc:  # noqa: BLE001
    # The RAG + Gemini pipeline (backend/rag/, GenAI engineer) needs its extra
    # dependencies, a built FAISS index and GEMINI_API_KEY. When any of that is
    # missing we fall back to a built-in offline responder so the rest of the
    # API still runs. This is expected in a fresh/Member-3-only setup.
    reason = type(exc).__name__
    print(f"[MedIntel] /chat: RAG + Gemini not configured ({reason}); using the built-in offline responder.")
    from backend.routers.chat_dummy import router as chat_router

app.include_router(chat_router)


@app.get("/")
def health_check():
    """Simple liveness check used by the frontend and by deployment probes."""
    return {
        "status": "ok",
        "service": "MedIntel AI backend",
        "disclaimer": "Educational project — not a certified medical diagnosis tool.",
    }

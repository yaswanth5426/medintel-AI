"""
POST /chat/ - symptom chat / medical Q&A, backed by the GenAI engineer's
RAG + Gemini pipeline (backend/rag/rag_pipeline.py). Owned by the GenAI
engineer - Member 3 only wires this router into the app in main.py.

Requires GEMINI_API_KEY in backend/.env and a built FAISS index. If either
is missing, main.py automatically falls back to routers/chat_dummy.py so
the frontend keeps working during local dev.
"""

from fastapi import APIRouter
from fastapi import HTTPException
from backend.models.chat import ChatRequest, ChatResponse
from backend.rag.rag_pipeline import generate_answer


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer, sources = generate_answer(request.question)
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

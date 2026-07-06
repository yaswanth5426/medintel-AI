"""
POST /chat — symptom chat / medical Q&A.

Dummy implementation for the Day 1 frontend/backend skeleton. The real
answer generation (FAISS retrieval + Gemini) belongs to the GenAI engineer
in backend/rag/ — this router should stay a thin HTTP layer that calls into
that module once it exists.
"""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = "General"


@router.post("/chat")
def chat(request: ChatRequest):
    """Return a dummy reply so the frontend has a real contract to build against."""
    return {
        "reply": (
            f"(dummy) Got your message about '{request.message}' "
            f"in the {request.context} context. The RAG + Gemini pipeline "
            "isn't connected yet."
        ),
        "sources": [],
    }

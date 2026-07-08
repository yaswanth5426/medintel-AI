"""
Fallback for POST /chat/, used automatically by main.py when the real RAG +
Gemini pipeline (backend/routers/chat.py, owned by the GenAI engineer) can't
be imported — e.g. GEMINI_API_KEY isn't set in backend/.env yet, the FAISS
index hasn't been built, or backend/rag's dependencies aren't installed.

Mirrors the real router's request/response contract (ChatRequest /
ChatResponse from backend/models/chat.py) so the frontend doesn't need to
know or care which one answered.
"""

from fastapi import APIRouter

from backend.models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat_dummy(request: ChatRequest):
    return ChatResponse(
        answer=(
            f"(dummy) Got your question: \"{request.question}\". "
            "The real RAG + Gemini pipeline isn't configured in this "
            "environment yet — set GEMINI_API_KEY in backend/.env and build "
            "the FAISS index to enable real answers."
        ),
        sources=[],
    )

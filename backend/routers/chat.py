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
    
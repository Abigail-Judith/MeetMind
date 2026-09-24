from fastapi import APIRouter

from app.services.rag_service import rag_answer


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/query/{meeting_id}")
def query_rag(
    meeting_id: int,
    question: str
):
    answer = rag_answer(
        question=question,
        meeting_id=meeting_id
    )

    return {
        "meeting_id": meeting_id,
        "question": question,
        "answer": answer
    }
from app.services.embedding_service import generate_embedding
from app.services.vector_service import add_document, search_documents
from app.services.gemini_service import ask_ai


def index_document(
    chunks: list[str],
    document_prefix: str,
    meeting_id: int
):
    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        add_document(
            document_id=f"{document_prefix}-{index}",
            text=chunk,
            embedding=embedding,
            meeting_id=meeting_id
        )

    return len(chunks)


def retrieve_relevant_chunks(
    question: str,
    meeting_id: int,
    top_k: int = 3
):
    question_embedding = generate_embedding(question)

    return search_documents(
        question_embedding,
        meeting_id,
        top_k
    )


def rag_answer(
    question: str,
    meeting_id: int,
    top_k: int = 3
):
    chunks = retrieve_relevant_chunks(
        question,
        meeting_id,
        top_k
    )

    context = "\n\n".join(chunks)

    prompt = f"""
You are MeetMind, an AI meeting assistant.

Answer the user's question using ONLY the provided context.

If the answer is not present in the context,
say that you don't have enough information.

Context:
{context}

Question:
{question}

Answer:
"""

    return ask_ai(prompt)
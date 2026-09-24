import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="meetmind_documents"
)


def add_document(
    document_id: str,
    text: str,
    embedding: list[float],
    meeting_id: int
):
    collection.upsert(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[
            {
                "meeting_id": meeting_id
            }
        ]
    )


def search_documents(
    embedding: list[float],
    meeting_id: int,
    top_k: int = 3
):
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where={
            "meeting_id": meeting_id
        }
    )

    return results["documents"][0]
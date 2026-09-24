import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.document_service import (
    extract_text,
    split_text
)
from app.services.rag_service import index_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload/{meeting_id}")
async def upload_document(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        allowed_extensions = [".pdf", ".docx"]

        if not any(
            file.filename.lower().endswith(ext)
            for ext in allowed_extensions
        ):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )

        os.makedirs("uploads/documents", exist_ok=True)

        filename = f"{uuid.uuid4()}_{file.filename}"

        file_path = os.path.join(
            "uploads/documents",
            filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        text = extract_text(file_path)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from document"
            )

        chunks = split_text(
            text,
            chunk_size=500,
            overlap=50
        )

        document_prefix = str(uuid.uuid4())

        indexed = index_document(
            chunks=chunks,
            document_prefix=document_prefix,
            meeting_id=meeting_id
        )

        os.remove(file_path)

        return {
            "message": "Document uploaded and indexed successfully",
            "meeting_id": meeting_id,
            "chunks_indexed": indexed
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
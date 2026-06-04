from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from database import get_db_connection
from chroma_store import get_collection
from utils import extract_text_from_pdf, extract_text_from_txt, extract_text_from_image, chunk_text

router = APIRouter()
MAX_SIZE_MB = 15


class UploadResponse(BaseModel):
    message: str
    file_name: str
    chunks_added: int
    extracted_text_preview: str


class DocumentInfo(BaseModel):
    id: int
    filename: str
    file_type: str
    chunks_count: int
    file_size: int
    uploaded_date: str


def _get_file_type(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return "pdf"
    elif name.endswith(".txt"):
        return "txt"
    elif name.endswith((".jpg", ".jpeg", ".png")):
        return "image"
    return ""


# ── Upload single or multiple files ──────────────────────────────────────────

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    file_type = _get_file_type(file.filename)
    if not file_type:
        raise HTTPException(status_code=400, detail="Supported formats: PDF, TXT, JPG, PNG")

    content = await file.read()
    file_size = len(content)

    if file_size > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_SIZE_MB}MB")

    # Extract text
    if file_type == "pdf":
        text = extract_text_from_pdf(content)
    elif file_type == "txt":
        text = extract_text_from_txt(content)
    else:
        text = extract_text_from_image(content)

    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    chunks = chunk_text(text, chunk_size=500, overlap=100)
    if not chunks:
        raise HTTPException(status_code=400, detail="Document is empty")

    # Store in ChromaDB
    collection = get_collection()
    ids = [f"{file.filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": file.filename, "chunk_index": i, "file_type": file_type} for i in range(len(chunks))]
    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)

    # Save record in SQLite
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO documents (filename, file_type, chunks_count, file_size, uploaded_date)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(filename) DO UPDATE SET
            chunks_count = excluded.chunks_count,
            file_size = excluded.file_size,
            uploaded_date = excluded.uploaded_date
    """, (file.filename, file_type, len(chunks), file_size, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return UploadResponse(
        message=f"'{file.filename}' uploaded successfully",
        file_name=file.filename,
        chunks_added=len(chunks),
        extracted_text_preview=text[:200].replace("\n", " "),
    )


@router.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    """Upload multiple files at once."""
    results = []
    for file in files:
        try:
            file_type = _get_file_type(file.filename)
            if not file_type:
                results.append({"file": file.filename, "status": "error", "message": "Unsupported format"})
                continue

            content = await file.read()
            file_size = len(content)

            if file_size > MAX_SIZE_MB * 1024 * 1024:
                results.append({"file": file.filename, "status": "error", "message": "File too large"})
                continue

            if file_type == "pdf":
                text = extract_text_from_pdf(content)
            elif file_type == "txt":
                text = extract_text_from_txt(content)
            else:
                text = extract_text_from_image(content)

            if not text:
                results.append({"file": file.filename, "status": "error", "message": "Could not extract text"})
                continue

            chunks = chunk_text(text, chunk_size=500, overlap=100)
            collection = get_collection()
            ids = [f"{file.filename}_{i}" for i in range(len(chunks))]
            metadatas = [{"source": file.filename, "chunk_index": i, "file_type": file_type} for i in range(len(chunks))]
            collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)

            conn = get_db_connection()
            conn.execute("""
                INSERT INTO documents (filename, file_type, chunks_count, file_size, uploaded_date)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(filename) DO UPDATE SET
                    chunks_count = excluded.chunks_count,
                    file_size = excluded.file_size,
                    uploaded_date = excluded.uploaded_date
            """, (file.filename, file_type, len(chunks), file_size, datetime.now().isoformat()))
            conn.commit()
            conn.close()

            results.append({"file": file.filename, "status": "success", "chunks": len(chunks)})

        except Exception as e:
            results.append({"file": file.filename, "status": "error", "message": str(e)})

    return {"results": results}


# ── List all uploaded documents ───────────────────────────────────────────────

@router.get("/documents", response_model=list[DocumentInfo])
def list_documents():
    """Return all uploaded documents."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents ORDER BY uploaded_date DESC")
    docs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return docs


# ── Delete a document ─────────────────────────────────────────────────────────

@router.delete("/documents/{filename:path}")
def delete_document(filename: str):
    """Delete a document from ChromaDB and the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents WHERE filename = ?", (filename,))
    doc = cur.fetchone()

    if not doc:
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found")

    # Remove all chunks from ChromaDB
    try:
        collection = get_collection()
        # Get all IDs that belong to this file
        all_results = collection.get(where={"source": filename})
        if all_results and all_results["ids"]:
            collection.delete(ids=all_results["ids"])
    except Exception as e:
        print(f"ChromaDB delete error: {e}")

    # Remove from database
    conn.execute("DELETE FROM documents WHERE filename = ?", (filename,))
    conn.commit()
    conn.close()

    return {"message": f"'{filename}' deleted successfully"}

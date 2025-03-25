from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

user_documents = {}

class UploadPayload(BaseModel):
    user_id: str
    content: str
    doc_type: Optional[str] = "text"
    source_name: Optional[str] = None

@app.post("/upload")
async def upload_document(request: Request):
    try:
        # Versuche, JSON sauber zu laden (auch mit Sonderzeichen)
        data = await request.json()
    except Exception as e:
        return {"status": "error", "message": f"Invalid JSON: {str(e)}"}

    try:
        # Versuche, das JSON in das Pydantic-Modell zu laden
        payload = UploadPayload(**data)
    except Exception as e:
        return {"status": "error", "message": f"Validation failed: {str(e)}"}

    # Fallbacks
    doc_id = str(uuid.uuid4())
    if payload.user_id not in user_documents:
        user_documents[payload.user_id] = []

    # Bereinige Inhalt vorsichtshalber nochmals (optional)
    safe_content = payload.content.encode("utf-8", "ignore").decode("utf-8")
    source = payload.source_name or "unbenannt"

    user_documents[payload.user_id].append({
        "doc_id": doc_id,
        "type": payload.doc_type,
        "source": source,
        "content": safe_content
    })

    return {"status": "ok", "doc_id": doc_id}

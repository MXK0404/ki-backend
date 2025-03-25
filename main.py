from fastapi import FastAPI
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
async def upload_document(payload: UploadPayload):
    doc_id = str(uuid.uuid4())

    if payload.user_id not in user_documents:
        user_documents[payload.user_id] = []

    user_documents[payload.user_id].append({
        "doc_id": doc_id,
        "type": payload.doc_type,
        "source": payload.source_name or "unbenannt",
        "content": payload.content
    })

    return {"status": "ok", "doc_id": doc_id}

from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
import uuid
import json

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
        # Lies rohen Body als Text (nicht als JSON!)
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8", "ignore")

        # Jetzt selbst JSON parsen
        data = json.loads(body_str)

        # Nutze Pydantic zum Validieren
        payload = UploadPayload(**data)

    except Exception as e:
        return {"status": "error", "message": f"Parsing failed: {str(e)}"}

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


from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
import uuid
import json
import os
import openai

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
user_documents = {}

class UploadPayload(BaseModel):
    user_id: str
    content: str
    doc_type: Optional[str] = "text"
    source_name: Optional[str] = None

# 🔹 /upload – Dokumente empfangen und speichern
@app.post("/upload")
async def upload_document(request: Request):
    try:
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8", "ignore")
        data = json.loads(body_str)
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

# 🔹 /embed – Text in Embeddings umwandeln
@app.post("/embed")
async def generate_embedding(request: Request):
    try:
        body = await request.json()
        text = body.get("text", "")

        if not text:
            return {"status": "error", "message": "Kein Text übergeben."}

        openai.api_key = OPENAI_API_KEY
        response = openai.Embedding.create(
            model="text-embedding-3-small",
            input=text
        )

        embedding = response["data"][0]["embedding"]

        return {
            "status": "ok",
            "embedding": embedding,
            "length": len(embedding)
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


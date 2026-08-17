from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.rag.vectorstore import (
    load_documents,
    split_documents,
    create_vector_store,
)

from app.rag.rag_chain import (
    create_rag_system,
    ask_question,
)


app = FastAPI(
    title="AI University Knowledge Assistant",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


# Create RAG system
retriever, llm = create_rag_system()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI University Knowledge Assistant is running!"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return {
            "error": "Only PDF and DOCX files are currently supported."
        }

    file_path = UPLOAD_DIR / file.filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # Ingest documents
    documents = load_documents()

    chunks = split_documents(documents)

    create_vector_store(chunks)

    return {
        "message": "File uploaded and indexed successfully!",
        "filename": file.filename,
        "chunks": len(chunks)
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    answer, sources = ask_question(
        request.question,
        retriever,
        llm
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            document.metadata
            for document in sources
        ]
    }
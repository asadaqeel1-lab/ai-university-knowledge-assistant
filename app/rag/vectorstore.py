from pathlib import Path

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DATA_PATH = Path("data/raw")
VECTOR_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "university_knowledge"


def load_documents():
    documents = []

    for file_path in DATA_PATH.iterdir():

        if file_path.suffix.lower() == ".docx":
            print(f"Loading DOCX: {file_path.name}")
            loader = Docx2txtLoader(str(file_path))
            documents.extend(loader.load())

        elif file_path.suffix.lower() == ".pdf":
            print(f"Loading PDF: {file_path.name}")
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    return chunks


def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
        collection_name=COLLECTION_NAME
    )

    return vector_store
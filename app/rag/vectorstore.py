from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DOCUMENT_PATH = "data/raw/Machine Learning Notes.docx"
VECTOR_DB_PATH = "data/chroma_db"


def load_and_split_document():
    loader = Docx2txtLoader(DOCUMENT_PATH)
    documents = loader.load()

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
        collection_name="university_knowledge"
    )

    return vector_store


if __name__ == "__main__":
    chunks = load_and_split_document()

    vector_store = create_vector_store(chunks)

    print("\nVector database created successfully! ✅")
    print(f"Stored at: {Path(VECTOR_DB_PATH).absolute()}")
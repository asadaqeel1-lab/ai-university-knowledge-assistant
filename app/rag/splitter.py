from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    loader = Docx2txtLoader(str(path))
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Original documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    return chunks


if __name__ == "__main__":
    file_path = "data/raw/Machine Learning Notes.docx"

    documents = load_document(file_path)
    chunks = split_documents(documents)

    print("\n--- CHUNK 1 ---\n")
    print(chunks[0].page_content)

    print("\n--- CHUNK 2 ---\n")
    print(chunks[1].page_content)

    print("\n--- METADATA ---\n")
    print(chunks[0].metadata)
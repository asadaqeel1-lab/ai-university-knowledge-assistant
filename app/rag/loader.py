from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader


def load_document(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    loader = Docx2txtLoader(str(path))
    documents = loader.load()

    print("Document loaded successfully!")
    print(f"Number of documents: {len(documents)}")

    return documents


if __name__ == "__main__":
    file_path = "data/raw/Machine Learning Notes.docx"

    documents = load_document(file_path)

    print("\n--- Document Content ---\n")
    print(documents[0].page_content[:3000])

    print("\n--- Metadata ---\n")
    print(documents[0].metadata)
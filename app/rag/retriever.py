from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


VECTOR_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "university_knowledge"


def create_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever


if __name__ == "__main__":
    retriever = create_retriever()

    query = "What programming languages does Asad know?"

    documents = retriever.invoke(query)

    print(f"\nQuestion: {query}")
    print(f"Retrieved documents: {len(documents)}")

    for i, document in enumerate(documents, start=1):
        print(f"\n--- Result {i} ---")
        print(document.page_content)
        print("\nMetadata:")
        print(document.metadata)
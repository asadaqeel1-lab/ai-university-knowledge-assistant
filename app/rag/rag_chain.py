from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


VECTOR_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "university_knowledge"


def create_rag_system():

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

    llm = OllamaLLM(
        model="llama3.2:latest"
    )

    return retriever, llm


def ask_question(question, retriever, llm):

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an AI University Knowledge Assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response, documents


if __name__ == "__main__":

    retriever, llm = create_rag_system()

    print("======================================")
    print(" AI University Knowledge Assistant")
    print("======================================")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer, sources = ask_question(
            question,
            retriever,
            llm
        )

        print("\n================ ANSWER ================\n")
        print(answer)

        print("\n================ SOURCES ================\n")

        for i, document in enumerate(sources, start=1):
            print(f"Source {i}:")
            print(document.metadata)

        print()
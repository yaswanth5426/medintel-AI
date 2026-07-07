import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Global variables
embedding_model = None
vector_store = None


def load_vector_store():
    """
    Load the embedding model and FAISS index only once.
    """

    global embedding_model
    global vector_store

    if vector_store is None:

        print("Loading embedding model...")

        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

        faiss_path = Path(__file__).parent / "faiss_index"

        print("Loading FAISS index...")

        vector_store = FAISS.load_local(
            folder_path=str(faiss_path),
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )

        print("FAISS index loaded.")

    return vector_store


def retrieve_documents(query: str, k: int = 3):
    """
    Retrieve the top-k relevant documents.
    """

    db = load_vector_store()

    results = db.max_marginal_relevance_search(
        query=query,
        k=k,
        fetch_k=10
    )

    return results


if __name__ == "__main__":

    while True:

        question = input("\nEnter your medical question: ")

        if question.lower() == "exit":
            break

        docs = retrieve_documents(question)

        print("\n" + "=" * 80)

        for i, doc in enumerate(docs, start=1):

            print("=" * 70)
            print(f"Result {i}")
            print(f"Source : {Path(doc.metadata['source']).name}")
            print(f"Page : {doc.metadata['page'] + 1}")
            print()
            print(doc.page_content)
            print()
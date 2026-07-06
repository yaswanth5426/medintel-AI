import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Load embedding model only once
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS only once
faiss_path = Path(__file__).parent / "faiss_index"

vector_store = FAISS.load_local(
    folder_path=str(faiss_path),
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)


def retrieve_documents(query, k=3):
    """
    Retrieve the top-k most relevant chunks.
    """

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k
    )

    return results


if __name__ == "__main__":

    question = input("\nEnter your medical question: ")

    docs = retrieve_documents(question)

    print("\n" + "=" * 80)

    for i, (doc, score) in enumerate(docs, start=1):

        print("=" * 70)
        print(f"Result {i}")
        print(f"Similarity Score : {score:.4f}")
        print(f"Source : {doc.metadata['source'].split('\\\\')[-1]}")
        print(f"Page : {doc.metadata['page'] + 1}")

        print()
        print(doc.page_content)
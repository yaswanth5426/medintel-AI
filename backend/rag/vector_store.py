import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from ingest import load_documents, split_documents


def create_vector_store():

    print("=" * 60)
    print("Creating FAISS Vector Store")
    print("=" * 60)

    # Load documents
    documents = load_documents()

    # Split into chunks
    chunks = split_documents(documents)

    print("\nLoading embedding model...")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded successfully!")

    print("\nCreating FAISS index...")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    save_path = Path(__file__).parent / "faiss_index"

    vector_store.save_local(str(save_path))

    print("\nFAISS index created successfully!")
    print(f"Saved to : {save_path}")

    return vector_store


if __name__ == "__main__":
    create_vector_store()
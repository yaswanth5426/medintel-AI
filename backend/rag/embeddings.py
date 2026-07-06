from sentence_transformers import SentenceTransformer
from ingest import load_documents, split_documents




def load_embedding_model():
    """
    Load the Sentence Transformer model.

    Returns:
        SentenceTransformer: Loaded embedding model.
    """
    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding model loaded successfully.\n")

    return model


def generate_embeddings(chunks):
    """
    Generate embeddings for all document chunks.

    Args:
        chunks (list): List of LangChain Document objects.

    Returns:
        tuple:
            embeddings -> numpy array
            texts -> list of chunk texts
    """

    model = load_embedding_model()

    texts = [chunk.page_content for chunk in chunks]

    print(f"Generating embeddings for {len(texts)} chunks...\n")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print("\nEmbeddings generated successfully!")
    print(f"Total Embeddings : {len(embeddings)}")
    print(f"Embedding Shape  : {embeddings.shape}")

    return embeddings, texts


if __name__ == "__main__":

    documents = load_documents()

    chunks = split_documents(documents)

    embeddings, texts = generate_embeddings(chunks)
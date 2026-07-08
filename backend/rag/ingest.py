import warnings
from pathlib import Path


from langchain_text_splitters import RecursiveCharacterTextSplitter


warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain_community.document_loaders import PyPDFLoader
def load_documents():
    """
    Load all PDF documents from the medical_docs directory.

    Returns:
        list: List of LangChain Document objects.
    """

    # Path to medical_docs folder
    docs_path = Path(__file__).parent / "medical_docs"

    # Find all PDFs
    pdf_files = list(docs_path.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {docs_path}"
        )

    documents = []

    print("=" * 60)
    print("Loading Medical Documents")
    print("=" * 60)

    for pdf in pdf_files:
        print(f"\nLoading: {pdf.name}")

        loader = PyPDFLoader(str(pdf))
        pdf_docs = loader.load()

        print(f"Pages Loaded: {len(pdf_docs)}")

        documents.extend(pdf_docs)

    print("\n" + "=" * 60)
    print("Loading Complete")
    print("=" * 60)
    print(f"Total PDFs      : {len(pdf_files)}")
    print(f"Total Documents : {len(documents)}")

    return documents
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks=text_splitter.split_documents(documents);
    print(f"Total Chunks: {len(chunks)}")
    return chunks


if __name__ == "__main__":
    documents = load_documents()

    chunks = split_documents(documents)

    print(chunks[0].page_content[:500])
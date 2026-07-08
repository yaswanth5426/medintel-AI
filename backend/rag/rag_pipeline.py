from pathlib import Path

from google import genai

from backend.rag.config import GEMINI_API_KEY
from backend.rag.retriever import retrieve_documents
from backend.rag.prompts import create_prompt


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question: str):

    documents = retrieve_documents(question)

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = create_prompt(
        context=context,
        question=question
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    sources = []

    for doc in documents:

        filename = Path(doc.metadata["source"]).name
        page = doc.metadata["page"] + 1

        source = f"{filename} (Page {page})"

        if source not in sources:
            sources.append(source)

    return response.text, sources
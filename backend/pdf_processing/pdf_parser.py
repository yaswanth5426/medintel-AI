import fitz


def extract_pdf_text(pdf_path: str):
    """
    Extract text from a PDF.

    Returns:
        {
            "pages": int,
            "text": str
        }
    """

    document = fitz.open(pdf_path)

    pages = len(document)      # ← Get page count BEFORE closing

    full_text = ""

    for page in document:
        full_text += page.get_text()

    document.close()           # ← Close only after everything is done

    return {
        "pages": pages,
        "text": full_text
    }


if __name__ == "__main__":

    pdf = "backend/uploads/sample.pdf"

    result = extract_pdf_text(pdf)

    print(result["pages"])
    print(result["text"][:1000])
"""
Extracts raw text and tables from uploaded lab report PDFs using PyMuPDF.

Not implemented yet — this is a placeholder so the folder structure matches
the project plan. Planned for a later day, owned by Member 3.
"""

# TODO: implement with PyMuPDF (fitz). Feeds into report_extractor.py.

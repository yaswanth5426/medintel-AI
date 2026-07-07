"""
POST /upload - receive an uploaded medical report PDF.

Placeholder endpoint: accepts the file and echoes back basic metadata so the
frontend upload flow can be built and tested end to end. Real parsing
(PyMuPDF + Tesseract OCR + lab value extraction) belongs to
backend/pdf_processing/, owned by Member 3, and isn't implemented yet.
"""

from fastapi import APIRouter, File, UploadFile

router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload_report(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "status": "received",
        "note": "Placeholder response - PDF parsing (backend/pdf_processing/) isn't implemented yet.",
    }

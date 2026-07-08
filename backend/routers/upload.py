from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.pdf_processing.pdf_parser import extract_pdf_text
from backend.pdf_processing.report_extractor import extract_report_details
from backend.pdf_processing.lab_value_parser import extract_lab_values


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


UPLOAD_FOLDER = Path("backend/uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post("/report")
async def upload_report(file: UploadFile = File(...)):

    # Validate file
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Save uploaded PDF
    file_path = UPLOAD_FOLDER / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    pdf_result = extract_pdf_text(str(file_path))

    # Extract report information
    report_details = extract_report_details(
        pdf_result["text"]
    )

    # Extract lab values
    lab_values = extract_lab_values(
        pdf_result["text"]
    )

    # Save extracted text (optional but useful)
    with open(file_path.with_suffix(".txt"), "w", encoding="utf-8") as f:
        f.write(pdf_result["text"])

    return {
        "status": "success",
        "message": "Medical report processed successfully.",

        "data": {

            "report": {
                "filename": file.filename,
                "pages": pdf_result["pages"]
            },

            "patient": report_details,

            "lab_values": lab_values

        }
    }

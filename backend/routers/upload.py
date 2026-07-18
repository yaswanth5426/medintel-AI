"""
POST /upload/report - parse an uploaded medical report PDF (Member 3 / routers).

Responsibilities kept intentionally narrow: save the PDF, pull text, best-effort
detect the report type, and extract patient details + lab values. The actual
risk prediction + AI summary happen in POST /predict (prediction_engine ->
backend/ml), so this endpoint has no ML or Gemini dependency and can't be broken
by them.

Response shape (consumed by frontend/src/pages/UploadReport.jsx):
    {
      "status": "success",
      "disease_detected": "diabetes" | "heart" | "ckd" | null,
      "data": { "report": {...}, "patient": {...}, "lab_values": {...} }
    }
"""

from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.pdf_processing.pdf_parser import extract_pdf_text
from backend.pdf_processing.report_extractor import extract_report_details
from backend.pdf_processing.lab_value_parser import extract_lab_values
from backend.pdf_processing.report_identifier import identify_disease

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_FOLDER = Path("backend/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/report")
async def upload_report(file: UploadFile = File(...)):

    # Validate file
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Save uploaded PDF
    pdf_path = UPLOAD_FOLDER / file.filename
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    pdf_result = extract_pdf_text(str(pdf_path))
    text = pdf_result["text"]

    # Best-effort report-type detection (never fatal). identify_disease returns
    # {"disease": "diabetes"|..., "matched_keyword": [...], "score": n}.
    try:
        detected = identify_disease(text)
        disease_detected = detected.get("disease") if isinstance(detected, dict) else detected
    except Exception:
        disease_detected = None

    # Extract structured details. extract_lab_values returns
    # {"report_name": ..., "lab_values": {...}} - unwrap the flat lab dict.
    report_details = extract_report_details(text)
    lab_result = extract_lab_values(text)
    if isinstance(lab_result, dict) and "lab_values" in lab_result:
        lab_values = lab_result["lab_values"]
        report_name = lab_result.get("report_name")
    else:
        lab_values = lab_result
        report_name = None

    # Persist extracted text alongside the PDF (handy for debugging)
    try:
        with open(pdf_path.with_suffix(".txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass

    return {
        "status": "success",
        "message": "Medical report processed successfully.",
        "disease_detected": disease_detected,
        "data": {
            "report": {
                "filename": file.filename,
                "pages": pdf_result["pages"],
                "report_name": report_name,
            },
            "patient": report_details,
            "lab_values": lab_values,
        },
    }

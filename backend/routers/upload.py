from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.pdf_processing.pdf_parser import extract_pdf_text
from backend.pdf_processing.report_extractor import extract_report_details
from backend.pdf_processing.lab_value_parser import extract_lab_values
from backend.pdf_processing.report_identifier import identify_disease

from backend.ml.predict import predict_disease

from backend.rag.generate_report import generate_report


router = APIRouter(

    prefix="/upload",

    tags=["Upload"]

)


UPLOAD_FOLDER = Path("backend/uploads")

UPLOAD_FOLDER.mkdir(

    parents=True,

    exist_ok=True

)


GENERATED_REPORTS = Path(

    "backend/generated_reports"

)

GENERATED_REPORTS.mkdir(

    parents=True,

    exist_ok=True

)


@router.post("/report")
async def upload_report(

    file: UploadFile = File(...)

):

    # ---------------------------------------
    # Validate File
    # ---------------------------------------

    if file.content_type != "application/pdf":

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are allowed."

        )

    # ---------------------------------------
    # Save Uploaded PDF
    # ---------------------------------------

    pdf_path = UPLOAD_FOLDER / file.filename

    with open(pdf_path, "wb") as f:

        f.write(await file.read())

    # ---------------------------------------
    # Extract Text
    # ---------------------------------------

    pdf_result = extract_pdf_text(

        str(pdf_path)

    )

    extracted_text = pdf_result["text"]

    pages = pdf_result["pages"]

    # ---------------------------------------
    # Detect Disease
    # ---------------------------------------

    

    disease = identify_disease(

        extracted_text

    )

    if disease is None:

        raise HTTPException(

            status_code=400,

            detail="Unable to identify report type."

        )

    # ---------------------------------------
    # Extract Patient Details
    # ---------------------------------------

    report_details = extract_report_details(

        extracted_text

    )

    # ---------------------------------------
    # Extract Lab Values
    # ---------------------------------------

    lab_values = extract_lab_values(

        extracted_text

    )


    # ---------------------------------------
    # Predict Disease
    # ---------------------------------------

    prediction = predict_disease(

        disease=disease,

        report_details=report_details,

        lab_values=lab_values

    )

    # ---------------------------------------
    # Generate AI Summary
    # ---------------------------------------

    try:

        summary = generate_report(

            patient=report_details,

            lab_values=lab_values,

            prediction=prediction

        )

    except Exception as e:

        summary = "Unable to generate AI report."

    # ---------------------------------------
    # Save AI Summary
    # ---------------------------------------

    summary_path = GENERATED_REPORTS / (

        pdf_path.stem + "_summary.txt"

    )

    with open(

        summary_path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(summary)

    # ---------------------------------------
    # Save Extracted Text
    # ---------------------------------------

    extracted_text_path = GENERATED_REPORTS / (

        pdf_path.stem + "_text.txt"

    )

    with open(

        extracted_text_path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(extracted_text)

    # ---------------------------------------
    # Response
    # ---------------------------------------

    return {

        "status": "success",

        "message": "Medical report processed successfully.",

        "disease_detected": disease,

        "report": {

            "filename": file.filename,

            "pages": pages

        },

        "patient": report_details,

        "lab_values": lab_values,

        "prediction": prediction,

        "summary": summary,

        "files": {

            "uploaded_pdf": str(pdf_path),

            "extracted_text": str(extracted_text_path),

            "generated_summary": str(summary_path)

        }

    }


import re


def extract_report_details(text: str):

    details = {
        "patient_name": None,
        "age": None,
        "gender": None,
        "hospital": None,
        "report_date": None,
        "doctor": None
    }

    # -----------------------
    # Patient Name
    # -----------------------
    match = re.search(
        r"Name\s*:?\s*([A-Za-z0-9 ]+)",
        text,
        re.IGNORECASE
    )

    if match:
        details["patient_name"] = match.group(1).strip()

    # -----------------------
    # Age
    # -----------------------
    match = re.search(
        r"Age\s*:?\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if match:
        details["age"] = int(match.group(1))

    # -----------------------
    # Gender
    # -----------------------
    match = re.search(
        r"Gender\s*:?\s*(Male|Female|Other)",
        text,
        re.IGNORECASE
    )

    if match:
        details["gender"] = match.group(1)

    # -----------------------
    # Report Date
    # -----------------------
    match = re.search(
        r"Reported\s*.*?(\d{1,2}/\d{1,2}/\d{4})",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        details["report_date"] = match.group(1)

    # -----------------------
    # Hospital
    # -----------------------

    first_lines = "\n".join(text.splitlines()[:20])

    if "lal pathlabs" in first_lines.lower():
        details["hospital"] = "Dr Lal PathLabs"

    elif "apollo" in first_lines.lower():
        details["hospital"] = "Apollo Hospital"

    elif "aig" in first_lines.lower():
        details["hospital"] = "AIG Hospital"

    elif "yashoda" in first_lines.lower():
        details["hospital"] = "Yashoda Hospital"

    # -----------------------
    # Doctor
    # -----------------------

    doctors = re.findall(
        r"Dr\.?\s+[A-Za-z ]+",
        text
    )

    if doctors:
        details["doctor"] = doctors[0].strip()

    return details
"""
Orchestrates the PDF workflow end to end: pdf_parser -> ocr (if needed) ->
lab_value_parser, returning a structured dict ready for the ML prediction
router.

Not implemented yet — placeholder for folder-structure consistency.
Planned for a later day, owned by Member 3.
"""

# TODO: tie pdf_parser.py, ocr.py and lab_value_parser.py together and
# call this from routers/upload.py once that router exists.

import re

LAB_KEYWORDS = {

    # -------------------------
    # Diabetes
    # -------------------------

    "glucose": [
        "glucose",
        "blood glucose",
        "fasting glucose",
        "fasting blood sugar",
        "fbs"
    ],

    "hba1c": [
        "hba1c",
        "a1c"
    ],

    # -------------------------
    # Kidney
    # -------------------------

    "blood_urea": [
        "blood urea",
        "urea",
        "bu"
    ],

    "serum_creatinine": [
        "creatinine",
        "serum creatinine"
    ],

    "egfr": [
        "egfr",
        "e-gfr"
    ],

    "specific_gravity": [
        "specific gravity",
        "sg"
    ],

    "albumin": [
        "albumin",
        "urine albumin"
    ],

    "sugar": [
        "urine sugar",
        "sugar"
    ],

    "serum_albumin": [
        "serum albumin"
    ],

    "calcium": [
        "calcium"
    ],

    "phosphate": [
        "phosphate"
    ],

    "cystatin_c": [
        "cystatin c"
    ],

    "urine_output": [
        "urine output"
    ],

    "urine_protein_creatinine_ratio": [
        "urine protein creatinine ratio",
        "protein creatinine ratio",
        "upcr"
    ],

    # -------------------------
    # Heart
    # -------------------------

    "cholesterol": [
        "cholesterol",
        "total cholesterol"
    ],

    "heart_rate": [
        "heart rate",
        "pulse"
    ],

    "cpk": [
        "cpk",
        "creatine phosphokinase",
        "creatine kinase"
    ],

    # -------------------------
    # CBC
    # -------------------------

    "hemoglobin": [
        "hemoglobin",
        "haemoglobin",
        "hb"
    ],

    "packed_cell_volume": [
        "packed cell volume",
        "pcv"
    ],

    "wbc": [
        "white blood cells",
        "wbc",
        "total leukocyte count"
    ],

    "rbc": [
        "red blood cells",
        "rbc"
    ],

    "platelets": [
        "platelets",
        "platelet count"
    ],

    # -------------------------
    # Electrolytes
    # -------------------------

    "sodium": [
        "sodium",
        "serum sodium"
    ],

    "potassium": [
        "potassium",
        "serum potassium"
    ],

    # -------------------------
    # Vitals
    # -------------------------

    "blood_pressure": [
        "blood pressure",
        "bp"
    ]
}

def convert_value(value):
    """
    Convert extracted value to int/float.
    Keep blood pressure as string.
    """
    if value is None:
        return None

    if "/" in value:
        return value

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def extract_numeric_value(text):
    """
    Extract:
    182
    8.1
    140/90
    """
    bp = re.search(r"\d{2,3}/\d{2,3}", text)
    if bp:
        return bp.group()

    number = re.search(r"\d+(?:\.\d+)?", text)
    if number:
        return number.group()

    return None

REPORT_NAMES = [
    "diabetes profile",
    "hba1c",
    "glycemic profile",
    "lipid profile",
    "cardiac profile",
    "kidney function test",
    "renal function test",
    "kft",
    "cbc",
    "complete blood count",
    "liver function test",
    "lft",
    "thyroid profile",
    "master health checkup",
    "executive health checkup"
]


def extract_report_name(text: str):

    first_lines = "\n".join(text.splitlines()[:20]).lower()

    for report in REPORT_NAMES:

        if report in first_lines:
            return report

    return "unknown"




def extract_lab_values(text: str):

    values = {key: None for key in LAB_KEYWORDS}

    lines = text.splitlines()

    total_lines = len(lines)

    for i in range(total_lines):

        current_line = lines[i].strip()

        if not current_line:
            continue

        current_lower = current_line.lower()

        for lab, keywords in LAB_KEYWORDS.items():

            if values[lab] is not None:
                continue

            for keyword in keywords:

                if keyword in current_lower:

                    # current line
                    value = extract_numeric_value(current_line)

                    if value:

                        values[lab] = convert_value(value)

                        break

                    # next line

                    if i + 1 < total_lines:

                        value = extract_numeric_value(lines[i + 1])

                        if value:

                            values[lab] = convert_value(value)

                            break

                    # second next line

                    if i + 2 < total_lines:

                        value = extract_numeric_value(lines[i + 2])

                        if value:

                            values[lab] = convert_value(value)

                            break

    return {
    "report_name": extract_report_name(text),
    "lab_values": values
}

sample = """
Apollo Hospital

Patient Name : Yaswanth

Age : 22

Glucose
182 mg/dL

HbA1c
8.1 %

Blood Urea
46 mg/dL

Serum Creatinine
1.9 mg/dL

Hemoglobin
13.4 g/dL

Platelets
2.8

WBC
7600

RBC
4.8

Sodium
138

Potassium
4.2

Total Cholesterol
220

Blood Pressure
140/90

eGFR
62
"""
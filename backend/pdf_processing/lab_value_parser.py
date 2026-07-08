import re

LAB_KEYWORDS = {
    "fasting_glucose": [
        "glucose fasting",
        "fasting glucose",
        "fasting blood sugar",
        "fbs"
    ],
    "post_meal_glucose": [
        "glucose (pp)",
        "post meal",
        "pp glucose",
        "post prandial"
    ],
    "hba1c": [
        "hba1c",
        "a1c"
    ],
    "creatinine": [
        "creatinine"
    ],
    "hemoglobin": [
        "hemoglobin",
        "haemoglobin",
        "hb"
    ],
    "cholesterol": [
        "cholesterol",
        "total cholesterol"
    ],
    "urea": [
        "urea"
    ],
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


def extract_lab_values(text: str):
    values = {
        "fasting_glucose": None,
        "post_meal_glucose": None,
        "hba1c": None,
        "creatinine": None,
        "hemoglobin": None,
        "cholesterol": None,
        "urea": None,
        "blood_pressure": None
    }

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
                    # Check current line
                    value = extract_numeric_value(current_line)
                    if value:
                        values[lab] = convert_value(value)
                        break

                    # Check next line
                    if i + 1 < total_lines:
                        value = extract_numeric_value(lines[i + 1])
                        if value:
                            values[lab] = convert_value(value)
                            break

                    # Check next two lines
                    if i + 2 < total_lines:
                        value = extract_numeric_value(lines[i + 2])
                        if value:
                            values[lab] = convert_value(value)
                            break

    return values


if __name__ == "__main__":
    sample = """
    Apollo Hospital
    Patient Name : Yaswanth
    Age : 22
    Glucose
    182 mg/dL
    HbA1c
    8.1 %
    Creatinine
    1.9 mg/dL
    Hemoglobin
    13.5 g/dL
    Blood Pressure
    140/90
    """

    result = extract_lab_values(sample)
    print(result)
"""
Parses extracted report text into structured lab values (e.g. glucose,
cholesterol, creatinine) that match the feature schema expected by the
ML model in backend/ml/.

Not implemented yet — placeholder for folder-structure consistency.
Planned for a later day, owned by Member 3.
"""

# TODO: regex / rule-based extraction of key-value pairs from report text.

"""
Patient-detail extractor (Member 3 / backend/pdf_processing).

Pulls age, gender, height, weight and BMI out of a report's raw text.

Robust to two layouts:
  * inline / adjacent   ->  "Age : 26"   "Sex: Female"   "Age/Sex : 22 / M"
  * transposed columns  ->  the label ("Age", "Gender") and its value
                            ("26 Years", "Female") land on separate lines,
                            far apart, the way Dr Lal PathLabs reports flatten.

For the transposed case we fall back to standalone tokens found near the top of
the report ("26 Years", "Female"/"Male").
"""

import re


def _search(patterns, text, flags=re.IGNORECASE):
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return match.group(1).strip()
    return None


def extract_report_details(text: str):
    details = {"age": None, "gender": None, "height": None,
               "weight": None, "bmi": None}

    header = "\n".join(text.splitlines()[:60])  # patient block is near the top

    # -----------------------------------------------------------------
    # AGE  -- prefer "26 Years" (reliable in transposed reports); only
    # accept an "Age: N" match when N sits on the SAME line (no newline
    # crossing, which is what produced the bogus age=3 before).
    # -----------------------------------------------------------------
    age = _search([
        r"(\d{1,3})\s*(?:years?|yrs?)\b",
        r"Age\s*/\s*Sex[ \t]*:?[ \t]*(\d{1,3})",
        r"Age[ \t]*:?[ \t]*(\d{1,3})\b",
    ], text)
    if age and 0 < int(age) <= 120:
        details["age"] = int(age)

    # -----------------------------------------------------------------
    # GENDER  -- labelled first, then a standalone Male/Female near the top.
    # -----------------------------------------------------------------
    gender = _search([
        r"Gender[ \t]*:?[ \t]*(Male|Female|Other)",
        r"Sex[ \t]*:?[ \t]*(Male|Female|Other)",
        r"Age\s*/\s*Sex[ \t]*:?[ \t]*\d+\s*/\s*(M|F)",
    ], text)
    if not gender:
        gender = _search([r"\b(Male|Female)\b"], header)  # transposed layout
    if gender:
        g = gender.upper()
        gender = "Male" if g in ("M", "MALE") else "Female" if g in ("F", "FEMALE") else gender.title()
        details["gender"] = gender

    # -----------------------------------------------------------------
    # HEIGHT / WEIGHT
    # -----------------------------------------------------------------
    height = _search([
        r"Height\s*\(cm\)[ \t]*:?[ \t]*(\d+(?:\.\d+)?)",
        r"Height[ \t]*:?[ \t]*(\d+(?:\.\d+)?)",
    ], text)
    if height:
        details["height"] = float(height)

    weight = _search([
        r"Weight\s*\(kg\)[ \t]*:?[ \t]*(\d+(?:\.\d+)?)",
        r"Weight[ \t]*:?[ \t]*(\d+(?:\.\d+)?)",
    ], text)
    if weight:
        details["weight"] = float(weight)

    # -----------------------------------------------------------------
    # BMI  (use printed value, else derive from height + weight)
    # -----------------------------------------------------------------
    bmi = _search([r"BMI[ \t]*:?[ \t]*(\d+(?:\.\d+)?)"], text)
    if bmi:
        details["bmi"] = float(bmi)
    elif details["height"] and details["weight"]:
        h = details["height"]
        if h > 3:                       # cm -> m
            h /= 100
        details["bmi"] = round(details["weight"] / (h * h), 2)

    return details


if __name__ == "__main__":
    transposed = "\n".join([
        "Report Status", "Female", "26 Years", "Age", "Gender", "Z00707", "DUMMY",
    ])
    inline = "Patient Name : Yaswanth\nAge/Sex : 22 / M\nHeight : 172\nWeight : 70\n"
    print("transposed:", extract_report_details(transposed))
    print("inline    :", extract_report_details(inline))

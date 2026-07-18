"""
Lab value parser (Member 3 / backend/pdf_processing).

Extracts structured lab values from the raw text of a medical report PDF.

Why this file was rewritten
---------------------------
Real lab reports (Dr Lal PathLabs, Apollo, AIG, Yashoda, etc.) do NOT lay their
numbers out the same way. When PyMuPDF flattens the PDF to text we mainly see
two shapes:

1. "value-above" layout  (Dr Lal PathLabs / most tabular reports)

       2.00                 <- the actual result
       Creatinine           <- the test name
       (Modified Jaffe)     <- method (optional)
        0.55 - 1.02         <- reference range
       mg/dL                <- unit

   Here the value sits on the line ABOVE the test name, and the line BELOW is the
   reference range. The old parser only looked below the name, so it grabbed the
   reference-range's lower bound (creatinine 0.55 instead of 2.00) and, for eGFR,
   it grabbed "2021" out of the footnote "...calculated using the 2021 CKD-EPI
   equation...". Both bugs are fixed here.

2. "value-below" layout  (simpler reports)

       Glucose
       182 mg/dL

   Here the value is on the line below the name.

The parser below understands both, and it deliberately ignores everything inside
the Notes / Interpretation / Comments / disclaimer sections so footnote numbers
(like "2021") can never be mistaken for a result. It also rejects reference
ranges, dates and unit strings, so it only ever keeps a genuine result value.

Public API (unchanged, consumed by backend/routers/upload.py):

    extract_lab_values(text) -> {"report_name": str, "lab_values": {name: value}}
"""

import re

# ---------------------------------------------------------------------------
# Lab keywords: canonical field name -> list of aliases to look for in the text
# (matched case-insensitively, on word boundaries). Longer / more specific
# aliases are listed first so they win over generic ones.
# ---------------------------------------------------------------------------
LAB_KEYWORDS = {

    # --- Diabetes ---
    "glucose": [
        "glucose fasting", "fasting glucose", "fasting blood sugar",
        "blood glucose", "glucose", "fbs",
    ],
    "hba1c": ["hba1c", "hb a1c", "glycated hemoglobin", "a1c"],

    # --- Kidney ---
    "blood_urea": ["blood urea", "urea nitrogen", "urea"],
    "serum_creatinine": ["serum creatinine", "creatinine"],
    # NOTE: Dr Lal PathLabs prints eGFR as "GFR Estimated" in the results table,
    # so we must match that phrasing (NOT the "(eGFR)" inside the footnote).
    "egfr": ["gfr estimated", "estimated gfr", "egfr", "e-gfr"],
    "specific_gravity": ["specific gravity"],
    "albumin": ["urine albumin", "albumin"],
    "sugar": ["urine sugar"],
    "serum_albumin": ["serum albumin"],
    "calcium": ["calcium"],
    "phosphate": ["phosphorus", "phosphate"],
    "cystatin_c": ["cystatin c"],
    "urine_output": ["urine output"],
    "urine_protein_creatinine_ratio": [
        "urine protein creatinine ratio", "protein creatinine ratio", "upcr",
    ],
    "uric_acid": ["uric acid"],
    "total_protein": ["total protein"],
    "chloride": ["chloride"],

    # --- Heart ---
    "cholesterol": ["total cholesterol", "cholesterol"],
    "hdl": ["hdl cholesterol", "hdl"],
    "ldl": ["ldl cholesterol", "ldl"],
    "triglycerides": ["triglycerides", "triglyceride"],
    "heart_rate": ["heart rate", "pulse"],
    "cpk": ["creatine phosphokinase", "creatine kinase", "cpk"],

    # --- CBC ---
    "hemoglobin": ["hemoglobin", "haemoglobin", "hb"],
    "packed_cell_volume": ["packed cell volume", "pcv"],
    "wbc": ["total leukocyte count", "white blood cells", "wbc"],
    "rbc": ["red blood cells", "rbc"],
    "platelets": ["platelet count", "platelets"],

    # --- Electrolytes ---
    "sodium": ["serum sodium", "sodium"],
    "potassium": ["serum potassium", "potassium"],

    # --- Vitals ---
    "blood_pressure": ["blood pressure", "bp"],
}

# ---------------------------------------------------------------------------
# Section handling: once we cross into a notes/disclaimer block we stop reading
# values, and we resume only when a results-table header appears again. This is
# what stops footnote numbers like "2021" from ever being read as a lab value.
# ---------------------------------------------------------------------------
NOTE_MARKERS = (
    "note", "notes", "interpretation", "comment", "comments", "remark",
    "remarks", "impression", "advice", "disclaimer", "method",
    "important instruction", "end of report", "probable cause", "conditions which",
)
TABLE_MARKERS = (
    "test name", "test report", "results", "bio. ref", "bio ref",
    "investigation", "parameter", "reference interval", "reference range",
)

# ---------------------------------------------------------------------------
# Small regex helpers for classifying a single line.
# ---------------------------------------------------------------------------
_RANGE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:[-–—]|to)\s*\d+(?:\.\d+)?")
_THRESH_RE = re.compile(r"^[<>≤≥]=?\s*\d")
_DATE_RE = re.compile(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}")
_BP_RE = re.compile(r"^\d{2,3}\s*/\s*\d{2,3}\b")
_NUM_ONLY_RE = re.compile(r"^(\d+(?:\.\d+)?)$")
_NUM_UNIT_RE = re.compile(
    r"^(\d+(?:\.\d+)?)\s*"
    r"(?:mg|ml|g|mmol|mol|meq|u|iu|%|mm|cm|x10|lakh|million|thousand|/|cells)",
    re.IGNORECASE,
)


def _is_range(s: str) -> bool:
    """True for reference ranges like '0.55 - 1.02', '70 to 100', '<90', '>126'."""
    s = s.strip()
    return bool(_RANGE_RE.search(s) or _THRESH_RE.match(s))


def _is_date(s: str) -> bool:
    return bool(_DATE_RE.search(s))


def _clean_value_line(s: str):
    """
    If the line is a *standalone result value*, return the number as a string;
    otherwise return None.

    Accepts:  '2.00', '34.68', '6', '140/90', '182 mg/dL'
    Rejects:  '0.55 - 1.02' (range), '<90' (threshold), 'mg/dL' (unit only),
              '27/2/2023  3:09:00PM' (date), 'GFR Estimated' (text)
    """
    s = s.strip().strip("|").strip()
    if not s:
        return None
    if _is_date(s):
        return None
    if _is_range(s):
        return None

    # Blood-pressure style "140/90"
    m = _BP_RE.match(s)
    if m:
        return m.group(0).replace(" ", "")

    # A line that is *only* a number, e.g. the Dr Lal PathLabs value column.
    m = _NUM_ONLY_RE.match(s)
    if m:
        return m.group(1)

    # A number immediately followed by a unit, e.g. Apollo's "182 mg/dL".
    m = _NUM_UNIT_RE.match(s)
    if m:
        return m.group(1)

    return None


def _value_after_keyword(remainder: str):
    """
    Extract a value that appears on the SAME line, right after the test name,
    e.g. 'eGFR 62 mL/min' or 'eGFR : 62'. Returns None if the remainder starts
    with a threshold ('<90'), a range, or plain text (so a sentence like
    'eGFR calculated using the 2021 ...' yields nothing).
    """
    r = remainder.strip(" :\t|-")
    if not r or r[0] in "<>≤≥":
        return None
    if _is_range(r) or _is_date(r):
        return None
    m = _BP_RE.match(r)
    if m:
        return m.group(0).replace(" ", "")
    m = re.match(r"^(\d+(?:\.\d+)?)\b", r)
    if m:
        return m.group(1)
    return None


def convert_value(value):
    """Convert an extracted string to int/float; keep blood pressure as text."""
    if value is None:
        return None
    if "/" in str(value):
        return value
    try:
        return float(value) if "." in str(value) else int(value)
    except (ValueError, TypeError):
        return value


# ---------------------------------------------------------------------------
# Report name detection (kept for the API response).
# ---------------------------------------------------------------------------
REPORT_NAMES = [
    "diabetes profile", "glucose fasting", "glycemic profile", "hba1c",
    "lipid profile", "cardiac profile", "kidney panel", "kidney function test",
    "renal function test", "kft", "cbc", "complete blood count",
    "liver function test", "lft", "thyroid profile",
    "master health checkup", "executive health checkup",
]


def extract_report_name(text: str):
    head = "\n".join(text.splitlines()[:60]).lower()
    for report in REPORT_NAMES:
        if report in head:
            return report
    return "unknown"


# ---------------------------------------------------------------------------
# Value location: given a keyword match on lines[i], find its value.
# ---------------------------------------------------------------------------
def _find_value_for_row(lines, i):
    """
    Priority:
        1. same line   (Apollo:  'eGFR 62')
        2. line above  (Dr Lal PathLabs value-above layout)
        3. line(s) below, skipping method '(...)' lines and stopping at the
           reference range (Apollo:  'Glucose' / '182 mg/dL')
    """
    line = lines[i]

    # 1. same line, after the test name: strip the leading label text and see if
    #    a value follows. Sentences yield nothing.
    tail = re.sub(r"^[A-Za-z()/,.&'\s:%-]+", "", line)
    same = _value_after_keyword(tail) if tail else None
    if same is not None:
        return same

    # 2. value on the line directly above (Dr Lal PathLabs)
    above = _clean_value_line(lines[i - 1]) if i - 1 >= 0 else None

    # 3. value on the next non-method line below, stopping at a range/unit
    below = None
    for j in (i + 1, i + 2):
        if j >= len(lines):
            break
        s = lines[j].strip()
        if not s:
            continue
        if s.startswith("("):          # method line e.g. "(Hexokinase)" -> skip
            continue
        if _is_range(s) or _THRESH_RE.match(s):
            break                      # reached the reference range: value isn't below
        below = _clean_value_line(s)
        break                          # first real line below decides it

    # In the value-above layout the line below is a range/unit, so `below` is
    # None and we take `above`. In the value-below layout `above` is usually
    # text, so we take `below`.
    if above is not None and below is None:
        return above
    if below is not None:
        return below
    return above


def extract_lab_values(text: str):
    values = {key: None for key in LAB_KEYWORDS}

    lines = [ln.strip() for ln in text.splitlines()]
    in_notes = False

    for i, current in enumerate(lines):
        if not current:
            continue
        low = current.lower()

        # ---- section tracking ---------------------------------------------
        stripped = low.strip(" .:-*")
        if any(stripped == m or stripped.startswith(m + " ") for m in NOTE_MARKERS):
            in_notes = True
            continue
        if any(m in low for m in TABLE_MARKERS):
            in_notes = False
            continue                    # header lines never carry values
        if in_notes:
            continue

        # Skip obvious non-result lines fast.
        if _is_range(current) or _is_date(current):
            continue

        # ---- keyword match -------------------------------------------------
        for lab, aliases in LAB_KEYWORDS.items():
            if values[lab] is not None:
                continue
            for alias in aliases:
                if re.search(r"\b" + re.escape(alias) + r"\b", low):
                    value = _find_value_for_row(lines, i)
                    if value is not None:
                        values[lab] = convert_value(value)
                    break  # stop after first matching alias for this lab

    return {
        "report_name": extract_report_name(text),
        "lab_values": values,
    }


# ---------------------------------------------------------------------------
# Manual smoke test (both layouts).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    lpl = """
Test Report
Test Name
Results
Units
Bio. Ref. Interval
KIDNEY PANEL; KFT,SERUM
2.00
Creatinine
(Modified Jaffe,Kinetic)
 0.55 - 1.02
mg/dL
34.68
GFR Estimated
 <90
mL/min/1.73m2
24.00
Urea
 13.00 - 43.00
mg/dL
140.00
Sodium
 136.00 - 145.00
mEq/L
Note
1.
Estimated GFR  (eGFR) calculated using the 2021 CKD-EPI creatinine equation.
"""
    apollo = """
Glucose
182 mg/dL
HbA1c
8.1 %
Blood Pressure
140/90
eGFR
62
"""
    from pprint import pprint
    print("LPL (value-above):")
    pprint({k: v for k, v in extract_lab_values(lpl)["lab_values"].items() if v is not None})
    print("\nApollo (value-below):")
    pprint({k: v for k, v in extract_lab_values(apollo)["lab_values"].items() if v is not None})

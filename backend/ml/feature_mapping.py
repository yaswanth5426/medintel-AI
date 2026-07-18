from backend.ml.default_values import DEFAULT_VALUES

DIABETES_FEATURES = [
    "Age",
    "Gender",
    "Pregnancies",
    "Glucose",
    "HbA1c",
    "BMI",
    "BloodPressure",
    "Insulin",
    "Hypertension",
    "Smoking",
    "FamilyHistory",
    "HeartDisease"
]

# ==========================================================
# HEART FEATURES (v2)
# ==========================================================

HEART_FEATURES = [
    "Age",
    "Sex",
    "Height",
    "Weight",
    "BMI",
    "SystolicBP",
    "DiastolicBP",
    "TotalCholesterol",
    "Glucose",
    "Smoking",
    "Diabetes",
    "Hypertension",
    "Alcohol",
    "PhysicalActivity",
    "HeartRate",
    "Platelets",
    "SerumCreatinine",
    "SerumSodium",
    "CPK"
]

# ==========================================================
# KIDNEY FEATURES (v2)
# ==========================================================

CKD_FEATURES = [
    "Age",
    "BloodPressure",
    "SpecificGravity",
    "Albumin",
    "Sugar",
    "BloodGlucose",
    "BloodUrea",
    "SerumCreatinine",
    "Sodium",
    "Potassium",
    "Hemoglobin",
    "PackedCellVolume",
    "WBC",
    "RBC",
    "Hypertension",
    "Diabetes",
    "CoronaryArteryDisease",
    "Appetite",
    "PedalEdema",
    "Anemia",
    "eGFR",
    "UrineProteinCreatinineRatio",
    "UrineOutput",
    "SerumAlbumin",
    "Calcium",
    "Phosphate",
    "BMI",
    "Smoking",
    "PhysicalActivity",
    "CystatinC"
]


def get_value(value, default):
    return value if value is not None else default


def calculate_bmi(height, weight):

    if height is None or weight is None:
        return DEFAULT_VALUES["BMI"]

    if height > 3:
        height = height / 100

    return round(weight / (height * height), 2)


def split_bp(bp):

    if bp and "/" in str(bp):

        s, d = bp.split("/")

        return int(s), int(d)

    return (
        DEFAULT_VALUES["SystolicBP"],
        DEFAULT_VALUES["DiastolicBP"]
    )


def encode_gender(g):
    """Map gender/sex to the numeric code the v2 models were trained on
    (male -> 1, female -> 0). Accepts strings or already-numeric values."""
    if g is None:
        return 1
    if isinstance(g, (int, float)):
        return int(g)
    s = str(g).strip().lower()
    if s.startswith("m"):
        return 1
    if s.startswith("f"):
        return 0
    return 1


def systolic_bp(bp):
    """Return the systolic component as a number. Handles '140/90', a bare
    number, or None (falls back to the default systolic value)."""
    if bp is None:
        return DEFAULT_VALUES["SystolicBP"]
    if isinstance(bp, (int, float)):
        return float(bp)
    text = str(bp)
    if "/" in text:
        try:
            return float(text.split("/")[0].strip())
        except ValueError:
            return DEFAULT_VALUES["SystolicBP"]
    try:
        return float(text)
    except ValueError:
        return DEFAULT_VALUES["SystolicBP"]


# ======================================================
# Diabetes
# ======================================================

def prepare_diabetes_features(report, lab):

    bmi = report.get("bmi")

    if bmi is None:
        bmi = calculate_bmi(
            report.get("height"),
            report.get("weight")
        )

    return {

        "Age": get_value(report.get("age"), 40),

        "Gender": encode_gender(report.get("gender")),

        "Pregnancies": DEFAULT_VALUES["Pregnancies"],

        "Glucose": get_value(
            lab.get("glucose"),
            DEFAULT_VALUES["Glucose"]
        ),

        "HbA1c": get_value(
            lab.get("hba1c"),
            DEFAULT_VALUES["HbA1c"]
        ),

        "BMI": bmi,

        "BloodPressure": systolic_bp(lab.get("blood_pressure")),

        "Insulin": DEFAULT_VALUES["Insulin"],

        "Hypertension": DEFAULT_VALUES["Hypertension"],

        "Smoking": DEFAULT_VALUES["Smoking"],

        "FamilyHistory": DEFAULT_VALUES["FamilyHistory"],

        "HeartDisease": DEFAULT_VALUES["HeartDisease"]

    }


# ======================================================
# Heart
# ======================================================

def prepare_heart_features(report, lab):

    bmi = report.get("bmi")

    if bmi is None:
        bmi = calculate_bmi(
            report.get("height"),
            report.get("weight")
        )

    systolic, diastolic = split_bp(
        lab.get("blood_pressure")
    )

    return {

        "Age": get_value(report.get("age"), 40),

        "Sex": encode_gender(report.get("gender")),

        "Height": get_value(
            report.get("height"),
            DEFAULT_VALUES["Height"]
        ),

        "Weight": get_value(
            report.get("weight"),
            DEFAULT_VALUES["Weight"]
        ),

        "BMI": bmi,

        "SystolicBP": systolic,

        "DiastolicBP": diastolic,

        "TotalCholesterol": get_value(
            lab.get("cholesterol"),
            DEFAULT_VALUES["TotalCholesterol"]
        ),

        "Glucose": get_value(
            lab.get("glucose"),
            DEFAULT_VALUES["Glucose"]
        ),

        "Smoking": DEFAULT_VALUES["Smoking"],

        "Diabetes": DEFAULT_VALUES["Diabetes"],

        "Hypertension": DEFAULT_VALUES["Hypertension"],

        "Alcohol": DEFAULT_VALUES["Alcohol"],

        "PhysicalActivity": DEFAULT_VALUES["PhysicalActivity"],

        "HeartRate": get_value(
            lab.get("heart_rate"),
            DEFAULT_VALUES["HeartRate"]
        ),

        "Platelets": get_value(
            lab.get("platelets"),
            DEFAULT_VALUES["Platelets"]
        ),

        "SerumCreatinine": get_value(
            lab.get("serum_creatinine"),
            DEFAULT_VALUES["SerumCreatinine"]
        ),

        "SerumSodium": get_value(
            lab.get("sodium"),
            DEFAULT_VALUES["Sodium"]
        ),

        "CPK": get_value(
            lab.get("cpk"),
            DEFAULT_VALUES["CPK"]
        )

    }


# ======================================================
# CKD
# ======================================================

def prepare_ckd_features(report, lab):

    bmi = report.get("bmi")

    if bmi is None:
        bmi = calculate_bmi(
            report.get("height"),
            report.get("weight")
        )

    return {

        "Age": get_value(report.get("age"), 40),

        "BloodPressure": systolic_bp(lab.get("blood_pressure")),

        "SpecificGravity": get_value(
            lab.get("specific_gravity"),
            DEFAULT_VALUES["SpecificGravity"]
        ),

        "Albumin": get_value(
            lab.get("albumin"),
            DEFAULT_VALUES["Albumin"]
        ),

        "Sugar": get_value(
            lab.get("sugar"),
            DEFAULT_VALUES["Sugar"]
        ),

        "BloodGlucose": get_value(
            lab.get("glucose"),
            DEFAULT_VALUES["BloodGlucose"]
        ),

        "BloodUrea": get_value(
            lab.get("blood_urea"),
            DEFAULT_VALUES["BloodUrea"]
        ),

        "SerumCreatinine": get_value(
            lab.get("serum_creatinine"),
            DEFAULT_VALUES["SerumCreatinine"]
        ),

        "Sodium": get_value(
            lab.get("sodium"),
            DEFAULT_VALUES["Sodium"]
        ),

        "Potassium": get_value(
            lab.get("potassium"),
            DEFAULT_VALUES["Potassium"]
        ),

        "Hemoglobin": get_value(
            lab.get("hemoglobin"),
            DEFAULT_VALUES["Hemoglobin"]
        ),

        "PackedCellVolume": get_value(
            lab.get("packed_cell_volume"),
            DEFAULT_VALUES["PackedCellVolume"]
        ),

        "WBC": get_value(
            lab.get("wbc"),
            DEFAULT_VALUES["WBC"]
        ),

        "RBC": get_value(
            lab.get("rbc"),
            DEFAULT_VALUES["RBC"]
        ),

        "Hypertension": DEFAULT_VALUES["Hypertension"],

        "Diabetes": DEFAULT_VALUES["Diabetes"],

        "CoronaryArteryDisease": DEFAULT_VALUES["CoronaryArteryDisease"],

        "Appetite": DEFAULT_VALUES["Appetite"],

        "PedalEdema": DEFAULT_VALUES["PedalEdema"],

        "Anemia": DEFAULT_VALUES["Anemia"],

        "eGFR": get_value(
            lab.get("egfr"),
            DEFAULT_VALUES["eGFR"]
        ),

        "UrineProteinCreatinineRatio": get_value(
            lab.get("urine_protein_creatinine_ratio"),
            DEFAULT_VALUES["UrineProteinCreatinineRatio"]
        ),

        "UrineOutput": get_value(
            lab.get("urine_output"),
            DEFAULT_VALUES["UrineOutput"]
        ),

        "SerumAlbumin": get_value(
            lab.get("serum_albumin"),
            DEFAULT_VALUES["SerumAlbumin"]
        ),

        "Calcium": get_value(
            lab.get("calcium"),
            DEFAULT_VALUES["Calcium"]
        ),

        "Phosphate": get_value(
            lab.get("phosphate"),
            DEFAULT_VALUES["Phosphate"]
        ),

        "BMI": bmi,

        "Smoking": DEFAULT_VALUES["Smoking"],

        "PhysicalActivity": DEFAULT_VALUES["PhysicalActivity"],

        "CystatinC": get_value(
            lab.get("cystatin_c"),
            DEFAULT_VALUES["CystatinC"]
        )

    }

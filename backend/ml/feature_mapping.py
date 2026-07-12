# pyrefly: ignore [missing-import]

import joblib

PREPROCESSOR_DIR = "backend/ml/models/preprocessors/"

# ==========================================================
# DIABETES FEATURES (v2)
# ==========================================================

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


# ==========================================================
# Feature Mapping
# ==========================================================

def map_features(disease: str, lab_values: dict):
    """
    Converts extracted lab values into the exact feature vector
    expected by the trained model.

    Missing values are automatically filled using the defaults
    saved during training.
    """

    disease = disease.lower()

    # -------------------------------
    # Diabetes
    # -------------------------------

    if disease == "diabetes":

        feature_order = DIABETES_FEATURES

        defaults = joblib.load(
            PREPROCESSOR_DIR + "diabetes_defaults_v2.pkl"
        )

    # -------------------------------
    # Heart
    # -------------------------------

    elif disease == "heart":

        feature_order = HEART_FEATURES

        defaults = joblib.load(
            PREPROCESSOR_DIR + "heart_defaults_v2.pkl"
        )

    # -------------------------------
    # Kidney
    # -------------------------------

    elif disease in ["kidney", "ckd"]:

        feature_order = CKD_FEATURES

        defaults = joblib.load(
            PREPROCESSOR_DIR + "ckd_defaults_v2.pkl"
        )

    else:

        raise ValueError(
            "Unsupported disease."
        )

    # -------------------------------
    # Build Feature Vector
    # -------------------------------

    feature_vector = []

    for feature in feature_order:

        value = lab_values.get(feature)

        if value is None:

            value = defaults.get(feature, 0)

        feature_vector.append(value)

    return feature_vector
# ==========================================================
# Feature Mapping
# ==========================================================

def map_features(disease: str, lab_values: dict):
    """
    Converts extracted lab values into the exact feature vector
    expected by the trained model.

    Missing values are automatically filled using the defaults
    saved during training.
    """

    disease = disease.lower()

    # -------------------------------
    # Diabetes
    # -------------------------------

    if disease == "diabetes":

        feature_order = DIABETES_FEATURES

        defaults = joblib.load(
            PREPROCESSOR_DIR + "diabetes_defaults_v2.pkl"
        )

    # -------------------------------
    # Heart
    # -------------------------------

    elif disease == "heart":

        feature_order = HEART_FEATURES

        defaults = joblib.load(
            PREPROCESSOR_DIR + "heart_defaults_v2.pkl"
        )

    # -------------------------------
    # Kidney
    # -------------------------------

    elif disease in ["kidney", "ckd"]:

        feature_order = CKD_FEATURES

        defaults = joblib.load(
            PREPROCESSOR_DIR + "ckd_defaults_v2.pkl"
        )

    else:

        raise ValueError(
            "Unsupported disease."
        )

    # -------------------------------
    # Build Feature Vector
    # -------------------------------

    feature_vector = []

    for feature in feature_order:

        value = lab_values.get(feature)

        if value is None:

            value = defaults.get(feature, 0)

        feature_vector.append(value)

    return feature_vector

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    # -----------------------------
    # Diabetes Test
    # -----------------------------

    diabetes_report = {

        "Age": 45,
        "Glucose": 180,
        "BMI": 31.5

    }

    diabetes_features = map_features(
        "diabetes",
        diabetes_report
    )

    print("=" * 60)
    print("DIABETES")
    print("=" * 60)
    print(diabetes_features)

    # -----------------------------
    # Heart Test
    # -----------------------------

    heart_report = {

        "Age": 55,
        "SystolicBP": 145,
        "Glucose": 170

    }

    heart_features = map_features(
        "heart",
        heart_report
    )

    print("=" * 60)
    print("HEART")
    print("=" * 60)
    print(heart_features)

    # -----------------------------
    # Kidney Test
    # -----------------------------

    kidney_report = {

        "Age": 50,
        "BloodPressure": 90,
        "SerumCreatinine": 2.3

    }

    kidney_features = map_features(
        "kidney",
        kidney_report
    )

    print("=" * 60)
    print("KIDNEY")
    print("=" * 60)
    print(kidney_features)    
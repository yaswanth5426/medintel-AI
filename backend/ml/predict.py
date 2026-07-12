import joblib
import numpy as np

DIABETES_FEATURES = {
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
}

HEART_FEATURES = {
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
}

CKD_FEATURES = {
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
}


# Load trained models
diabetes_model = joblib.load(
    "backend/ml/models/diabetes_model_v2.pkl"
)

heart_model = joblib.load(
    "backend/ml/models/heart_model_v2.pkl"
)

kidney_model = joblib.load(
    "backend/ml/models/ckd_model_v2.pkl"
)


def calculate_risk(disease_probability):
    """
    Convert disease probability into a risk level.
    """

    if disease_probability >= 0.90:
        return "High"

    elif disease_probability >= 0.70:
        return "Medium"

    else:
        return "Low"


# ============================
# Diabetes Prediction
# ============================

def predict_diabetes(features):

    scaler = joblib.load("backend/ml/models/preprocessors/diabetes_scaler_v2.pkl")

    features = np.array(features).reshape(1, -1)

    prediction = diabetes_model.predict(features)[0]

    probabilities = diabetes_model.predict_proba(features)[0]

    confidence = max(probabilities)

    disease_probability = probabilities[1]

    risk = calculate_risk(disease_probability)

    return {
        "prediction": "Diabetes" if prediction == 1 else "No Diabetes",

        "confidence": round(float(confidence), 2),

        "risk": risk,

        "probabilities": {
            "No Diabetes": round(float(probabilities[0]), 2),
            "Diabetes": round(float(probabilities[1]), 2)
        }
    }


# ============================
# Heart Disease Prediction
# ============================

def predict_heart(features):

    scaler = joblib.load("backend/ml/models/preprocessors/heart_scaler_v2.pkl")

    features = np.array(features).reshape(1, -1)

    prediction = heart_model.predict(features)[0]

    probabilities = heart_model.predict_proba(features)[0]

    confidence = max(probabilities)

    disease_probability = probabilities[1]

    risk = calculate_risk(disease_probability)

    return {
        "prediction": "Heart Disease" if prediction == 1 else "No Heart Disease",

        "confidence": round(float(confidence), 2),

        "risk": risk,

        "probabilities": {
            "No Heart Disease": round(float(probabilities[0]), 2),
            "Heart Disease": round(float(probabilities[1]), 2)
        }
    }


# ============================
# Kidney Disease Prediction
# ============================

def predict_kidney(features):

    scaler = joblib.load("backend/ml/models/preprocessors/ckd_scaler_v2.pkl")

    features = np.array(features).reshape(1, -1)

    prediction = kidney_model.predict(features)[0]

    probabilities = kidney_model.predict_proba(features)[0]

    confidence = max(probabilities)

    disease_probability = probabilities[1]

    risk = calculate_risk(disease_probability)

    return {
        "prediction": "Kidney Disease" if prediction == 1 else "No Kidney Disease",

        "confidence": round(float(confidence), 2),

        "risk": risk,

        "probabilities": {
            "No Kidney Disease": round(float(probabilities[0]), 2),
            "Kidney Disease": round(float(probabilities[1]), 2)
        }
    }

# pyrefly: ignore [missing-import]
try:
    from backend.ml.feature_mapping import map_features
except ModuleNotFoundError:
    # pyrefly: ignore [missing-import]
    from feature_mapping import map_features


def predict_disease(
    disease: str,
    lab_values: dict
):
    """
    Generic prediction function used by the backend API.
    """

    disease = disease.lower()

    if disease not in ["diabetes", "heart", "kidney", "ckd"]:
        raise ValueError("Unsupported disease.")

    if not lab_values:
        raise ValueError("Empty lab values.")

    # -----------------------------------
    # Validate input
    # -----------------------------------

    for key, value in lab_values.items():

        if value is None:
            continue

        if not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be numeric.")

        if value < 0:
            raise ValueError(f"{key} cannot be negative.")

    # -----------------------------------
    # Feature Mapping
    # -----------------------------------

    features = map_features(
        disease,
        lab_values
    )

    # -----------------------------------
    # Prediction
    # -----------------------------------

    if disease == "diabetes":

        result = predict_diabetes(features)

    elif disease == "heart":

        result = predict_heart(features)

    else:

        result = predict_kidney(features)

    # -----------------------------------
    # Return
    # -----------------------------------

    return {

        "prediction": result["prediction"],

        "confidence": result["confidence"],

        "risk": result["risk"],

        "probabilities": result["probabilities"]

    }
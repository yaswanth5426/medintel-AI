import joblib
import numpy as np

DIABETES_FEATURES = {
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
}

HEART_FEATURES = {
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
}

CKD_FEATURES = {
    "id",
    "age",
    "bp",
    "sg",
    "al",
    "su",
    "rbc",
    "pc",
    "pcc",
    "ba",
    "bgr",
    "bu",
    "sc",
    "sod",
    "pot",
    "hemo",
    "pcv",
    "wc",
    "rc",
    "htn",
    "dm",
    "cad",
    "appet",
    "pe",
    "ane"
}


# Load trained models
diabetes_model = joblib.load("backend/ml/models/diabetes_model.pkl")
heart_model = joblib.load("backend/ml/models/heart_model.pkl")
kidney_model = joblib.load("backend/ml/models/ckd_model.pkl")


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
from backend.ml.feature_mapping import map_features


def predict_disease(lab_values: dict):
    """
    Generic prediction function used by the backend API.
    Automatically detects which disease model to use.
    """

    if not lab_values:
        raise ValueError("Empty lab values.")

    keys = set(lab_values.keys())

    # -------------------------
    # Detect disease
    # -------------------------

    if DIABETES_FEATURES.issubset(keys):
        disease = "diabetes"

    elif HEART_FEATURES.issubset(keys):
        disease = "heart"

    elif CKD_FEATURES.issubset(keys):
        disease = "kidney"

    else:
        raise ValueError("Unsupported or incomplete feature set.")

    # -------------------------
    # Validate input
    # -------------------------

    for key, value in lab_values.items():

        if value is None:
            continue

        if not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be numeric.")

        if value < 0:
            raise ValueError(f"{key} cannot be negative.")

    # -------------------------
    # Feature Mapping
    # -------------------------

    features = map_features(disease, lab_values)

    # -------------------------
    # Prediction
    # -------------------------

    if disease == "diabetes":
        result = predict_diabetes(features)

    elif disease == "heart":
        result = predict_heart(features)

    else:
        result = predict_kidney(features)

    # -------------------------
    # Return
    # -------------------------

    return {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "risk": result["risk"]
    }

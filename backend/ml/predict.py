import joblib
import numpy as np

from backend.ml.feature_mapping import (
    prepare_diabetes_features,
    prepare_heart_features,
    prepare_ckd_features,
    DIABETES_FEATURES,
    HEART_FEATURES,
    CKD_FEATURES
)


# ======================================================
# Load Models
# ======================================================

diabetes_model = joblib.load(
    "backend/ml/models/diabetes_model_v2.pkl"
)

heart_model = joblib.load(
    "backend/ml/models/heart_model_v2.pkl"
)

ckd_model = joblib.load(
    "backend/ml/models/ckd_model_v2.pkl"
)


# ======================================================
# Load Scalers
# ======================================================

diabetes_scaler = joblib.load(
    "backend/ml/models/preprocessors/diabetes_scaler_v2.pkl"
)

heart_scaler = joblib.load(
    "backend/ml/models/preprocessors/heart_scaler_v2.pkl"
)

ckd_scaler = joblib.load(
    "backend/ml/models/preprocessors/ckd_scaler_v2.pkl"
)


# ======================================================
# Helper Functions
# ======================================================

def calculate_risk(probability):

    if probability >= 0.90:
        return "High"

    elif probability >= 0.70:
        return "Medium"

    return "Low"


def create_feature_vector(feature_dict, feature_order):

    """
    Converts

    {
        Age:22,
        BMI:24,
        ...
    }

    ↓

    [22,24,...]
    """

    return [

        feature_dict[name]

        for name in feature_order

    ]


# ======================================================
# Diabetes Prediction
# ======================================================

def predict_diabetes(feature_vector):

    feature_vector = np.array(
        feature_vector
    ).reshape(1, -1)

    feature_vector = diabetes_scaler.transform(
        feature_vector
    )

    prediction = diabetes_model.predict(
        feature_vector
    )[0]

    probabilities = diabetes_model.predict_proba(
        feature_vector
    )[0]

    confidence = float(max(probabilities))

    disease_probability = float(probabilities[1])

    return {

        "prediction":

            "Diabetes"

            if prediction == 1

            else "No Diabetes",

        "confidence":

            round(confidence, 2),

        "risk":

            calculate_risk(
                disease_probability
            ),

        "probabilities": {

            "No Diabetes":

                round(
                    float(probabilities[0]),
                    2
                ),

            "Diabetes":

                round(
                    float(probabilities[1]),
                    2
                )

        }

    }


# ======================================================
# Heart Prediction
# ======================================================

def predict_heart(feature_vector):

    feature_vector = np.array(
        feature_vector
    ).reshape(1, -1)

    feature_vector = heart_scaler.transform(
        feature_vector
    )

    prediction = heart_model.predict(
        feature_vector
    )[0]

    probabilities = heart_model.predict_proba(
        feature_vector
    )[0]

    confidence = float(max(probabilities))

    disease_probability = float(probabilities[1])

    return {

        "prediction":

            "Heart Disease"

            if prediction == 1

            else "No Heart Disease",

        "confidence":

            round(confidence, 2),

        "risk":

            calculate_risk(
                disease_probability
            ),

        "probabilities": {

            "No Heart Disease":

                round(
                    float(probabilities[0]),
                    2
                ),

            "Heart Disease":

                round(
                    float(probabilities[1]),
                    2
                )

        }

    }


# ======================================================
# CKD Prediction
# ======================================================

def predict_ckd(feature_vector):

    feature_vector = np.array(
        feature_vector
    ).reshape(1, -1)

    feature_vector = ckd_scaler.transform(
        feature_vector
    )

    prediction = ckd_model.predict(
        feature_vector
    )[0]

    probabilities = ckd_model.predict_proba(
        feature_vector
    )[0]

    confidence = float(max(probabilities))

    disease_probability = float(probabilities[1])

    return {

        "prediction":

            "Kidney Disease"

            if prediction == 1

            else "No Kidney Disease",

        "confidence":

            round(confidence, 2),

        "risk":

            calculate_risk(
                disease_probability
            ),

        "probabilities": {

            "No Kidney Disease":

                round(
                    float(probabilities[0]),
                    2
                ),

            "Kidney Disease":

                round(
                    float(probabilities[1]),
                    2
                )

        }

    }

    # ======================================================
# Main Prediction Function
# ======================================================

def predict_disease(
    disease: str,
    report_details: dict,
    lab_values: dict
):
    """
    Generic prediction function.

    Parameters
    ----------
    disease : str
        diabetes | heart | ckd

    report_details : dict
        Output from report_extractor.py

    lab_values : dict
        Output from lab_value_parser.py
    """

    disease = disease.lower()

    # ---------------------------------------------
    # Basic Validation
    # ---------------------------------------------

    if disease not in ["diabetes", "heart", "ckd", "kidney"]:
        raise ValueError("Unsupported disease.")

    if report_details is None:
        report_details = {}

    if lab_values is None:
        lab_values = {}

    # ---------------------------------------------
    # Diabetes
    # ---------------------------------------------

    if disease == "diabetes":

        mapped = prepare_diabetes_features(
            report_details,
            lab_values
        )

        feature_vector = create_feature_vector(
            mapped,
            DIABETES_FEATURES
        )

        result = predict_diabetes(
            feature_vector
        )

    # ---------------------------------------------
    # Heart Disease
    # ---------------------------------------------

    elif disease == "heart":

        mapped = prepare_heart_features(
            report_details,
            lab_values
        )

        feature_vector = create_feature_vector(
            mapped,
            HEART_FEATURES
        )

        result = predict_heart(
            feature_vector
        )

    # ---------------------------------------------
    # CKD
    # ---------------------------------------------

    else:

        mapped = prepare_ckd_features(
            report_details,
            lab_values
        )

        feature_vector = create_feature_vector(
            mapped,
            CKD_FEATURES
        )

        result = predict_ckd(
            feature_vector
        )

    return {

        "status": "success",

        "disease": disease,

        "prediction": result["prediction"],

        "confidence": result["confidence"],

        "risk": result["risk"],

        "probabilities": result["probabilities"],

        "features_used": mapped

    }


# ======================================================
# Testing
# ======================================================

if __name__ == "__main__":

    report_details = {

        "age": 48,

        "gender": "Male",

        "height": 170,

        "weight": 74,

        "bmi": None

    }

    lab_values = {

        "glucose": 185,

        "hba1c": 8.3,

        "blood_pressure": "140/90",

        "cholesterol": 220,

        "blood_urea": 48,

        "serum_creatinine": 1.8,

        "hemoglobin": 13.5,

        "platelets": 250000,

        "wbc": 7600,

        "rbc": 4.8,

        "sodium": 138,

        "potassium": 4.2,

        "egfr": 65,

        "albumin": None,

        "specific_gravity": None,

        "sugar": None,

        "packed_cell_volume": None,

        "heart_rate": None,

        "cpk": None,

        "urine_protein_creatinine_ratio": None,

        "urine_output": None,

        "serum_albumin": None,

        "calcium": None,

        "phosphate": None,

        "cystatin_c": None

    }

    result = predict_disease(

        disease="diabetes",

        report_details=report_details,

        lab_values=lab_values

    )

    print(result)
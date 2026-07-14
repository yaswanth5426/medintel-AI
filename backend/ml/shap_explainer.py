# pyrefly: ignore [missing-import]
import joblib
# pyrefly: ignore [missing-import]
import shap
import pandas as pd


# -----------------------------
# Model Information
# -----------------------------

MODELS = {

    "diabetes": {
        "path": "backend/ml/models/diabetes_model_v2.pkl",
        "features": [
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
    },

    "heart": {
        "path": "backend/ml/models/heart_model_v2.pkl",
        "features": [
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
    },

    "kidney": {
        "path": "backend/ml/models/ckd_model_v2.pkl",
        "features": [
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
    }

}


# -----------------------------
# Load Model
# -----------------------------

def load_model(model_name):

    return joblib.load(MODELS[model_name]["path"])


# -----------------------------
# SHAP Explanation
# -----------------------------

def explain_prediction(model_name, sample):

    model = load_model(model_name)

    feature_names = MODELS[model_name]["features"]

    sample_df = pd.DataFrame(
        [sample],
        columns=feature_names
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(sample_df)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_values = shap_values[0]

    feature_importance = {}

    for feature, value in zip(feature_names, shap_values):

        feature_importance[feature] = float(value)

    feature_importance = dict(
        sorted(
            feature_importance.items(),
            key=lambda item: abs(item[1]),
            reverse=True
        )
    )

    return feature_importance
if __name__ == "__main__":

    diabetes_sample = [
        45,
        0,
        2,
        180,
        6.2,
        31.5,
        80,
        150,
        1,
        0,
        0.45,
        0
    ]

    heart_sample = [
        63,
        1,
        170,
        72,
        25.4,
        145,
        80,
        220,
        170,
        1,
        1,
        1,
        0,
        1,
        75,
        262000,
        1.1,
        137,
        250
    ]

    kidney_sample = [
        48,
        80,
        1.015,
        2,
        2,
        281,
        103,
        2.2,
        135,
        4.9,
        12,
        38,
        9062,
        4.3,
        0,
        0,
        0,
        1,
        0,
        0,
        62.1,
        2.28,
        1645,
        3.25,
        8.99,
        4.23,
        27.6,
        0,
        1,
        1.75
    ]

    for disease, sample in [
        ("diabetes", diabetes_sample),
        ("heart", heart_sample),
        ("kidney", kidney_sample)
    ]:

        print("\n" + "=" * 60)
        print(disease.upper())
        print("=" * 60)

        explanation = explain_prediction(disease, sample)

        print("\nTop 10 Important Features\n")

        for feature, value in list(explanation.items())[:10]:
            print(f"{feature:<35} {value:.4f}")
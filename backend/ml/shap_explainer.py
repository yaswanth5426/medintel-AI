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
        "path": "backend/ml/models/diabetes_model.pkl",
        "features": [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ]
    },

    "heart": {
        "path": "backend/ml/models/heart_model.pkl",
        "features": [
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
        ]
    },

    "kidney": {
        "path": "backend/ml/models/ckd_model.pkl",
        "features": [
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
        2,
        120,
        70,
        20,
        80,
        30,
        0.45,
        45
    ]
    kidney_sample = [
    1,      # id
    48,     # age
    80,     # bp
    1.020,  # sg
    1,      # al
    0,      # su
    1,      # rbc
    1,      # pc
    0,      # pcc
    0,      # ba
    121,    # bgr
    36,     # bu
    1.2,    # sc
    135,    # sod
    4.5,    # pot
    15.4,   # hemo
    44,     # pcv
    7800,   # wc
    5.2,    # rc
    1,      # htn
    1,      # dm
    0,      # cad
    1,      # appet
    0,      # pe
    0       # ane
]

    explanation = explain_prediction(
        "kidney",
        kidney_sample
    )

    print("\nTop Features\n")

    for feature, value in list(explanation.items())[:5]:
        print(feature, value)    
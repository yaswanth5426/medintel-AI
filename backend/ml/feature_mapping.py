# pyrefly: ignore [missing-import]
import joblib

PREPROCESSOR_DIR = "backend/ml/models/preprocessors/"

# -----------------------------------------
# Feature order for each trained model
# -----------------------------------------

DIABETES_FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

HEART_FEATURES = [
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

CKD_FEATURES = [
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


# -----------------------------------------
# Feature Mapping
# -----------------------------------------

def map_features(report_data, disease):
    """
    Convert extracted report data into the feature
    vector expected by the trained model.
    Missing values are filled using the defaults
    saved during training.
    """

    disease = disease.lower()

    if disease == "diabetes":
        feature_order = DIABETES_FEATURES
        defaults = joblib.load(
            PREPROCESSOR_DIR + "diabetes_defaults.pkl"
        )

    elif disease == "heart":
        feature_order = HEART_FEATURES
        defaults = joblib.load(
            PREPROCESSOR_DIR + "heart_defaults.pkl"
        )

    elif disease == "kidney":
        feature_order = CKD_FEATURES
        defaults = joblib.load(
            PREPROCESSOR_DIR + "ckd_defaults.pkl"
        )

    else:
        raise ValueError("Unsupported disease")

    feature_vector = []

    for feature in feature_order:

        value = report_data.get(feature)

        if value is None:
            value = defaults[feature]

        feature_vector.append(value)

    return feature_vector


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    report = {
        "Glucose": 180,
        "Age": 45
    }

    mapped = map_features(report, "diabetes")

    print("Mapped Feature Vector:\n")
    print(mapped)
# pyrefly: ignore [missing-import]
import joblib
# pyrefly: ignore [missing-import]
import numpy as np
diabetes_model = joblib.load("backend/ml/models/diabetes_model.pkl")
heart_model = joblib.load("backend/ml/models/heart_model.pkl")
kidney_model = joblib.load("backend/ml/models/ckd_model.pkl")

def predict_diabetes(features):
    features = np.array(features).reshape(1, -1)

    prediction = diabetes_model.predict(features)[0]

    probabilities = diabetes_model.predict_proba(features)[0]

    confidence = max(probabilities)

    return {
        "prediction": "Diabetes" if prediction == 1 else "No Diabetes",

        "confidence": round(float(confidence), 2),

        "probabilities": {
            "No Diabetes": round(float(probabilities[0]), 2),
            "Diabetes": round(float(probabilities[1]), 2)
        }
    }

def predict_heart(features):
    features = np.array(features).reshape(1, -1)

    prediction = heart_model.predict(features)[0]

    probabilities = heart_model.predict_proba(features)[0]

    confidence = max(probabilities)

    return {
        "prediction": "Heart Disease" if prediction == 1 else "No Heart Disease",

        "confidence": round(float(confidence), 2),

        "probabilities": {
            "No Heart Disease": round(float(probabilities[0]), 2),
            "Heart Disease": round(float(probabilities[1]), 2)
        }
    }
def predict_kidney(features):
    features = np.array(features).reshape(1, -1)

    prediction = kidney_model.predict(features)[0]

    probabilities = kidney_model.predict_proba(features)[0]

    confidence = max(probabilities)

    return {
        "prediction": "Kidney Disease" if prediction == 1 else "No Kidney Disease",

        "confidence": round(float(confidence), 2),

        "probabilities": {
            "No Kidney Disease": round(float(probabilities[0]), 2),
            "Kidney Disease": round(float(probabilities[1]), 2)
        }
    }




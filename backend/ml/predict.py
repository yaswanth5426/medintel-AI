import joblib
import numpy as np
diabetes_model = joblib.load("backend/ml/models/xgboost_diabetes_model.pkl")
heart_model = joblib.load("backend/ml/models/xgboost_heart_model.pkl")
kidney_model = joblib.load("backend/ml/models/xgboost_kidney_model.pkl")

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


from backend.ml.predict import predict_diabetes

sample = [
    6,
    148,
    72,
    35,
    0,
    33.6,
    0.627,
    50
]

print(predict_diabetes(sample))

import joblib
import numpy as np
diabetes_model = joblib.load("backend/ml/models/xgboost_diabetes_model.pkl")
heart_model = joblib.load("backend/ml/models/xgboost_heart_model.pkl")
kidney_model = joblib.load("backend/ml/models/xgboost_kidney_model.pkl")

def predict_diabetes(features):
    features = np.array(features).reshape(1, -1)

    prediction = diabetes_model.predict(features)[0]
    confidence = diabetes_model.predict_proba(features).max()

    return {
        "prediction": "Diabetes" if prediction else "No Diabetes",
        "confidence": round(float(confidence), 2)
    }

def predict_heart(features):
    features = np.array(features).reshape(1, -1)

    prediction = heart_model.predict(features)[0]
    confidence = heart_model.predict_proba(features).max()

    return {
        "prediction": "Heart Disease" if prediction else "No Heart Disease",
        "confidence": round(float(confidence), 2)
    }  
def predict_kidney(features):
    features = np.array(features).reshape(1, -1)

    prediction = kidney_model.predict(features)[0]
    confidence = kidney_model.predict_proba(features).max()

    return {
        "prediction": "Kidney Disease" if prediction else "No Kidney Disease",
        "confidence": round(float(confidence), 2)
    }   
print("Diabetes:", diabetes_model.n_features_in_)
print("Heart:", heart_model.n_features_in_)
print("Kidney:", kidney_model.n_features_in_)


import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
# pyrefly: ignore [missing-import]
from feature_engineering import load_dataset, prepare_features


def evaluate_model(model_path, dataset_path, target_column):
    # Load model
    model = joblib.load(model_path)

    # Load dataset
    df = load_dataset(dataset_path)

    X, y, scaler = prepare_features(
        df,
        target_column
)

    # Train-Test Split (same as training)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Predictions
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    return {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    }


# ================= Diabetes =================

diabetes_results = evaluate_model(
    "backend/ml/models/xgboost_diabetes_model.pkl",
    "datasets/processed_diabetes.csv",
    "Outcome"
)


# ================= Heart Disease =================

heart_results = evaluate_model(
    "backend/ml/models/xgboost_heart_model.pkl",
    "datasets/processed_heart.csv",
    "target"
)


# ================= Kidney Disease =================

kidney_results = evaluate_model(
    "backend/ml/models/xgboost_kidney_model.pkl",
    "datasets/processed_kidney.csv",
    "classification"
)


# ================= Save Results =================

output_file = "backend/ml/evaluation_results.txt"

with open(output_file, "w") as file:

    file.write("========== Diabetes ==========\n")

    for metric, value in diabetes_results.items():
        file.write(f"{metric}: {value * 100:.2f}%\n")

    file.write("\n")

    file.write("========== Heart Disease ==========\n")

    for metric, value in heart_results.items():
        file.write(f"{metric}: {value * 100:.2f}%\n")

    file.write("\n")

    file.write("========== Kidney Disease ==========\n")

    for metric, value in kidney_results.items():
        file.write(f"{metric}: {value * 100:.2f}%\n")


print("========================================")
print("Model Evaluation Completed Successfully")
print("========================================")
print(f"Results saved to: {output_file}")
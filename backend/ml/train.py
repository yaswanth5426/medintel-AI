# pyrefly: ignore [missing-import]
import joblib

from xgboost import XGBClassifier

# pyrefly: ignore [missing-import]
from feature_engineering import (
    load_dataset,
    prepare_features
)


MODEL_DIR = "backend/ml/models/"


def train_model(dataset_path, target_column, model_name):

    print(f"\nTraining {model_name}...")

    df = load_dataset(dataset_path)

    X, y, scaler = prepare_features(df, target_column)

    model = XGBClassifier(
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X, y)

    joblib.dump(
        model,
        MODEL_DIR + model_name
    )

    print(f"Saved: {MODEL_DIR}{model_name}")


if __name__ == "__main__":

    train_model(
        "datasets/processed_diabetes.csv",
        "Outcome",
        "diabetes_model.pkl"
    )

    train_model(
        "datasets/processed_heart.csv",
        "target",
        "heart_model.pkl"
    )

    train_model(
        "datasets/processed_kidney.csv",
        "classification",
        "ckd_model.pkl"
    )

    print("\n===================================")
    print("All models trained successfully.")
    print("===================================")
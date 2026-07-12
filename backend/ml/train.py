# pyrefly: ignore [missing-import]
import joblib
from xgboost import XGBClassifier

# pyrefly: ignore [missing-import]
from feature_engineering import (
    load_dataset,
    clean_data,
    encode_features,
    prepare_features
)

MODEL_DIR = "backend/ml/models/"
PREPROCESSOR_DIR = "backend/ml/models/preprocessors/"


def train_model(dataset_path, target_column, model_name, defaults_name, scaler_name):

    print(f"\nTraining {model_name}...")

    # -------------------------
    # Load dataset
    # -------------------------
    df = load_dataset(dataset_path)

    # -------------------------
    # Compute default values
    # -------------------------
    df_defaults = clean_data(df.copy())
    df_defaults = encode_features(df_defaults)

    defaults = df_defaults.drop(columns=[target_column]).median().to_dict()

    joblib.dump(
        defaults,
        PREPROCESSOR_DIR + defaults_name
    )

    print(f"Saved defaults: {PREPROCESSOR_DIR}{defaults_name}")

    # -------------------------
    # Prepare training data
    # -------------------------
    X, y, scaler = prepare_features(df, target_column)

    # -------------------------
    # Save scaler
    # -------------------------
    if scaler is not None:

        joblib.dump(
            scaler,
            PREPROCESSOR_DIR + scaler_name
        )

        print(f"Saved scaler: {PREPROCESSOR_DIR}{scaler_name}")

    # -------------------------
    # Train model
    # -------------------------
    model = XGBClassifier(
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X, y)

    # -------------------------
    # Save model
    # -------------------------
    joblib.dump(
        model,
        MODEL_DIR + model_name
    )

    print(f"Saved model: {MODEL_DIR}{model_name}")


if __name__ == "__main__":

    train_model(
     "datasets/clean_diabetes_dataset.csv",
    "Outcome",
    "diabetes_model_v2.pkl",
    "diabetes_defaults_v2.pkl",
    "diabetes_scaler_v2.pkl"
    )

    train_model(
        "datasets/clean_heart_dataset.csv",
    "Target",
    "heart_model_v2.pkl",
    "heart_defaults_v2.pkl",
    "heart_scaler_v2.pkl"
    )

    train_model(
        "datasets/clean_kidney_dataset.csv",
    "Target",
    "ckd_model_v2.pkl",
    "ckd_defaults_v2.pkl",
    "ckd_scaler_v2.pkl"
    )

    print("\n===================================")
    print("All models trained successfully.")
    print("===================================")
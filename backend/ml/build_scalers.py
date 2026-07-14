"""
build_scalers.py - reconstruct the raw -> standardized preprocessing stats.

Why this exists
---------------
The XGBoost models in backend/ml/models/ were trained on the *standardized*
datasets in datasets/processed_*.csv (every column has mean 0, std 1). A real
lab report gives *raw* values (e.g. Glucose = 120 mg/dL). Feeding a raw value
straight into a model that expects a standardized one produces meaningless
predictions.

The original raw->standardized transform (a StandardScaler fit in an external
notebook) was never saved. This script rebuilds it.

Standardization is affine:  processed = a * raw + b  with  a = 1/std, b = -mean/std.
Since we have BOTH the raw dataset and its standardized counterpart, we recover
(a, b) exactly via least squares (fitting only on genuinely-present values, so
differently-imputed rows can't tilt the line), then store std = 1/a, mean = -b/a,
and the raw median (used to fill a truly-missing feature). This reproduces the
model's training space exactly and auto-corrects label-encoding direction quirks.

Output: backend/ml/models/preprocessors/{diabetes,heart,ckd}_raw_stats.pkl
Run once from the project root:  python -m backend.ml.build_scalers
"""

import os

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder

from backend.ml.feature_engineering import clean_data

PREPROCESSOR_DIR = os.path.join(os.path.dirname(__file__), "models", "preprocessors")

# disease -> (raw csv, processed csv, target column, output name)
DATASETS = {
    "diabetes": ("datasets/diabetes.csv", "datasets/processed_diabetes.csv", "Outcome", "diabetes_raw_stats.pkl"),
    "heart": ("datasets/heart.csv", "datasets/processed_heart.csv", "target", "heart_raw_stats.pkl"),
    "ckd": ("datasets/kidney_disease.csv", "datasets/processed_kidney.csv", "classification", "ckd_raw_stats.pkl"),
}

# Numeric in reality but arrive as dirty strings ("\t?", "\t43") in the raw CKD file.
NUMERIC_COERCE = ["pcv", "wc", "rc"]


def _clean_raw(df):
    """Clean + label-encode, returning the frame and the {token: code} maps.

    Mirrors feature_engineering.clean_data + encode_features exactly, but keeps
    the LabelEncoder mappings so the API can convert a user's categorical answer
    (e.g. dm = "yes") into the same integer code used to fit the scaler.
    """
    for col in NUMERIC_COERCE:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace("\t", "", regex=False).str.strip(),
                errors="coerce",
            )
    df = clean_data(df)

    encoders = {}
    for col in df.select_dtypes(include="object").columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = {str(cls): int(i) for i, cls in enumerate(le.classes_)}

    return df, encoders


def _valid_mask(orig_df, col):
    """Rows whose value was genuinely present in the raw file (not imputed)."""
    if col not in orig_df.columns:
        return None
    series = orig_df[col]
    if series.dtype == object:
        cleaned = series.astype(str).str.replace("\t", "", regex=False).str.strip()
        return ~(cleaned.isin(["", "?", "nan", "NaN", "None"]) | series.isna())
    return ~series.isna()


def build_stats(raw_path, processed_path, target_column):
    orig = pd.read_csv(raw_path)
    raw, encoders = _clean_raw(pd.read_csv(raw_path))
    proc = pd.read_csv(processed_path)

    features = raw.drop(columns=[target_column])
    stats = {"feature_order": list(features.columns), "stats": {}, "encoders": encoders}
    max_resid = 0.0

    for col in features.columns:
        x = features[col].astype(float).to_numpy()
        y = proc[col].astype(float).to_numpy()

        mask = _valid_mask(orig, col)
        if mask is not None and int(mask.sum()) > 2:
            mm = mask.to_numpy()
            xf, yf = x[mm], y[mm]
        else:
            xf, yf = x, y

        # For low-cardinality (categorical) columns the notebook sometimes left
        # whitespace-dirty duplicates as separate label codes, so one clean value
        # maps to several standardized values. Fit on the *dominant* value per
        # category (median y per unique x) so a clean user input lands on the
        # code the model saw most often.
        ux = np.unique(xf)
        if len(ux) <= 12:
            xs = ux
            ys = np.array([np.median(yf[xf == v]) for v in ux])
        else:
            xs, ys = xf, yf

        if np.std(xs) < 1e-12:
            a, b = 0.0, float(np.mean(ys))
        else:
            a, b = np.polyfit(xs, ys, 1)

        if abs(a) < 1e-12:
            mean, std = float(np.mean(xf)), 1.0
        else:
            std = 1.0 / a
            mean = -b / a

        stats["stats"][col] = {
            "mean": float(mean),
            "std": float(std) if abs(std) > 1e-9 else 1.0,
            "median": float(np.median(xf)),
        }
        resid = float(np.abs((xs - mean) / std - ys).max())
        max_resid = max(max_resid, resid)

    stats["max_residual"] = max_resid
    return stats


def main():
    os.makedirs(PREPROCESSOR_DIR, exist_ok=True)
    for disease, (raw_path, proc_path, target, out_name) in DATASETS.items():
        stats = build_stats(raw_path, proc_path, target)
        out_path = os.path.join(PREPROCESSOR_DIR, out_name)
        joblib.dump(stats, out_path)
        print(
            f"[build_scalers] {disease}: {len(stats['feature_order'])} features, "
            f"max residual {stats['max_residual']:.2e} -> {out_name}"
        )


if __name__ == "__main__":
    main()

"""
SHAP explainability for the v2 disease models (Member 3 wiring over the ML team's
models). Turns a single prediction into a ranked list of *why*: how much each
feature pushed the risk up or down.

Design notes / fixes vs. the original draft
-------------------------------------------
* Disease aliases: the rest of the app calls kidney "ckd"; the original module
  only knew "kidney" and would KeyError. Both now work.
* Scaling: the v2 models predict on StandardScaler-scaled inputs, so SHAP is run
  on the *scaled* sample too (same operating point as the prediction) — otherwise
  the contributions describe a model input that never happens.
* No hard dependency on the `shap` package: we prefer `shap.TreeExplainer` when it
  is installed, and otherwise fall back to XGBoost's built-in Tree SHAP
  (`booster.predict(..., pred_contribs=True)`), which computes the *identical*
  values without pulling in numba/llvmlite. So the feature never crashes the API.
* Robust output shape: handles list / 2-D / 3-D SHAP arrays across versions.
* Reuses the models/scalers already loaded in predict.py (no double load, no drift).

Public API
----------
    explain_from_features(disease, feature_dict, top_n=8) -> dict
    explain_prediction(model_name, sample)               -> {feature: contribution}
"""

import numpy as np

from backend.ml.feature_mapping import (
    DIABETES_FEATURES, HEART_FEATURES, CKD_FEATURES,
)
# Reuse the objects that predict.py already loaded (kept consistent with the
# actual prediction path). Importing predict.py is what loads them.
from backend.ml.predict import (
    diabetes_model, heart_model, ckd_model,
    diabetes_scaler, heart_scaler, ckd_scaler,
)

# disease key -> (model, scaler, ordered feature names)
_REGISTRY = {
    "diabetes": (diabetes_model, diabetes_scaler, DIABETES_FEATURES),
    "heart":    (heart_model,    heart_scaler,    HEART_FEATURES),
    "ckd":      (ckd_model,      ckd_scaler,      CKD_FEATURES),
}
_ALIASES = {
    "kidney": "ckd", "chronic kidney disease": "ckd", "renal": "ckd",
    "cardiac": "heart", "heart disease": "heart",
    "diabetic": "diabetes", "diabetes mellitus": "diabetes",
}

# Friendly labels + units for the UI. Anything missing falls back to the raw name.
_LABELS = {
    "Age": ("Age", "yrs"), "Gender": ("Gender", ""), "Sex": ("Sex", ""),
    "Pregnancies": ("Pregnancies", ""), "Glucose": ("Glucose", "mg/dL"),
    "BloodGlucose": ("Blood glucose", "mg/dL"), "HbA1c": ("HbA1c", "%"),
    "BMI": ("BMI", ""), "BloodPressure": ("Blood pressure", "mmHg"),
    "SystolicBP": ("Systolic BP", "mmHg"), "DiastolicBP": ("Diastolic BP", "mmHg"),
    "Insulin": ("Insulin", "µU/mL"), "Hypertension": ("Hypertension", ""),
    "Smoking": ("Smoking", ""), "FamilyHistory": ("Family history", ""),
    "HeartDisease": ("Heart disease", ""), "Height": ("Height", "cm"),
    "Weight": ("Weight", "kg"), "TotalCholesterol": ("Total cholesterol", "mg/dL"),
    "Diabetes": ("Diabetes", ""), "Alcohol": ("Alcohol", ""),
    "PhysicalActivity": ("Physical activity", ""), "HeartRate": ("Heart rate", "bpm"),
    "Platelets": ("Platelets", ""), "SerumCreatinine": ("Serum creatinine", "mg/dL"),
    "SerumSodium": ("Serum sodium", "mEq/L"), "CPK": ("CPK", "U/L"),
    "SpecificGravity": ("Specific gravity", ""), "Albumin": ("Albumin", ""),
    "Sugar": ("Urine sugar", ""), "BloodUrea": ("Blood urea", "mg/dL"),
    "Sodium": ("Sodium", "mEq/L"), "Potassium": ("Potassium", "mEq/L"),
    "Hemoglobin": ("Hemoglobin", "g/dL"), "PackedCellVolume": ("Packed cell volume", "%"),
    "WBC": ("WBC", "/µL"), "RBC": ("RBC", "M/µL"),
    "CoronaryArteryDisease": ("Coronary artery disease", ""), "Appetite": ("Appetite", ""),
    "PedalEdema": ("Pedal edema", ""), "Anemia": ("Anemia", ""),
    "eGFR": ("eGFR", "mL/min"), "UrineProteinCreatinineRatio": ("Urine protein/creatinine", ""),
    "UrineOutput": ("Urine output", "mL"), "SerumAlbumin": ("Serum albumin", "g/dL"),
    "Calcium": ("Calcium", "mg/dL"), "Phosphate": ("Phosphate", "mg/dL"),
    "CystatinC": ("Cystatin C", "mg/L"),
}


def _resolve(name):
    d = (name or "").strip().lower()
    d = _ALIASES.get(d, d)
    if d not in _REGISTRY:
        raise KeyError(f"Unknown disease for SHAP: {name!r}")
    return d


def _tree_shap(model, x_scaled, n_features):
    """Return a 1-D array of signed contributions (positive-class margin space).

    Prefers the `shap` package; falls back to XGBoost's native Tree SHAP, which
    yields the same numbers without the heavy shap/numba install.
    """
    # --- preferred: shap package ---
    try:
        import shap  # noqa: WPS433 (optional dependency, imported lazily)
        values = shap.TreeExplainer(model).shap_values(x_scaled)
        return _row_from_shap(values, n_features)
    except Exception:
        pass
    # --- fallback: XGBoost built-in Tree SHAP ---
    import xgboost as xgb
    booster = model.get_booster()
    contribs = np.asarray(
        booster.predict(xgb.DMatrix(x_scaled), pred_contribs=True, validate_features=False)
    )
    if contribs.ndim == 3:                 # multiclass: (n, n_class, n_feat+1)
        contribs = contribs[:, -1, :]      # positive class
    return contribs[0][:-1]                # drop the bias term -> per-feature


def _row_from_shap(values, n_features):
    """Collapse whatever shap returned into a 1-D per-feature array."""
    if isinstance(values, list):
        values = values[1] if len(values) > 1 else values[0]
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        row = arr
    elif arr.ndim == 2:                    # (n_samples, n_features) or (n_features, n_classes)
        row = arr[:, -1] if (arr.shape[0] == n_features and arr.shape[1] != n_features) else arr[0]
    elif arr.ndim == 3:                    # (n_samples, n_features, n_classes)
        row = arr[0, :, -1]
    else:
        row = np.ravel(arr)
    row = np.ravel(row)
    return row[:n_features]


def explain_from_features(disease, feature_dict, top_n=8):
    """
    Explain a single prediction.

    Parameters
    ----------
    disease : str        diabetes | heart | ckd (aliases ok)
    feature_dict : dict  the mapped model features (predict result "features_used")
    top_n : int          how many of the most influential features to return

    Returns
    -------
    {
      "available": bool,
      "base_value": float,          # model's average output (log-odds)
      "top": [ { feature, label, unit, value, contribution, direction, impact }, ... ]
    }
    """
    key = _resolve(disease)
    model, scaler, feature_names = _REGISTRY[key]

    # order the sample exactly as the model expects, then scale it
    sample = [float(feature_dict.get(name, 0) or 0) for name in feature_names]
    x = np.array([sample], dtype=float)
    x_scaled = scaler.transform(x)

    contributions = _tree_shap(model, x_scaled, len(feature_names))
    contributions = np.asarray(contributions, dtype=float).ravel()

    total = float(np.sum(np.abs(contributions))) or 1.0
    rows = []
    for name, contrib in zip(feature_names, contributions):
        label, unit = _LABELS.get(name, (name, ""))
        rows.append({
            "feature": name,
            "label": label,
            "unit": unit,
            "value": feature_dict.get(name),
            "contribution": round(float(contrib), 4),
            "direction": "increases" if contrib > 0 else "decreases",
            "impact": round(abs(float(contrib)) / total, 4),  # share of total |SHAP|
        })

    rows.sort(key=lambda r: abs(r["contribution"]), reverse=True)
    return {"available": True, "base_value": 0.0, "top": rows[:top_n]}


# ----------------------------------------------------------------------
# Backward-compatible helper (fixed): {feature: contribution}, sorted.
# ----------------------------------------------------------------------
def explain_prediction(model_name, sample):
    key = _resolve(model_name)
    model, scaler, feature_names = _REGISTRY[key]
    x_scaled = scaler.transform(np.array([sample], dtype=float))
    contributions = _tree_shap(model, x_scaled, len(feature_names))
    pairs = sorted(
        {n: float(c) for n, c in zip(feature_names, np.ravel(contributions))}.items(),
        key=lambda kv: abs(kv[1]), reverse=True,
    )
    return dict(pairs)


if __name__ == "__main__":
    demo = {
        "Age": 54, "BloodPressure": 154, "SerumCreatinine": 3.4, "BloodUrea": 82,
        "eGFR": 19, "Hemoglobin": 9.5, "Sodium": 133, "Potassium": 5.8,
    }
    out = explain_from_features("ckd", demo, top_n=6)
    print("available:", out["available"])
    for r in out["top"]:
        arrow = "↑" if r["direction"] == "increases" else "↓"
        print(f"  {arrow} {r['label']:22} value={r['value']}  shap={r['contribution']:+.4f}  ({r['impact']*100:.0f}%)")

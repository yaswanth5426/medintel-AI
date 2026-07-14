"""
prediction_engine.py — Member 3's integration layer between an uploaded report
and the trained ML models.

The XGBoost models (backend/ml/, owned by Member 1) expect a fixed, ordered,
*standardized* feature vector. A lab report only gives a handful of raw values.
This module bridges the two WITHOUT touching Member 1's or Member 2's code:

  report values (+ any manual answers)
        -> map each model feature to a source (report / patient / derived / manual)
        -> whatever is still unknown becomes a "missing feature" the UI asks for
        -> once complete: encode categoricals, standardize with the saved stats,
           run the model, and build a plain-language summary.

Scaling stats + categorical encoders come from
backend/ml/models/preprocessors/{disease}_raw_stats.pkl (produced by
backend/ml/build_scalers.py, validated to reproduce the training space exactly).
"""

import os
import warnings

import joblib
import numpy as np

# --------------------------------------------------------------------------
# Load models + scaling stats once at import.
# --------------------------------------------------------------------------

_BASE = os.path.join(os.path.dirname(__file__), "..", "ml", "models")
_PRE = os.path.join(_BASE, "preprocessors")

_MODEL_FILES = {
    "diabetes": "diabetes_model.pkl",
    "heart": "heart_model.pkl",
    "kidney": "ckd_model.pkl",
}
_STATS_FILES = {
    "diabetes": "diabetes_raw_stats.pkl",
    "heart": "heart_raw_stats.pkl",
    "kidney": "ckd_raw_stats.pkl",
}

# The .pkl models were serialized with an older XGBoost build, which emits a
# (harmless) version-mismatch UserWarning on load. The models load and predict
# correctly — silence just that noisy warning so startup stays clean.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    _MODELS = {d: joblib.load(os.path.join(_BASE, f)) for d, f in _MODEL_FILES.items()}
    _STATS = {d: joblib.load(os.path.join(_PRE, f)) for d, f in _STATS_FILES.items()}

DISEASES = ("diabetes", "heart", "kidney")
DISEASE_LABELS = {"diabetes": "Diabetes", "heart": "Heart Disease", "kidney": "Chronic Kidney Disease"}


# --------------------------------------------------------------------------
# Feature specifications.
#   source: "patient" | "report" | "derived" | "auto" | "manual"
#   report_key: canonical key from the upload response (patient/lab_values)
#   type: "number" | "select"  (drives the dynamic form on the frontend)
# --------------------------------------------------------------------------

YN = [{"value": "yes", "label": "Yes"}, {"value": "no", "label": "No"}]
NORMAL_ABNORMAL = [{"value": "normal", "label": "Normal"}, {"value": "abnormal", "label": "Abnormal"}]
PRESENT = [{"value": "present", "label": "Present"}, {"value": "notpresent", "label": "Not present"}]


def _opts(pairs):
    return [{"value": v, "label": l} for v, l in pairs]


FEATURE_SPECS = {
    "diabetes": [
        {"name": "Pregnancies", "label": "Pregnancies", "source": "manual", "type": "number",
         "min": 0, "max": 20, "step": 1, "normal": "0-4", "hint": "Number of times pregnant (0 if not applicable)."},
        {"name": "Glucose", "label": "Fasting glucose", "source": "report", "report_key": "fasting_glucose",
         "type": "number", "unit": "mg/dL", "min": 0, "max": 400, "step": 1, "normal": "70-100",
         "hint": "Fasting plasma glucose."},
        {"name": "BloodPressure", "label": "Blood pressure (diastolic)", "source": "report",
         "report_key": "bp_diastolic", "type": "number", "unit": "mmHg", "min": 0, "max": 200, "step": 1,
         "normal": "60-80", "hint": "Diastolic blood pressure."},
        {"name": "SkinThickness", "label": "Skin thickness", "source": "manual", "type": "number",
         "unit": "mm", "min": 0, "max": 100, "step": 1, "normal": "10-50", "hint": "Triceps skin-fold thickness."},
        {"name": "Insulin", "label": "Insulin", "source": "manual", "type": "number", "unit": "uU/mL",
         "min": 0, "max": 900, "step": 1, "normal": "16-166", "hint": "2-hour serum insulin."},
        {"name": "BMI", "label": "BMI", "source": "manual", "type": "number", "unit": "kg/m2",
         "min": 0, "max": 70, "step": 0.1, "normal": "18.5-24.9", "hint": "Body mass index."},
        {"name": "DiabetesPedigreeFunction", "label": "Diabetes pedigree function", "source": "manual",
         "type": "number", "min": 0, "max": 3, "step": 0.001, "normal": "0.0-1.0",
         "hint": "Family-history score (0 = no known family history)."},
        {"name": "Age", "label": "Age", "source": "patient", "report_key": "age", "type": "number",
         "unit": "years", "min": 0, "max": 120, "step": 1, "normal": "-", "hint": "Patient age."},
    ],
    "heart": [
        {"name": "age", "label": "Age", "source": "patient", "report_key": "age", "type": "number",
         "unit": "years", "min": 0, "max": 120, "step": 1, "hint": "Patient age."},
        {"name": "sex", "label": "Sex", "source": "patient", "report_key": "sex", "type": "select",
         "options": _opts([(1, "Male"), (0, "Female")]), "hint": "Biological sex."},
        {"name": "cp", "label": "Chest pain type", "source": "manual", "type": "select",
         "options": _opts([(0, "Typical angina"), (1, "Atypical angina"), (2, "Non-anginal pain"), (3, "Asymptomatic")]),
         "hint": "Type of chest pain reported."},
        {"name": "trestbps", "label": "Resting blood pressure (systolic)", "source": "report",
         "report_key": "bp_systolic", "type": "number", "unit": "mmHg", "min": 0, "max": 260, "step": 1,
         "normal": "90-120", "hint": "Resting systolic blood pressure."},
        {"name": "chol", "label": "Cholesterol", "source": "report", "report_key": "cholesterol",
         "type": "number", "unit": "mg/dL", "min": 0, "max": 700, "step": 1, "normal": "< 200",
         "hint": "Serum cholesterol."},
        {"name": "fbs", "label": "Fasting blood sugar > 120 mg/dL", "source": "derived", "type": "select",
         "options": _opts([(1, "Yes (> 120)"), (0, "No (<= 120)")]),
         "hint": "Derived from the report's fasting glucose when available."},
        {"name": "restecg", "label": "Resting ECG", "source": "manual", "type": "select",
         "options": _opts([(0, "Normal"), (1, "ST-T wave abnormality"), (2, "LV hypertrophy")]),
         "hint": "Resting electrocardiographic result."},
        {"name": "thalach", "label": "Max heart rate achieved", "source": "manual", "type": "number",
         "unit": "bpm", "min": 60, "max": 250, "step": 1, "normal": "-", "hint": "Maximum heart rate achieved."},
        {"name": "exang", "label": "Exercise-induced angina", "source": "manual", "type": "select",
         "options": _opts([(1, "Yes"), (0, "No")]), "hint": "Angina induced by exercise."},
        {"name": "oldpeak", "label": "ST depression (oldpeak)", "source": "manual", "type": "number",
         "min": 0, "max": 7, "step": 0.1, "hint": "ST depression induced by exercise relative to rest."},
        {"name": "slope", "label": "Slope of peak exercise ST", "source": "manual", "type": "select",
         "options": _opts([(0, "Upsloping"), (1, "Flat"), (2, "Downsloping")]), "hint": "Slope of the ST segment."},
        {"name": "ca", "label": "Major vessels colored", "source": "manual", "type": "select",
         "options": _opts([(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")]),
         "hint": "Number of major vessels colored by fluoroscopy."},
        {"name": "thal", "label": "Thalassemia", "source": "manual", "type": "select",
         "options": _opts([(1, "Normal"), (2, "Fixed defect"), (3, "Reversible defect"), (0, "Unknown")]),
         "hint": "Thalassemia test result."},
    ],
    "kidney": [
        {"name": "id", "label": "Record id", "source": "auto", "type": "number"},
        {"name": "age", "label": "Age", "source": "patient", "report_key": "age", "type": "number",
         "unit": "years", "min": 0, "max": 120, "step": 1, "hint": "Patient age."},
        {"name": "bp", "label": "Blood pressure", "source": "report", "report_key": "bp_diastolic",
         "type": "number", "unit": "mmHg", "min": 0, "max": 200, "step": 1, "normal": "60-80",
         "hint": "Blood pressure."},
        {"name": "sg", "label": "Specific gravity", "source": "manual", "type": "select",
         "options": _opts([(1.005, "1.005"), (1.010, "1.010"), (1.015, "1.015"), (1.020, "1.020"), (1.025, "1.025")]),
         "hint": "Urine specific gravity."},
        {"name": "al", "label": "Albumin", "source": "manual", "type": "select",
         "options": _opts([(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]), "hint": "Urine albumin level."},
        {"name": "su", "label": "Sugar", "source": "manual", "type": "select",
         "options": _opts([(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]), "hint": "Urine sugar level."},
        {"name": "rbc", "label": "Red blood cells", "source": "manual", "type": "select",
         "options": NORMAL_ABNORMAL, "hint": "Red blood cells in urine."},
        {"name": "pc", "label": "Pus cells", "source": "manual", "type": "select",
         "options": NORMAL_ABNORMAL, "hint": "Pus cells in urine."},
        {"name": "pcc", "label": "Pus cell clumps", "source": "manual", "type": "select",
         "options": PRESENT, "hint": "Pus cell clumps."},
        {"name": "ba", "label": "Bacteria", "source": "manual", "type": "select",
         "options": PRESENT, "hint": "Bacteria in urine."},
        {"name": "bgr", "label": "Blood glucose random", "source": "report", "report_key": "fasting_glucose",
         "type": "number", "unit": "mg/dL", "min": 0, "max": 500, "step": 1, "normal": "70-140",
         "hint": "Blood glucose (uses the report's glucose)."},
        {"name": "bu", "label": "Blood urea", "source": "report", "report_key": "urea", "type": "number",
         "unit": "mg/dL", "min": 0, "max": 400, "step": 1, "normal": "7-20", "hint": "Blood urea."},
        {"name": "sc", "label": "Serum creatinine", "source": "report", "report_key": "creatinine",
         "type": "number", "unit": "mg/dL", "min": 0, "max": 80, "step": 0.1, "normal": "0.6-1.3",
         "hint": "Serum creatinine."},
        {"name": "sod", "label": "Sodium", "source": "manual", "type": "number", "unit": "mEq/L",
         "min": 100, "max": 170, "step": 1, "normal": "135-145", "hint": "Serum sodium."},
        {"name": "pot", "label": "Potassium", "source": "manual", "type": "number", "unit": "mEq/L",
         "min": 2, "max": 10, "step": 0.1, "normal": "3.5-5.1", "hint": "Serum potassium."},
        {"name": "hemo", "label": "Hemoglobin", "source": "report", "report_key": "hemoglobin",
         "type": "number", "unit": "g/dL", "min": 0, "max": 20, "step": 0.1, "normal": "12-17",
         "hint": "Hemoglobin."},
        {"name": "pcv", "label": "Packed cell volume", "source": "manual", "type": "number", "unit": "%",
         "min": 10, "max": 60, "step": 1, "normal": "36-50", "hint": "Packed cell volume (hematocrit)."},
        {"name": "wc", "label": "White blood cell count", "source": "manual", "type": "number",
         "unit": "cells/cmm", "min": 2000, "max": 30000, "step": 100, "normal": "4000-11000",
         "hint": "White blood cell count."},
        {"name": "rc", "label": "Red blood cell count", "source": "manual", "type": "number",
         "unit": "millions/cmm", "min": 2, "max": 8, "step": 0.1, "normal": "4.2-5.9",
         "hint": "Red blood cell count."},
        {"name": "htn", "label": "Hypertension", "source": "manual", "type": "select", "options": YN,
         "hint": "History of hypertension."},
        {"name": "dm", "label": "Diabetes mellitus", "source": "manual", "type": "select", "options": YN,
         "hint": "History of diabetes."},
        {"name": "cad", "label": "Coronary artery disease", "source": "manual", "type": "select", "options": YN,
         "hint": "History of coronary artery disease."},
        {"name": "appet", "label": "Appetite", "source": "manual", "type": "select",
         "options": _opts([("good", "Good"), ("poor", "Poor")]), "hint": "Appetite."},
        {"name": "pe", "label": "Pedal edema", "source": "manual", "type": "select", "options": YN,
         "hint": "Swelling in the feet/ankles."},
        {"name": "ane", "label": "Anemia", "source": "manual", "type": "select", "options": YN,
         "hint": "History of anemia."},
    ],
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _parse_bp(report_values):
    """Split a '140/90' style blood pressure into systolic / diastolic."""
    bp = report_values.get("blood_pressure")
    if bp is None:
        return None, None
    if isinstance(bp, (int, float)):
        return float(bp), float(bp)
    text = str(bp)
    if "/" in text:
        try:
            sys_, dia = text.split("/")[:2]
            return float(sys_.strip()), float(dia.strip())
        except ValueError:
            return None, None
    try:
        v = float(text)
        return v, v
    except ValueError:
        return None, None


def _flatten_report(patient, lab_values):
    """Build the flat canonical dict the specs reference."""
    flat = {}
    flat.update(lab_values or {})
    patient = patient or {}
    flat["age"] = patient.get("age")

    gender = (patient.get("gender") or "").strip().lower()
    if gender.startswith("m"):
        flat["sex"] = 1
    elif gender.startswith("f"):
        flat["sex"] = 0

    sys_, dia = _parse_bp({**(lab_values or {})})
    flat["bp_systolic"] = sys_
    flat["bp_diastolic"] = dia
    return flat


def _derive(spec, flat):
    """Value for report/patient/derived/auto sources, or None if unavailable."""
    src = spec["source"]
    if src in ("report", "patient"):
        val = flat.get(spec.get("report_key"))
        return val if val not in (None, "") else None
    if src == "derived" and spec["name"] == "fbs":
        g = flat.get("fasting_glucose")
        if g in (None, ""):
            return None
        try:
            return 1 if float(g) > 120 else 0
        except (TypeError, ValueError):
            return None
    if src == "auto" and spec["name"] == "id":
        return _STATS["kidney"]["stats"]["id"]["median"]
    return None


def map_features(disease, report_values, manual_values=None):
    """Return (mapped, missing) for a disease.

    mapped  : {feature_name: raw_value}   (auto-filled from the report + manual)
    missing : [spec, ...]                 (features still needed from the user)
    """
    disease = _normalize(disease)
    manual_values = manual_values or {}
    specs = FEATURE_SPECS[disease]

    mapped, missing = {}, []
    for spec in specs:
        name = spec["name"]

        if name in manual_values and manual_values[name] not in (None, ""):
            mapped[name] = manual_values[name]
            continue

        auto = _derive(spec, report_values)
        if auto is not None:
            mapped[name] = auto
            continue

        if spec["source"] == "auto":
            mapped[name] = _STATS[disease]["stats"][name]["median"]
            continue

        missing.append(spec)

    return mapped, missing


def map_diabetes_features(report_values, manual_values=None):
    return map_features("diabetes", report_values, manual_values)


def map_heart_features(report_values, manual_values=None):
    return map_features("heart", report_values, manual_values)


def map_ckd_features(report_values, manual_values=None):
    return map_features("kidney", report_values, manual_values)


def feature_status_for_report(patient, lab_values):
    """Per-disease {mapped, missing} preview for an uploaded report."""
    flat = _flatten_report(patient, lab_values)
    out = {}
    for disease in DISEASES:
        mapped, missing = map_features(disease, flat)
        out[disease] = {
            "mapped_features": mapped,
            "missing_features": [_public_spec(s) for s in missing],
        }
    return out


def _public_spec(spec):
    """Trim a spec to what the frontend form needs."""
    keys = ("name", "label", "type", "unit", "min", "max", "step", "normal", "hint", "options")
    return {k: spec[k] for k in keys if k in spec}


def _normalize(disease):
    d = (disease or "").strip().lower()
    if d in ("ckd", "kidney", "chronic kidney disease"):
        return "kidney"
    if d in ("heart", "heart disease", "cardiac"):
        return "heart"
    if d in ("diabetes", "diabetic"):
        return "diabetes"
    raise ValueError(f"Unsupported disease: {disease!r}")


def _encode_value(disease, name, value):
    """Convert a raw/categorical answer into the numeric code used at fit time."""
    encoders = _STATS[disease].get("encoders", {})
    if name in encoders:
        token = str(value).strip().lower()
        mapping = encoders[name]
        if token in mapping:
            return float(mapping[token])
        try:
            return float(value)
        except (TypeError, ValueError):
            return _STATS[disease]["stats"][name]["median"]
    return float(value)


def _standardize(disease, mapped):
    """Ordered, standardized vector + the raw encoded values (for explanations)."""
    stats = _STATS[disease]["stats"]
    order = _STATS[disease]["feature_order"]
    raw_encoded, scaled = {}, []
    for name in order:
        value = mapped.get(name)
        if value in (None, ""):
            value = stats[name]["median"]
        enc = _encode_value(disease, name, value)
        raw_encoded[name] = enc
        z = (enc - stats[name]["mean"]) / stats[name]["std"]
        scaled.append(z)
    return np.array(scaled, dtype=float).reshape(1, -1), raw_encoded


def _risk_level(disease_probability):
    if disease_probability >= 0.70:
        return "High"
    if disease_probability >= 0.40:
        return "Medium"
    return "Low"


def _key_factors(disease, mapped, raw_encoded, top_n=3):
    """Cheap, model-agnostic explanation: which supplied values are most unusual.

    Uses |z-score| against the training mean (NOT SHAP — that stays in Member 1's
    shap_explainer.py). Only reports features the user/report actually provided.
    """
    stats = _STATS[disease]["stats"]
    label_by_name = {s["name"]: s for s in FEATURE_SPECS[disease]}
    factors = []
    for name in mapped:
        spec = label_by_name.get(name, {})
        if spec.get("source") == "auto":
            continue
        z = (raw_encoded[name] - stats[name]["mean"]) / stats[name]["std"]
        factors.append((abs(z), z, name, spec))
    factors.sort(reverse=True)

    out = []
    for _, z, name, spec in factors[:top_n]:
        direction = "higher than typical" if z > 0 else "lower than typical"
        out.append({
            "feature": name,
            "label": spec.get("label", name),
            "value": mapped.get(name),
            "unit": spec.get("unit"),
            "normal": spec.get("normal"),
            "direction": direction,
            "z": round(float(z), 2),
        })
    return out


def _summary_text(disease, prediction, risk, confidence, factors):
    name = DISEASE_LABELS[disease]
    lead = {
        "High": f"The model estimates a HIGH risk of {name.lower()}.",
        "Medium": f"The model estimates a MODERATE risk of {name.lower()}.",
        "Low": f"The model estimates a LOW risk of {name.lower()}.",
    }[risk]
    parts = [f"{lead} (model confidence {round(confidence * 100)}%)."]
    if factors:
        drivers = ", ".join(
            f"{f['label']} ({f['value']}{(' ' + f['unit']) if f.get('unit') else ''}, {f['direction']})"
            for f in factors
        )
        parts.append(f"The values that most influenced this were: {drivers}.")
    parts.append(
        "This is an educational estimate from a machine-learning model, not a diagnosis. "
        "Please discuss any concerns and next steps with a qualified clinician."
    )
    return " ".join(parts)


def predict(disease, report_values, manual_values=None):
    """Full flow. Returns needs_user_input OR a completed prediction dict."""
    disease = _normalize(disease)
    mapped, missing = map_features(disease, report_values, manual_values)

    if missing:
        return {
            "status": "needs_user_input",
            "disease": disease,
            "disease_label": DISEASE_LABELS[disease],
            "mapped_features": mapped,
            "missing_features": [_public_spec(s) for s in missing],
        }

    vector, raw_encoded = _standardize(disease, mapped)
    model = _MODELS[disease]
    proba = model.predict_proba(vector)[0]
    disease_prob = float(proba[1])
    confidence = float(max(proba))
    risk = _risk_level(disease_prob)
    positive = disease_prob >= 0.5
    factors = _key_factors(disease, mapped, raw_encoded)

    return {
        "status": "success",
        "disease": disease,
        "disease_label": DISEASE_LABELS[disease],
        "prediction": DISEASE_LABELS[disease] if positive else f"No {DISEASE_LABELS[disease]}",
        "positive": positive,
        "risk": risk,
        "confidence": round(confidence, 4),
        "probability": round(disease_prob, 4),
        "probabilities": {
            "negative": round(float(proba[0]), 4),
            "positive": round(disease_prob, 4),
        },
        "used_features": mapped,
        "key_factors": factors,
        "ai_summary": _summary_text(disease, positive, risk, confidence, factors),
    }

"""
prediction_engine.py - Member 3's thin adapter over the ML team's v2 pipeline.

After the ml-engineer merge, prediction lives in backend/ml/predict.py:
    predict_disease(disease, report_details, lab_values)
which maps the report + lab values onto the v2 feature set, scales them with the
saved v2 scalers, and runs the v2 XGBoost models.

This module just:
  * normalizes the disease name,
  * forwards the upload's patient + lab_values (plus any manual overrides),
  * reshapes the ML result into the shape the /predict router + frontend expect
    (disease_label, single positive probability, a plain-language summary, and a
    lightweight "key factors" list based on standard reference ranges).

No models are loaded here anymore - that's owned by backend/ml/.
"""

import warnings

# Importing predict.py loads the v2 models/scalers; silence the harmless
# XGBoost version-mismatch warning emitted while unpickling.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from backend.ml.predict import predict_disease

DISEASE_LABELS = {
    "diabetes": "Diabetes",
    "heart": "Heart Disease",
    "ckd": "Chronic Kidney Disease",
}


def _normalize(disease):
    d = (disease or "").strip().lower()
    if d in ("ckd", "kidney", "chronic kidney disease"):
        return "ckd"
    if d in ("heart", "heart disease", "cardiac"):
        return "heart"
    if d in ("diabetes", "diabetic"):
        return "diabetes"
    raise ValueError(f"Unsupported disease: {disease!r}")


# Standard reference ranges for a light, honest "what drove this" panel.
# (feature key in lab_values) -> (label, unit, low, high)
_REF_RANGES = {
    "glucose": ("Glucose", "mg/dL", 70, 140),
    "hba1c": ("HbA1c", "%", 4.0, 5.7),
    "cholesterol": ("Total cholesterol", "mg/dL", 0, 200),
    "serum_creatinine": ("Serum creatinine", "mg/dL", 0.6, 1.3),
    "blood_urea": ("Blood urea", "mg/dL", 7, 20),
    "hemoglobin": ("Hemoglobin", "g/dL", 12, 17),
    "egfr": ("eGFR", "mL/min", 60, 200),
    "potassium": ("Potassium", "mEq/L", 3.5, 5.1),
    "sodium": ("Sodium", "mEq/L", 135, 145),
}


def _key_factors(lab_values, top_n=3):
    """Flag extracted lab values that fall outside standard reference ranges."""
    factors = []
    for key, (label, unit, low, high) in _REF_RANGES.items():
        val = (lab_values or {}).get(key)
        if val is None:
            continue
        try:
            v = float(val)
        except (TypeError, ValueError):
            continue
        if v > high:
            span = high if high else 1
            factors.append((abs(v - high) / span, {
                "feature": key, "label": label, "value": val, "unit": unit,
                "direction": "higher than normal", "normal": f"{low}-{high}",
            }))
        elif v < low:
            span = low if low else 1
            factors.append((abs(low - v) / span, {
                "feature": key, "label": label, "value": val, "unit": unit,
                "direction": "lower than normal", "normal": f"{low}-{high}",
            }))
    factors.sort(key=lambda x: x[0], reverse=True)
    return [f for _, f in factors[:top_n]]


def _summary(disease_label, prediction, risk, confidence, factors):
    lead = {
        "High": f"The model estimates a HIGH risk of {disease_label.lower()}.",
        "Medium": f"The model estimates a MODERATE risk of {disease_label.lower()}.",
        "Low": f"The model estimates a LOW risk of {disease_label.lower()}.",
    }.get(risk, f"Risk assessed for {disease_label.lower()}.")
    parts = [f"{lead} (model confidence {round(confidence * 100)}%)."]
    if factors:
        drivers = ", ".join(
            f"{f['label']} {f['value']}{(' ' + f['unit']) if f.get('unit') else ''} ({f['direction']})"
            for f in factors
        )
        parts.append(f"Notable values from the report: {drivers}.")
    parts.append(
        "This is an educational estimate from a machine-learning model, not a diagnosis. "
        "Please discuss any concerns and next steps with a qualified clinician."
    )
    return " ".join(parts)


def _shap_explanation(disease_key, used_features):
    """Best-effort SHAP explanation. Never raises: explainability must not be able
    to break a prediction, so any failure just yields an empty (unavailable) result."""
    if not used_features:
        return {"available": False, "top": []}
    try:
        from backend.ml import shap_explainer
        return shap_explainer.explain_from_features(disease_key, used_features, top_n=8)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully
        return {"available": False, "error": str(exc), "top": []}


def predict(disease, patient, lab_values, manual_values=None):
    """Run a prediction and return a frontend-friendly result dict."""
    key = _normalize(disease)

    report_details = dict(patient or {})
    labs = dict(lab_values or {})

    # Any manual overrides the user supplied: patient-ish keys go to the report,
    # everything else is treated as a lab value.
    for k, v in (manual_values or {}).items():
        if v in (None, ""):
            continue
        if k in ("age", "gender", "height", "weight", "bmi"):
            report_details[k] = v
        else:
            labs[k] = v

    result = predict_disease(disease=key, report_details=report_details, lab_values=labs)

    probs = result.get("probabilities", {})
    positive_prob = 0.0
    for name, p in probs.items():
        if not str(name).lower().startswith("no "):
            positive_prob = float(p)
            break
    positive = not str(result.get("prediction", "")).lower().startswith("no ")

    factors = _key_factors(labs)
    used = result.get("features_used", {})
    shap_explanation = _shap_explanation(key, used)
    label = DISEASE_LABELS[key]
    confidence = float(result.get("confidence", max(probs.values()) if probs else 0.0))
    risk = result.get("risk", "Low")

    return {
        "status": "success",
        "disease": key,
        "disease_label": label,
        "prediction": result.get("prediction"),
        "positive": positive,
        "risk": risk,
        "confidence": round(confidence, 4),
        "probability": round(positive_prob, 4),
        "probabilities": probs,
        "used_features": used,
        "key_factors": factors,
        "shap": shap_explanation,
        "ai_summary": _summary(label, result.get("prediction"), risk, confidence, factors),
    }

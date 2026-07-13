"""
POST /predict — disease risk prediction (Member 3 / routers).

This is the thin HTTP layer over prediction_engine.py. It accepts the values
extracted from a report (patient + lab_values, exactly as upload.py returns
them) plus any manual answers the user gave for missing fields, and returns
either:

  * status = "needs_user_input"  + the list of missing feature specs, or
  * status = "success"           + prediction, confidence, risk, key factors
                                   and a plain-language AI summary.

Successful predictions are saved to the history store so they show on the
Dashboard. The ML models and feature mapping stay entirely inside
prediction_engine.py / backend/ml — this file only orchestrates.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.routers import prediction_engine as engine
from backend.database import history_store

router = APIRouter(tags=["prediction"])


class PredictRequest(BaseModel):
    disease: str  # "diabetes" | "heart" | "kidney" (aliases accepted)
    patient: Dict[str, Any] = {}
    lab_values: Dict[str, Any] = {}
    manual_values: Dict[str, Any] = {}
    # Optional pre-flattened values; if given, merged over patient+lab_values.
    report_values: Optional[Dict[str, Any]] = None
    source: str = "Lab report"  # for the history row ("Lab report" | "Symptoms")


@router.post("/predict")
def predict_disease(request: PredictRequest):
    try:
        flat = engine._flatten_report(request.patient, request.lab_values)
        if request.report_values:
            flat.update(request.report_values)

        result = engine.predict(request.disease, flat, request.manual_values)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Only completed predictions are recorded.
    if result.get("status") == "success":
        record = {
            "date": datetime.now(timezone.utc).strftime("%b %d"),
            "source": request.source,
            "disease": result["disease_label"],
            "risk_level": result["risk"],
            "confidence": result["confidence"],
            "probability": result["probability"],
            "patient_name": (request.patient or {}).get("patient_name"),
        }
        try:
            saved = history_store.save_prediction(record)
            result["history_id"] = saved["id"]
        except Exception as exc:  # noqa: BLE001 — persistence must never break a prediction
            result["history_warning"] = f"Prediction succeeded but was not saved: {exc}"

    return result


@router.get("/predict/features/{disease}")
def get_feature_specs(disease: str):
    """Full feature spec for a disease — lets the frontend render a blank form."""
    try:
        key = engine._normalize(disease)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {
        "disease": key,
        "disease_label": engine.DISEASE_LABELS[key],
        "features": [engine._public_spec(s) for s in engine.FEATURE_SPECS[key]],
    }

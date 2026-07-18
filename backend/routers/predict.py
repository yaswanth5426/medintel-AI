"""
POST /predict - disease risk prediction (Member 3 / routers).

Thin HTTP layer over prediction_engine.predict(), which forwards the uploaded
report's patient + lab_values (plus any manual overrides) to the ML team's v2
pipeline (backend/ml/predict.py) and reshapes the result for the frontend.

Successful predictions are saved to the history store for the Dashboard.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.routers import prediction_engine as engine
from backend.database import history_store

router = APIRouter(tags=["prediction"])


class PredictRequest(BaseModel):
    disease: str  # "diabetes" | "heart" | "ckd"/"kidney"
    patient: Dict[str, Any] = {}
    lab_values: Dict[str, Any] = {}
    manual_values: Dict[str, Any] = {}
    source: str = "Lab report"  # for the history row


@router.post("/predict")
def create_prediction(request: PredictRequest):
    try:
        result = engine.predict(
            request.disease,
            request.patient,
            request.lab_values,
            request.manual_values,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # noqa: BLE001 - surface a clean message to the UI
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

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
        except Exception as exc:  # noqa: BLE001 - persistence must never break a prediction
            result["history_warning"] = f"Prediction succeeded but was not saved: {exc}"

    return result

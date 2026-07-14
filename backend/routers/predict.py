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
from typing import Dict, Any

from backend.ml.predict import predict_disease

from backend.routers import prediction_engine as engine
from backend.database import history_store

router = APIRouter(tags=["prediction"])


class PredictRequest(BaseModel):
    disease: str
    lab_values: dict[str, Any]


@router.post("/predict")
def predict(request: PredictRequest):

    try:

        result = predict_disease(
            # pyrefly: ignore [unexpected-keyword]
            disease=request.disease,
            lab_values=request.lab_values
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

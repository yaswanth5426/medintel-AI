"""
POST /predict — disease risk prediction.

Dummy implementation for the Day 1 frontend/backend skeleton. The real
prediction logic (feature engineering, XGBoost inference, SHAP
explanations) belongs to the ML engineer in backend/ml/ and will be called
from here once it's ready — this router should stay a thin HTTP layer.
"""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["prediction"])


class PredictRequest(BaseModel):
    # Loosely typed for now — either symptom text or lab values can be sent.
    # backend/ml/feature_engineering.py will define the real schema.
    input_type: str = "symptoms"  # "symptoms" | "lab_report"
    disease_context: Optional[str] = None
    payload: dict = {}


@router.post("/predict")
def predict_disease(request: PredictRequest):
    """Return a dummy prediction so the frontend has a real contract to build against."""
    return {
        "disease": request.disease_context or "Diabetes",
        "risk_level": "Medium",
        "confidence": 0.62,
        "shap_explanation": None,  # populated once backend/ml/shap_explainer.py exists
        "note": "Dummy response — XGBoost model not connected yet.",
    }

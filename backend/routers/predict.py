from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.ml.predict import predict_disease

router = APIRouter(tags=["prediction"])


class PredictRequest(BaseModel):
    lab_values: dict


@router.post("/predict")
def predict(request: PredictRequest):

    try:
        result = predict_disease(request.lab_values)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed."
        )
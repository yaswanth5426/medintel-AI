from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from backend.ml.predict import predict_disease

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
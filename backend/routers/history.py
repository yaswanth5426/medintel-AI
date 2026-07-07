"""
GET /history - list past predictions for the Dashboard.

Placeholder endpoint: returns a static list of example predictions so the
Dashboard can be wired up before backend/database/ (MongoDB) is
implemented. Owned by Member 3 - real persistence will read from
backend/database/history_schema.py once that's built.
"""

from fastapi import APIRouter

router = APIRouter(tags=["history"])

_PLACEHOLDER_HISTORY = [
    {"date": "Jun 30", "source": "Symptoms", "disease": "Diabetes", "risk_level": "Low", "confidence": 0.22},
    {"date": "Jul 1", "source": "Lab report", "disease": "Heart Disease", "risk_level": "Medium", "confidence": 0.54},
    {"date": "Jul 2", "source": "Symptoms", "disease": "CKD", "risk_level": "Low", "confidence": 0.18},
    {"date": "Jul 4", "source": "Lab report", "disease": "Diabetes", "risk_level": "High", "confidence": 0.81},
    {"date": "Jul 5", "source": "Symptoms", "disease": "Heart Disease", "risk_level": "Medium", "confidence": 0.47},
    {"date": "Jul 6", "source": "Lab report", "disease": "CKD", "risk_level": "Medium", "confidence": 0.39},
]


@router.get("/history")
def get_history():
    return {
        "predictions": _PLACEHOLDER_HISTORY,
        "note": "Placeholder data - MongoDB persistence (backend/database/) isn't implemented yet.",
    }

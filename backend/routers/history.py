"""
GET /history — prediction history for the Dashboard (Member 3 / routers).

Reads from backend/database/history_store.py, which uses MongoDB Atlas when
configured and otherwise a local JSON file. Rows are shaped to match what the
Dashboard renders: date, source, disease, risk_level, confidence.
"""

from fastapi import APIRouter

from backend.database import history_store

router = APIRouter(tags=["history"])


@router.get("/history")
def get_history(limit: int = 50):
    records = history_store.get_history(limit)
    return {
        "predictions": records,
        "count": len(records),
        "note": "Live prediction history.",
    }

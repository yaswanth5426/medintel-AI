"""
history_store.py — persistence for prediction history (Member 3 / database).

Uses MongoDB Atlas when MONGODB_URI is configured and pymongo is installed;
otherwise falls back to a local JSON file so the Dashboard works out of the box
during development. Both paths share the same tiny interface:

    save_prediction(record) -> record (with id + timestamp)
    get_history(limit)      -> list[record]  (newest first)
"""

import json
import os
import threading
import uuid
from datetime import datetime, timezone

_LOCK = threading.Lock()
_JSON_PATH = os.path.join(os.path.dirname(__file__), "history_store.json")

_mongo_collection = None


def _init_mongo():
    """Return a MongoDB collection if configured + reachable, else None."""
    global _mongo_collection
    if _mongo_collection is not None:
        return _mongo_collection

    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return None
    try:
        from pymongo import MongoClient  # imported lazily — optional dependency

        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        db = client.get_database("medintel")
        _mongo_collection = db.get_collection("history")
        print("[history_store] Connected to MongoDB Atlas.")
        return _mongo_collection
    except Exception as exc:  # noqa: BLE001 — any failure falls back to JSON
        print(f"[history_store] MongoDB unavailable ({exc!r}); using JSON file.")
        return None


def _read_json():
    if not os.path.exists(_JSON_PATH):
        return []
    try:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _write_json(records):
    tmp = _JSON_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    os.replace(tmp, _JSON_PATH)


def save_prediction(record):
    """Persist one prediction. Adds id + ISO timestamp, returns the record."""
    record = dict(record)
    record.setdefault("id", uuid.uuid4().hex)
    record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())

    collection = _init_mongo()
    with _LOCK:
        if collection is not None:
            collection.insert_one({**record})
        else:
            records = _read_json()
            records.append(record)
            _write_json(records)
    return record


def get_history(limit=50):
    """Return up to `limit` predictions, newest first."""
    collection = _init_mongo()
    if collection is not None:
        docs = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
        return docs

    records = _read_json()
    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return records[:limit]

import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient

# Environment variables are provided by the platform
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[MongoClient] = None
_db = None

try:
    _client = MongoClient(DATABASE_URL, serverSelectionTimeoutMS=3000)
    # Trigger a server selection to validate connection lazily
    _client.server_info()
    _db = _client[DATABASE_NAME]
except Exception:
    _client = None
    _db = None


def db():
    """Return the connected database instance or raise error if unavailable."""
    if _db is None:
        raise RuntimeError("Database connection is not available")
    return _db


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    doc = {**data, "created_at": now, "updated_at": now}
    result = db()[collection_name].insert_one(doc)
    inserted = db()[collection_name].find_one({"_id": result.inserted_id})
    if inserted:
        inserted["id"] = str(inserted.pop("_id"))
    return inserted or {}


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    filter_dict = filter_dict or {}
    cursor = db()[collection_name].find(filter_dict).sort("created_at", -1).limit(limit)
    items: List[Dict[str, Any]] = []
    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items

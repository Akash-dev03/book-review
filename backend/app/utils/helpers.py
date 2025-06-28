from typing import Any, Dict
import json
from datetime import datetime


def serialize_datetime(obj: Any) -> str:
    """Serialize datetime objects to string"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def clean_dict_for_cache(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean dictionary for caching by removing SQLAlchemy internal attributes"""
    cleaned = {}
    for key, value in data.items():
        if not key.startswith('_'):
            cleaned[key] = value
    return cleaned
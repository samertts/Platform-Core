"""
NHDOS Frontend Utilities

Helper functions for frontend development
"""

import hashlib
import json
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def format_date(date: datetime, format: str = "%Y-%m-%d") -> str:
    return date.strftime(format)


def format_datetime(date: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return date.strftime(format)


def parse_date(date_string: str, format: str = "%Y-%m-%d") -> datetime | None:
    try:
        return datetime.strptime(date_string, format)
    except (ValueError, TypeError):
        return None


def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def validate_uuid(uuid_string: str) -> bool:
    try:
        uuid_obj = uuid4()
        uuid_obj.__init__(uuid_string)
        return True
    except ValueError:
        return False


def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(d: dict, sep: str = ".") -> dict:
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def capitalize_words(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())


def snake_to_camel(name: str) -> str:
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(name: str) -> str:
    import re

    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def sanitize_filename(filename: str) -> str:
    import re

    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def chunk_list(lst: list, chunk_size: int) -> list[list]:
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def unique_by_key(lst: list[dict], key: str) -> list[dict]:
    seen = set()
    result = []
    for item in lst:
        value = item.get(key)
        if value not in seen:
            seen.add(value)
            result.append(item)
    return result

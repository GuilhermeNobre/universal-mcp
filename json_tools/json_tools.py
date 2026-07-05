import json
from typing import Any


def _load_json(text: str) -> tuple[Any | None, str | None]:
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"


def validate_json(text: str) -> str:
    """Validate a JSON string.

    Args:
        text: JSON text to validate.
    """
    _, error = _load_json(text)
    if error:
        return error

    return "Valid JSON."


def format_json(text: str, indent: int = 2) -> str:
    """Format a JSON string with indentation.

    Args:
        text: JSON text to format.
        indent: Number of spaces for indentation.
    """
    data, error = _load_json(text)
    if error:
        return error

    return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)


def minify_json(text: str) -> str:
    """Minify a JSON string.

    Args:
        text: JSON text to minify.
    """
    data, error = _load_json(text)
    if error:
        return error

    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def json_keys(text: str) -> str:
    """List top-level keys from a JSON object.

    Args:
        text: JSON object text to inspect.
    """
    data, error = _load_json(text)
    if error:
        return error

    if not isinstance(data, dict):
        return "JSON value is not an object, so it has no top-level keys."

    if not data:
        return "JSON object has no keys."

    return "\n".join(str(key) for key in data.keys())

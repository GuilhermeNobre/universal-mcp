import base64
import json
from datetime import datetime, timezone
from typing import Any


def _decode_base64url(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _format_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def decode_jwt(token: str) -> str:
    """Decode a JWT header and payload without validating the signature.

    Args:
        token: The JWT string to decode.
    """
    parts = token.split(".")
    if len(parts) != 3:
        return "Invalid JWT format. Expected three dot-separated parts."

    try:
        header = json.loads(_decode_base64url(parts[0]))
        payload = json.loads(_decode_base64url(parts[1]))
    except Exception:
        return "Failed to decode JWT header or payload."

    lines = [
        "Header:",
        _format_json(header),
        "",
        "Payload:",
        _format_json(payload),
    ]

    exp = payload.get("exp")
    if isinstance(exp, int):
        expires_at = datetime.fromtimestamp(exp, timezone.utc)
        now = datetime.now(timezone.utc)
        status = "expired" if expires_at <= now else "not expired"
        lines.extend(
            [
                "",
                f"Expiration: {expires_at.isoformat()} ({status})",
            ]
        )

    return "\n".join(lines)

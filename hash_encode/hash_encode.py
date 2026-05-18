import hashlib
import base64
import re
from urllib.parse import quote, unquote

SUPPORTED_ALGORITHMS = ("md5", "sha1", "sha256", "sha512")

# (length, charset) → possible algorithms
_HEX_HASH_MAP: dict[int, list[str]] = {
    32:  ["MD5", "MD4", "NTLM"],
    40:  ["SHA-1", "RIPEMD-160"],
    56:  ["SHA-224", "SHA-3-224"],
    64:  ["SHA-256", "SHA-3-256", "BLAKE2s"],
    96:  ["SHA-384", "SHA-3-384"],
    128: ["SHA-512", "SHA-3-512", "BLAKE2b-512"],
}

_PREFIX_MAP = [
    (r"^\$2[aby]\$", "bcrypt"),
    (r"^\$argon2", "Argon2"),
    (r"^\$scrypt\$", "scrypt"),
    (r"^\$1\$", "MD5-crypt"),
    (r"^\$5\$", "SHA-256-crypt"),
    (r"^\$6\$", "SHA-512-crypt"),
    (r"^\$pbkdf2", "PBKDF2"),
]


def detect_hash(text: str) -> str:
    """Detect the likely hash algorithm(s) used to produce a given hash string.

    Args:
        text: The hash string to identify.
    """
    text = text.strip()

    for pattern, name in _PREFIX_MAP:
        if re.match(pattern, text, re.IGNORECASE):
            return f"Detected: {name}\nHash: {text}"

    if re.fullmatch(r"[0-9a-fA-F]+", text):
        candidates = _HEX_HASH_MAP.get(len(text))
        if candidates:
            return (
                f"Length: {len(text)} hex chars\n"
                f"Possible algorithms: {', '.join(candidates)}\n"
                f"Hash: {text}"
            )
        return f"Looks like a hex hash but length {len(text)} doesn't match any known algorithm."

    try:
        decoded = base64.b64decode(text + "==")
        candidates = _HEX_HASH_MAP.get(len(decoded) * 2)
        if candidates:
            return (
                f"Looks like Base64-encoded hash ({len(decoded)} bytes)\n"
                f"Possible algorithms: {', '.join(candidates)}\n"
                f"Hash: {text}"
            )
    except Exception:
        pass

    return f"Could not identify '{text}' as a known hash format."


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Hash a string using a cryptographic algorithm.

    Args:
        text: The text to hash.
        algorithm: Hash algorithm to use. Options: md5, sha1, sha256, sha512. Defaults to sha256.
    """
    algorithm = algorithm.lower()
    if algorithm not in SUPPORTED_ALGORITHMS:
        return f"Unsupported algorithm '{algorithm}'. Choose from: {', '.join(SUPPORTED_ALGORITHMS)}."

    digest = hashlib.new(algorithm, text.encode()).hexdigest()
    return f"{algorithm.upper()}({text!r}) = {digest}"


def base64_encode(text: str) -> str:
    """Encode a string to Base64.

    Args:
        text: The text to encode.
    """
    encoded = base64.b64encode(text.encode()).decode()
    return f"Base64({text!r}) = {encoded}"


def base64_decode(text: str) -> str:
    """Decode a Base64 string back to plain text.

    Args:
        text: The Base64 string to decode.
    """
    try:
        decoded = base64.b64decode(text.encode()).decode()
        return f"Decoded({text!r}) = {decoded}"
    except Exception:
        return f"Failed to decode '{text}': invalid Base64 string."


def url_encode(text: str) -> str:
    """URL-encode a string (percent-encoding).

    Args:
        text: The text to URL-encode.
    """
    encoded = quote(text, safe="")
    return f"URL-encoded({text!r}) = {encoded}"


def url_decode(text: str) -> str:
    """Decode a URL-encoded (percent-encoded) string.

    Args:
        text: The URL-encoded string to decode.
    """
    decoded = unquote(text)
    return f"URL-decoded({text!r}) = {decoded}"

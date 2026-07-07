import re


def text_stats(text: str) -> str:
    """Count characters, words, and lines in text.

    Args:
        text: The text to inspect.
    """
    words = re.findall(r"\S+", text)
    lines = text.splitlines() or [text]
    return f"Characters: {len(text)}\nWords: {len(words)}\nLines: {len(lines)}"


def transform_text(text: str, mode: str = "lower") -> str:
    """Transform text casing or whitespace.

    Args:
        text: The text to transform.
        mode: Transformation mode. Options: lower, upper, title, trim_spaces.
    """
    mode = mode.lower()
    if mode == "lower":
        return text.lower()
    if mode == "upper":
        return text.upper()
    if mode == "title":
        return text.title()
    if mode == "trim_spaces":
        return " ".join(text.split())

    return "Unsupported mode. Choose from: lower, upper, title, trim_spaces."


def slugify_text(text: str, separator: str = "-") -> str:
    """Create a URL-friendly slug from text.

    Args:
        text: The text to slugify.
        separator: Word separator to use in the slug. Defaults to '-'.
    """
    if not separator:
        return "Separator cannot be empty."

    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", separator, slug)
    slug = slug.strip(separator)
    slug = re.sub(rf"{re.escape(separator)}+", separator, slug)
    return slug


TOOLS = [
    text_stats,
    transform_text,
    slugify_text,
]

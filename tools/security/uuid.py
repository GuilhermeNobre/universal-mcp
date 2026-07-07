import uuid


def generate_uuid(version: int = 4) -> str:
    """Generate a UUID.

    Args:
        version: UUID version to generate. Options: 4 (random) or 7 (time-ordered).
    """
    if version == 4:
        return str(uuid.uuid4())
    if version == 7:
        return str(uuid.uuid7())

    return "Only UUID versions 4 and 7 are supported."


def validate_uuid(value: str) -> str:
    """Validate whether a string is a UUID.

    Args:
        value: The UUID string to validate.
    """
    try:
        parsed = uuid.UUID(value)
    except ValueError:
        return f"'{value}' is not a valid UUID."

    return f"'{value}' is a valid UUID version {parsed.version}."


TOOLS = [
    generate_uuid,
    validate_uuid,
]

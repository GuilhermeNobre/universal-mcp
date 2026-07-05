import uuid


def generate_uuid(version: int = 4) -> str:
    """Generate a UUID.

    Args:
        version: UUID version to generate. Currently only version 4 is supported.
    """
    if version != 4:
        return "Only UUID version 4 is supported."

    return str(uuid.uuid4())


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

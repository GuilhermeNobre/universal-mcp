from datetime import datetime, timedelta, timezone


def _parse_datetime(value: str) -> datetime:
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def unix_timestamp_to_date(timestamp: int, utc_offset: int = 0) -> str:
    """Convert a Unix timestamp to an ISO datetime.

    Args:
        timestamp: Unix timestamp in seconds.
        utc_offset: UTC offset in hours. Defaults to UTC.
    """
    tz = timezone(timedelta(hours=utc_offset))
    return datetime.fromtimestamp(timestamp, tz).isoformat()


def date_to_unix_timestamp(date: str) -> str:
    """Convert an ISO datetime string to a Unix timestamp.

    Args:
        date: ISO datetime string. Naive values are treated as UTC.
    """
    try:
        parsed = _parse_datetime(date)
    except ValueError:
        return "Invalid date. Use an ISO format like 2026-07-05T10:30:00+00:00."

    return str(int(parsed.timestamp()))


def date_difference(start_date: str, end_date: str) -> str:
    """Calculate the difference between two ISO datetime strings.

    Args:
        start_date: Start ISO datetime string.
        end_date: End ISO datetime string.
    """
    try:
        start = _parse_datetime(start_date)
        end = _parse_datetime(end_date)
    except ValueError:
        return "Invalid date. Use ISO format for both dates."

    delta = end - start
    seconds = int(delta.total_seconds())
    return (
        f"Seconds: {seconds}\n"
        f"Minutes: {seconds / 60:.2f}\n"
        f"Hours: {seconds / 3600:.2f}\n"
        f"Days: {seconds / 86400:.2f}"
    )


def add_time(
    date: str,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> str:
    """Add or subtract time from an ISO datetime string.

    Args:
        date: ISO datetime string.
        days: Days to add. Use negative values to subtract.
        hours: Hours to add. Use negative values to subtract.
        minutes: Minutes to add. Use negative values to subtract.
        seconds: Seconds to add. Use negative values to subtract.
    """
    try:
        parsed = _parse_datetime(date)
    except ValueError:
        return "Invalid date. Use an ISO format like 2026-07-05T10:30:00+00:00."

    result = parsed + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
    return result.isoformat()

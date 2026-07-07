from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def get_current_time(utc_offset: float = 0, timezone_name: str = "") -> str:
    """Get the current date and time for a UTC offset or IANA timezone.

    Args:
        utc_offset: UTC offset in hours (e.g. -3 for UTC-3, 5.5 for UTC+5:30). Ignored when timezone_name is given.
        timezone_name: Optional IANA timezone name like America/Sao_Paulo. Handles daylight saving time correctly.
    """
    if timezone_name:
        try:
            tz = ZoneInfo(timezone_name)
        except Exception:
            return f"'{timezone_name}' is not a valid IANA timezone name."

        now = datetime.now(tz)
        return f"{timezone_name}:\n{now.strftime('%Y-%m-%d %H:%M:%S')} (UTC{now.strftime('%:z')})"

    tz = timezone(timedelta(hours=utc_offset))
    now = datetime.now(tz)
    sign = "+" if utc_offset >= 0 else ""
    offset = f"{utc_offset:g}"
    return f"{sign}{offset}:\n{now.strftime('%Y-%m-%d %H:%M:%S')} (UTC{sign}{offset})"


TOOLS = [get_current_time]

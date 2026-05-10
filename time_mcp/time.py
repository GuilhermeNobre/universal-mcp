from datetime import datetime, timezone, timedelta

def get_current_time(utc_offset: int) -> str:
    """Get the current date and time for a given UTC offset.

    Args:
        utc_offset: UTC offset in hours (e.g. -3 for UTC-3, 5 for UTC+5)
    """
    tz = timezone(timedelta(hours=utc_offset))
    now = datetime.now(tz)
    sign = "+" if utc_offset >= 0 else ""
    return (
        f"{sign}{utc_offset}:\n"
        f"{now.strftime('%Y-%m-%d %H:%M:%S')} (UTC{sign}{utc_offset})"
    )

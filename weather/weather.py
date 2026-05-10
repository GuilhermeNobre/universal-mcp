NWS_API_BASE = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,rain,precipitation_probability"
USER_AGENT = "universal-app/1.0"

import httpx
from typing import Any

async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = NWS_API_BASE.format(latitude=latitude, longitude=longitude)
    data = await make_nws_request(url)

    if not data or "hourly" not in data:
        return "Unable to fetch forecast data for this location."

    hourly = data["hourly"]
    units = data["hourly_units"]

    times = hourly["time"]
    temps = hourly["temperature_2m"]
    humidity = hourly["relative_humidity_2m"]
    rain = hourly["rain"]
    precip_prob = hourly["precipitation_probability"]

    forecasts = []
    for i in range(min(24, len(times))):
        forecasts.append(
            f"{times[i]}  "
            f"Temp: {temps[i]}{units['temperature_2m']}  "
            f"Humidity: {humidity[i]}{units['relative_humidity_2m']}  "
            f"Rain: {rain[i]}{units['rain']}  "
            f"Precip. prob: {precip_prob[i]}{units['precipitation_probability']}"
        )

    return "\n".join(forecasts)
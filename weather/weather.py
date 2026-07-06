from common.http import fetch_json

FORECAST_API = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,rain,precipitation_probability"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search?name={name}&count={count}&language=en&format=json"


async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = FORECAST_API.format(latitude=latitude, longitude=longitude)
    data = await fetch_json(url)

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


async def search_location(name: str, count: int = 5) -> str:
    """Search a place by name and return latitude/longitude candidates.

    Args:
        name: Place name to search, like a city (e.g. Sao Paulo, Berlin).
        count: Maximum number of results. Defaults to 5.
    """
    name = name.strip()
    if not name:
        return "Place name cannot be empty."
    if count < 1 or count > 20:
        return "Count must be between 1 and 20."

    url = GEOCODING_API.format(name=name, count=count)
    data = await fetch_json(url)

    if data is None:
        return "Unable to fetch location data."

    results = data.get("results")
    if not results:
        return f"No locations found for '{name}'."

    lines = []
    for place in results:
        parts = [place.get("name", "?")]
        if place.get("admin1"):
            parts.append(place["admin1"])
        if place.get("country"):
            parts.append(place["country"])
        lines.append(
            f"{', '.join(parts)}  lat: {place.get('latitude')}  lon: {place.get('longitude')}"
        )

    return "\n".join(lines)

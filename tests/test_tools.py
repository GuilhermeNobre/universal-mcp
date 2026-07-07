import re
import unittest
from unittest.mock import AsyncMock, patch

from tools.conversion.colors import convert_color, validate_color
from tools.conversion.numbers import convert_angle, convert_number_base
from tools.conversion.units import convert_unit
from tools.datetime.current_time import get_current_time
from tools.datetime.dates import date_to_unix_timestamp, unix_timestamp_to_date
from tools.external.currency import get_coin_price
from tools.external.weather import get_forecast, search_location
from tools.media.qr import generate_qr_code
from tools.network.ip import cidr_info, ip_in_cidr, validate_ip
from tools.security.jwt import decode_jwt
from tools.security.passwords import generate_password
from tools.security.uuid import generate_uuid, validate_uuid
from tools.text.json import format_json, validate_json
from tools.text.regex import test_regex
from tools.text.text import slugify_text, text_stats, transform_text


class ToolTests(unittest.TestCase):
    def test_generate_password_count_and_ambiguous_exclusion(self):
        result = generate_password(
            length=16,
            include_numbers=True,
            include_special_chars=True,
            include_uppercase=True,
            exclude_ambiguous=True,
            count=3,
        )

        passwords = result.splitlines()
        self.assertEqual(len(passwords), 3)
        for password in passwords:
            self.assertEqual(len(password), 16)
            self.assertFalse(set(password) & set("0O1lI"))

    def test_uuid_tools(self):
        value = generate_uuid()

        self.assertIn("valid UUID version 4", validate_uuid(value))
        self.assertIn("not a valid UUID", validate_uuid("invalid"))

    def test_json_tools(self):
        formatted = format_json('{"b":1,"a":2}')

        self.assertEqual(validate_json(formatted), "Valid JSON.")
        self.assertIn('"a": 2', formatted)

    def test_jwt_decode_without_signature_validation(self):
        token = "eyJhbGciOiJub25lIn0.eyJzdWIiOiIxMjMifQ."

        result = decode_jwt(token)

        self.assertIn('"alg": "none"', result)
        self.assertIn('"sub": "123"', result)

    def test_text_tools(self):
        self.assertEqual(slugify_text("Hello Universal MCP!"), "hello-universal-mcp")
        self.assertEqual(transform_text("  hello   world  ", "trim_spaces"), "hello world")
        self.assertIn("Words: 2", text_stats("hello world"))

    def test_date_tools(self):
        timestamp = date_to_unix_timestamp("1970-01-01T00:00:00+00:00")

        self.assertEqual(timestamp, "0")
        self.assertEqual(unix_timestamp_to_date(0), "1970-01-01T00:00:00+00:00")

    def test_color_tools(self):
        self.assertIn("valid HEX color", validate_color("#369"))
        self.assertIn("RGB: rgb(51, 102, 153)", convert_color("#369"))

    def test_qr_code(self):
        result = generate_qr_code("universal-mcp", box_size=2)

        self.assertTrue(result.startswith("data:image/png;base64,"))

    def test_time_accepts_fractional_offsets(self):
        result = get_current_time(5.5)

        self.assertRegex(result, re.compile(r"^\+5\.5:", re.MULTILINE))

    def test_time_accepts_iana_timezone(self):
        result = get_current_time(timezone_name="America/Sao_Paulo")

        self.assertIn("America/Sao_Paulo:", result)
        self.assertIn(
            "'invalid/zone' is not a valid IANA timezone name.",
            get_current_time(timezone_name="invalid/zone"),
        )

    def test_generate_uuid_v7(self):
        value = generate_uuid(version=7)

        self.assertIn("valid UUID version 7", validate_uuid(value))
        self.assertIn("Only UUID versions 4 and 7", generate_uuid(version=1))

    def test_number_base_conversion(self):
        self.assertIn("= ff (base 16)", convert_number_base("255", 10, 16))
        self.assertIn("= 1010 (base 2)", convert_number_base("10", 10, 2))
        self.assertIn("= -255 (base 10)", convert_number_base("-ff", 16, 10))
        self.assertIn("not a valid base-2 number", convert_number_base("102", 2, 10))
        self.assertIn("Bases must be between 2 and 36", convert_number_base("10", 1, 10))

    def test_angle_conversion(self):
        self.assertIn("= 3.14159 rad", convert_angle(180, "deg", "rad"))
        self.assertIn("= 360 deg", convert_angle(1, "turn", "deg"))
        self.assertIn("= 200 grad", convert_angle(180, "deg", "grad"))
        self.assertIn("Unsupported angle unit", convert_angle(1, "foo", "rad"))

    def test_unit_conversion(self):
        self.assertIn("= 212 f", convert_unit(100, "c", "f"))
        self.assertIn("= 273.15 k", convert_unit(0, "c", "k"))
        self.assertIn("= 1000 m", convert_unit(1, "km", "m"))
        self.assertIn("= 2.20462 lb", convert_unit(1, "kg", "lb"))
        self.assertIn("= 1024 mib", convert_unit(1, "gib", "mib"))
        self.assertIn("Cannot convert between different categories", convert_unit(1, "kg", "m"))
        self.assertIn("Unsupported unit", convert_unit(1, "foo", "m"))

    def test_regex_tester(self):
        result = test_regex(r"(?P<word>h\w+)", "hello Hi hey", ignore_case=True)

        self.assertIn("Match 1", result)
        self.assertIn("'hello'", result)
        self.assertIn("word='hello'", result)
        self.assertEqual(test_regex(r"\d+", "no digits"), "No matches found.")
        self.assertIn("Invalid regex pattern", test_regex("(", "text"))

    def test_network_tools(self):
        self.assertIn("valid IPv4 address", validate_ip("192.168.1.1"))
        self.assertIn("private", validate_ip("192.168.1.1"))
        self.assertIn("valid IPv6 address", validate_ip("::1"))
        self.assertIn("not a valid IP address", validate_ip("999.1.1.1"))

        info = cidr_info("192.168.1.0/24")
        self.assertIn("Netmask: 255.255.255.0", info)
        self.assertIn("Usable hosts: 254 (192.168.1.1 - 192.168.1.254)", info)

        self.assertIn("is inside", ip_in_cidr("10.1.2.3", "10.0.0.0/8"))
        self.assertIn("is NOT inside", ip_in_cidr("11.1.2.3", "10.0.0.0/8"))


class HttpToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_forecast_formats_hourly_data(self):
        payload = {
            "hourly": {
                "time": ["2026-07-06T00:00"],
                "temperature_2m": [21.5],
                "relative_humidity_2m": [80],
                "rain": [0.0],
                "precipitation_probability": [10],
            },
            "hourly_units": {
                "temperature_2m": "°C",
                "relative_humidity_2m": "%",
                "rain": "mm",
                "precipitation_probability": "%",
            },
        }

        with patch("tools.external.weather.fetch_json", new=AsyncMock(return_value=payload)):
            result = await get_forecast(-23.55, -46.63)

        self.assertIn("Temp: 21.5°C", result)
        self.assertIn("Precip. prob: 10%", result)

    async def test_get_forecast_handles_failure(self):
        with patch("tools.external.weather.fetch_json", new=AsyncMock(return_value=None)):
            result = await get_forecast(0, 0)

        self.assertIn("Unable to fetch forecast data", result)

    async def test_search_location_lists_candidates(self):
        payload = {
            "results": [
                {
                    "name": "São Paulo",
                    "admin1": "São Paulo",
                    "country": "Brazil",
                    "latitude": -23.5475,
                    "longitude": -46.6361,
                }
            ]
        }

        with patch("tools.external.weather.fetch_json", new=AsyncMock(return_value=payload)):
            result = await search_location("Sao Paulo")

        self.assertIn("São Paulo, São Paulo, Brazil", result)
        self.assertIn("lat: -23.5475", result)

    async def test_search_location_handles_no_results(self):
        with patch("tools.external.weather.fetch_json", new=AsyncMock(return_value={})):
            result = await search_location("nowhere-xyz")

        self.assertIn("No locations found", result)

    async def test_get_coin_price_requires_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            result = await get_coin_price("BTC", "USD")

        self.assertIn("UNIRATE_API_KEY", result)

    async def test_get_coin_price_returns_rate(self):
        payload = {"rate": 5.43}

        with (
            patch.dict("os.environ", {"UNIRATE_API_KEY": "test-key"}),
            patch("tools.external.currency.fetch_json", new=AsyncMock(return_value=payload)),
        ):
            result = await get_coin_price("usd", "brl")

        self.assertEqual(result, "1 USD = 5.43 BRL")


if __name__ == "__main__":
    unittest.main()

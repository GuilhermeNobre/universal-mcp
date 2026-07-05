import re
import unittest

from color_tools.color_tools import convert_color, validate_color
from date_tools.date_tools import date_to_unix_timestamp, unix_timestamp_to_date
from json_tools.json_tools import format_json, validate_json
from jwt_tools.jwt_tools import decode_jwt
from password_generator.password_generator import generate_password
from qr_tools.qr_tools import generate_qr_code
from text_tools.text_tools import slugify_text, text_stats, transform_text
from time_mcp.time import get_current_time
from uuid_tools.uuid_tools import generate_uuid, validate_uuid


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


if __name__ == "__main__":
    unittest.main()

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from color_tools.color_tools import convert_color, generate_color_palette, validate_color
from currency.coins import get_coin_price
from date_tools.date_tools import (
    add_time,
    date_difference,
    date_to_unix_timestamp,
    unix_timestamp_to_date,
)
from hash_encode.hash_encode import (
    base64_decode,
    base64_encode,
    detect_hash,
    hash_text,
    url_decode,
    url_encode,
)
from json_tools.json_tools import format_json, json_keys, minify_json, validate_json
from jwt_tools.jwt_tools import decode_jwt
from network_tools.network_tools import cidr_info, ip_in_cidr, validate_ip
from number_tools.number_tools import convert_angle, convert_number_base
from password_generator.password_generator import generate_password
from qr_tools.qr_tools import generate_qr_code
from regex_tools.regex_tools import test_regex
from text_tools.text_tools import slugify_text, text_stats, transform_text
from time_mcp.time import get_current_time
from unit_tools.unit_tools import convert_unit
from uuid_tools.uuid_tools import generate_uuid, validate_uuid
from weather.weather import get_forecast, search_location

_RESOURCE_DIR = Path(__file__).parent / ".resource"

mcp = FastMCP()


@mcp.resource("currency://coins")
def list_coins() -> str:
    return (_RESOURCE_DIR / "coins.json").read_text()


@mcp.resource("currency://crypto")
def list_crypto() -> str:
    return (_RESOURCE_DIR / "crypto.json").read_text()


mcp.tool()(get_forecast)
mcp.tool()(search_location)
mcp.tool()(get_current_time)
mcp.tool()(get_coin_price)
mcp.tool()(detect_hash)
mcp.tool()(hash_text)
mcp.tool()(base64_encode)
mcp.tool()(base64_decode)
mcp.tool()(url_encode)
mcp.tool()(url_decode)
mcp.tool()(generate_password)
mcp.tool()(generate_uuid)
mcp.tool()(validate_uuid)
mcp.tool()(decode_jwt)
mcp.tool()(text_stats)
mcp.tool()(transform_text)
mcp.tool()(slugify_text)
mcp.tool()(validate_json)
mcp.tool()(format_json)
mcp.tool()(minify_json)
mcp.tool()(json_keys)
mcp.tool()(unix_timestamp_to_date)
mcp.tool()(date_to_unix_timestamp)
mcp.tool()(date_difference)
mcp.tool()(add_time)
mcp.tool()(generate_qr_code)
mcp.tool()(validate_color)
mcp.tool()(convert_color)
mcp.tool()(generate_color_palette)
mcp.tool()(convert_number_base)
mcp.tool()(convert_angle)
mcp.tool()(convert_unit)
mcp.tool()(test_regex)
mcp.tool()(validate_ip)
mcp.tool()(cidr_info)
mcp.tool()(ip_in_cidr)


def main():
    mcp.run()


if __name__ == "__main__":
    main()

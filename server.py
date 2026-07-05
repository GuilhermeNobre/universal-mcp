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
from password_generator.password_generator import generate_password
from qr_tools.qr_tools import generate_qr_code
from text_tools.text_tools import slugify_text, text_stats, transform_text
from time_mcp.time import get_current_time
from uuid_tools.uuid_tools import generate_uuid, validate_uuid
from weather.weather import get_forecast

mcp = FastMCP()

# @mcp.resource("currency://coins")
# def list_coins():
#     with open(".resource/coins.json", "r") as f:
#         return f.read()

# @mcp.resource("currency://crypto")
# def list_crypto():
#     with open(".resource/crypto.json", "r") as f:
#         return f.read()

mcp.tool()(get_forecast)
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


def main():
    mcp.run()


if __name__ == "__main__":
    main()


from mcp.server.fastmcp import FastMCP

from weather.weather import get_forecast
from time_mcp.time import get_current_time
from currency.coins import get_coin_price
from hash_encode.hash_encode import hash_text, base64_encode, base64_decode, url_encode, url_decode, detect_hash
from password_generator.password_generator import generate_password

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

def main():
    mcp.run()
    
if __name__ == "__main__":
    main()

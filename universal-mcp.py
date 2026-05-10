
from mcp.server.fastmcp import FastMCP

from weather.weather import get_forecast
from time_mcp.time import get_current_time
from currency.coins import get_coin_price

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

def main():
    mcp.run()
    
if __name__ == "__main__":
    main()
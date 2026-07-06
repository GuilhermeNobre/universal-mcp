import os

from common.http import fetch_json

UNIRATE_BASE_API = (
    "https://api.unirateapi.com/api/convert?api_key={api_key}&amount=1&from={coin}&to={base}"
)


async def get_coin_price(coin: str, base: str = "USD") -> str:
    """Convert a currency or cryptocurrency to another currency.

    Args:
        coin: Currency or crypto code to convert from (e.g. BRL, BTC, ETH)
        base: Currency code to convert to (e.g. USD, EUR). Defaults to USD.
    """
    api_key = os.getenv("UNIRATE_API_KEY")
    if not api_key:
        return "UNIRATE_API_KEY environment variable is required for currency conversion."

    coin = coin.upper()
    base = base.upper()

    data = await fetch_json(UNIRATE_BASE_API.format(api_key=api_key, coin=coin, base=base))
    if not data:
        return "Failed to fetch conversion rate."

    rate = data.get("rate") or data.get("result")
    return f"1 {coin} = {rate} {base}"

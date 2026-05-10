import json
import httpx
from pathlib import Path
from typing import Any

UNIRATE_BASE_API = "https://api.unirateapi.com/api/convert?api_key=XL89LFgeWPhfIwgPt0z3KEeZjile4bIebTJajctKWSyJ5UifiP0SZcOrNNJl7JpG&amount=1&from={coin}&to={base}"
USER_AGENT = "universal-app/1.0"

_base = Path(__file__).parent.parent / ".resource"
COINS: dict = json.loads((_base / "coins.json").read_text())
CRYPTO: dict = json.loads((_base / "crypto.json").read_text())

async def _request(url: str) -> dict[str, Any] | None:
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def get_coin_price(coin: str, base: str = "USD") -> str:
    """Convert a currency or cryptocurrency to another currency.

    Args:
        coin: Currency or crypto code to convert from (e.g. BRL, BTC, ETH)
        base: Currency code to convert to (e.g. USD, EUR). Defaults to USD.
    """
    coin = coin.upper()
    base = base.upper()

    # DEVELOPMENT NOTE: For now we won't validate the coin/base against the lists, since the API seems to support a wide range of currencies. We can add validation later if needed.
    # if coin not in COINS or coin not in CRYPTO.values():
    #     return f"'{coin}' is not a supported currency or crypto. Valid examples: BRL, EUR, BTC, ETH."
    # if base not in COINS or base not in CRYPTO.values():
    #     return f"'{base}' is not a supported base currency. Valid examples: USD, EUR, BRL."

    data = await _request(UNIRATE_BASE_API.format(coin=coin, base=base))
    if not data:
        return "Failed to fetch conversion rate."

    rate = data.get("rate") or data.get("result")
    return f"1 {coin} = {rate} {base}"
    
   
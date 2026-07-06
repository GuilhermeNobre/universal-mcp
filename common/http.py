from typing import Any

import httpx

USER_AGENT = "universal-app/1.0"


async def fetch_json(url: str) -> dict[str, Any] | None:
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

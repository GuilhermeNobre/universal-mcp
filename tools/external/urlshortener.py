import httpx

from common.http import USER_AGENT

TINYURL_API = "https://tinyurl.com/api-create.php?url={url}"


async def shorten_url(url: str) -> str:
    """Shorten a URL using TinyURL. No account or API key required.

    Args:
        url: The full URL to shorten (must start with http:// or https://).
    """
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "URL must start with http:// or https://"

    headers = {"User-Agent": USER_AGENT}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TINYURL_API.format(url=url), headers=headers, timeout=30.0)
            response.raise_for_status()
            short = response.text.strip()
            if not short.startswith("https://tinyurl.com/"):
                return "Failed to shorten URL."
            return short
    except Exception:
        return "Failed to shorten URL."


TOOLS = [shorten_url]

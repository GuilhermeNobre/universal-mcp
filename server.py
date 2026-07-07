from pathlib import Path

from mcp.server.fastmcp import FastMCP

from tools import ALL_TOOLS

_RESOURCE_DIR = Path(__file__).parent / "resources"

mcp = FastMCP()


@mcp.resource("currency://coins")
def list_coins() -> str:
    return (_RESOURCE_DIR / "coins.json").read_text()


@mcp.resource("currency://crypto")
def list_crypto() -> str:
    return (_RESOURCE_DIR / "crypto.json").read_text()


for tool in ALL_TOOLS:
    mcp.tool()(tool)


def main():
    mcp.run()


if __name__ == "__main__":
    main()

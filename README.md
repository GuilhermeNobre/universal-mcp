# Universal MCP

Universal MCP is a Python MCP server that exposes small utility tools for agents and MCP clients.

## Available Tools

- `get_forecast`: Gets a 24-hour weather forecast from Open-Meteo using latitude and longitude.
- `get_current_time`: Gets the current date and time for a UTC offset.
- `get_coin_price`: Converts a currency or cryptocurrency value to another currency.
- `detect_hash`: Detects likely hash formats.
- `hash_text`: Hashes text using `md5`, `sha1`, `sha256`, or `sha512`.
- `base64_encode`: Encodes text as Base64.
- `base64_decode`: Decodes Base64 text.
- `url_encode`: URL-encodes text.
- `url_decode`: URL-decodes text.
- `generate_password`: Generates a random password without saving it.

## Requirements

- Python `>=3.14`
- `uv`

Project dependencies are defined in `pyproject.toml`.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/GuilhermeNobre/universal-mcp.git
cd universal-mcp
uv sync
```

## Running the MCP Server

Run the server directly:

```bash
uv run python universal-mcp.py
```

The server runs over MCP stdio, so it is usually started by an MCP-compatible client rather than manually.

## MCP Client Configuration

Use this command from your MCP client:

```bash
uv --directory /absolute/path/to/universal-mcp run python universal-mcp.py
```

Example JSON-style MCP configuration:

```json
{
  "mcpServers": {
    "universal-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/universal-mcp",
        "run",
        "python",
        "universal-mcp.py"
      ]
    }
  }
}
```

Replace `/absolute/path/to/universal-mcp` with the real path on your machine.

## Agent Instructions

This repository includes [AGENT.md](./AGENT.md), which contains setup and usage instructions for AI coding agents.

Use it when connecting this MCP server to:

- Claude Desktop or Claude Code
- Codex
- Any other MCP-compatible agent or client

Agents should read `AGENT.md` before modifying or installing the project.

## Development Notes

- Keep tools small and focused.
- Register new tools in `universal-mcp.py`.
- Do not store generated passwords or other sensitive user inputs.
- Prefer async HTTP helpers for tools that call external APIs.
- Run a syntax check before committing changes:

```bash
uv run python -m py_compile universal-mcp.py */*.py
```


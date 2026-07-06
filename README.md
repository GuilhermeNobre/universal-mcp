<div align="center">

# Universal MCP

### 💍 *One MCP to rule them all, one MCP to find them,*<br>*one MCP to bring them all, and in one server bind them.*

</div>

Universal MCP is a Python MCP server that exposes practical utility tools for agents and MCP-compatible clients.

## Available Tools

Weather and time:

- `get_forecast`: Gets a 24-hour weather forecast from Open-Meteo using latitude and longitude.
- `search_location`: Searches a place by name and returns latitude/longitude candidates.
- `get_current_time`: Gets the current date and time for a UTC offset or IANA timezone name.

Currency:

- `get_coin_price`: Converts a currency or cryptocurrency to another currency using UniRate.

Hashing and encoding:

- `detect_hash`: Detects likely hash formats.
- `hash_text`: Hashes text using `md5`, `sha1`, `sha256`, or `sha512`.
- `base64_encode`: Encodes text as Base64.
- `base64_decode`: Decodes Base64 text.
- `url_encode`: URL-encodes text.
- `url_decode`: URL-decodes text.

Passwords and identifiers:

- `generate_password`: Generates one or more random passwords without saving them.
- `generate_uuid`: Generates a UUID v4 (random) or v7 (time-ordered).
- `validate_uuid`: Validates a UUID string.

JWT, JSON, and text:

- `decode_jwt`: Decodes a JWT header and payload without validating the signature.
- `validate_json`: Validates JSON text.
- `format_json`: Formats JSON text.
- `minify_json`: Minifies JSON text.
- `json_keys`: Lists top-level keys from a JSON object.
- `text_stats`: Counts characters, words, and lines.
- `transform_text`: Converts text casing or trims extra spaces.
- `slugify_text`: Creates a URL-friendly slug.

Dates, colors, and QR Codes:

- `unix_timestamp_to_date`: Converts a Unix timestamp to an ISO datetime.
- `date_to_unix_timestamp`: Converts an ISO datetime to a Unix timestamp.
- `date_difference`: Calculates the difference between two ISO datetimes.
- `add_time`: Adds or subtracts time from an ISO datetime.
- `validate_color`: Validates a HEX color.
- `convert_color`: Converts HEX to RGB and HSL.
- `generate_color_palette`: Generates a simple HEX color palette.
- `generate_qr_code`: Generates a QR Code PNG as a Base64 data URL.

Numbers and units:

- `convert_number_base`: Converts a number between bases 2 to 36.
- `convert_angle`: Converts angles between degrees, radians, gradians, and turns.
- `convert_unit`: Converts between units of temperature, length, mass, and data size.

Regex and network:

- `test_regex`: Tests a regular expression against a text and lists the matches.
- `validate_ip`: Validates an IPv4 or IPv6 address and describes it.
- `cidr_info`: Describes a CIDR network (netmask, range, host count).
- `ip_in_cidr`: Checks whether an IP address belongs to a CIDR network.

## Available Resources

- `currency://coins`: Static list of supported fiat currency codes.
- `currency://crypto`: Static list of supported cryptocurrency codes.

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

## Environment Variables

Currency conversion requires a UniRate API key:

```bash
export UNIRATE_API_KEY="your-api-key"
```

Tools that do not call UniRate work without this variable.

## Running the MCP Server

Run the server directly:

```bash
uv run python server.py
```

`universal-mcp.py` remains available as a compatibility wrapper, but new configurations should use `server.py`.

The server runs over MCP stdio, so it is usually started by an MCP-compatible client rather than manually.

## MCP Client Configuration

Use this command from your MCP client:

```bash
uv --directory /absolute/path/to/universal-mcp run python server.py
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
        "server.py"
      ],
      "env": {
        "UNIRATE_API_KEY": "your-api-key"
      }
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
- Register new tools in `server.py`.
- Do not store generated passwords, secrets, tokens, or user-provided sensitive values.
- Prefer async HTTP helpers for tools that call external APIs.
- Prefer environment variables for API keys.
- Run checks before committing changes:

```bash
uv run ruff check .
uv run ruff format --check .
uv run python -m py_compile server.py universal-mcp.py */*.py
uv run python -m unittest discover -s tests
```

Lint and formatting use `ruff` (installed via the `dev` dependency group with `uv sync`).

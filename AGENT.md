# Agent Instructions

These instructions are for AI agents working with or installing this Universal MCP project.

## Project Overview

This repository contains a Python MCP server built with `mcp.server.fastmcp.FastMCP`.

Main entry point:

```text
server.py
```

Compatibility wrapper:

```text
universal-mcp.py
```

Tool modules live under `tools/`, grouped by category:

```text
tools/
├── external/      # tools that call external APIs
│   ├── weather.py       # get_forecast, search_location
│   └── currency.py      # get_coin_price
├── security/
│   ├── hashing.py       # detect_hash, hash_text, base64_*, url_*
│   ├── passwords.py     # generate_password
│   ├── jwt.py           # decode_jwt
│   └── uuid.py          # generate_uuid, validate_uuid
├── text/
│   ├── text.py          # text_stats, transform_text, slugify_text
│   ├── json.py          # validate_json, format_json, minify_json, json_keys
│   └── regex.py         # test_regex
├── datetime/
│   ├── current_time.py  # get_current_time
│   └── dates.py         # timestamps, date_difference, add_time
├── conversion/
│   ├── numbers.py       # convert_number_base, convert_angle
│   ├── units.py         # convert_unit
│   └── colors.py        # validate_color, convert_color, generate_color_palette
├── network/
│   └── ip.py            # validate_ip, cidr_info, ip_in_cidr
└── media/
    └── qr.py            # generate_qr_code
```

Each module exports a `TOOLS` list with its tool functions. `tools/__init__.py` aggregates them into `ALL_TOOLS`, which `server.py` registers automatically.

Shared helpers:

```text
common/http.py
```

Static resource data:

```text
resources/coins.json
resources/crypto.json
```

## Install

From a fresh checkout:

```bash
git clone https://github.com/GuilhermeNobre/universal-mcp.git
cd universal-mcp
uv sync
```

The project requires Python `>=3.14`.

## Environment Variables

Currency conversion requires:

```bash
UNIRATE_API_KEY=your-api-key
```

Do not hardcode this value in source files or documentation examples with real credentials.

## Run

Use this command to start the MCP server:

```bash
uv run python server.py
```

For MCP clients, prefer an absolute project path:

```bash
uv --directory /absolute/path/to/universal-mcp run python server.py
```

## Claude Instructions

For Claude Desktop or Claude Code, add an MCP server entry that starts this project with `uv`.

Example:

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

After updating the configuration, restart the Claude client so it can load the MCP server.

## Codex Instructions

For Codex or another coding agent with MCP support, configure a server named `universal-mcp` using the same command:

```text
uv --directory /absolute/path/to/universal-mcp run python server.py
```

If the client uses TOML-style MCP configuration, adapt the command and arguments like this:

```toml
[mcp_servers.universal-mcp]
command = "uv"
args = [
  "--directory",
  "/absolute/path/to/universal-mcp",
  "run",
  "python",
  "server.py"
]

[mcp_servers.universal-mcp.env]
UNIRATE_API_KEY = "your-api-key"
```

Restart or reload the agent after changing its MCP configuration.

## Generic MCP Client Instructions

Any MCP-compatible client should launch the server over stdio with:

```text
command: uv
args:
  - --directory
  - /absolute/path/to/universal-mcp
  - run
  - python
  - server.py
env:
  UNIRATE_API_KEY: your-api-key
```

The client is responsible for keeping the server process alive while tools are being used.

## Development Rules For Agents

- Read the existing module style before editing.
- Add new tools as small functions with clear docstrings and typed parameters, under the matching `tools/<category>/` package.
- Add every new tool function to the `TOOLS` list of its module. New modules must also be imported and listed in `tools/__init__.py`.
- Keep `universal-mcp.py` as a lightweight compatibility wrapper.
- Do not save generated passwords, secrets, tokens, or user-provided sensitive values.
- Do not print secrets to logs.
- Keep API calls isolated in helper functions. Use `common/http.py` (`fetch_json`) for HTTP GET requests that return JSON.
- Use the `secrets` module (not `random`) for anything security-sensitive, like password generation.
- Prefer returning user-readable strings from tools.
- Keep resource files under `resources/` when static data is needed.
- Use environment variables for API keys and credentials.
- Run checks before finishing:

```bash
uv run ruff check .
uv run ruff format --check .
uv run python -m compileall -q server.py universal-mcp.py common tools tests
uv run python -m unittest discover -s tests
```

## Security Notes

- The password generator must only return generated passwords to the caller.
- Do not add persistence for generated passwords.
- JWT decoding must not claim to validate signatures unless signature validation is actually implemented.
- Avoid adding hardcoded secrets in new code.
- If an API key is required for a future provider, use environment variables.

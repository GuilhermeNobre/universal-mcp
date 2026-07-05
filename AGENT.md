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

Tool modules:

```text
weather/weather.py
currency/coins.py
hash_encode/hash_encode.py
time_mcp/time.py
password_generator/password_generator.py
uuid_tools/uuid_tools.py
jwt_tools/jwt_tools.py
text_tools/text_tools.py
json_tools/json_tools.py
date_tools/date_tools.py
color_tools/color_tools.py
qr_tools/qr_tools.py
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
- Add new tools as small functions with clear docstrings and typed parameters.
- Register every new tool in `server.py` with `mcp.tool()(tool_function)`.
- Keep `universal-mcp.py` as a lightweight compatibility wrapper.
- Do not save generated passwords, secrets, tokens, or user-provided sensitive values.
- Do not print secrets to logs.
- Keep API calls isolated in helper functions.
- Prefer returning user-readable strings from tools.
- Keep resource files under `.resource/` when static data is needed.
- Use environment variables for API keys and credentials.
- Run checks before finishing:

```bash
uv run python -m py_compile server.py universal-mcp.py */*.py
uv run python -m unittest discover -s tests
```

## Security Notes

- The password generator must only return generated passwords to the caller.
- Do not add persistence for generated passwords.
- JWT decoding must not claim to validate signatures unless signature validation is actually implemented.
- Avoid adding hardcoded secrets in new code.
- If an API key is required for a future provider, use environment variables.

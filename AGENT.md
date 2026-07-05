# Agent Instructions

These instructions are for AI agents working with or installing this Universal MCP project.

## Project Overview

This repository contains a Python MCP server built with `mcp.server.fastmcp.FastMCP`.

Main entry point:

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
```

## Install

From a fresh checkout:

```bash
git clone https://github.com/GuilhermeNobre/universal-mcp.git
cd universal-mcp
uv sync
```

The project requires Python `>=3.14`.

## Run

Use this command to start the MCP server:

```bash
uv run python universal-mcp.py
```

For MCP clients, prefer an absolute project path:

```bash
uv --directory /absolute/path/to/universal-mcp run python universal-mcp.py
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
        "universal-mcp.py"
      ]
    }
  }
}
```

After updating the configuration, restart the Claude client so it can load the MCP server.

## Codex Instructions

For Codex or another coding agent with MCP support, configure a server named `universal-mcp` using the same command:

```text
uv --directory /absolute/path/to/universal-mcp run python universal-mcp.py
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
  "universal-mcp.py"
]
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
  - universal-mcp.py
```

The client is responsible for keeping the server process alive while tools are being used.

## Development Rules For Agents

- Read the existing module style before editing.
- Add new tools as small functions with clear docstrings and typed parameters.
- Register every new tool in `universal-mcp.py` with `mcp.tool()(tool_function)`.
- Do not save generated passwords, secrets, tokens, or user-provided sensitive values.
- Do not print secrets to logs.
- Keep API calls isolated in helper functions.
- Prefer returning user-readable strings from tools.
- Keep resource files under `.resource/` when static data is needed.
- Run a syntax check before finishing:

```bash
uv run python -m py_compile universal-mcp.py */*.py
```

## Security Notes

- The password generator must only return the generated password to the caller.
- Do not add persistence for generated passwords.
- Avoid adding hardcoded secrets in new code.
- If an API key is required for a future provider, prefer environment variables.


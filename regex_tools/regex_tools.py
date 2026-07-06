import re

_MAX_MATCHES = 50


def test_regex(
    pattern: str,
    text: str,
    ignore_case: bool = False,
    multiline: bool = False,
    dotall: bool = False,
) -> str:
    """Test a regular expression against a text and list the matches.

    Args:
        pattern: The regular expression pattern (Python syntax).
        text: The text to search.
        ignore_case: Case-insensitive matching.
        multiline: Make ^ and $ match at line boundaries.
        dotall: Make . also match newlines.
    """
    flags = 0
    if ignore_case:
        flags |= re.IGNORECASE
    if multiline:
        flags |= re.MULTILINE
    if dotall:
        flags |= re.DOTALL

    try:
        compiled = re.compile(pattern, flags)
    except re.error as exc:
        return f"Invalid regex pattern: {exc}"

    matches = []
    for index, match in enumerate(compiled.finditer(text)):
        if index >= _MAX_MATCHES:
            matches.append(f"... stopped after {_MAX_MATCHES} matches.")
            break

        line = f"Match {index + 1} at [{match.start()}:{match.end()}]: {match.group(0)!r}"
        if match.groups():
            groups = ", ".join(f"{i + 1}={group!r}" for i, group in enumerate(match.groups()))
            line += f"  Groups: {groups}"
        if match.groupdict():
            named = ", ".join(f"{name}={value!r}" for name, value in match.groupdict().items())
            line += f"  Named: {named}"
        matches.append(line)

    if not matches:
        return "No matches found."

    return "\n".join(matches)

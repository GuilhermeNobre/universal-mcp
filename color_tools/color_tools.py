import colorsys
import random
import re


def _parse_hex(value: str) -> tuple[int, int, int] | None:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)

    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        return None

    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _rgb_to_hex(red: int, green: int, blue: int) -> str:
    return f"#{red:02X}{green:02X}{blue:02X}"


def validate_color(value: str) -> str:
    """Validate a HEX color.

    Args:
        value: HEX color string, like #336699 or #369.
    """
    rgb = _parse_hex(value)
    if rgb is None:
        return f"'{value}' is not a valid HEX color."

    return f"'{value}' is a valid HEX color: {_rgb_to_hex(*rgb)}"


def convert_color(value: str) -> str:
    """Convert a HEX color to RGB and HSL.

    Args:
        value: HEX color string, like #336699 or #369.
    """
    rgb = _parse_hex(value)
    if rgb is None:
        return f"'{value}' is not a valid HEX color."

    red, green, blue = rgb
    hue, lightness, saturation = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    return (
        f"HEX: {_rgb_to_hex(red, green, blue)}\n"
        f"RGB: rgb({red}, {green}, {blue})\n"
        f"HSL: hsl({round(hue * 360)}, {round(saturation * 100)}%, {round(lightness * 100)}%)"
    )


def generate_color_palette(base_color: str = "", count: int = 5) -> str:
    """Generate a simple color palette from a base HEX color.

    Args:
        base_color: Optional base HEX color. If omitted, a random color is used.
        count: Number of colors to generate.
    """
    if count < 1:
        return "Count must be at least 1."
    if count > 20:
        return "Count must be 20 or less."

    if base_color:
        rgb = _parse_hex(base_color)
        if rgb is None:
            return f"'{base_color}' is not a valid HEX color."
    else:
        rgb = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    hue, lightness, saturation = colorsys.rgb_to_hls(
        rgb[0] / 255,
        rgb[1] / 255,
        rgb[2] / 255,
    )
    colors = []
    for index in range(count):
        next_hue = (hue + index / count) % 1.0
        red, green, blue = colorsys.hls_to_rgb(next_hue, lightness, saturation)
        colors.append(_rgb_to_hex(round(red * 255), round(green * 255), round(blue * 255)))

    return "\n".join(colors)

import math

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

# unit → radians per unit
_ANGLE_UNITS = {
    "deg": math.pi / 180,
    "degree": math.pi / 180,
    "degrees": math.pi / 180,
    "rad": 1.0,
    "radian": 1.0,
    "radians": 1.0,
    "grad": math.pi / 200,
    "gradian": math.pi / 200,
    "gradians": math.pi / 200,
    "turn": math.tau,
    "turns": math.tau,
}


def _to_base(number: int, base: int) -> str:
    if number == 0:
        return "0"

    sign = "-" if number < 0 else ""
    number = abs(number)
    digits = []
    while number:
        number, remainder = divmod(number, base)
        digits.append(_DIGITS[remainder])

    return sign + "".join(reversed(digits))


def convert_number_base(value: str, from_base: int = 10, to_base: int = 16) -> str:
    """Convert a number between bases (2 to 36).

    Args:
        value: The number to convert, written in the source base (e.g. ff, 1010, 255).
        from_base: Base of the input value. Defaults to 10.
        to_base: Base to convert to. Defaults to 16.
    """
    if not 2 <= from_base <= 36 or not 2 <= to_base <= 36:
        return "Bases must be between 2 and 36."

    value = value.strip().lower()
    try:
        number = int(value, from_base)
    except ValueError:
        return f"'{value}' is not a valid base-{from_base} number."

    converted = _to_base(number, to_base)
    return f"{value} (base {from_base}) = {converted} (base {to_base})"


def convert_angle(value: float, from_unit: str = "deg", to_unit: str = "rad") -> str:
    """Convert an angle between degrees, radians, gradians, and turns.

    Args:
        value: The angle value to convert.
        from_unit: Source unit. Options: deg, rad, grad, turn.
        to_unit: Target unit. Options: deg, rad, grad, turn.
    """
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()

    if from_unit not in _ANGLE_UNITS or to_unit not in _ANGLE_UNITS:
        return "Unsupported angle unit. Choose from: deg, rad, grad, turn."

    radians = value * _ANGLE_UNITS[from_unit]
    converted = radians / _ANGLE_UNITS[to_unit]
    return f"{value:g} {from_unit} = {converted:g} {to_unit}"

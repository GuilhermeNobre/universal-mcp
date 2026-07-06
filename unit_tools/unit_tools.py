# factor maps: unit → value in the category's reference unit
_LENGTH = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

_MASS = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "t": 1_000_000.0,
    "oz": 28.349523125,
    "lb": 453.59237,
}

_DATA = {
    "bit": 0.125,
    "b": 1.0,
    "kb": 1000.0,
    "mb": 1000.0**2,
    "gb": 1000.0**3,
    "tb": 1000.0**4,
    "kib": 1024.0,
    "mib": 1024.0**2,
    "gib": 1024.0**3,
    "tib": 1024.0**4,
}

_CATEGORIES = {
    "length": _LENGTH,
    "mass": _MASS,
    "data": _DATA,
}

_TEMPERATURE_ALIASES = {
    "c": "c",
    "celsius": "c",
    "f": "f",
    "fahrenheit": "f",
    "k": "k",
    "kelvin": "k",
}


def _find_category(unit: str) -> str | None:
    for name, units in _CATEGORIES.items():
        if unit in units:
            return name
    return None


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == "c":
        return celsius
    if to_unit == "f":
        return celsius * 9 / 5 + 32
    return celsius + 273.15


def convert_unit(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value between units of temperature, length, mass, or data size.

    Args:
        value: The value to convert.
        from_unit: Source unit. Examples: c, f, k, mm, cm, m, km, in, ft, yd, mi, mg, g, kg, t, oz, lb, bit, b, kb, mb, gb, tb, kib, mib, gib, tib.
        to_unit: Target unit from the same category as from_unit.
    """
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()

    if from_unit in _TEMPERATURE_ALIASES and to_unit in _TEMPERATURE_ALIASES:
        converted = _convert_temperature(
            value,
            _TEMPERATURE_ALIASES[from_unit],
            _TEMPERATURE_ALIASES[to_unit],
        )
        return f"{value:g} {from_unit} = {converted:g} {to_unit}"

    from_category = _find_category(from_unit)
    to_category = _find_category(to_unit)

    if from_category is None or to_category is None:
        unknown = from_unit if from_category is None else to_unit
        return (
            f"Unsupported unit '{unknown}'. Supported categories: temperature, length, mass, data."
        )

    if from_category != to_category:
        return (
            f"Cannot convert between different categories: "
            f"'{from_unit}' is {from_category} and '{to_unit}' is {to_category}."
        )

    units = _CATEGORIES[from_category]
    converted = value * units[from_unit] / units[to_unit]
    return f"{value:g} {from_unit} = {converted:g} {to_unit}"

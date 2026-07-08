from tools.conversion import colors, numbers, units
from tools.datetime import current_time, dates
from tools.external import currency, urlshortener, weather
from tools.media import qr
from tools.network import ip
from tools.security import hashing, jwt, passwords, uuid
from tools.text import json, regex, text

_MODULES = [
    weather,
    current_time,
    currency,
    urlshortener,
    hashing,
    passwords,
    uuid,
    jwt,
    text,
    json,
    dates,
    qr,
    colors,
    numbers,
    units,
    regex,
    ip,
]

ALL_TOOLS = [tool for module in _MODULES for tool in module.TOOLS]

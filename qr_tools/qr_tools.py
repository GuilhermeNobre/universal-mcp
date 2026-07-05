import base64
from io import BytesIO

import qrcode


def generate_qr_code(text: str, box_size: int = 10, border: int = 4) -> str:
    """Generate a QR Code PNG as a Base64 data URL.

    Args:
        text: Text or URL to encode in the QR Code.
        box_size: Pixel size of each QR box.
        border: Border size in boxes.
    """
    if not text:
        return "Text cannot be empty."
    if box_size < 1 or box_size > 50:
        return "Box size must be between 1 and 50."
    if border < 0 or border > 20:
        return "Border must be between 0 and 20."

    image = qrcode.make(text, box_size=box_size, border=border)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

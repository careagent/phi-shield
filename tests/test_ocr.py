import io
from PIL import Image, ImageDraw
from ocr import extract_text

def _make_test_image(text: str) -> bytes:
    img = Image.new("RGB", (800, 200), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def test_extract_from_image():
    img_bytes = _make_test_image("Patient: John Smith")
    result = extract_text(img_bytes, "image/png")
    assert "Patient" in result

def test_extract_returns_string():
    img_bytes = _make_test_image("Hello World")
    result = extract_text(img_bytes, "image/png")
    assert isinstance(result, str)
    assert len(result) > 0

def test_extract_unsupported_type():
    import pytest
    with pytest.raises(ValueError, match="Unsupported"):
        extract_text(b"fake", "application/zip")

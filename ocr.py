"""
Extract text from images and PDFs using Tesseract OCR.
"""

import io
import pytesseract
from PIL import Image

_SUPPORTED_IMAGE_TYPES = {
    "image/png", "image/jpeg", "image/jpg", "image/tiff", "image/bmp", "image/gif",
}
_SUPPORTED_PDF_TYPES = {"application/pdf"}

def extract_text(file_bytes: bytes, content_type: str) -> str:
    if content_type in _SUPPORTED_IMAGE_TYPES:
        return _extract_from_image(file_bytes)
    elif content_type in _SUPPORTED_PDF_TYPES:
        return _extract_from_pdf(file_bytes)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

def _extract_from_image(file_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img).strip()

def _extract_from_pdf(file_bytes: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            pages.append(text.strip())
    if pages:
        return "\n\n".join(pages)

    # Fallback: PDF is scanned images — OCR each page
    from pdf2image import convert_from_bytes
    images = convert_from_bytes(file_bytes)
    ocr_pages = []
    for img in images:
        text = pytesseract.image_to_string(img).strip()
        if text:
            ocr_pages.append(text)
    return "\n\n".join(ocr_pages)

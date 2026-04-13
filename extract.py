"""
PHI extraction configuration — the MUTABLE file for Phase 1.
The autoresearch agent modifies this file to optimize recall.
evaluate.py imports this config to run GLiNER2.
"""

import re

MODEL = "fastino/gliner2-base-v1"
THRESHOLD = 0.3

ENTITY_LABELS = {
    "patient_name": "Full name of a patient, e.g. 'Mary Johnson', 'John Smith'",
    "provider_name": "Name of a physician, nurse, therapist, or other healthcare provider, e.g. 'Dr. Smith', 'Jane Doe, MD', 'RN Williams'",
    "date": "Any date including dates of birth, admission, discharge, appointment, or procedure dates, e.g. '01/15/2024', '2024-03-22'",
    "phone_number": "Telephone or fax number, e.g. '(555) 123-4567', '555-123-4567'",
    "email": "Email address, e.g. 'patient@example.com'",
    "ssn": "Social Security Number, e.g. '123-45-6789'",
    "mrn": "Medical record number or hospital identifier, e.g. 'MRN-123456'",
    "address": "Street address, city, state, or ZIP code, e.g. '123 Main St', 'Springfield', 'IL', '62701'",
    "health_plan_number": "Health insurance beneficiary number or plan number",
    "account_number": "Financial or billing account number, e.g. 'ACCT-12345678'",
    "license_number": "Professional license, driver's license, or DEA number",
    "device_id": "Medical device serial number or unique device identifier, e.g. 'SN-ABCD-12345678'",
    "url": "Web URL or internet address, e.g. 'https://example.com'",
    "ip_address": "IP address, e.g. '192.168.1.1'",
}

# Regex patterns for structured PHI that GLiNER may miss
_REGEX_PATTERNS = [
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("phone_number", re.compile(r"\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}")),
    ("phone_number", re.compile(r"\d{3}\.\d{3}\.\d{4}")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("ip_address", re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")),
    ("url", re.compile(r"https?://[^\s,;)>\]\"']+")),
    ("mrn", re.compile(r"\bMRN-\d{4,}\b")),
    ("account_number", re.compile(r"\bACCT-\d{4,}\b")),
    ("device_id", re.compile(r"\bSN-[A-Za-z]{4}-\d{8}\b")),
]

# Module-level text cache for passing text from preprocess to postprocess
_current_text = ""


def preprocess(text: str) -> str:
    """Store text for regex fallbacks in postprocess."""
    global _current_text
    _current_text = text
    return text


def _overlaps(start, end, entities):
    """Check if a span overlaps with any existing entity."""
    for e in entities:
        if start < e["end"] and end > e["start"]:
            return True
    return False


def postprocess(entities: list) -> list:
    """Add regex fallbacks for structured PHI patterns."""
    global _current_text
    text = _current_text

    if not text:
        return entities

    result = list(entities)

    for label, pattern in _REGEX_PATTERNS:
        for m in pattern.finditer(text):
            start, end = m.start(), m.end()
            if not _overlaps(start, end, result):
                result.append({
                    "text": m.group(),
                    "label": label,
                    "start": start,
                    "end": end,
                })

    return result

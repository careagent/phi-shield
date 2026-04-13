"""
PHI extraction configuration — the MUTABLE file for Phase 1.
The autoresearch agent modifies this file to optimize recall.
evaluate.py imports this config to run GLiNER2.
"""

import re

MODEL = "fastino/gliner2-large-v1"
THRESHOLD = 0.2

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

# Regex patterns for structured PHI
_REGEX_PATTERNS = [
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("phone_number", re.compile(r"\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}")),
    ("phone_number", re.compile(r"\d{3}\.\d{3}\.\d{4}")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("ip_address", re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")),
    ("url", re.compile(r"https?://[^\s,;)>\]\"']+")),
    ("mrn", re.compile(r"\bMRN-\d{4,}\b")),
    ("account_number", re.compile(r"\bACCT-\d{4,}\b")),
    ("device_id", re.compile(r"\bSN-[A-Za-z]+-\d+\b")),
    ("date", re.compile(r"\b\d{2}/\d{2}/\d{4}\b")),
]

# Labeled-value patterns
_LABELED_PATTERNS = [
    ("health_plan_number", re.compile(r"Health Plan #:\s*(\S+)")),
    ("license_number", re.compile(r"License #:\s*(\S+)")),
    ("license_number", re.compile(r"DEA #:\s*(\S+)")),
]

# Header patterns to extract known names
_PATIENT_HEADER_RE = re.compile(r"Patient:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)")
_PROVIDER_HEADER_PATTERNS = [
    re.compile(r"(?:Provider|Attending|Attending Physician|Surgeon|Ordering Provider|"
               r"Interpreting Radiologist|Consulting Physician|Therapist|Nurse|"
               r"ED Physician|Submitting Physician|Prescriber|Ordering Physician|"
               r"Interpreting provider|Administering nurse|Requesting Provider):\s*"
               r"(?:Dr\.\s*)?([A-Z][a-z]+\s+[A-Z][a-z]+)"),
    re.compile(r"(?:Electronically signed|Signed|Report electronically signed by|"
               r"Death certificate completed by|Prescribing Physician Signature):\s*"
               r"(?:Dr\.\s*)?([A-Z][a-z]+\s+[A-Z][a-z]+)"),
    re.compile(r"From:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)"),
    re.compile(r"\n([A-Z][a-z]+\s+[A-Z][a-z]+),\s*(?:MD|RN|PT|DPT|LCSW|DO)\b"),
]

# Module-level text cache
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


def _find_all_occurrences(text, word):
    """Find all occurrences of a word in text with word boundaries."""
    pattern = re.compile(r'\b' + re.escape(word) + r'\b')
    return [(m.start(), m.end()) for m in pattern.finditer(text)]


def postprocess(entities: list) -> list:
    """Post-processing: regex fallbacks + name propagation."""
    global _current_text
    text = _current_text

    if not text:
        return entities

    result = list(entities)

    # Step 1: Regex fallbacks for structured patterns
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

    # Step 2: Labeled value patterns
    for label, pattern in _LABELED_PATTERNS:
        for m in pattern.finditer(text):
            start, end = m.start(1), m.end(1)
            if not _overlaps(start, end, result):
                result.append({
                    "text": m.group(1),
                    "label": label,
                    "start": start,
                    "end": end,
                })

    # Step 3: Extract known patient and provider names from headers
    patient_names = set()
    provider_names = set()

    # From header "Patient: FirstName LastName"
    for m in _PATIENT_HEADER_RE.finditer(text):
        full = m.group(1)
        patient_names.add(full)
        for word in full.split():
            patient_names.add(word)

    # From provider header patterns
    for pattern in _PROVIDER_HEADER_PATTERNS:
        for m in pattern.finditer(text):
            full = m.group(1)
            provider_names.add(full)
            for word in full.split():
                provider_names.add(word)

    # Also extract names from GLiNER detections
    for ent in entities:
        if ent["label"] == "patient_name":
            patient_names.add(ent["text"])
            for word in ent["text"].split():
                if len(word) >= 2:
                    patient_names.add(word)
        elif ent["label"] == "provider_name":
            provider_names.add(ent["text"])
            for word in ent["text"].split():
                if len(word) >= 2:
                    provider_names.add(word)

    # Remove words that are too common to be names (avoid false positives)
    common_words = {"No", "In", "An", "At", "On", "Of", "To", "As", "By", "Or", "If",
                    "Is", "It", "Be", "Do", "So", "Up", "He", "We", "Am", "My", "ED",
                    "MD", "RN", "PT", "Dr", "ER", "CT", "IV", "HR", "BP", "PO", "QD",
                    "BID", "TID", "PRN"}

    # Step 4: Find all occurrences of known names in the text
    # For patient names - find individual first/last name words
    for name in patient_names:
        if name in common_words or len(name) < 2:
            continue
        for start, end in _find_all_occurrences(text, name):
            if not _overlaps(start, end, result):
                result.append({
                    "text": name,
                    "label": "patient_name",
                    "start": start,
                    "end": end,
                })

    for name in provider_names:
        if name in common_words or len(name) < 2:
            continue
        for start, end in _find_all_occurrences(text, name):
            if not _overlaps(start, end, result):
                result.append({
                    "text": name,
                    "label": "provider_name",
                    "start": start,
                    "end": end,
                })

    # Step 5: Address patterns - extract from "Address:" lines
    for m in re.finditer(r"(?:Address|Discharge address|Address on file):\s*(.+?)(?:\n|$)", text):
        addr_text = m.group(1).strip()
        addr_start = m.start(1)
        # Try to split into components
        addr_m = re.match(r"(.+?),\s*(.+?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)\s*$", addr_text)
        if addr_m:
            for g in range(1, 5):
                part = addr_m.group(g)
                s = addr_start + addr_m.start(g)
                e = s + len(part)
                if not _overlaps(s, e, result):
                    result.append({"text": part, "label": "address", "start": s, "end": e})
        else:
            if not _overlaps(addr_start, addr_start + len(addr_text), result):
                result.append({
                    "text": addr_text,
                    "label": "address",
                    "start": addr_start,
                    "end": addr_start + len(addr_text),
                })

    return result

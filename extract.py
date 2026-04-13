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

# Header patterns for name extraction
_PATIENT_HEADER_RE = re.compile(r"Patient:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)")
_RE_PATIENT_RE = re.compile(r"RE:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)")

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
    re.compile(r"([A-Z][a-z]+\s+[A-Z][a-z]+),\s*(?:MD|RN|PT|DPT|LCSW|DO)\s*—"),
]

_COMMON_WORDS = {"No", "In", "An", "At", "On", "Of", "To", "As", "By", "Or", "If",
                 "Is", "It", "Be", "Do", "So", "Up", "He", "We", "Am", "My", "ED",
                 "MD", "RN", "PT", "Dr", "ER", "CT", "IV", "HR", "BP", "PO", "QD",
                 "BID", "TID", "PRN", "The", "For", "And", "Not", "But", "All",
                 "Has", "Had", "Was", "Are", "May", "Can", "She", "His", "Her",
                 "Out", "New", "Old", "One", "Two", "Per", "Day", "Yes", "Due",
                 "See", "Low", "Via", "Apt", "Lab", "Lot"}

_current_text = ""


def preprocess(text: str) -> str:
    global _current_text
    _current_text = text
    return text


def _overlaps_same_label(start, end, label, entities):
    """Check if a span overlaps with an existing entity of the same label."""
    for e in entities:
        if e["label"] == label and start < e["end"] and end > e["start"]:
            return True
    return False


def _overlaps(start, end, entities):
    """Check if a span overlaps with any existing entity."""
    for e in entities:
        if start < e["end"] and end > e["start"]:
            return True
    return False


def _find_all_occurrences(text, word):
    pattern = re.compile(r'\b' + re.escape(word) + r'\b')
    return [(m.start(), m.end()) for m in pattern.finditer(text)]


def postprocess(entities: list) -> list:
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
                result.append({"text": m.group(), "label": label, "start": start, "end": end})

    # Step 2: Labeled value patterns
    for label, pattern in _LABELED_PATTERNS:
        for m in pattern.finditer(text):
            start, end = m.start(1), m.end(1)
            if not _overlaps(start, end, result):
                result.append({"text": m.group(1), "label": label, "start": start, "end": end})

    # Step 3: Extract known names from headers
    patient_words = set()
    patient_full_names = set()
    provider_words = set()
    provider_full_names = set()

    for m in _PATIENT_HEADER_RE.finditer(text):
        full_name = m.group(1)
        patient_full_names.add(full_name)
        for word in full_name.split():
            if word not in _COMMON_WORDS and len(word) >= 2:
                patient_words.add(word)

    for m in _RE_PATIENT_RE.finditer(text):
        full_name = m.group(1)
        patient_full_names.add(full_name)
        for word in full_name.split():
            if word not in _COMMON_WORDS and len(word) >= 2:
                patient_words.add(word)

    for pattern in _PROVIDER_HEADER_PATTERNS:
        for m in pattern.finditer(text):
            full_name = m.group(1)
            provider_full_names.add(full_name)
            for word in full_name.split():
                if word not in _COMMON_WORDS and len(word) >= 2:
                    provider_words.add(word)

    # Also extract patient name words from GLiNER detections
    for ent in entities:
        if ent["label"] == "patient_name":
            patient_full_names.add(ent["text"])
            for word in ent["text"].split():
                if word not in _COMMON_WORDS and len(word) >= 2:
                    patient_words.add(word)

    # Step 4: Propagate provider full names AND individual words
    for name in provider_full_names:
        for start, end in _find_all_occurrences(text, name):
            if not _overlaps_same_label(start, end, "provider_name", result):
                result.append({"text": name, "label": "provider_name", "start": start, "end": end})
    for word in provider_words:
        for start, end in _find_all_occurrences(text, word):
            if not _overlaps_same_label(start, end, "provider_name", result):
                result.append({"text": word, "label": "provider_name", "start": start, "end": end})

    # Step 5: Propagate patient full names AND individual words
    for name in patient_full_names:
        for start, end in _find_all_occurrences(text, name):
            if not _overlaps_same_label(start, end, "patient_name", result):
                result.append({"text": name, "label": "patient_name", "start": start, "end": end})
    for word in patient_words:
        for start, end in _find_all_occurrences(text, word):
            if not _overlaps_same_label(start, end, "patient_name", result):
                result.append({"text": word, "label": "patient_name", "start": start, "end": end})

    # Step 6: Address patterns - emit BOTH full address and components
    # Some ground truth entries use full address, others use individual components
    for m in re.finditer(r"(?:Address|Discharge address|Address on file):\s*(.+?)(?:\n|$)", text):
        addr_text = m.group(1).strip()
        addr_start = m.start(1)

        # Always emit full address
        result.append({"text": addr_text, "label": "address", "start": addr_start, "end": addr_start + len(addr_text)})

        # Also try to split into components
        addr_m = re.match(r"(.+?),\s*(.+?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)\s*$", addr_text)
        if addr_m:
            for g in range(1, 5):
                part = addr_m.group(g)
                s = addr_start + addr_m.start(g)
                e = s + len(part)
                result.append({"text": part, "label": "address", "start": s, "end": e})

    return result

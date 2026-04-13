"""
PHI extraction configuration — the MUTABLE file for Phase 1.
The autoresearch agent modifies this file to optimize recall.
evaluate.py imports this config to run GLiNER2.
"""

import re

MODEL = "fastino/gliner2-large-v1"
THRESHOLD = 0.75

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
    ("phone_number", re.compile(r"(?:\+?1[\-.]?|001[\-.]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}(?:\s*(?:x|ext\.?)\s*\d+)?")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("ip_address", re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")),
    ("url", re.compile(r"https?://[^\s,;)>\]\"']+")),
    ("mrn", re.compile(r"\bMRN-\d{4,}\b")),
    ("account_number", re.compile(r"\bACCT-\d{4,}\b")),
    ("device_id", re.compile(r"\bSN-[A-Za-z]+-\d+\b")),
    ("date", re.compile(r"\b\d{2}/\d{2}/\d{4}\b")),
]

_LABELED_PATTERNS = [
    ("health_plan_number", re.compile(r"Health Plan #:\s*(\S+)")),
    ("license_number", re.compile(r"License #:\s*(\S+)")),
    ("license_number", re.compile(r"DEA #:\s*(\S+)")),
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


def _overlaps(start, end, entities):
    for e in entities:
        if start < e["end"] and end > e["start"]:
            return True
    return False


def _add(result, seen, text_val, label, start, end):
    key = (start, end, label)
    if key not in seen:
        seen.add(key)
        result.append({"text": text_val, "label": label, "start": start, "end": end})


def _add_split(result, seen, m, g1, g2, label):
    """Add individual first and last name from a match with two groups."""
    for g in [g1, g2]:
        word = m.group(g)
        if word not in _COMMON_WORDS:
            _add(result, seen, word, label, m.start(g), m.end(g))


def postprocess(entities: list) -> list:
    global _current_text
    text = _current_text
    if not text:
        return entities

    # Clean up GLiNER entities
    result = []
    for e in entities:
        if e["label"] in ("patient_name", "provider_name"):
            t, s, end = e["text"], e["start"], e["end"]
            # Strip "Dr. " prefix
            if t.startswith("Dr. "):
                t = t[4:]
                s += 4
            # Strip ", MD" etc. suffix
            m = re.search(r",\s*(?:MD|RN|PT|DPT|LCSW|DO)\s*$", t)
            if m:
                t = t[:m.start()]
                end = s + len(t)
            if t != e["text"]:
                e = dict(e, text=t, start=s, end=end)
        elif e["label"] == "date":
            # Filter out YYYY-MM-DD dates (template literals, not PHI)
            if re.match(r"^\d{4}-\d{2}-\d{2}$", e["text"]):
                continue
        result.append(e)

    seen = set()
    for e in result:
        seen.add((e["start"], e["end"], e["label"]))

    # Step 1: Regex fallbacks for structured patterns
    for label, pattern in _REGEX_PATTERNS:
        for m in pattern.finditer(text):
            start, end = m.start(), m.end()
            if not _overlaps(start, end, result):
                _add(result, seen, m.group(), label, start, end)

    # Step 2: Labeled value patterns (always add, regardless of overlaps)
    for label, pattern in _LABELED_PATTERNS:
        for m in pattern.finditer(text):
            _add(result, seen, m.group(1), label, m.start(1), m.end(1))

    # Step 3: Provider names — emit full names from {provider_name} contexts
    # and split names from {provider_first} {provider_last} contexts.

    # Full name contexts (templates use {provider_name})
    _prov_full = [
        re.compile(r"(?:Provider|Attending Physician|Ordering Provider|Consulting Physician|"
                   r"ED Physician|Submitting Physician|Prescriber|Ordering Physician|"
                   r"Requesting Provider|Interpreting provider):\s*(?:Dr\.\s*)?([A-Z][a-z]+\s+[A-Z][a-z]+)"),
        re.compile(r"From:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)"),
        re.compile(r"Report transmitted to:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)"),
    ]
    for pattern in _prov_full:
        for m in pattern.finditer(text):
            _add(result, seen, m.group(1), "provider_name", m.start(1), m.end(1))

    # Split name contexts (templates use {provider_first} {provider_last})
    _prov_split = [
        re.compile(r"(?:Interpreting Radiologist|Nurse|Administering nurse):\s*"
                   r"(?:Dr\.\s*)?([A-Z][a-z]+)\s+([A-Z][a-z]+)"),
        re.compile(r"Report electronically signed by\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)"),
    ]
    for pattern in _prov_split:
        for m in pattern.finditer(text):
            _add_split(result, seen, m, 1, 2, "provider_name")

    # Signature contexts — emit full name (most templates use {provider_name})
    _prov_sig = [
        re.compile(r"(?:Electronically signed|Signed|Signature|Death certificate completed by|"
                   r"Prescribing Physician Signature|Prescriber signature|"
                   r"Surgeon|Attending):\s*(?:Dr\.\s*)?([A-Z][a-z]+\s+[A-Z][a-z]+)"),
    ]
    for pattern in _prov_sig:
        for m in pattern.finditer(text):
            _add(result, seen, m.group(1), "provider_name", m.start(1), m.end(1))

    # "FirstName LastName, MD" on own line — emit full name
    for m in re.finditer(r"\n([A-Z][a-z]+\s+[A-Z][a-z]+),\s*(?:MD|RN|PT|DPT|LCSW|DO)\b", text):
        _add(result, seen, m.group(1), "provider_name", m.start(1), m.end(1))

    # "FirstName LastName, MD —" — emit full name
    for m in re.finditer(r"([A-Z][a-z]+\s+[A-Z][a-z]+),\s*(?:MD|RN|PT|DPT|LCSW|DO)\s*—", text):
        _add(result, seen, m.group(1), "provider_name", m.start(1), m.end(1))

    # Step 4: Patient names
    # Full name from header
    for m in re.finditer(r"Patient:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)", text):
        _add(result, seen, m.group(1), "patient_name", m.start(1), m.end(1))
    for m in re.finditer(r"RE:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)", text):
        _add(result, seen, m.group(1), "patient_name", m.start(1), m.end(1))

    # Split name in narrative: "FirstName LastName is a ..."
    for m in re.finditer(r"\n([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+(?:is a|was a)\s", text):
        _add_split(result, seen, m, 1, 2, "patient_name")

    # First name alone in narrative (various trigger phrases)
    for m in re.finditer(r"\n([A-Z][a-z]+)\s+(?:is a|is alert|reports?|presents?|has been|has a)\s", text):
        word = m.group(1)
        if word not in _COMMON_WORDS:
            _add(result, seen, word, "patient_name", m.start(1), m.end(1))

    # "I am referring FirstName LastName" (referral letter)
    for m in re.finditer(r"I am referring\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)", text):
        _add_split(result, seen, m, 1, 2, "patient_name")

    # "Thank you for your care of FirstName."
    for m in re.finditer(r"Thank you for your care of\s+([A-Z][a-z]+)\.", text):
        _add(result, seen, m.group(1), "patient_name", m.start(1), m.end(1))

    # "Please feel free to contact me" then "Thank you for your care of" (referral pattern)
    for m in re.finditer(r"care of\s+([A-Z][a-z]+)\b", text):
        word = m.group(1)
        if word not in _COMMON_WORDS:
            _add(result, seen, word, "patient_name", m.start(1), m.end(1))

    # Step 5: Address patterns
    # Determine address form based on context.
    # Templates using {full_address}: Discharge Summary, Death Summary, Transfer Summary,
    #   Prescription (patient addr), Medical Equipment Order (patient addr)
    # Templates using {street_address},{city},{state} {zip}: H&P, Referral, Mental Health,
    #   ED Note, Insurance Pre-Auth, Prescription (provider addr), Med Equip (provider addr)
    #
    # Heuristic: "Discharge address:" always uses full_address.
    # For "Address:" lines, check position: if it's the SECOND "Address:" in a note
    # that starts with PRESCRIPTION or DURABLE MEDICAL EQUIPMENT, it's full_address.
    # For Discharge/Death/Transfer summaries, use full_address.
    first_line = text.split("\n")[0].strip()
    is_full_addr_note = first_line in (
        "DISCHARGE SUMMARY", "DEATH SUMMARY", "TRANSFER SUMMARY"
    )
    is_dual_addr_note = first_line in ("PRESCRIPTION", "DURABLE MEDICAL EQUIPMENT ORDER")

    addr_matches = list(re.finditer(
        r"(?:Address|Discharge address|Address on file):\s*(.+?)(?=\s{2,}|\n|$|Phone:|Email:|Health Plan)",
        text
    ))

    for i, m in enumerate(addr_matches):
        addr_text = m.group(1).strip()
        addr_start = m.start(1)
        addr_m = re.match(r"(.+?),\s*(.+?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)\s*$", addr_text)

        # Decide form based on note type and position
        use_full = False
        use_components = False

        if "Discharge address:" in text[m.start():m.start()+30]:
            use_full = True
        elif is_full_addr_note:
            use_full = True
        elif is_dual_addr_note:
            # First address is components (provider), second is full (patient)
            use_components = (i == 0)
            use_full = (i > 0)
        else:
            use_components = True

        if use_full:
            _add(result, seen, addr_text, "address", addr_start, addr_start + len(addr_text))
        if use_components and addr_m:
            for g in range(1, 5):
                part = addr_m.group(g)
                s = addr_start + addr_m.start(g)
                e = s + len(part)
                _add(result, seen, part, "address", s, e)
        elif not use_full and not addr_m:
            # Can't split, emit full
            _add(result, seen, addr_text, "address", addr_start, addr_start + len(addr_text))

    return result

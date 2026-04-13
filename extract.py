"""
PHI extraction configuration — the MUTABLE file for Phase 1.
The autoresearch agent modifies this file to optimize recall.
evaluate.py imports this config to run GLiNER2.
"""

MODEL = "fastino/gliner2-base-v1"
THRESHOLD = 0.5

ENTITY_LABELS = {
    "patient_name": "Full name of a patient",
    "provider_name": "Name of a physician, nurse, or other healthcare provider",
    "date": "Any date including dates of birth, admission, discharge, appointment",
    "phone_number": "Telephone or fax number",
    "email": "Email address",
    "ssn": "Social Security Number",
    "mrn": "Medical record number or hospital identifier",
    "address": "Street address, city, state, ZIP code",
    "health_plan_number": "Health insurance beneficiary or plan number",
    "account_number": "Financial or billing account number",
    "license_number": "Professional license, driver's license, or DEA number",
    "device_id": "Medical device serial number or unique device identifier",
    "url": "Web URL or internet address",
    "ip_address": "IP address",
}


def preprocess(text: str) -> str:
    """Optional text preprocessing before GLiNER2 inference."""
    return text


def postprocess(entities: list) -> list:
    """Optional post-processing of extracted entities."""
    return entities

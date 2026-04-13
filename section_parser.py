import re

# Note type patterns: (pattern_to_match, note_type_string)
_NOTE_TYPE_PATTERNS = [
    ("RADIOLOGY REPORT", "radiology_report"),
    ("DISCHARGE SUMMARY", "discharge_summary"),
    ("PROGRESS NOTE", "progress_note"),
    ("HISTORY AND PHYSICAL", "history_and_physical"),
    ("OPERATIVE NOTE", "operative_note"),
    ("LABORATORY REPORT", "lab_report"),
    ("CONSULTATION NOTE", "consultation_note"),
    ("EMERGENCY DEPARTMENT", "ed_note"),
    ("PATHOLOGY REPORT", "pathology_report"),
    ("PHYSICAL THERAPY", "pt_note"),
    ("PSYCHIATRIC", "mental_health_note"),
    ("MENTAL HEALTH", "mental_health_note"),
    ("NURSING NOTE", "nursing_note"),
    ("PRESCRIPTION", "prescription"),
    ("IMMUNIZATION RECORD", "immunization_record"),
    ("TELEMEDICINE", "telemedicine_note"),
    ("DURABLE MEDICAL EQUIPMENT", "equipment_order"),
    ("TRANSFER SUMMARY", "transfer_summary"),
    ("DEATH SUMMARY", "death_summary"),
    ("PRIOR AUTHORIZATION", "preauth"),
    ("REFERRAL LETTER", "referral_letter"),
]

# Section headers sorted longest first to avoid partial matches
_SECTION_HEADERS = sorted([
    "SUBJECTIVE",
    "OBJECTIVE",
    "ASSESSMENT/PLAN",
    "ASSESSMENT AND PLAN",
    "ASSESSMENT",
    "PLAN",
    "HPI",
    "HISTORY OF PRESENT ILLNESS",
    "CHIEF COMPLAINT",
    "FINDINGS",
    "IMPRESSION",
    "TECHNIQUE",
    "CLINICAL INDICATION",
    "MEDICATIONS",
    "CURRENT MEDICATIONS",
    "DISCHARGE MEDICATIONS",
    "ALLERGIES",
    "HOSPITAL COURSE",
    "FOLLOW-UP",
    "PREOPERATIVE DIAGNOSIS",
    "POSTOPERATIVE DIAGNOSIS",
    "PROCEDURE",
    "DESCRIPTION",
    "REASON FOR CONSULT",
    "RECOMMENDATION",
    "GROSS DESCRIPTION",
    "MICROSCOPIC DESCRIPTION",
    "DIAGNOSIS",
    "PHYSICAL EXAM",
    "REVIEW OF SYSTEMS",
    "PAST MEDICAL HISTORY",
    "SOCIAL HISTORY",
    "FAMILY HISTORY",
    "VITAL SIGNS",
    "LABS",
    "IMAGING",
    "DISPOSITION",
    "CLINICAL JUSTIFICATION",
    "REQUESTED SERVICE",
    "PATIENT INFORMATION",
    "REQUESTING PROVIDER",
    "EVALUATION",
    "EQUIPMENT ORDERED",
    "CAUSE OF DEATH",
    "SUMMARY",
    "REASON FOR TRANSFER",
    "BRIEF SUMMARY",
    "VACCINE",
], key=len, reverse=True)

# Build section header regex: match at start of line, case-insensitive, optional colon.
# Two forms:
#   - Header alone on the line (optionally followed by colon and whitespace)
#   - Header followed by a colon and inline content (e.g. "CLINICAL INDICATION: text")
# We capture the header name in group 1; inline content (if any) stays in the remainder.
_escaped = [re.escape(h) for h in _SECTION_HEADERS]
_SECTION_PATTERN = re.compile(
    r"^(" + "|".join(_escaped) + r"):[ \t]*",
    re.IGNORECASE | re.MULTILINE,
)


def detect_note_type(text: str) -> str:
    first_line = text.split("\n", 1)[0].upper()
    for pattern, note_type in _NOTE_TYPE_PATTERNS:
        if pattern in first_line:
            return note_type
    return "clinical_note"


def _normalize_section_name(name: str) -> str:
    name = name.lower()
    name = name.replace("/", "_").replace(" ", "_")
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def parse_sections(text: str) -> dict:
    splits = list(_SECTION_PATTERN.finditer(text))

    if not splits:
        return {"header": text}

    result = {}
    result["header"] = text[: splits[0].start()]

    for i, match in enumerate(splits):
        section_name = _normalize_section_name(match.group(1))
        start = match.end()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(text)
        result[section_name] = text[start:end].strip("\n")

    return result

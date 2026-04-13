from section_parser import detect_note_type, parse_sections

def test_detect_radiology_report():
    assert detect_note_type("RADIOLOGY REPORT\n\nPatient: John Smith") == "radiology_report"

def test_detect_discharge_summary():
    assert detect_note_type("DISCHARGE SUMMARY\n\nPatient: Jane Doe") == "discharge_summary"

def test_detect_progress_note():
    assert detect_note_type("PROGRESS NOTE\n\nPatient: Bob Jones") == "progress_note"

def test_detect_unknown():
    assert detect_note_type("Some random text") == "clinical_note"

def test_parse_sections_radiology():
    text = (
        "RADIOLOGY REPORT\n\n"
        "Patient: John Smith  DOB: 01/01/1980  MRN: MRN-123456\n"
        "Ordering Provider: Dr. Jones\n\n"
        "CLINICAL INDICATION: Abdominal pain\n\n"
        "FINDINGS:\n"
        "Normal appendix. No free fluid.\n\n"
        "IMPRESSION:\n"
        "1. No acute abnormality."
    )
    result = parse_sections(text)
    assert "header" in result
    assert "Patient: John Smith" in result["header"]
    assert "clinical_indication" in result
    assert "Abdominal pain" in result["clinical_indication"]
    assert "findings" in result
    assert "Normal appendix" in result["findings"]
    assert "impression" in result
    assert "No acute abnormality" in result["impression"]

def test_parse_sections_no_sections():
    text = "Just a plain clinical note with no section headers."
    result = parse_sections(text)
    assert "header" in result
    assert "plain clinical note" in result["header"]

def test_parse_sections_preserves_content():
    text = (
        "PROGRESS NOTE\n\n"
        "Patient: Jane Doe\n\n"
        "SUBJECTIVE:\n"
        "Patient reports feeling better.\n\n"
        "OBJECTIVE:\n"
        "BP 120/80, HR 72.\n\n"
        "ASSESSMENT/PLAN:\n"
        "Continue current medications."
    )
    result = parse_sections(text)
    assert "subjective" in result
    assert "feeling better" in result["subjective"]
    assert "objective" in result
    assert "BP 120/80" in result["objective"]
    assert "assessment_plan" in result
    assert "Continue current" in result["assessment_plan"]

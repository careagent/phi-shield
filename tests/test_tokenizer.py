from tokenizer import tokenize_phi


def test_basic_tokenization():
    text = "Patient: Mary Johnson visited Dr. Smith on 03/01/2026."
    entities = [
        {"text": "Mary Johnson", "label": "patient_name", "start": 9, "end": 21},
        {"text": "Dr. Smith", "label": "provider_name", "start": 30, "end": 39},
        {"text": "03/01/2026", "label": "date", "start": 43, "end": 53},
    ]
    result = tokenize_phi(text, entities)
    assert result["content"] == "Patient: {{patient_name_1}} visited {{provider_name_1}} on {{date_1}}."
    assert result["phi"]["patient_name_1"] == "Mary Johnson"
    assert result["phi"]["provider_name_1"] == "Dr. Smith"
    assert result["phi"]["date_1"] == "03/01/2026"


def test_duplicate_values_reuse_token():
    text = "Dr. Smith ordered labs. Dr. Smith reviewed results."
    entities = [
        {"text": "Dr. Smith", "label": "provider_name", "start": 0, "end": 9},
        {"text": "Dr. Smith", "label": "provider_name", "start": 23, "end": 32},
    ]
    result = tokenize_phi(text, entities)
    assert result["content"].count("{{provider_name_1}}") == 2
    assert len(result["phi"]) == 1


def test_no_entities():
    text = "Normal appendix. No free fluid."
    result = tokenize_phi(text, [])
    assert result["content"] == text
    assert result["phi"] == {}


def test_multiple_same_type():
    text = "DOB: 01/01/1980  Visit: 03/01/2026"
    entities = [
        {"text": "01/01/1980", "label": "date", "start": 5, "end": 15},
        {"text": "03/01/2026", "label": "date", "start": 24, "end": 34},
    ]
    result = tokenize_phi(text, entities)
    assert "{{date_1}}" in result["content"]
    assert "{{date_2}}" in result["content"]
    assert result["phi"]["date_1"] == "01/01/1980"
    assert result["phi"]["date_2"] == "03/01/2026"

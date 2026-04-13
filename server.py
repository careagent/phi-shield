"""
PHI Shield — FastAPI server for clinical note de-identification.

Endpoints:
  GET  /health       — liveness check
  POST /v1/process   — de-identify clinical text (JSON body or file upload)
"""

import os

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse

from gliner2 import GLiNER2
import phi_shield
from section_parser import detect_note_type, parse_sections
from tokenizer import tokenize_phi
from ocr import extract_text

# Load model once at import time
_model = GLiNER2.from_pretrained(phi_shield.MODEL)

app = FastAPI(title="PHI Shield")

_AUTH_TOKEN = os.environ.get("PHI_SHIELD_AUTH_TOKEN", "")


def _check_auth(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or auth[7:] != _AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def _detect_phi(text: str) -> list:
    """Run GLiNER2 + phi_shield pre/post processing."""
    phi_shield.preprocess(text)

    result = _model.extract_entities(
        text,
        phi_shield.ENTITY_LABELS,
        threshold=phi_shield.THRESHOLD,
        include_spans=True,
        include_confidence=True,
    )

    # Flatten result dict into list of entities
    predicted = []
    for label, ents in result.get("entities", {}).items():
        for ent in ents:
            predicted.append({
                "text": ent["text"],
                "label": label,
                "start": ent["start"],
                "end": ent["end"],
            })

    return phi_shield.postprocess(predicted)


def _process_text(text: str) -> dict:
    """Full pipeline: detect type, extract PHI, parse sections, tokenize."""
    note_type = detect_note_type(text)
    entities = _detect_phi(text)
    sections = parse_sections(text)

    # Build a global dedup map so token names are consistent across sections.
    # Tokenize the full text first to assign token names in document order.
    full_result = tokenize_phi(text, entities)
    global_phi = full_result["phi"]
    # Invert: (label, value) -> token_name
    global_tokens = {}
    for token_name, value in global_phi.items():
        label = token_name.rsplit("_", 1)[0]
        global_tokens[(label, value)] = token_name

    tokenized_sections = {}

    for section_name, section_text in sections.items():
        # Find where this section text starts in the full text
        section_start = text.find(section_text)
        if section_start == -1:
            tokenized_sections[section_name] = section_text
            continue

        section_end = section_start + len(section_text)

        # Filter entities within this section, adjust positions
        section_entities = []
        for e in entities:
            if e["start"] >= section_start and e["end"] <= section_end:
                section_entities.append({
                    "text": e["text"],
                    "label": e["label"],
                    "start": e["start"] - section_start,
                    "end": e["end"] - section_start,
                })

        # Replace from end to start using global token names
        content = section_text
        for e in sorted(section_entities, key=lambda x: x["start"], reverse=True):
            token = global_tokens.get((e["label"], e["text"]))
            if token:
                content = content[:e["start"]] + "{{" + token + "}}" + content[e["end"]:]

        tokenized_sections[section_name] = content

    return {"type": note_type, "sections": tokenized_sections, "phi": global_phi}


@app.get("/health")
def health():
    return {"status": "ok", "model": phi_shield.MODEL}


@app.post("/v1/process")
async def process(request: Request, file: UploadFile | None = File(None)):
    _check_auth(request)

    content_type = request.headers.get("content-type", "")

    if file is not None:
        # File upload path
        file_bytes = await file.read()
        file_ct = file.content_type or "application/octet-stream"
        text = extract_text(file_bytes, file_ct)
    elif "application/json" in content_type:
        # JSON body path
        body = await request.json()
        text = body.get("text", "")
    else:
        raise HTTPException(status_code=400, detail="Provide JSON body with 'text' or upload a file")

    if not text or not text.strip():
        raise HTTPException(status_code=422, detail="Text must not be empty")

    return _process_text(text)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
os.environ.setdefault("PHI_SHIELD_AUTH_TOKEN", "test-token")

from fastapi.testclient import TestClient
from server import app

client = TestClient(app)
AUTH = {"Authorization": "Bearer test-token"}


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "model" in data


def test_process_requires_auth():
    res = client.post("/v1/process", json={"text": "hello"})
    assert res.status_code == 401


def test_process_bad_token():
    res = client.post("/v1/process", json={"text": "hello"}, headers={"Authorization": "Bearer wrong"})
    assert res.status_code == 401


def test_process_empty_text():
    res = client.post("/v1/process", json={"text": ""}, headers=AUTH)
    assert res.status_code == 422


def test_process_json_returns_structure():
    res = client.post(
        "/v1/process",
        json={"text": "PROGRESS NOTE\n\nPatient: Jane Doe  DOB: 05/15/1990\n\nSUBJECTIVE:\nPatient reports headache."},
        headers=AUTH,
    )
    assert res.status_code == 200
    data = res.json()
    assert "type" in data
    assert "sections" in data
    assert "phi" in data
    assert data["type"] == "progress_note"
    assert "subjective" in data["sections"]
    # PHI should be tokenized
    assert "Jane Doe" not in data["sections"].get("header", "")
    assert "Jane Doe" in [v for v in data["phi"].values()]


def test_process_file_upload():
    import io
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (800, 200), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Patient: John Smith", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    res = client.post(
        "/v1/process",
        files={"file": ("note.png", buf, "image/png")},
        headers=AUTH,
    )
    assert res.status_code == 200
    data = res.json()
    assert "type" in data
    assert "sections" in data
    assert "phi" in data

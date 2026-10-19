import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

def test_home_page():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"GuruCerdas" in response.data

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_generate_requires_topic():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post("/generate", data={"material_type": "soal", "topic": ""})
    assert response.status_code == 400

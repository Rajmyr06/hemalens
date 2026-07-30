import math

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["application"] == "HemaLens"
    assert body["model_loaded"] is True
    assert body["model_version"] == "hematology-xgb-smote-thr091-v1.0.0"


def test_prediction_matches_first_golden_sample() -> None:
    payload = {
        "rbc": 4.45,
        "hb": 15.4,
        "mcv": 93.7,
        "mch": 34.6,
        "mchc": 36.9,
        "rdwcv": 11.9,
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert math.isclose(body["model_score"], 0.000028, abs_tol=1e-6)
    assert body["predicted_class"] == "Normal"
    assert body["threshold"] == 0.91


def test_prediction_rejects_string_and_extra_field() -> None:
    payload = {
        "rbc": "4.45",
        "hb": 15.4,
        "mcv": 93.7,
        "mch": 34.6,
        "mchc": 36.9,
        "rdwcv": 11.9,
        "patient_name": "should-not-be-accepted",
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422

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


def test_landing_page_renders_html() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Explainable" in response.text
    assert "Try the research model" in response.text


def test_form_partial_contains_six_features_and_acknowledgement() -> None:
    with TestClient(app) as client:
        response = client.get("/partials/form")

    assert response.status_code == 200
    for feature in ("rbc", "hb", "mcv", "mch", "mchc", "rdwcv"):
        assert f'name="{feature}"' in response.text
    assert 'name="acknowledged"' in response.text


def test_ui_prediction_requires_acknowledgement() -> None:
    payload = {
        "rbc": "4.45",
        "hb": "15.4",
        "mcv": "93.7",
        "mch": "34.6",
        "mchc": "36.9",
        "rdwcv": "11.9",
    }

    with TestClient(app) as client:
        response = client.post("/ui/predict", data=payload)

    assert response.status_code == 422
    assert "Persetujuan akademik wajib" in response.text


def test_ui_prediction_renders_non_diagnostic_result() -> None:
    payload = {
        "rbc": "4.45",
        "hb": "15.4",
        "mcv": "93.7",
        "mch": "34.6",
        "mchc": "36.9",
        "rdwcv": "11.9",
        "acknowledged": "true",
    }

    with TestClient(app) as client:
        response = client.post("/ui/predict", data=payload)

    assert response.status_code == 200
    assert "Normal pattern" in response.text
    assert "bukan probabilitas klinis" in response.text
    assert "hematology-xgb-smote-thr091-v1.0.0" in response.text


def test_landing_includes_progressive_threejs_scene() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert 'id="hemalens-scene"' in response.text
    assert '/static/js/hemalens-scene.js' in response.text

def test_three_vendor_modules_are_served() -> None:
    with TestClient(app) as client:
        module_response = client.get("/static/vendor/three.module.js")
        core_response = client.get("/static/vendor/three.core.js")

    assert module_response.status_code == 200
    assert core_response.status_code == 200

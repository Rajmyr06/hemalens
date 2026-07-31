from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_main_page_includes_mobile_navigation_and_responsive_assets() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert 'name="viewport"' in response.text
    assert "viewport-fit=cover" in response.text
    assert "data-mobile-nav-toggle" in response.text
    assert "data-mobile-nav-panel" in response.text
    assert "/static/js/mobile-nav.js" in response.text
    assert "/static/css/responsive.css" in response.text


def test_secondary_pages_include_mobile_navigation() -> None:
    with TestClient(app) as client:
        research = client.get("/research")
        about = client.get("/about")

    for response in (research, about):
        assert response.status_code == 200
        assert "data-mobile-nav-toggle" in response.text
        assert "data-mobile-nav-panel" in response.text
        assert "/static/js/mobile-nav.js" in response.text
        assert "/static/css/responsive.css" in response.text


def test_form_exposes_mobile_keyboard_and_accessible_descriptions() -> None:
    with TestClient(app) as client:
        response = client.get("/partials/form")

    assert response.status_code == 200
    assert response.text.count('inputmode="decimal"') == 6
    assert response.text.count('aria-describedby="') >= 7
    assert 'data-analysis-form' in response.text
    assert 'data-page-heading' in response.text


def test_result_uses_unambiguous_score_target_and_responsive_hooks() -> None:
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
    assert "Score target" in response.text
    assert "Class<br" not in response.text
    assert "result-score-header" in response.text
    assert "result-metadata-row" in response.text
    assert 'data-page-heading' in response.text


def test_responsive_css_contains_required_breakpoints_and_touch_target() -> None:
    css = (ROOT / "app/static/css/responsive.css").read_text(encoding="utf-8")

    assert "--touch-target: 44px" in css
    assert "@media (max-width: 900px)" in css
    assert "@media (max-width: 639px)" in css
    assert "@media (max-width: 370px)" in css
    assert "safe-area-inset-bottom" in css
    assert "overflow-x: clip" in css


def test_threejs_mobile_performance_guards_are_present() -> None:
    script = (ROOT / "app/static/js/hemalens-scene.js").read_text(
        encoding="utf-8",
    )

    assert "(pointer: coarse)" in script
    assert "navigator.connection?.saveData" in script
    assert "minimumFrameInterval" in script
    assert "1000 / 30" in script
    assert 'powerPreference: this.profile.constrained ? "low-power"' in script


def test_mobile_navigation_supports_escape_and_focus_trapping() -> None:
    script = (ROOT / "app/static/js/mobile-nav.js").read_text(encoding="utf-8")

    assert 'event.key === "Escape"' in script
    assert 'event.key !== "Tab"' in script
    assert 'document.body.classList.add("mobile-nav-open")' in script
    assert 'setAttribute("inert", "")' in script

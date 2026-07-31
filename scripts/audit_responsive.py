from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CHECKS: dict[str, tuple[str, ...]] = {
    "app/templates/index.html": (
        "viewport-fit=cover",
        "data-mobile-nav-toggle",
        "data-mobile-nav-panel",
        "/css/responsive.css",
        "/js/mobile-nav.js",
    ),
    "app/templates/secondary_base.html": (
        "viewport-fit=cover",
        "data-mobile-nav-toggle",
        "data-mobile-nav-panel",
        "/css/responsive.css",
        "/js/mobile-nav.js",
    ),
    "app/templates/partials/form.html": (
        'inputmode="decimal"',
        "data-analysis-form",
        "data-page-heading",
    ),
    "app/templates/partials/result.html": (
        "Score target",
        "result-score-header",
        "result-metadata-row",
        "data-page-heading",
    ),
    "app/static/css/responsive.css": (
        "--touch-target: 44px",
        "safe-area-inset-bottom",
        "@media (max-width: 639px)",
        "overflow-x: clip",
    ),
    "app/static/js/mobile-nav.js": (
        'event.key === "Escape"',
        'event.key !== "Tab"',
        "mobile-nav-open",
    ),
    "app/static/js/hemalens-scene.js": (
        "(pointer: coarse)",
        "navigator.connection?.saveData",
        "1000 / 30",
    ),
}


def main() -> None:
    failures: list[str] = []

    for relative_path, required_tokens in CHECKS.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"MISSING: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in content:
                failures.append(f"TOKEN MISSING: {relative_path}: {token}")

    result_template = (
        ROOT / "app/templates/partials/result.html"
    ).read_text(encoding="utf-8")
    if "Class<br" in result_template:
        failures.append("AMBIGUOUS LABEL: result.html still contains Class<br")

    if failures:
        print("Responsive audit failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Responsive audit passed.")
    print("Validated stages: mobile nav, responsive pages, accessibility hooks,")
    print("Three.js mobile guards, and regression-test selectors.")


if __name__ == "__main__":
    main()

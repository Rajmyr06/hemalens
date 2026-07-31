<div align="center">

# HemaLens

### Explainable hematology pattern analysis.

A non-diagnostic research interface for exploring patterns from six
hematology parameters using a frozen XGBoost inference bundle.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Inference-EC6B23)](https://xgboost.ai/)
[![Status](https://img.shields.io/badge/status-active%20development-8B1E2D)](#roadmap)

</div>

> [!IMPORTANT]
> HemaLens is an academic research prototype, not a medical device.
> Its outputs must not be used for diagnosis, clinical screening,
> treatment decisions, or other medical decision-making.

## Overview

HemaLens provides a focused web interface for running a frozen hematology
classification model. Users enter six numerical hematology parameters,
acknowledge the non-diagnostic limitation, and receive a model classification,
decision score, threshold, and model version.

The application currently performs inference without user accounts, a patient
database, or stored prediction history.

## Current Features

- Single-screen research landing page with a continuous typewriter heading.
- Responsive server-rendered interface using Jinja2 and HTMX.
- Six-parameter hematology input form.
- Required academic-use acknowledgement before inference.
- Server-side input validation through Pydantic.
- Frozen XGBoost model loading with artifact integrity checks.
- Basic result page with:
  - model classification;
  - decision score;
  - score target;
  - threshold;
  - model version;
  - non-diagnostic disclaimer.
- Separate Research and About pages.
- Health and JSON prediction endpoints.
- Automated API, UI, navigation, and golden-parity tests.
- Docker configuration for reproducible execution.
- No account, database, or prediction-history storage.

## Demo

A public deployment has not been published yet.

The current release is developed and tested locally before mobile-responsive
quality assurance and preview deployment.

## Model Interface

HemaLens uses the following feature order:

```text
rbc → hb → mcv → mch → mchc → rdwcv
```

Current model metadata:

| Property | Value |
|---|---|
| Model type | XGBoost classifier |
| Model version | `hematology-xgb-smote-thr091-v1.0.0` |
| Decision threshold | `0.91` |
| Score target | `Thalassemia_related` |
| Golden parity samples | `18` |

The model decision score is an internal research output. It is not a clinical
probability, disease risk estimate, or diagnostic confidence score.

## Architecture

```text
Client browser
├── Tailwind CSS
├── HTMX
├── Alpine.js
└── Three.js
        │
        ▼
FastAPI application
├── Jinja2 page rendering
├── Pydantic validation
├── Health endpoint
├── Prediction endpoint
└── UI routes
        │
        ▼
Frozen inference bundle
├── Artifact metadata
├── Preprocessing objects
├── XGBoost model
└── Decision threshold
```

## Technology Stack

### Backend

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Jinja2
- XGBoost
- scikit-learn
- NumPy
- Joblib

### Frontend

- Tailwind CSS
- HTMX
- Alpine.js
- Three.js
- Server-rendered HTML

### Development and Quality

- Pytest
- Docker and Docker Compose
- Git and GitHub
- npm for frontend asset builds

## Getting Started

### Prerequisites

For the current macOS workflow:

- Git
- Homebrew
- Python 3.13
- Node.js and npm
- XGBoost OpenMP runtime (`libomp`)
- Docker Desktop, optional for container testing

### Clone the Repository

```bash
git clone https://github.com/Rajmyr06/hemalens.git
cd hemalens
```

### macOS Bootstrap

The bootstrap script prepares the Python environment, installs the OpenMP
runtime when needed, verifies the model bundle, and runs the test suite.

```bash
chmod +x scripts/*.sh
./scripts/bootstrap_macos.sh
```

Activate the virtual environment after bootstrap:

```bash
source .venv/bin/activate
```

### Build Frontend Assets

```bash
chmod +x scripts/build_frontend.sh
./scripts/build_frontend.sh
```

Alternatively:

```bash
npm install
npm run build
```

## Running Locally

Start the FastAPI development server:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open these routes:

| Route | Purpose |
|---|---|
| `http://127.0.0.1:8000/` | Main interface |
| `http://127.0.0.1:8000/research` | Research transparency |
| `http://127.0.0.1:8000/about` | Project information |
| `http://127.0.0.1:8000/health` | Application health |
| `http://127.0.0.1:8000/docs` | OpenAPI documentation |

Stop the development server with `Control + C`.

## API Usage

### Health Check

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

Expected structure:

```json
{
  "status": "healthy",
  "application": "HemaLens",
  "application_version": "0.1.0",
  "model_loaded": true,
  "model_version": "hematology-xgb-smote-thr091-v1.0.0"
}
```

### Prediction

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "rbc": 4.45,
    "hb": 15.4,
    "mcv": 93.7,
    "mch": 34.6,
    "mchc": 36.9,
    "rdwcv": 11.9
  }' | python3 -m json.tool
```

Example response:

```json
{
  "model_version": "hematology-xgb-smote-thr091-v1.0.0",
  "model_score": 2.8008566005155444e-05,
  "threshold": 0.91,
  "predicted_class": "Normal",
  "predicted_class_index": 0
}
```

## Testing

Run the complete test suite:

```bash
source .venv/bin/activate
pytest
```

Verify the frozen model bundle separately:

```bash
python -m scripts.verify_bundle
```

The verification process checks model metadata and the included golden samples.

## Docker

Build and start the application:

```bash
docker compose up --build -d
```

Check the container:

```bash
docker compose ps
docker compose logs --tail=100 hemalens
```

Test the application:

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

Stop the container:

```bash
docker compose down
```

## Project Structure

```text
hemalens/
├── app/
│   ├── core/                 # Configuration and logging
│   ├── ml/                   # Artifact loading and inference
│   ├── routers/              # API and UI routes
│   ├── schemas/              # Request and response models
│   ├── static/               # Compiled CSS and JavaScript assets
│   ├── templates/            # Jinja2 pages and partials
│   └── main.py               # FastAPI application
├── artifacts/                # Frozen model bundle
├── scripts/                  # Setup, build, run, and verification scripts
├── tests/                    # Automated test suite
├── compose.yaml
├── Dockerfile
├── package.json
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Privacy and Safety

HemaLens currently does not provide:

- user registration or authentication;
- patient profiles;
- a clinical database;
- prediction history;
- automatic storage of submitted values;
- clinical interpretation or treatment recommendations.

Do not submit directly identifying patient information. Use only the six
numerical parameters required by the research interface.

## Limitations

- The model is intended for academic exploration only.
- The application does not establish a medical diagnosis.
- Model outputs depend on the frozen research dataset and methodology.
- Clinical reference ranges are not currently presented as decision rules.
- Local SHAP explanations are not part of the current stable milestone.
- Out-of-distribution detection has not yet been implemented.
- Public deployment and cross-platform parity testing are still pending.

## License

A project license has not yet been selected. Do not redistribute or reuse the
source code until a `LICENSE` file is added to the repository.

## Maintainer

Maintained by [@Rajmyr06](https://github.com/Rajmyr06).

## Acknowledgments

- Visual direction references the editorial dark-interface approach used by
  [Forrm Studio](https://forrm.studio/).
- Built with FastAPI, XGBoost, HTMX, Alpine.js, Tailwind CSS, and Three.js.

---

<div align="center">

**Academic use only · No input history · Not a clinical diagnosis**

</div>

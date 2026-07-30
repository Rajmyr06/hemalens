# HemaLens

HemaLens is an academic research application for hematology pattern analysis using a frozen XGBoost inference bundle.

> The application is not a diagnostic tool and must not be used for clinical decisions.

## Frozen model contract

- Model version: `hematology-xgb-smote-thr091-v1.0.0`
- Positive class: `Thalassemia_related`
- Threshold: `0.91`
- Feature order: `rbc`, `hb`, `mcv`, `mch`, `mchc`, `rdwcv`
- SMOTE is training-only and is not executed during inference.

## macOS setup

```bash
cd ~/Developer/HemaLens
chmod +x scripts/*.sh
./scripts/bootstrap_macos.sh
```

Run:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Open:

- Application: http://127.0.0.1:8000
- Health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

## Manual API test

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "rbc": 4.45,
    "hb": 15.4,
    "mcv": 93.7,
    "mch": 34.6,
    "mchc": 36.9,
    "rdwcv": 11.9
  }'
```

## Test

```bash
pytest
python -m scripts.verify_bundle
```

## Docker

```bash
docker compose up --build
```

## Privacy rule

Do not log request bodies, feature values, or model outputs. Do not add patient identity fields.

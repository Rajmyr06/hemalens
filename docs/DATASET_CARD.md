# Dataset Card — HPLC-Based Thalassemia Screening Data

## Local file

- File: `HPLC data.csv`
- SHA-256: `51a5729c9864a5292c134fb911e199d628fb4812e19367c8cc503363b009daee`
- Rows: 13,031
- Columns: 19

## Public dataset page

The matching public dataset page is **HPLC-Based Thalassemia Screening Data** on
Kaggle. It describes anonymized HPLC and CBC screening data from West Bengal,
India, and lists the license as CC BY-SA 4.0.

Source:
https://www.kaggle.com/datasets/abhraghoshcmc/hplc-based-thalassemia-screening-data

## Columns used by this project

- RBC
- HB
- MCV
- MCH
- MCHC
- RDWcv
- Diagnosis

## Target mapping

- Exact `Normal` label → `Normal`
- Labels containing thalassemia-related keywords → `Thalassemia_related`
- Remaining labels → `Other`
- `Other` excluded from binary modeling

## Data-quality findings

- No missing value in the six model features after numeric conversion.
- No numeric conversion failure.
- Seven duplicated feature-target rows.
- Three exact feature-target groups occur in both train and test under the
  original random split.
- Extreme values exist, including values far outside the central distribution.
  These are preserved to reproduce the research but listed for manual review.

See:

- `reports/data_audit.json`
- `reports/feature_distribution_audit.csv`
- `reports/extreme_rows_for_manual_review.csv`
- `reports/deduplication_sensitivity.json`

## Usage constraints

- Preserve dataset attribution and license requirements.
- Do not expose row-level source data through the public website.
- Do not treat the target mapping as clinical diagnosis.
- Do not present observed dataset bounds as clinical reference ranges.

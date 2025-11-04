# GCP Sales Analytics Platform

[![Terraform](https://img.shields.io/badge/IaC-Terraform-7b42bc)]()
[![FastAPI](https://img.shields.io/badge/API-FastAPI-05998b)]()
[![GCP](https://img.shields.io/badge/Cloud-Google_Cloud-4285F4)]()
[![BigQuery](https://img.shields.io/badge/Data-BigQuery-0066ff)]()
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Serverless data platform on Google Cloud:
- **Terraform** provisions core infra (GCS, BigQuery, Pub/Sub).
- **ETL (Python + pandas):** loads CSVs from GCS → cleans → appends to BigQuery.
- **FastAPI** service on **Cloud Run** exposes analytics endpoints powered by BigQuery.

**Live demo:**  
**Cloud Run** → https://sales-api-109403326759.europe-west1.run.app  
Docs: `/docs` • Health: `/healthz` • Endpoints: `/sales/summary`, `/sales/top-products?store_id=A1&limit=5`

---

## Architecture

       ┌───────────────────────┐
       │  CSV files (hourly)   │
       │  gs://<proj>-sales-   │
       │  data-raw/            │
       └─────────┬─────────────┘
                 │ (manual or future trigger)
                 ▼
         [Python Loader / ETL]
         - pandas clean
         - compute total
         - append to BigQuery
                 │
                 ▼
    ┌─────────────────────────────┐
    │   BigQuery (sales_analytics)│
    │   table: daily_sales        │
    └─────────┬───────────────────┘
              │ SQL (parameterized)
              ▼
       Cloud Run (FastAPI)
       /sales/summary
       /sales/top-products

---

## Components

- **infra/** — Terraform for:
  - GCS bucket: `<project_id>-sales-data-raw`
  - BigQuery dataset: `sales_analytics`
  - BigQuery table: `daily_sales`
  - Pub/Sub topic: `sales-data-uploaded` (ready for future automation)
- **app/** — `data_loader.py` to ingest `sample_sales.csv` from GCS → BigQuery
- **api/** — FastAPI app that queries BigQuery and serves JSON

---

## Quick start (dev)

### Prereqs
- Google Cloud SDK (`gcloud`), Terraform ≥ 1.0, Python 3.11+
- Auth locally:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  gcloud auth application-default set-quota-project <PROJECT_ID>

cd infra
terraform init
terraform apply -var="project_id=<PROJECT_ID>"

cd ../app
python -m pip install -r requirements.txt

# upload sample CSV to GCS
gsutil cp sample_sales.csv gs://<PROJECT_ID>-sales-data-raw/

# run loader
python data_loader.py sample_sales.csv

cd ../api
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8080
# http://127.0.0.1:8080/docs


# one-shot build+deploy from source
gcloud run deploy sales-api \
  --source ./api \
  --region europe-west1 \
  --allow-unauthenticated \
  --project <PROJECT_ID>

# grant BigQuery read to Cloud Run runtime SA
PN=$(gcloud projects describe <PROJECT_ID> --format='value(projectNumber)')
SA="$PN-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding <PROJECT_ID> --member="serviceAccount:$SA" --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding <PROJECT_ID> --member="serviceAccount:$SA" --role="roles/bigquery.jobUser"

Endpoints

GET /sales/summary → revenue per store

GET /sales/top-products?store_id=A1&limit=5 → top products by revenue for a store

GET /healthz → status

GET /docs → Swagger UI

Example:
curl "https://<SERVICE_URL>/sales/top-products?store_id=A1&limit=5"

Security & Ops Notes

No secrets in code; local dev uses ADC (gcloud auth application-default login).

Cloud Run uses a service account with minimal roles (bigquery.dataViewer, bigquery.jobUser).

Parameterized queries via QueryJobConfig (prevents injection).

TODO: move Terraform state to a GCS backend, introduce separate dev/prod workspaces.

Roadmap (next steps)

Auto-ingest: GCS notification → Pub/Sub → Cloud Run/Function to trigger data_loader.

CI/CD: Cloud Build triggers for API + Terraform plan/apply with approvals.

Observability: Cloud Monitoring dashboards + request/SQL latency metrics.

Analytics: BigQuery views for common aggregations; Looker Studio dashboard.

Tests: pandas cleaning unit tests, contract tests for endpoints.

IAM hardening: dataset-level roles instead of project-level; custom SA for Cloud Run.

Tech decisions (brief)

Cloud Run: fully managed, zero-ops, per-request autoscaling.

BigQuery: serverless analytics at scale; easy SQL & partitioning (add later).

Terraform: reproducible infra; ready for remote state and env workspaces.

pandas + pyarrow: fast CSV → columnar → BigQuery load.

FastAPI: clean, typed, modern Python API with built-in OpenAPI.


---

### 2) `.gitignore`
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
.env
.env.*

# Virtualenvs
.venv/
venv/

# Node / misc (safety)
node_modules/

# OS & editors
.DS_Store
.vscode/
.idea/

# Terraform
.terraform/
*.tfstate
*.tfstate.*
crash.log
override.tf
override.tf.json
.terraform.lock.hcl

# Google Cloud / credentials
*.json
*.key
application_default_credentials.json

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
...
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED...

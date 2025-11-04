# Infra (Terraform)

Provisions:
- GCS bucket: `<project_id>-sales-data-raw`
- BigQuery dataset: `sales_analytics`
- BigQuery table: `daily_sales`
- Pub/Sub topic: `sales-data-uploaded` (for future auto-ingest)

## Usage
```bash
terraform init
terraform apply -var="project_id=<PROJECT_ID>"


---

### 5) `app/README.md`
```markdown
# ETL Loader (Python)

Loads a CSV from GCS → cleans → appends to BigQuery.

## Run
```bash
python -m pip install -r requirements.txt
gsutil cp sample_sales.csv gs://<PROJECT_ID>-sales-data-raw/
python data_loader.py sample_sales.csv


---

### 6) `api/README.md`
```markdown
# FastAPI (Cloud Run)

Endpoints:
- `GET /sales/summary`
- `GET /sales/top-products?store_id=A1&limit=5`
- `GET /healthz`
- Swagger: `/docs`

## Local
```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8080

gcloud run deploy sales-api --source . --region europe-west1 --allow-unauthenticated --project <PROJECT_ID>

PN=$(gcloud projects describe <PROJECT_ID> --format='value(projectNumber)')
SA="$PN-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding <PROJECT_ID> --member="serviceAccount:$SA" --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding <PROJECT_ID> --member="serviceAccount:$SA" --role="roles/bigquery.jobUser"


---

### 7) Suggested **repository name** & description

- **Name:** `gcp-sales-analytics-platform`
- **Description:** _Serverless sales analytics on GCP — Terraform (GCS, BigQuery, Pub/Sub), Python ETL, and a FastAPI service on Cloud Run._

---

### 8) Suggested first 5 commit messages

1. `chore(repo): scaffold repo structure, .gitignore, MIT license`
2. `feat(infra): terraform for GCS bucket, BigQuery dataset/table, Pub/Sub`
3. `feat(app): pandas-based CSV loader (GCS -> BigQuery) with cleaning`
4. `feat(api): FastAPI endpoints for store summary & top products, containerized`
5. `docs: enterprise README with architecture, deploy steps, and roadmap`

---

### 9) 3-minute interview walkthrough (script)

- **30s Summary:** “This repo is a minimal but production-shaped serverless data platform on GCP. Terraform provisions GCS, BigQuery, and Pub/Sub. A Python ETL ingests CSVs into BigQuery. A FastAPI service on Cloud Run exposes analytics endpoints.”

- **1m Architecture:** “CSV lands in a uniquely named GCS bucket. The loader cleans with pandas and appends to `sales_analytics.daily_sales` (we compute `total` in ETL). The API runs in Cloud Run, authenticates via the runtime service account, and runs parameterized queries in BigQuery. No secrets are committed; local dev via ADC.”

- **1m Ops & Security:** “I used minimal roles: `dataViewer` + `jobUser`. Next I’d move Terraform state to GCS, add workspaces, and GitHub Actions + Cloud Build for CI/CD. I’d also add a Pub/Sub trigger so new uploads auto-ingest, plus Looker Studio for business-friendly dashboards.”

- **30s Close:** “It’s intentionally small, but the patterns scale: infra as code, serverless runtime, parameterized BI queries, least privilege. It’s easy to extend per client domain (retail, media, travel). Happy to demo the live endpoints.”

---

If you want, I can also generate a **concise architecture PNG** later, but this is already interview-ready. Push this to GitHub and drop me the repo link if you want a quick “portfolio polish” pass.
::contentReference[oaicite:0]{index=0}

import os
import sys
import io
import logging
from datetime import datetime

import pandas as pd
from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound

PROJECT_ID = "ringed-pad-477122-k9"
DATASET_ID = "sales_analytics"
TABLE_ID = "daily_sales"
BUCKET_NAME = f"{PROJECT_ID}-sales-data-raw"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def load_csv_from_gcs(blob_name: str) -> pd.DataFrame:
    """Download a CSV from GCS into a pandas DataFrame."""
    logging.info(f"Downloading gs://{BUCKET_NAME}/{blob_name}")
    storage_client = storage.Client(project=PROJECT_ID)
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        data = blob.download_as_text()
    except NotFound:
        raise SystemExit(f"❌ File not found: gs://{BUCKET_NAME}/{blob_name}")
    df = pd.read_csv(io.StringIO(data))
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning and add total = quantity * price."""
    required = ["store_id", "timestamp", "product", "quantity", "price"]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Drop rows with missing essential fields
    df = df.dropna(subset=["store_id", "price", "quantity", "timestamp"])

    # Coerce types safely
    df["store_id"] = df["store_id"].astype(str)
    df["product"] = df["product"].astype(str)

    # quantity → int, price → float
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0).astype(float)

    # Parse timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"])

    # Compute total
    df["total"] = df["quantity"] * df["price"]

    # Reorder columns to match BQ schema order (not strictly required, just tidy)
    cols = ["store_id", "timestamp", "product", "quantity", "price", "total"]
    df = df[cols]
    logging.info(f"Cleaned rows: {len(df)}")
    return df

def load_into_bigquery(df: pd.DataFrame):
    """Append the DataFrame into BigQuery table."""
    table_fqn = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    logging.info(f"Loading {len(df)} rows into {table_fqn}")

    client = bigquery.Client(project=PROJECT_ID)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    # Load DataFrame
    load_job = client.load_table_from_dataframe(df, table_fqn, job_config=job_config)
    load_job.result()
    dest = client.get_table(table_fqn)
    logging.info(f"✅ Load complete. Table now has {dest.num_rows} rows.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python data_loader.py <blob_name_in_bucket>")
        print("Example: python data_loader.py sample_sales.csv")
        sys.exit(2)

    blob_name = sys.argv[1]
    df = load_csv_from_gcs(blob_name)
    df = clean_data(df)
    if df.empty:
        logging.warning("No valid rows after cleaning; skipping load.")
        return
    load_into_bigquery(df)

if __name__ == "__main__":
    # Let the BigQuery/Storage SDKs pick up ADC from `gcloud auth application-default login`
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", PROJECT_ID)
    main()

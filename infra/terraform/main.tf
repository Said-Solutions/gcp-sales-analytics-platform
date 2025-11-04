resource "google_storage_bucket" "raw_sales_bucket" {
  name          = "${var.project_id}-sales-data-raw"
  location      = var.region
  force_destroy = true
}

resource "google_bigquery_dataset" "sales_dataset" {
  dataset_id                  = "sales_analytics"
  location                    = var.region
  default_table_expiration_ms = null
}

resource "google_bigquery_table" "sales_table" {
  dataset_id = google_bigquery_dataset.sales_dataset.dataset_id
  table_id   = "daily_sales"

  schema = jsonencode([
    { name = "store_id",  type = "STRING",    mode = "REQUIRED" },
    { name = "timestamp", type = "TIMESTAMP", mode = "REQUIRED" },
    { name = "product",   type = "STRING" },
    { name = "quantity",  type = "INTEGER" },
    { name = "price",     type = "FLOAT" },
    { name = "total",     type = "FLOAT" }   # <-- add this
  ])
}


resource "google_pubsub_topic" "sales_topic" {
  name = "sales-data-uploaded"
}

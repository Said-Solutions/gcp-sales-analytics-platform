output "bucket_name" {
  value = google_storage_bucket.raw_sales_bucket.name
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.sales_dataset.dataset_id
}

output "bigquery_table" {
  value = google_bigquery_table.sales_table.table_id
}

output "pubsub_topic" {
  value = google_pubsub_topic.sales_topic.name
}

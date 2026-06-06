terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------------
# Pub/Sub Topic
# -----------------------------
resource "google_pubsub_topic" "clickstream_raw" {
  name = "clickstream-raw"
}

# -----------------------------
# Pub/Sub Subscription
# -----------------------------
resource "google_pubsub_subscription" "clickstream_subscription" {
  name  = "clickstream-subscription"
  topic = google_pubsub_topic.clickstream_raw.name
}

# -----------------------------
# BigQuery Dataset
# -----------------------------
resource "google_bigquery_dataset" "clickstream_warehouse" {
  dataset_id = "clickstream_warehouse"
  location   = var.region
}

# -----------------------------
# BigQuery Table
# -----------------------------
resource "google_bigquery_table" "realtime_clicks" {
  dataset_id = google_bigquery_dataset.clickstream_warehouse.dataset_id
  table_id   = "realtime_clicks"

  deletion_protection = false

  schema = jsonencode([
    {
      name = "session_id"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "user_id"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "timestamp"
      type = "TIMESTAMP"
      mode = "NULLABLE"
    },
    {
      name = "event_type"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "page_url"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "ip_address"
      type = "STRING"
      mode = "NULLABLE"
    }
  ])
}

# -----------------------------
# Storage Bucket for Dataflow
# -----------------------------
resource "google_storage_bucket" "dataflow_staging" {
  name          = "${var.project_id}-dataflow-staging"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

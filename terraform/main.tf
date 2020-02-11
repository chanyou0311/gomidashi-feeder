provider "google" {
  credentials = var.google_provider_configurations.credentials
  project     = var.google_provider_configurations.project_name
  region      = var.google_provider_configurations.region
}

data "archive_file" "app_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/files/functions.zip"
}

resource "google_storage_bucket" "app_bucket" {
  name     = "${var.google_provider_configurations.project_name}-scheduler-bucket"
  location = "ASIA-NORTHEAST1"
}

resource "google_storage_bucket_object" "app_object" {
  name   = "app_${formatdate("YYYYMMDD_hhmmss", timestamp())}.zip"
  bucket = google_storage_bucket.app_bucket.name
  source = data.archive_file.app_zip.output_path
}

resource "google_pubsub_topic" "app_topic" {
  name = "slack-notify"
}

resource "google_cloudfunctions_function" "app_function" {
  name                = "app"
  runtime             = "python37"
  entry_point         = "hello_pubsub"
  available_memory_mb = 128

  source_archive_bucket = google_storage_bucket.app_bucket.name
  source_archive_object = google_storage_bucket_object.app_object.name

  environment_variables = {
    SLACK_WEBHOOK_URL = var.webhook_url
  }

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.app_topic.name
  }
}

resource "google_cloud_scheduler_job" "app_scheduler_job" {
  // region      = "asia-northeast1"
  name      = "app"
  schedule  = "0 22 * * *"
  time_zone = "Asia/Tokyo"

  pubsub_target {
    topic_name = google_pubsub_topic.app_topic.id
    data       = base64encode("{\"mention\":\"channel\",\"channel\":\"random\"}")
  }
}

resource "google_storage_bucket" "tf-bucket" {
  project       = var.gcp_project
  name          = var.bucket-name
  location      = var.gcp_region
  force_destroy = true
  storage_class = var.storage-class
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

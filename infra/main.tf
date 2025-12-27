# 1. The Provider: Tells Terraform we are using Google Cloud
provider "google" {
  project = "restaurant-booking-instant-30"
  region  = "us-central1"
}

# 2. The Network: Creating the "Gated Community"
resource "google_compute_network" "vpc_network" {
  name                    = "restaurant-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "restaurant-subnet"
  ip_cidr_range = "10.0.0.0/18"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
}

# 3. GKE Autopilot: The "Building Manager"
resource "google_container_cluster" "primary" {
  name     = "restaurant-cluster"
  location = "us-central1"

  enable_autopilot = true
  network          = google_compute_network.vpc_network.name
  subnetwork       = google_compute_subnetwork.subnet.name

  # We set this to true so we can delete it easily later
  deletion_protection = false 
}
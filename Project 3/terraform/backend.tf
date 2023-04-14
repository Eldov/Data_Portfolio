terraform {
  backend "s3" {
    # Edit the bucket name and region
    bucket         = "state-terraform-backend-075234807813"
    key            = "global/s3/terraform.tfstate"
    region         = "eu-west-2"
  }
}
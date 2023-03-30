terraform {
  backend "s3" {
    # Edit the bucket name and region
    bucket         = "eldov-project2-terraform-backend"
    key            = "terraform/tfstate"
    region         = "us-east-1"
  }
}

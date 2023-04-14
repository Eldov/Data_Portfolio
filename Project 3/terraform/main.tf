terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 4.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
    region = "eu-west-2"
}
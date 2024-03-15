terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.22.0"
        }
        docker = {
            source  = "kreuzwerker/docker"
            version = "3.0.2"
        }
    }

    required_version = "~> 1.0"
}

provider "aws" {
    region = var.aws_region

    default_tags {
        tags = var.default_tags
    }
}

provider "docker" {
    host = "unix:///Users/ondrej/.docker/run/docker.sock"

    registry_auth {
    address  = "816259561563.dkr.ecr.us-east-1.amazonaws.com"
    username = "usrnm"
    password = "pswd"
  }
}

terraform {
   backend "s3" {
     bucket = "project-1-sre-course-toanld7"
     key    = "terraform/terraform.tfstate"
     region = "us-east-2"
   }
 }

 provider "aws" {
   region = "us-east-2"

   default_tags {
     tags = local.tags
   }
 }
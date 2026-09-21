data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "aws_arn" {
  value = data.aws_caller_identity.current.arn
}

output "aws_region" {
  value = data.aws_region.current.region
}
resource "aws_s3_bucket" "lab" {
  bucket_prefix = "s29-terraform-lab-"

  tags = {
    Name      = "s29-terraform-lab"
    Session   = "S29"
    ManagedBy = "Terraform"
  }
}
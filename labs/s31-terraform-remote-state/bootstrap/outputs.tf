output "state_bucket_name" {
  description = "Tên S3 bucket dùng làm Terraform remote backend"
  value       = aws_s3_bucket.terraform_state.bucket
}

output "state_bucket_arn" {
  description = "ARN của S3 bucket dùng làm Terraform remote backend"
  value       = aws_s3_bucket.terraform_state.arn
}
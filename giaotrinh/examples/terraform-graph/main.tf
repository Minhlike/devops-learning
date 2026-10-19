terraform {
  required_version = ">= 1.5, < 1.17"
}

variable "schema_revision" {
  type    = string
  default = "v1"
}

resource "terraform_data" "schema" {
  input = var.schema_revision
}

resource "terraform_data" "service" {
  triggers_replace = terraform_data.schema.output
}

resource "terraform_data" "audit" {
  input      = "ready"
  depends_on = [terraform_data.service]
}

output "service_id" {
  value = terraform_data.service.id
}

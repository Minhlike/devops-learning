resource "terraform_data" "this" {
  input = {
    name    = var.name
    message = var.message
  }
}

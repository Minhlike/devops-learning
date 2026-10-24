resource "terraform_data" "demo" {
  input = {
    session = "S31"
    purpose = "state-versioning-demo"
  }
}

resource "terraform_data" "lock_holder" {
  input = "S31-lock-demo"

  provisioner "local-exec" {
    command = "sleep 120"
  }
}

module "message_app" {
  source = "./modules/message"

  name    = "app"
  message = "Hello from application module"
}

module "message_ops" {
  source = "./modules/message"

  name    = "ops"
  message = "Hello from operations module"
}

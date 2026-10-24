output "demo_input" {
  value = terraform_data.demo.input
}

output "app_module_data" {
  value = module.message_app.data
}

output "ops_module_data" {
  value = module.message_ops.data
}

resource "terraform_data" "server_app" {
    input = "application-server"
}

moved {
    from = terraform_data.server_old
    to = terraform_data.server_app
}
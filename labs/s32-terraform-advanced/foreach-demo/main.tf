locals {
    services = toset([
        "api",
        "scheduler"
    ])
}

resource "terraform_data" "service" {
    for_each = local.services

    input = each.key
}
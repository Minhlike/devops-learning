locals {
    services = [
        "api",
        "scheduler"
    ]
}

resource "terraform_data" "service" {
    count = length(local.services)

    input = local.services[count.index]
}
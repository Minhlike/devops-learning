terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
}

provider "docker" {}

locals {
  port_mappings = [
    {
      internal = 80
      external = 18091
    },
    {
      internal = 80
      external = 18092
    }
  ]
}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = true
}

resource "docker_container" "web" {
  name  = "s32-dynamic-demo"
  image = docker_image.nginx.image_id

  dynamic "ports" {
    for_each = local.port_mappings
    iterator = port

    content {
      internal = port.value.internal
      external = port.value.external
    }
  }
}
locals {
  name_prefix = var.project_name

  common_tags = merge(
    {
      Project = var.project_name
    },
    var.extra_tags
  )
}
resource "terraform_data" "protected" {
    input = "critical-database"
}

resource "terraform_data" "rolling" {
    input = "application"
    triggers_replace = "v2"

    lifecycle {
        create_before_destroy = true
    }
}

resource "terraform_data" "externally_managed" {
    input = "value-v2"

    lifecycle {
        ignore_changes = [input]
    }
}

resource "terraform_data" "source" {
    input = "version-2"
}

resource "terraform_data" "dependent" {
    input = "application"

    lifecycle {
        replace_triggered_by = [
            terraform_data.source
        ]
    }
}
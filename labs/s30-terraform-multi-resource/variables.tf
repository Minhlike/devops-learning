variable "aws_region" {
  description = "AWS region dùng cho lab S30"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Tên dùng làm prefix cho tài nguyên"
  type        = string
  default     = "s30-terraform"
}

variable "vpc_cidr" {
  description = "CIDR của VPC"
  type        = string
  default     = "10.30.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "vpc_cidr phải là một CIDR hợp lệ."
  }
}

variable "public_subnet_cidr" {
  description = "CIDR của public subnet"
  type        = string
  default     = "10.30.1.0/24"

  validation {
    condition     = can(cidrnetmask(var.public_subnet_cidr))
    error_message = "public_subnet_cidr phải là một CIDR hợp lệ."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "enable_public_ip" {
  description = "Có gán public IPv4 cho EC2 hay không"
  type        = bool
  default     = true
}

variable "allowed_http_cidrs" {
  description = "Các CIDR được phép truy cập HTTP port 80"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "extra_tags" {
  description = "Các tag bổ sung cho toàn bộ tài nguyên"
  type        = map(string)
  default = {
    Session = "S30"
  }
}
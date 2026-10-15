output "vpc_id" {
  description = "ID của VPC S30"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID của public subnet"
  value       = aws_subnet.public.id
}

output "ami_id" {
  description = "Amazon Linux 2023 AMI được Terraform chọn"
  value       = data.aws_ami.amazon_linux_2023.id
}

output "web_public_ip" {
  description = "Public IPv4 của EC2 web server"
  value       = aws_instance.web.public_ip
}

output "web_public_dns" {
  description = "Public DNS của EC2 web server"
  value       = aws_instance.web.public_dns
}

output "web_url" {
  description = "URL HTTP của web server"
  value       = "http://${aws_instance.web.public_ip}"
}
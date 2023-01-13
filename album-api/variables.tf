# Input variable definitions

variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "ap-northeast-1"
}

variable "ACCESS_KEY_ID" {}

variable "SECRET_ACCESS_KEY" {}
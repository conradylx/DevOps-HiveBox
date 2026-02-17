variable "region" {
    description = "AWS region"
    type = string
    default = "eu-west-1"
}

variable "cluster_name" {
    description = "EKS cluster name"
    type = string
    default = "hivebox-cluster"
}

variable "cluster_version" {
    description = "Kubernetes version"
    type = string
    default = "1.31"
}

variable "node_instance_type" {
    description = "EC2 instance type for worker nodes"
    type = string
    default = "t3.small"
}

variable "node_desired_count" {
  type        = number
  default     = 1
  description = "Desired number of worker nodes"
}

variable "node_min_count" {
  type        = number
  default     = 1
  description = "Minimum number of worker nodes"
}

variable "node_max_count" {
    type = number
    default = 1
    description = "Maximum number of worker nodes"
}

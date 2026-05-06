variable "region" {
    description = "AWS region where resources will be created."
    type        = string
    default     = "eu-west-1"
}

variable "cluster_name" {
    description = "Name of the EKS cluster."
    type        = string
    default     = "hivebox-cluster"
}

variable "cluster_version" {
    description = "Kubernetes version."
    type        = string
    default     = "1.31"
}

variable "node_instance_type" {
    description = "EC2 instance type for worker nodes."
    type        = string
    default     = "t3.small"
}

variable "node_desired_count" {
    description = "Expected worker nodes count."
    type        = number
    default     = 2
}

variable "node_min_count" {
    description = "Minimum worker nodes count."
    type        = number
    default     = 2
}

variable "node_max_count" {
    description = "Maximum worker nodes count."
    type        = number
    default     = 4
}

variable "vpc_cidr" {
    description = "CIDR block for the VPC."
    type        = string
    default     = "10.0.0.0/16"
}
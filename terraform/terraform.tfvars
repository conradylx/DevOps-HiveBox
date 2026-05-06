# This file should not be committed to version control as it contains sensitive information.

region = "eu-west-1"
cluster_name = "hivebox-cluster"
cluster_version = "1.31"

node_instance_type = "t3.small"
node_desired_count = 2
node_min_count = 2
node_max_count = 4

vpc_cidr = "10.0.0.0/16"
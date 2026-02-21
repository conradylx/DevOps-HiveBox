# AZ
data "aws_availability_zones" "available" {
    state = "available"
}

# VPC
resource "aws_vpc" "main" {
    cidr_block = var.vpc_cidr
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = {
        Name = "${var.cluster_name}-vpc"
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    }
}

# Public subnets
resource "aws_subnet" "public" {
    count = 2
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.${count.index}.0/24"
    availability_zone = data.aws_availability_zones.available.names[count.index]
    map_public_ip_on_launch = true
    tags = {
        Name = "${var.cluster_name}-public-${count.index + 1}"
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
        "kubernetes.io/role/elb" = "1"
    }

}

# Private subnets
resource "aws_subnet" "private" {
    count = 2
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.${count.index + 10}.0/24"
    availability_zone = data.aws_availability_zones.available.names[count.index]
    tags = {
        Name = "${var.cluster_name}-private-${count.index + 1}"
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
        "kubernetes.io/role/internal-elb" = "1"
    } 
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
    vpc_id = aws_vpc.main.id
    tags = {
        Name = "${var.cluster_name}-igw"
    }
}

# Route Table for public subnets
resource "aws_route_table" "public" {
    vpc_id = aws_vpc.main.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.main.id
    }
    tags = {
        Name = "${var.cluster_name}-public-rt"
    }
}

resource "aws_route_table_association" "public" {
    count = 2
    subnet_id = aws_subnet.public[count.index].id
    route_table_id = aws_route_table.public.id
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
    domain = "vpc"
    tags = {
        Name = "${var.cluster_name}-nat-eip"
    }
    depends_on = [ aws_internet_gateway.main ]
}

# NAT
resource "aws_nat_gateway" "main" {
    allocation_id = aws_eip.nat.id
    subnet_id = aws_subnet.public[0].id
    tags = {
        Name = "${var.cluster_name}-nat-gw"
    }
    depends_on = [ aws_internet_gateway.main ]
}

# Route Table for private subnets
resource "aws_route_table" "private" {
    vpc_id = aws_vpc.main.id
    route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = aws_nat_gateway.main.id
    }
    tags = {
        Name = "${var.cluster_name}-private-rt"
    }
}

resource "aws_route_table_association" "private" {
    count = 2
    subnet_id = aws_subnet.private[count.index].id
    route_table_id = aws_route_table.private.id
}

# IAM
resource "aws_iam_role" "eks_cluster" {
    name = "${var.cluster_name}-cluster-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "eks.amazonaws.com"
            }
        }]
    })
    tags = {
        Name = "${var.cluster_name}-cluster-role"
    }
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
    role       = aws_iam_role.eks_cluster.name
}

# Role for worker nodes
resource "aws_iam_role" "eks_node" {
    name = "${var.cluster_name}-node-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "ec2.amazonaws.com"
            }
        }]
    })
    tags = {
        Name = "${var.cluster_name}-node-role"
    }
}

# Policies for worker nodes
resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
    role       = aws_iam_role.eks_node.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
    role       = aws_iam_role.eks_node.name
}

resource "aws_iam_role_policy_attachment" "eks_ecr_read_only" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
    role       = aws_iam_role.eks_node.name
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
    name = var.cluster_name
    version = var.cluster_version
    role_arn = aws_iam_role.eks_cluster.arn
    vpc_config {
        subnet_ids = concat(
            aws_subnet.private[*].id,
            aws_subnet.public[*].id
        )
        endpoint_private_access = true
        endpoint_public_access = true
    }
    depends_on = [ aws_iam_role_policy_attachment.eks_cluster_policy ]
    tags = {
        Name = var.cluster_name
    }
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = aws_iam_role.eks_node.arn
  subnet_ids      = aws_subnet.private[*].id   
  
  instance_types = [var.node_instance_type]
  
  scaling_config {
    desired_size = var.node_desired_count  
    min_size     = var.node_min_count      
    max_size     = var.node_max_count      
  }
  
  update_config {
    max_unavailable = 1  
  }
  
  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_ecr_read_only,
  ]
  
  tags = {
    Name = "${var.cluster_name}-nodes"
  }
  
  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }
}
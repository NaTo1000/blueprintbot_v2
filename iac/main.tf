## Terraform Configuration for BlueprintBot v2 Infrastructure (AWS Example)

# This Terraform configuration defines the core AWS infrastructure
# for deploying the BlueprintBot v2 Kernel and OS.
# It includes a Virtual Private Cloud (VPC), subnets, IAM roles,
# and an Amazon Elastic Kubernetes Service (EKS) cluster.

# --- AWS Provider Configuration ---
provider "aws" {
  region = "us-east-1" # Example region, can be parameterized
}

# --- Networking (VPC) ---
resource "aws_vpc" "blueprintbot_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "blueprintbot-v2-vpc"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.blueprintbot_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "blueprintbot-v2-public-1"
  }
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.blueprintbot_vpc.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "blueprintbot-v2-private-1"
  }
}

resource "aws_internet_gateway" "blueprintbot_igw" {
  vpc_id = aws_vpc.blueprintbot_vpc.id

  tags = {
    Name = "blueprintbot-v2-igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.blueprintbot_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.blueprintbot_igw.id
  }

  tags = {
    Name = "blueprintbot-v2-public-rt"
  }
}

resource "aws_route_table_association" "public_rt_assoc_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

# --- IAM Roles for EKS ---
resource "aws_iam_role" "eks_cluster_role" {
  name = "blueprintbot-v2-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}

resource "aws_iam_role" "eks_node_role" {
  name = "blueprintbot-v2-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_node_policy_1" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "eks_node_policy_2" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "eks_node_policy_3" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}

# --- EKS Cluster ---
resource "aws_eks_cluster" "blueprintbot_cluster" {
  name     = "blueprintbot-v2-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = [
      aws_subnet.public_subnet_1.id,
      aws_subnet.private_subnet_1.id
    ]
    security_group_ids = [] # Managed by EKS
  }

  # Ensure that the EKS cluster is created in the specified subnets
  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_internet_gateway.blueprintbot_igw,
    aws_route_table_association.public_rt_assoc_1
  ]

  tags = {
    Name = "blueprintbot-v2-eks-cluster"
  }
}

resource "aws_eks_node_group" "blueprintbot_node_group" {
  cluster_name    = aws_eks_cluster.blueprintbot_cluster.name
  node_group_name = "blueprintbot-v2-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = [
    aws_subnet.private_subnet_1.id
  ]
  instance_types  = ["t3.medium"] # Example instance type, can be parameterized

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_node_policy_1,
    aws_iam_role_policy_attachment.eks_node_policy_2,
    aws_iam_role_policy_attachment.eks_node_policy_3,
    aws_eks_cluster.blueprintbot_cluster
  ]

  tags = {
    Name = "blueprintbot-v2-eks-node-group"
  }
}

# --- Output Variables ---
output "eks_cluster_name" {
  description = "The name of the EKS cluster"
  value       = aws_eks_cluster.blueprintbot_cluster.name
}

output "eks_cluster_endpoint" {
  description = "The endpoint for the EKS cluster API"
  value       = aws_eks_cluster.blueprintbot_cluster.endpoint
}

output "kubeconfig_command" {
  description = "Command to configure kubectl for the EKS cluster"
  value       = "aws eks update-kubeconfig --region ${aws_eks_cluster.blueprintbot_cluster.vpc_config[0].subnet_ids[0].region} --name ${aws_eks_cluster.blueprintbot_cluster.name}"
}

# --- Database (RDS PostgreSQL) ---
resource "aws_db_subnet_group" "blueprintbot_db_subnet_group" {
  name       = "blueprintbot-v2-db-subnet-group"
  subnet_ids = [
    aws_subnet.private_subnet_1.id
  ]

  tags = {
    Name = "blueprintbot-v2-db-subnet-group"
  }
}

resource "aws_db_instance" "blueprintbot_db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "14.5"
  instance_class       = "db.t3.micro"
  name                 = "blueprintbotdb"
  username             = "blueprintbotuser"
  password             = "${var.db_password}" # Use a variable for sensitive data
  db_subnet_group_name = aws_db_subnet_group.blueprintbot_db_subnet_group.name
  vpc_security_group_ids = [] # Attach appropriate security group
  skip_final_snapshot  = true

  tags = {
    Name = "blueprintbot-v2-db"
  }
}

# --- Object Storage (S3) ---
resource "aws_s3_bucket" "blueprintbot_assets" {
  bucket = "blueprintbot-v2-assets-${var.aws_account_id}" # Unique bucket name
  acl    = "private"

  tags = {
    Name = "blueprintbot-v2-assets"
  }
}

resource "aws_s3_bucket_versioning" "blueprintbot_assets_versioning" {
  bucket = aws_s3_bucket.blueprintbot_assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

# --- Container Registry (ECR) ---
resource "aws_ecr_repository" "blueprintbot_ecr" {
  name                 = "blueprintbot-v2-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "blueprintbot-v2-ecr"
  }
}

# --- Variables for sensitive data ---
variable "db_password" {
  description = "Password for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "aws_account_id" {
  description = "AWS Account ID for unique S3 bucket naming"
  type        = string
}

# --- Update Outputs ---
output "db_endpoint" {
  description = "The endpoint of the RDS PostgreSQL instance"
  value       = aws_db_instance.blueprintbot_db.address
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket for assets"
  value       = aws_s3_bucket.blueprintbot_assets.id
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.blueprintbot_ecr.repository_url
}

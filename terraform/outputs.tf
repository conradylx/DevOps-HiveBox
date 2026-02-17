output "cluster_name" {
    description = "EKS cluster name"
    value       = aws_eks_cluster.hivebox.name
}

output "cluster_endpoint" {
    description = "EKS cluster endpoint"
    value       = aws_eks_cluster.hivebox.endpoint
}

output "cluster_version" {
    description = "Kubernetes version"
    value       = aws_eks_cluster.hivebox.version
}

output "configure_kubectl" {
    description = "Command to configure kubectl"
    value       = "aws eks update-kubeconfig --name ${aws_eks_cluster.hivebox.name} --region ${var.region}"
}
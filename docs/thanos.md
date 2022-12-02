# THANOS DEMO

### Step 1: Create another cluster on Eleastic Kubernetes Service AWS

- Some prerequisites: Terraform, repair s3 bucket to store tfstate, AMI EC2
- After repairing, you will input name of bucket to [config file](../cluster-eks-infra/_config.tf) and AMI EC2 to [ec2 config](../cluster-eks-infra/ec2.tf). And start to deploy infrastructure cluster

### Step 2: Setup Thanos Agent on EKS

- Update kubeconfig by using command: ```aws eks --region region update-kubeconfig --name cluster_name```
- Setup config storage and sidecard: we will define storage in [thanos-storage-config](../thanos-config/thanos-storage-config.yaml) and values prometheus chart in [prometheus-operator-values](../thanos-config/prometheus-operator-values.yaml). And then upgrade the values of helm chart prometheus, and create the secret from-file thanos-storage-config.
- [Expose sidecard service](../thanos-config/thanos-sidecar-svc.yaml), therefor the prometheus master can access and query.
- Deploy [thanos-store](../thanos-config/thanos-store.yaml) to store backup data to storage object.

### Step 3: Setup Thanos Master on Local
- We will deploy all step in thanos agent, but discard the step expose sidecard. Because Thanos master can access in locally. 
- Next, we deploy [querier](../thanos-config/querier-deployment.yaml) for collecting data from thanos agent. Replace and add more agent in line 29 on [querier-deployment](../thanos-config/querier-deployment.yaml), that is the service sidecar we expose in setup thanos agent.
- Finally, we expose the [querier-service](../thanos-config/querier-service.yaml) to show Thanos UI.
    ![default ns](/image-promql-screenshot/thanos-screenshot/node_cpu_sidecar_eks_local.png)
    ![default ns](/image-promql-screenshot/thanos-screenshot/thanos-store.png)
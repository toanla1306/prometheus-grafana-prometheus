#! /bin/bash
# Setup config file in kubelet
sudo bash
mkdir ~/.kube/
cp /etc/rancher/k3s/k3s.yaml ~/.kube/
mv ~/.kube/k3s.yaml ~/.kube/config

# Start docker
systemctl daemon-reload
systemctl start docker

# Install Prometheus Grafana and Prometheus MSTeam with helm chart
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
cp /usr/local/bin/kubectl /bin/
cp /usr/local/bin/helm /bin/

kubectl create namespace monitoring

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-msteams https://prometheus-msteams.github.io/prometheus-msteams/

helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
helm install msteams prometheus-msteams/prometheus-msteams -n monitoring

# Create pod application
kubectl apply -f /vagrant/deployment/backend.yaml
kubectl apply -f /vagrant/deployment/frontend.yaml
kubectl apply -f /vagrant/deployment/trial.yaml

### Sending alert over SMTP ###
cd /vagrant/alertmanager-smtp/
# Create Alert Manager Config
helm upgrade --reuse-values \
    -f alertmanager-config.yaml prometheus \
    --namespace monitoring
    prometheus-community/kube-prometheus-stack

# Create record rules which sending alert
helm upgrade --reuse-values \
    -f alert-rules.yaml prometheus \
    --namespace monitoring \
    prometheus-community/kube-prometheus-stack


### Sending alert over MS Teams ###
cd /vagrant/alertmanager-msteams/
# Set connectors for alert manager msteams
helm upgrade -f connectors.yaml msteams \
    --namespace monitoring \
    prometheus-msteams/prometheus-msteams

kubectl create secret generic myalertmanager \
    --namespace monitoring \
    --from-file=alertmanager.yaml=alertmanager-msteams.yaml

helm upgrade -f enable-alert.yaml prometheus \
    --namespace monitoring \
    prometheus-community/kube-prometheus-stack
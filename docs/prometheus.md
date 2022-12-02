# PROMETHEUS DEMO
### 💡 Forward Multiple Port for Using on Host Machine
```
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring & \
kubectl port-forward service/prometheus-operated --address 0.0.0.0 9090:9090 -n monitoring & \
kubectl port-forward service/alertmanager-operated --address 0.0.0.0 9093:9093 -n monitoring &
```

### 💡 ServiceMonitoring in Pods
We will use servicemonitoring when we want to monitor each application on each pod. But prerequisites of servicemonitoring, the application in pod already installed libary prometheus metrics. And in this demo, we will know how to define prometheus metrics with Python and Java programming language.

- Step 1: we will develop application with prometheus metrics. 
  - In Python application, we will define package ```from prometheus_flask_exporter import PrometheusMetrics```. Additional, we can counter some request or connection database. Follow [backend](../demopython/backend/app.py), [frontend](../demopython/frontend/app.py), [trial](../demopython/trial/app.py) to more detail.
  - In Java application, we will define ```spring-boot-starter-actuator``` and ```micrometer-registry-prometheus``` dependency in [pom.xml](../demojava/pom.xml)
  - 

- Step 2: Create ServiceMonitor
  
  - After we build application image, and define it with kind deployment. We define it with kind ServiceMonitor custom resource in prometheus. Follow [ServiceMonitor Python application](../deployment/backend.yaml), [ServiceMonitor Java application](../deployment/java-monitor.yaml)
  ![default ns](/image-promql-screenshot/prometheus/servicemonitor.png)


### 💡 Blackbox Exporter
With blackbox method, we can easily to monitor status of the application.The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP, ICMP and gRPC. In this demo, we just focus on HTTP method.

- Step 1: Install node-exporter on the monitored server
  
  - Ref: https://ourcodeworld.com/articles/read/1686/how-to-install-prometheus-node-exporter-on-ubuntu-2004

- Step 2: Define Prometheus addition and create secret

    - Follow [prometheus-additional.yaml](../blackbox-exporter/prometheus-additional.yaml), you can change the right IP server that you want monitor
    - Create secret key with command: ```kubectl create secret generic additional-scrape-configs --from-file=prometheus-additional.yaml --namespace monitoring```
- Step 3: Enable additionalScrapeConfigsSecret and upgrade values helm chart Prometheus

  - Open file [values.yaml](../blackbox-exporter/values.yaml), find and enable additionalScrapeConfigsSecret
  - Upgrade helm chart prometheus with [values.yaml](../blackbox-exporter/values.yaml)
  
- Step 4: Install helm chart blackbox exporter

  - ```helm install prometheus-blackbox-exporter prometheus-community/prometheus-blackbox-exporter -f "blackbox-values.yaml" --namespace monitoring```
  ![default ns](/image-promql-screenshot/prometheus/blackbox.png)

### 💡 Backup and Restore
Reference: https://suraj.io/post/how-to-backup-and-restore-prometheus/
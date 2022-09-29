# prometheus-grafana-prometheus

> ### 💡 Forward multiple port for using on host machine
```
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring & \
kubectl port-forward service/prometheus-operated --address 0.0.0.0 9090:9090 -n monitoring & \
kubectl port-forward service/alertmanager-operated --address 0.0.0.0 9093:9093 -n monitoring &
```

> ### 💡 Login to Grafana
> - Access to localhost:3000
> - **Email or username:** admin
> - **Password:** prom-operator



> ### 💡 PromQL and Metrics in Grafana
![default ns](/image-promql-screenshot/container_cpu_usage_seconds_total.png)\
```rate(container_cpu_usage_seconds_total{namespace="monitoring"}[10m])```\
![default ns](/image-promql-screenshot/container_memory_cache.png)\
```rate(container_memory_cache{namespace="monitoring"}[10m])```\
![default ns](/image-promql-screenshot/container_memory_usage_bytes.png)\
```rate(container_memory_usage_bytes{namespace="monitoring"}[10m])```\
![default ns](/image-promql-screenshot/container_writes_per_read.png)\
```container_fs_writes_total{namespace="monitoring"} / container_fs_reads_bytes_total{namespace="monitoring"}```


> ### 💡 Create alert with SMTP
> 1. Create password application on Google account [Create password application for Gmail](https://www.getmailbird.com/gmail-app-password/)
> 2. Create file alertmanager-smtp/alertmanager-config.yaml used to define information of receivers that they will receive some alert
> ```helm upgrade --reuse-values -f alertmanager-smtp/alertmanager-config.yaml prometheus prometheus-community/kube-prometheus-stack -n monitoring```
> 3. Create file alertmanager-smtp/alert-rules.yaml which used to define record rule when some case alert
> ```helm upgrade --reuse-values -f alertmanager-smtp/alert-rules.yaml prometheus prometheus-community/kube-prometheus-stack -n monitoring```
> Reference: [Prometheus Alertmanager | Use Cases and Tutorial](https://www.containiq.com/post/prometheus-alertmanager)

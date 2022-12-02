# GRAFANA DEMO

### 💡 Forward Multiple Port for Using on Host Machine
```
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring & \
kubectl port-forward service/prometheus-operated --address 0.0.0.0 9090:9090 -n monitoring & \
kubectl port-forward service/alertmanager-operated --address 0.0.0.0 9093:9093 -n monitoring &
```

### 💡 Login to Grafana
- Access to localhost:3000
- **Email or username:** admin
- **Password:** prom-operator


### 💡 PromQL and Metrics in Grafana
![default ns](/image-promql-screenshot/container_cpu_usage_seconds_total.png)

```rate(container_cpu_usage_seconds_total{namespace="monitoring"}[10m])```

![default ns](/image-promql-screenshot/container_memory_cache.png)

```rate(container_memory_cache{namespace="monitoring"}[10m])```

![default ns](/image-promql-screenshot/container_memory_usage_bytes.png)

```rate(container_memory_usage_bytes{namespace="monitoring"}[10m])```

![default ns](/image-promql-screenshot/container_writes_per_read.png)

```container_fs_writes_total{namespace="monitoring"} / container_fs_reads_bytes_total{namespace="monitoring"}```

![default ns](/image-promql-screenshot/grafana/calculate_node_cpu_used.png)

```100 - (avg by (instance) (rate(node_cpu_seconds_total{job="node-exporter", mode="idle"}[1m])) * 100)```

### 💡 Create Variables in Dashboard
- Some case when we monitoring a lot of pods in multiple namespace, we should create a lot metrics with filter each namespace. It's very difficult to monitor. 
- Therefor, we will use variables in dashboard and can easy to switch between multiple namespace in only one metric.
    ![default ns](/image-promql-screenshot/grafana/edit-variable.png)
- After creating variable successfully, we will create metric in dashboard with promql syntax ```namespace="$namespace"```. In this demo, I monitor container CPU usage senconds totals, and easy to switch between multiple namespaces.
    ![default ns](/image-promql-screenshot/grafana/use-variable.png)

### 💡 Create Alert with SMTP
1. Create password application on Google account [Create password application for Gmail](https://www.getmailbird.com/gmail-app-password/)
2. Create file [alertmanager-smtp/alertmanager-config.yaml](../alertmanager-smtp/alertmanager-config.yaml) used to define information of receivers that they will receive some alert
```helm upgrade --reuse-values -f alertmanager-smtp/alertmanager-config.yaml prometheus prometheus-community/kube-prometheus-stack -n monitoring```
3. Create file [alertmanager-smtp/alert-rules.yaml](alertmanager-smtp/alert-rules.yaml) which used to define record rule when some case alert
```helm upgrade --reuse-values -f alertmanager-smtp/alert-rules.yaml prometheus prometheus-community/kube-prometheus-stack -n monitoring```
Reference: [Prometheus Alertmanager | Use Cases and Tutorial](https://www.containiq.com/post/prometheus-alertmanager)

### 💡 Create Alert Microsoft Teams
1. Create a channel will receive information alert. And then create incoming webhook in that channel. When created completely incoming webhook, we will have a url webhook like "https://xxx.webhook.office.com/webhookb2/(token)/IncomingWebhook/(another-token)"
   
   ![default ns](/image-promql-screenshot/grafana/incoming-webhook.png)

2. We can get http://localhost:3000/alerting/list or we can go to metrics in dashboard, and then create a new alert. In the template create alert, some case we should to define the tag. Because we will use it when we define Notification policies in the next step.
   
   ![default ns](/image-promql-screenshot/grafana/create-alert.png)

   ![default ns](/image-promql-screenshot/grafana/create-alert-in-metrics.png)

3. Create Contact points. In that step, we will define the way receive information of alert message. We will add url webhook in step 1.
   
   ![default ns](/image-promql-screenshot/grafana/create_contact_points.png)

4. Setting Notification policies. We will define contact point which you want to receive message, and all the labels of metrics that you want to monitoring. Additional, you can modify the repeat interval when grafana send alert.
   
   ![default ns](/image-promql-screenshot/grafana/setting_policy_firing.png)

5. We will receive the message alert when CPU higher than the point we created alert.
   
   ![default ns](/image-promql-screenshot/grafana/firing_first_time.png)


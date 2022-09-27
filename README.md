# prometheus-grafana-prometheus

> ### 💡 Forward multiple port for using on host machine
```
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring & \
kubectl port-forward service/prometheus-operated --address 0.0.0.0 9090:9090 -n monitoring & \
kubectl port-forward service/alertmanager-operated --address 0.0.0.0 9093:9093 -n monitoring &
```

> ### 💡 Login to Grafana
> 1. Access to localhost:3000
> 2. **Email or username:** admin
> 3. **Password:** prom-operator

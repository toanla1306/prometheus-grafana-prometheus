# PROMETHEUS
Prometheus is an open-source systems monitoring and alerting toolkit originally built at SoundCloud. Since its inception in 2012, many companies and organizations have adopted Prometheus, and the project has a very active developer and user community. It is now a standalone open source project and maintained independently of any company. To emphasize this, and to clarify the project's governance structure, Prometheus joined the Cloud Native Computing Foundation in 2016 as the second hosted project, after Kubernetes.

Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.

![default ns](/image-promql-screenshot/logo/prometheus-icon.png)

Reference: https://prometheus.io/docs/introduction/overview/

Details demo: [Prometheus.md](docs/prometheus.md)

# Grafana
Grafana open source software enables you to query, visualize, alert on, and explore your metrics, logs, and traces wherever they are stored. Grafana OSS provides you with tools to turn your time-series database (TSDB) data into insightful graphs and visualizations.

![default ns](/image-promql-screenshot/logo/grafana-icon.png)

Reference: https://grafana.com/docs/grafana/latest/introduction/

Details demo: [Grafana.md](docs/starter_grafana.md)

# Thanos
Thanos provides a global query view, high availability, data backup with historical, cheap data access as its core features in a single binary.

Those features can be deployed independently of each other. This allows you to have a subset of Thanos features ready for immediate benefit or testing, while also making it flexible for gradual roll outs in more complex environments.

![default ns](/image-promql-screenshot/logo/thanos-icon.png)

Reference: https://thanos.io/tip/thanos/getting-started.md/

Details demo: [Thanos.md](docs/thanos.md)

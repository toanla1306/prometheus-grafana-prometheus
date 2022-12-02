import logging

from flask import Flask, render_template, request
from flask_opentracing import FlaskTracing

from prometheus_flask_exporter import PrometheusMetrics

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Configure Jaeger tracer
def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

# Initial flask application
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

#Initial tracer
tracer = init_tracer('frontend')
flask_tracer = FlaskTracing(tracer, True, app)

#Metrics config
metrics = PrometheusMetrics(app)
metrics.info('frontend', 'Frontend Application info', version='1.0.3')
record_requests_by_status = metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
common_counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)
historgram_status_path = metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path', labels={'status': lambda r: r.status_code, 'path': lambda: request.path})

@app.route("/")
@record_requests_by_status
@common_counter
@historgram_status_path
def homepage():
    with tracer.start_active_span('home-page'):
        return render_template("main.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)

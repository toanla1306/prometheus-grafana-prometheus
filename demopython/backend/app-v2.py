from flask import Flask, render_template, request, jsonify

import os
import pymongo
import logging
from flask_pymongo import PyMongo

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.jaeger import JaegerPropagator

from prometheus_flask_exporter import PrometheusMetrics

jaeger_exporter = JaegerExporter(
   agent_host_name="simplest-query.observability.svc.cluster.local",
   agent_port=16686,
)

provider = TracerProvider(
    resource = Resource.create({SERVICE_NAME: "backend"})
)

processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

set_global_textmap(JaegerPropagator())


app = Flask(__name__)

# Metrics config
metrics = PrometheusMetrics(app)
metrics.info('backend', 'Backend Application info', version='1.0.3')
record_requests_by_status = metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
common_counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)
historgram_status_path = metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path', labels={'status': lambda r: r.status_code, 'path': lambda: request.path})

# DB config
app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

@app.route("/")
@record_requests_by_status
@common_counter
@historgram_status_path
@tracer.start_as_current_span("homepage")
def homepage():
    return "Hello World"


@app.route("/api")
@record_requests_by_status
@common_counter
@historgram_status_path
@tracer.start_as_current_span("api")
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
@record_requests_by_status
@common_counter
@historgram_status_path
@tracer.start_as_current_span("add start")
def add_star():
    star = mongo.db.stars
    name = request.json["name"]
    distance = request.json["distance"]
    star_id = star.insert({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})
from flask import Flask, request
from prometheus_client import start_http_server, Counter, Histogram
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total HTTP Requests")
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Latency in seconds")

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0.1, 0.5))  # Simulate processing
    return "Hello from Microservice!"

@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    start_http_server(8001)  # Start Prometheus metrics server
    app.run(host="0.0.0.0", port=8000)


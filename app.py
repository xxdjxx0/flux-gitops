from flask import Flask, render_template, jsonify

from flask import request, make_response
import random
import socket

import time
import sys

from prometheus_client import Counter, Histogram
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('test_app', request.path).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('test_app', request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
setup_metrics(app)

# list of cat images
images = [
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Combing-Itself.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Hug.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Playing-Basketball.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Playing-Ping-Pong.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Using-Chopsticks.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Using-Computer.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Wearing-Glasses.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-With-Beer.jpg",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-With-Teddy-Bear.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cats-Sitting-Like-Human.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cats-Using-iPad.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cats-Wearing-Party-Hats.gif"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

@app.route('/api')
def api():
    url = random.choice(images)
    podname = socket.gethostname()
    return jsonify({"version": "GIT_HASH", "podname": podname, "cat": url})

@app.route('/alive')
def alive():
    return "OK"

@app.route('/ready')
def ready():
    return "OK"

@app.route('/metrics')
def metrics():
    return make_response(generate_latest())

if __name__ == "__main__":
    app.run(host="0.0.0.0")

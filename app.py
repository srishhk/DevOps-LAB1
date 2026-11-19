"""Lab 1 sample application: a small Flask service used to demonstrate CI/CD.

Author: Srishti Kainth (2301730175)
"""
import os
import platform
import time
from datetime import datetime, timezone

from flask import Flask, jsonify

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local")
START_TIME = time.time()

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        message="Hello from Srishti's DevOps Lab 1 CI/CD pipeline!",
        version=APP_VERSION,
        build=BUILD_NUMBER,
    )


@app.route("/health")
def health():
    return jsonify(status="UP", uptime_seconds=round(time.time() - START_TIME, 2))


@app.route("/api/info")
def info():
    return jsonify(
        app="lab1-flask-app",
        version=APP_VERSION,
        build=BUILD_NUMBER,
        python=platform.python_version(),
        host=platform.node(),
        time_utc=datetime.now(timezone.utc).isoformat(),
    )


@app.route("/api/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify(a=a, b=b, result=a + b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))  # nosec B104

"""Demo service for the end-to-end CI/CD pipeline project.

Endpoints:
  GET /        -> service info + version
  GET /health  -> health check used by Kubernetes probes and CI smoke tests
"""
import os

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "dev")


@app.get("/")
def index():
    return jsonify(service="cicd-demo-app", version=VERSION, status="ok")


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

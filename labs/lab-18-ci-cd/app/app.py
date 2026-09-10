from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "DevOps CI/CD Lab 18", "version": "1.0.0"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


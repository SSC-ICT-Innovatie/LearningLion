from flask import Flask, jsonify, request

from DataFetcher.libraries.data_classes.range_enum import Range
from DataFetcher.run_local import run_local_datafetcher
from deployment.run_local import run_local_ingest_stores, run_local_query_stores
from inference.run_local import infer_run_local

app = Flask(__name__)

@app.route('/')
def index():
    return {"Hello": "World"}

@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/ping')
def ping():
    return {"pong"}

@app.route('/init', methods=['POST'])
def init():
    if request.is_json is False:
        return jsonify({"error": "Invalid JSON"})
    data = request.get_json()
    range = Range.Tiny
    if "range" in data:
        if data["range"] not in Range.__members__:
            return jsonify({"error": "Invalid range"})
        range = Range[data["range"]]
    run_local_datafetcher(range=range)
    run_local_ingest_stores()
    return True

@app.route('/prompt', methods=['POST'])
def prompt():
    # Access the JSON data sent in the request body
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No data provided"})
    if "prompt" not in data:
        return jsonify({"error": "No prompt provided"})

    documents = run_local_query_stores("Hallo")
    print(f"Got {len(documents)} documents")
    print(f"Documents: {documents[:5]}")
    AIresponse = infer_run_local("hallo")
    print(f"AI response: {AIresponse}")
    return jsonify({
        "prompt": data["prompt"],
        "output": AIresponse
    })
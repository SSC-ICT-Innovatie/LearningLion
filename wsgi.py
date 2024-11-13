from flask import Flask, jsonify, make_response, request

from DataFetcher.libraries.data_classes.range_enum import Range
from DataFetcher.run_local import run_local_datafetcher
from querier.run_local import getDocumentBlobFromDatabase, run_local_query_stores
from ingester.run_local import run_local_ingest_stores
from inference.run_local import infer_run_local
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

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
@cross_origin()
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
@cross_origin()
def prompt():
    # Access the JSON data sent in the request body
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No data provided"})
    if "prompt" not in data:
        return jsonify({"error": "No prompt provided"})

    documents = run_local_query_stores(data["prompt"])
    print(f"Got {len(documents)} documents")
    print(f"Documents: {documents[:5]}")
    AIresponse = infer_run_local(data["prompt"], files=documents)
    print(f"AI response: {AIresponse}")
    return jsonify({
        "prompt": data["prompt"],
        "documents": documents,
        "output": AIresponse
    })
@app.route('/document', methods=['GET'])
@cross_origin()
def document():
    getParams = request.args
    uuid = getParams.get('uuid')  # Fetch UUID safely
    if not uuid:
        return "UUID parameter is missing", 400  # Bad request if UUID is missing
    pdf_data = getDocumentBlobFromDatabase(uuid)
    if pdf_data is None:
        return "Document not found", 404  # Not found if UUID does not exist

    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename="document.pdf"'
    
    return response

@app.route('/query', methods=['POST'])
@cross_origin()
def query():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No data provided"})
    if "query" not in data:
        return jsonify({"error": "No query provided"})
    documents = run_local_query_stores(data["query"])
    return jsonify({
        "query": data["query"],
        "documents": documents
    })
    
@app.route('/llm', methods=['POST'])
@cross_origin()
def infer():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No data provided"})
    if "prompt" not in data:
        return jsonify({"error": "No prompt provided"})
    AIresponse = infer_run_local(data["prompt"], files=data["files"])
    return jsonify({
        "prompt": data["prompt"],
        "output": AIresponse
    })
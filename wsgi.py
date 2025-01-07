import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, make_response, request

from DataFetcher.libraries.data_classes.range_enum import Range
from DataFetcher.run_local import run_local_datafetcher
from ingester.libraries.database import Database
from ingester.libraries.embedding import Embedding
from querier.run_local import getDocumentBlobFromDatabase, run_local_query_stores
from ingester.run_local import run_local_ingest_stores
from inference.run_local import infer_run_local
from flask_cors import CORS, cross_origin

class RequestFilter(logging.Filter):
    def filter(self, record):
        record.ip = request.remote_addr if request else "No-IP"
        return True



range = Range.Tiny
app = Flask(__name__)

# if not app.debug:  # Enable logging only in production mode
# Create a file handler
file_handler = RotatingFileHandler(
    'app.log', maxBytes=1024 * 1024 * 10, backupCount=5
)  # Log file size = 10MB, keep 5 backups

# Set logging level and format
file_handler.setLevel(logging.INFO)  # Change to logging.DEBUG for debug info
formatter = logging.Formatter(
    '%(asctime)s - %(ip)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
file_handler.addFilter(RequestFilter())
# Add handler to Flask app logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Log that logging has started
app.logger.info('Logging is set up.')


cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    app.logger.info('Hello, World!')
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
    # log ip address
    app.logger.info(f"IP address: {request.remote_addr}")
    app.logger.info(f"Data recived: {data}")
    _range = range
    if data is None:
        app.logger.error("No data provided")
        return jsonify({"error": "No data provided"})
    if "query" not in data:
        app.logger.error("No query provided")
        return jsonify({"error": "No query provided"})
    if("range" in data):
        if data["range"] not in Range.__members__:
            return jsonify({"error": "Invalid range"})
        _range = Range[data["range"]]
    app.logger.info("Using range: {range.name}")
    documents = run_local_query_stores(data["query"], range=_range)
    app.logger.info(f"Documents: {documents}")
    return jsonify({
        "query": data["query"],
        "documents": documents
    })
    
@app.route('/llm', methods=['POST'])
@cross_origin()
def infer():
    data = request.get_json()
    app.logger.info(f"IP address: {request.remote_addr}")
    app.logger.info(f"Data recived: {data}")
    _range = range
    if data is None:
        app.logger.error("No data provided")
        return jsonify({"error": "No data provided"})
    if "prompt" not in data:
        app.logger.error("No prompt provided")
        return jsonify({"error": "No prompt provided"})
    files = []
    if "range" in data:
        if data["range"] not in Range.__members__:
            return jsonify({"error": "Invalid range"})
        _range = Range[data["range"]]
    app.logger.info(f"Using range: {range.name}")
    if "files" in data:
        embeddings = Embedding()
        database = Database(embed=embeddings, range=_range)
        files = data['files']
        fetchedFiles = []
        print(f"Files: {files}")
        for file in files:
            print(f"File: {file}")
            print(f"uuid {file.get('uuid')}")
            database.get_database_connection()
            # get answer from database
            fetchedData = database.getQuestion(file.get('uuid'), file.get('question_number'))
            fetchedFiles.append(fetchedData)
            
        print(f"Question and answer: {fetchedFiles}")
        app.logger.info(f"Question and answer: {fetchedFiles}")
    app.logger.info(f"Prompt: {data['prompt']}")
    AIresponse = infer_run_local(data["prompt"], files=fetchedFiles)
    app.logger.info(f"AI response: {AIresponse}")
    return jsonify({
        "prompt": data["prompt"],
        "output": AIresponse
    })
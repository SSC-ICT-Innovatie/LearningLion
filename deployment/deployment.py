# import database
# import embedding
# import ingestion
# import query

from langchain_core.documents import Document
import os
from pypdf import PdfReader

class Deployment:
  def __init__(self, base_directory=None, context=None):
    print("Initialized Main class")
  
  def request(self, data, context):
    try:
      if(data["action"] == "init"):
        source_dir=None
        if("source_dir" in data):
          source_dir = data["source_dir"]
        self.run(source_dir)
        return {
            "output": "Done"
        }
      if(data["action"] == "query"):
        return {
            "output": self.query_stores(data["query"])
        }
    except Exception as e:
      print("Error in request")
      print(f"Error: {str(e)}")
      return {
          "output": "Error",
          "error": str(e)
      }
      
  def query_stores(self, prompt):
    print("Querying stores")
    embed = embedding.Embedding()
    ingest = ingestion.Ingestion()
    data = database.Database(embed)
    data.download_vector_store()
    data.download_bm25_retriever()
    querier = query.Query()
    querier.setup_querier(data)
    return querier.query(prompt)
  
  def run(self, source_dir):
    try:
      print("Running Main class")
      
      # Initialize components
      embed = embedding.Embedding()
      data = database.Database(embed)
      querier = query.Query()
      ingest = ingestion.Ingestion()
      print("Classes initialized")

      # Set up embeddings and vector store
      print("Set up embeddings and vector store")
      ingest.setupTextSplitter()
      embed.setup_embeddings()
      data.setup_database()

      # Perform ingestion and retrieve BM25 retriever
      print("Perform ingestion")
      vector_store = data.get_vector_store()
      embeddings = embed.get_embeddings()
      (_, bm25) = ingest.ingest(source_dir=source_dir, vector_store=vector_store, embeddings=embeddings, bm25=data.get_bm25_retriever())
      print("Ingested")

      # Set and save BM25 retriever to ensure it's stored
      print("Set and save BM25")
      data.set_bm25_retriever(bm25)

      # Setup querier
      print("Setup querier")
      querier.setup_querier(data)

      # Upload vector store to bucket
      print("Upload vector store")
      data.upload_vector_store()
      print("Upload BM25 retriever")
      data.upload_bm25_retriever()
      
      print("Ready to query")
      # Test a query
      print("running test query")
      print(querier.query("test"))
      print("Main class done")
      print("Done")
    except Exception as e:
      print("Error in run")
      print(f"Error: {str(e)}")
      raise e
import database
import embedding
import ingestion
import query

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
    data = database.Database(embed)
    data.download_vector_store()
    data.download_bm25_retriever()
    querier = query.Query()
    querier.setup_querier(data)
    return querier.query(prompt)
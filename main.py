import database
import embedding
import preprocessor
import ingestion
import query

from langchain_core.documents import Document
import os
from pypdf import PdfReader

class Main:
  def __init__(self):
    print("Initialized Main class")
  def run(self):
    print("Running Main class")
    embed = embedding.Embedding()
    querier = query.Query()
    ingest = ingestion.Ingestion()
    data = database.Database()
    print("Classes initialized")
    ingest.setupTextSplitter()
    embed.setup_embeddings()
    data.setup_database(embeddings=embed.get_embeddings())
    (_, bm25) =  ingest.ingest(vector_store=data.get_vector_store(), embeddings=embed.get_embeddings(), bm25=data.get_bm25_retriever())
    print("Ingested")
    data.set_bm25_retriever(bm25)
    querier.setup_querier(data)
    print("Ready to query")
    print(querier.query("test"))
    print("Main class done")
    print("Done")

if __name__ == "__main__":
  main = Main()
  main.run()
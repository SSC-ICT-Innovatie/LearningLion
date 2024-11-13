from DataFetcher.libraries.data_classes.range_enum import Range
from ingester.libraries import database, ingestion
from ingester.libraries.embedding import Embedding

def run_local_ingest_stores(range=Range.Tiny):
  print("Running Main class")
  # Initialize components
  embed = Embedding()
  data = database.Database(embed)
  ingest = ingestion.Ingestion()
  print("Classes initialized")

  # Set up embeddings and vector store
  print("Set up embeddings and vector store")
  ingest.setupTextSplitter()
  embed.setup_embeddings(modelname="textgain/allnli-GroNLP-bert-base-dutch-cased")
  data.setup_database(range=range)

  # Perform ingestion and retrieve BM25 retriever
  print("Perform ingestion")
  vector_store = data.get_vector_store()
  db_connection = data.get_database_connection()
  embeddings = embed.get_embeddings()
  (_, bm25) = ingest.ingest(source_dir='./tmp', vector_store=vector_store, embeddings=embeddings, db_connection=db_connection)
  print("Ingested")

  # Set and save BM25 retriever to ensure it's stored
  print("Set and save BM25")
  data.set_bm25_retriever(bm25)
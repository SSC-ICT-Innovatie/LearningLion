from deployment.libraries import database, embedding, ingestion, query

def run_local_query_stores(prompt):
  print("Querying stores")
  embed = embedding.Embedding()
  ingest = ingestion.Ingestion()
  data = database.Database(embed)
  data.download_vector_store()
  data.download_bm25_retriever()
  querier = query.Query()
  querier.setup_querier(data)
  return querier.query(prompt)

def run_local_ingest_stores():
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
  (_, bm25) = ingest.ingest(source_dir='./tmp', vector_store=vector_store, embeddings=embeddings, bm25=data.get_bm25_retriever())
  print("Ingested")

  # Set and save BM25 retriever to ensure it's stored
  print("Set and save BM25")
  data.set_bm25_retriever(bm25)

  # Setup querier
  print("Setup querier")
  querier.setup_querier(data)
  
  print("Ready to query")
  # Test a query
  print("running test query")
  print(querier.query("test"))
  print("Main class done")
  print("Done")
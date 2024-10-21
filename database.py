from langchain_chroma import Chroma
import os
from langchain.retrievers import BM25Retriever

class Database:
  bm25Retriever = None
  vector_store = None
  
  def setup_database(self, embeddings):
    vectordb_folder = "./vectordb"
    vectordb_name = "NewPipeChroma"
    if not os.path.exists(vectordb_folder):
        os.mkdir(vectordb_folder)
    self.vector_store = Chroma(
        collection_name=vectordb_name,
        embedding_function=embeddings,
        persist_directory=vectordb_folder,
        collection_metadata={"hnsw:space": "cosine"}
    )

  def get_vector_store(self):
    if self.vector_store is None:
        print("Vector store not set")
        return None
    return self.vector_store

  def setup_bm25_retriever(self, docs=None):
    if docs is None:
      print("No documents to setup BM25 retriever")
      return
    print(f"got {len(docs)} documents")
    if self.bm25Retriever is None:
      print("BM25 retriever not set")
      return
    self.bm25Retriever = BM25Retriever(docs=docs)

  def get_bm25_retriever(self) -> BM25Retriever|None:
    if self.bm25Retriever is None:
        print("BM25 retriever not set")
        return None
    return self.bm25Retriever

  def set_bm25_retriever(self, bm25Retriever) -> bool:
    if type(bm25Retriever) != BM25Retriever:
      print("Didn't get a BM25Retriever object")
      return False
    self.bm25Retriever = bm25Retriever
import pickle
import sqlite3
from langchain_chroma import Chroma
import os
from langchain.retrievers import BM25Retriever

# from embedding import Embedding
from DataFetcher.libraries.data_classes.range_enum import Range
from querier.libraries.embedding import Embedding
from querier.libraries.ubiops_helper import UbiopsHelper
# from ubiops_helper import UbiopsHelper

class Database:
  bm25Retriever = None
  vector_store = None
  vectordb_folder = "vectordb"
  vectordb_name = "NewPipeChroma"
  embeddings = None
  con = None
  
  def __init__(self, embed:Embedding):
        if embed is not None:
            self.embeddings = embed
        else:
            print("No embeddings provided to Database class")
        print("Database class initialized")

  def getNameBasedOnRange(self, range=Range.Tiny):
        if range is not None:
            return (f"NewPipeChroma_{range.name}", f"vectordb_{range.name}")
  
  def setup_database(self,range=Range.Tiny):
      # Set up Chroma vector store
      if not os.path.exists(self.vectordb_folder):
          os.mkdir(self.vectordb_folder)
      if range is not None:
            print(f"Setting up database with range {range}")
            names = self.getNameBasedOnRange(range)
            Database.con = sqlite3.connect(f"{names[0]}.db", detect_types=sqlite3.PARSE_DECLTYPES)
            self.vectordb_name = names[0]
            self.vectordb_folder = names[1]
      
      # Initialize Chroma and save it
      Database.vector_store = Chroma(
          collection_name=self.vectordb_name,
          embedding_function=self.embeddings.get_embeddings(),
          persist_directory=self.vectordb_folder,
          collection_metadata={"hnsw:space": "cosine"}
      )        
  def get_database_connection(self, range: Range = Range.Tiny) -> sqlite3.Connection:
        if Database.con is None:
            names = self.getNameBasedOnRange(range)
            Database.con = sqlite3.connect(f"{names[0]}.db", detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
            print(f"Database connection set to {names[0]}")
        else:
            print("Database connection already set")
        return Database.con

  def close_database_connection(self):
        if Database.con:
            Database.con.close()
            Database.con = None
            print("Database connection closed")
        else:
            print("No database connection to close")
  def get_vector_store(self) -> Chroma | None:
      # Load vector store if not already set
      if Database.vector_store is None and self.embeddings is not None:
          if os.path.exists(self.vectordb_folder):
              Database.vector_store = Chroma(
                  persist_directory=self.vectordb_folder,
                  embedding_function=self.embeddings.get_embeddings(),
              )
              print("Vector store loaded from disk")
          else:
              print("No vector store found on disk")
              return None
      return Database.vector_store

  def setup_bm25_retriever(self, docs=None) -> BM25Retriever | None:
      if docs is None:
          print("No documents to setup BM25 retriever")
          return
      print(f"Got {len(docs)} documents")
      Database.bm25Retriever = BM25Retriever(docs=docs)
      self.save_bm25_retriever()
      
  def set_bm25_retriever(self, bm25):
      Database.bm25Retriever = bm25
      self.save_bm25_retriever()

  def get_bm25_retriever(self) -> BM25Retriever | None:
      if Database.bm25Retriever is None:
          self.load_bm25_retriever()
      return Database.bm25Retriever

  def save_bm25_retriever(self, filename="bm25_retriever.pkl"):
      if Database.bm25Retriever is None:
          print("BM25 retriever not set, nothing to save.")
          return False
      with open(filename, 'wb') as file:
          pickle.dump(Database.bm25Retriever, file)
      print(f"BM25 retriever saved to {filename}")
      return True

  def load_bm25_retriever(self, filename="bm25_retriever.pkl"):
      if not os.path.exists(filename):
          print(f"No file found at {filename} to load BM25 retriever.")
          return False
      with open(filename, 'rb') as file:
          Database.bm25Retriever = pickle.load(file)
      print(f"BM25 retriever loaded from {filename}")
      return True

  def upload_vector_store(self):
      if Database.vector_store is None:
          print("Vector store not set, nothing to upload.")
          return False
      # Upload each file in the vector store's persist directory
      for root, _, files in os.walk(self.vectordb_folder):
          for file in files:
              file_path = os.path.join(root, file)
              UbiopsHelper.uploadfile(file_path=file_path, dest_path='')
      print(f"Vector store uploaded successfully from {self.vectordb_folder}")
      return True

  def download_vector_store(self):
        # Download the vector store files
        UbiopsHelper.download_folder(project_name='learning-lion', bucket_name='default', folder_path=self.vectordb_folder, output_folder=self.vectordb_folder)
        print(f"Vector store downloaded successfully to {self.vectordb_folder}")
        return True
    
  def upload_bm25_retriever(self, filename="bm25_retriever.pkl"):
      # Ensure BM25 retriever is saved first
      if not self.save_bm25_retriever(filename):
          print("Failed to save BM25 retriever, not uploading.")
          return False
      # Upload the saved BM25 retriever file
      UbiopsHelper.uploadfile(file_path=filename, dest_path='')
      print(f"BM25 retriever uploaded successfully from {filename}")
      return True
  
  def download_bm25_retriever(self, filename="bm25_retriever.pkl"):
        # Download the BM25 retriever file
        UbiopsHelper.downloadfile(filename, project_name='learning-lion', bucket_name='default')
        # Load the BM25 retriever from the downloaded file
        self.load_bm25_retriever(filename)
        print(f"BM25 retriever downloaded successfully to {filename}")
        return True
import json
from sqlite3 import Connection
import traceback
import zipfile
import pymupdf
import pymupdf4llm
import requests
import ubiops
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from pypdf import PdfReader
from langchain.retrievers import BM25Retriever

from ingester.libraries.preprocessor import Preprocessor
from ingester.libraries.ubiops_helper import UbiopsHelper
import sqlite3
# from preprocessor import Preprocessor
# from ubiops_helper import UbiopsHelper

class Ingestion:
    text_splitter = None
    
    def __init__(self, base_directory=None, context=None):
        self.setupTextSplitter()
        print("Ingestion class initialized")
    
    def request(self):
        try:
            self.ingest()
            return True
        except:
            return False
        
    def getTextSplitter(self):
        return self.text_splitter

    def setupTextSplitter(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )

    def convert_text_to_document(self, text):
        return Document(page_content=text)
    
    def download_files_fromUbiOps_bucket(self, url):
        project_name = "learning-lion"
        bucket_items = url.split("/")
        bucket_items = list(filter(None, bucket_items))
        bucket_name = bucket_items[1]
        filesinBucket = UbiopsHelper.listFilesInBucket(project_name, bucket_name)
        print(f"full url: {bucket_items}")
        print(f"Downloading files from bucket: {bucket_name}")
        # remove ending in /
        output_dir = "./tmp/"
        print(filesinBucket)
        for file in filesinBucket.files:
            print(f"Downloading file: {file.file}")
            UbiopsHelper.downloadfile(file.file, project_name, bucket_name, output_dir)
        return output_dir
    
    def download_zip_only_fromUbiOps_bucket(self, url):
        project_name = "learning-lion"
        bucket_items = url.split("/")
        bucket_items = list(filter(None, bucket_items))
        bucket_name = bucket_items[1]
        filesinBucket = UbiopsHelper.listFilesInBucket(project_name, bucket_name)
        print(f"full url: {bucket_items}")
        print(f"Downloading zips from bucket: {bucket_name}")
        # remove ending in /
        output_dir = "./tmp/"
        print(filesinBucket)
        for file in filesinBucket.files:
            if not file.file.endswith(".zip"):
                continue
            print(f"Downloading file: {file.file}")
            UbiopsHelper.downloadfile(file.file, project_name, bucket_name, output_dir)
        return output_dir
    
    def summirize(self, text):
        # TODO: Implement summarization
        return "Summarized text"

    def ingest(self, source_dir=None, vector_store=None, embeddings=None, db_connection:Connection|None =None):
        vector_store = vector_store
        text_splitter = self.getTextSplitter()
        embeddings = embeddings
        sourceDir = source_dir if source_dir else "ubiops-file://default"
        if "ubiops-file://" in sourceDir:
            sourceDir = self.download_zip_only_fromUbiOps_bucket(sourceDir)
        documents = []
        # if zip is downloaded, unzip it with shutil
        for filename in os.listdir(sourceDir):
                file_path = os.path.join(sourceDir, filename)
                
                if filename.endswith(".zip"):
                    print(f"Unzipping {filename}")
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(sourceDir)
                    
                    print(f"Unzipped and removed {filename}")

        totalFiles_in_dir = len([name for name in os.listdir(sourceDir) 
                                if os.path.isfile(os.path.join(sourceDir, name)) and name.endswith('.pdf')])
        print(f"Total PDF files in directory found: {totalFiles_in_dir}")
        items = 0
        if os.path.exists(sourceDir):
            for filename in os.listdir(sourceDir):
                try:
                    if filename.endswith(".pdf"):
                        items += 1
                        file_path = os.path.join(sourceDir, filename)
                        with open(file_path, "rb") as pdf_file:
                            uuid = filename.split(".")[0]
                            reader = pymupdf.Document(pdf_file)
                            # Move the pointer back to the start of the file
                            pdf_file.seek(0)
                            # Read the raw bytes of the PDF document
                            blobData = pdf_file.read()
                            pdf_file.seek(0)
                            metadata_text = reader.metadata
                            print(f"metadata: {metadata_text.get('subject')}" )
                            pages = []
                            full_text = ""
                            doc_subject = metadata_text.get('subject') or "unknown"
                            doc_producer = metadata_text.get('producer') or "unknown"
                            full_text = pymupdf4llm.to_markdown(reader)
                            
                            pre = Preprocessor()
                            clean_full_text = pre.clean_text_MD(full_text)
                            
                            heading = pre.get_heading(clean_full_text)
                            qa_list = pre.get_question_and_answer(clean_full_text)
                            
                            
                            if db_connection:
                                # Check if document already exists
                                results = db_connection.execute("SELECT * FROM documents WHERE UUID=?", (uuid,)).fetchall()
                                if len(results) > 0:
                                    print(f"Document with UUID {uuid} already exists in database")
                                else:
                                    # Insert document
                                    db_connection.execute("INSERT INTO documents (UUID, filename, subject, producer, content, summirized, document_type, document) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                                                      (uuid, filename, doc_subject, doc_producer, clean_full_text, self.summirize(clean_full_text), "pdf", blobData))
                                    db_connection.commit()
                                    print("Written to database")

                            print("Processing pages")
                            print(f"Total pages: {len(pages)}")

                            questions = qa_list[0]
                            answers = qa_list[1]

                            if len(questions) == len(answers):
                                for i in range(len(questions)):
                                    question = questions[i]
                                    answer = answers[i]
                                    
                                    text = f"{heading}\nQuestion {i+1}: {question}\nAnswer {i+1}: {answer}"
                                
                                    split_pages = text_splitter.split_text(text)
                                    chunkNumber = 0
                                    for split_page in split_pages:
                                        doc = Document(page_content=split_page, 
                                                        metadata={"UUID": uuid, 
                                                                    "filename": filename,
                                                                    "subject":doc_subject,
                                                                    "total_pages": len(pages),
                                                                    "producer": doc_producer}, 
                                                        id=f"{uuid}_Q{i}_A{i}_{chunkNumber}")
                                        print(f"Adding document {doc.id} to vector store")
                                        print(doc)
                                        documents.append(doc)
                                        chunkNumber += 1
                                print(f"Processed {items} files out of {totalFiles_in_dir}")
                            else:
                                print("The number of questions and answers do not match.")
                except Exception as e:
                    print(f"Error while processing file: {filename}")
                    print(f"Error: {e}")
        print("Adding documents to vector store")

        # Set the batch size to 40,000 or any safe limit below the max size
        batch_size = 50
        total_batches = (len(documents) // batch_size) + 1
        batch_count = 0

        print("Adding documents to vector store in batches")
        for doc_batch in batch(documents, batch_size):
            batch_count += 1
            progress = (batch_count / total_batches) * 100
            print(f"Progress: {progress:.2f}% complete")
            try:
                vector_store.add_documents(
                    documents=doc_batch,
                    embedding=embeddings,
                )
            except Exception as e:
                print(f"Error adding batch {batch_count} to vector store:")
                traceback.print_exc()  # Print the full traceback
                print(f"Exception details: {str(e)}")  # Print any additional details from the exception object
                print(f"Batch {batch_count} content: {doc_batch}")

        print("Setting up BM25 retriever")
        print(f"Total documents: {len(documents)}")
        bm25 = BM25Retriever.from_documents(documents)

        print("done")
        print(f"Total files: {items}")
        return vector_store, bm25
        

def batch(iterable, batch_size):
    """Yield successive batches of specified size from the iterable."""
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]
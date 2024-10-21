from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from pypdf import PdfReader
from langchain.retrievers import BM25Retriever

class Ingestion:
    text_splitter = None
    
    def __init__(self):
        print("Ingestion class initialized")
    
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

    def ingest(self, vector_store=None, embeddings=None, bm25: BM25Retriever|None =None):
        vector_store = vector_store
        text_splitter = self.getTextSplitter()
        embeddings = embeddings
        sourceDir = "./docs/kamerVragen"
        documents = []

        totalFiles_in_dir = len([name for name in os.listdir(sourceDir) 
                                if os.path.isfile(os.path.join(sourceDir, name)) and name.endswith('.pdf')])
        print(f"Total PDF files in directory found: {totalFiles_in_dir}")
        items = 0
        if os.path.exists(sourceDir):
            for filename in os.listdir(sourceDir):
                if filename.endswith(".pdf"):
                    items += 1
                    file_path = os.path.join(sourceDir, filename)
                    with open(file_path, "rb") as pdf_file:
                        reader = PdfReader(pdf_file)
                        metadata_text = reader.metadata
                        pages = []
                        for i, p in enumerate(reader.pages):
                            extracted_text = p.extract_text().strip()
                            if extracted_text:
                                pages.append((i + 1, extracted_text))

                        cleaned_pages = []
                        for page_num, text in pages:
                            split_pages = text_splitter.split_text(text)
                            chunkNumber = 0
                            for split_page in split_pages:
                                uuid = filename.split(".")[0]
                                doc = Document(page_content=split_page, metadata={"page_number": page_num, "UUID": uuid}, id=f"{uuid}_{page_num}_{chunkNumber}")
                                documents.append(doc)
                                chunkNumber += 1
                    print(f"Processed {items} files out of {totalFiles_in_dir}")

        vector_store.add_documents(
            documents=documents,
            embedding=embeddings,
        )
        
        bm25 = BM25Retriever.from_documents(documents)

        print("done")
        print(f"Total files: {items}")
        return vector_store, bm25
        

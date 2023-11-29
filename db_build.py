# =========================
#  Module: Vector DB Build
# =========================
import box
import yaml
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
import timeit
import sys
import os


# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

# Build vector database
def run_db_build():
    start = timeit.default_timer()
   
    documents = []

    source = cfg.DATA_PATH
    log_file = cfg.LOG_FILE
    log_path = os.path.join(source, log_file)
    all_items = os.listdir(source)
    
    # Check which files are already loaded in the database (if any)
    existing_files = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            existing_files = file.read().splitlines()
    # Obtain files that aren't yet loaded
    new_files = [name for name in all_items if name not in existing_files and name != log_file]
    # Save their names to the logging file
    with open(log_path, 'a') as file:
        for name in new_files:
            file.write(name + '\n')
    if new_files:
        total_files = len(new_files)
    else:
        print("No (new) files available")
        sys.exit()
    
    for index, file in enumerate(new_files, start=1):
        if not file == log_file: # skip adding the logging file to the database
            print(f"Loading... {file} - File {index}/{total_files}", end='\r')
            print(end='\x1b[2K') # clear previous print so no overlap occurs

            if file.endswith('.pdf'):
                pdf_path = './data/' + file
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                doc_path = './data/' + file
                loader = Docx2txtLoader(doc_path)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                text_path = './data/' + file
                loader = TextLoader(text_path)
                documents.extend(loader.load())
    print(f"Done loading all {total_files} files")

    print("Splitting document text ...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                   chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    print("Loading embeddings ...")
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    print("Building FAISS VectorStore from documents and embeddings ...")
    vectorstore = FAISS.from_documents(texts, embeddings)

    if os.path.isfile('vectorstore/db_faiss/index.faiss') & os.path.isfile('vectorstore/db_faiss/index.pkl'):
        print(f"Loading existing database from ./{cfg.DB_FAISS_PATH}/ ...")
        local_index = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
        print(f"Merging new and existing databases ...")
        local_index.merge_from(vectorstore)
        print(f"Saving database to ./{cfg.DB_FAISS_PATH}/ ...")
        local_index.save_local(cfg.DB_FAISS_PATH)
    else:    
        print(f"Saving database to ./{cfg.DB_FAISS_PATH}/ ...")
        vectorstore.save_local(cfg.DB_FAISS_PATH)
    end = timeit.default_timer()
    print(f"Done building database. Time to build database: {round((end - start)/60, 2)} minutes")

if __name__ == "__main__":
    run_db_build()

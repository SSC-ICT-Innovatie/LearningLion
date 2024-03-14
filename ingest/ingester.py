"""
Ingester class
Creates Ingester object
Also parses files, chunks the files and stores the chunks in vector store
When instantiating without parameters, attributes get values from settings.py
"""
import os
from dotenv import load_dotenv
from loguru import logger
# local imports
import settings
# from ingest.content_iterator import ContentIterator
from ingest.ingest_utils import IngestUtils
from ingest.file_parser import FileParser
from ingest.woo_parser import WooParser
import utils as ut
import pandas as pd


class Ingester:
    """
    Create Ingester object
    When instantiating without parameters, attributes get values from settings.py
    """
    def __init__(self, collection_name: str, content_folder: str, vectordb_folder: str,
                 embeddings_provider=None, embeddings_model=None, text_splitter_method=None,
                 vecdb_type=None, chunk_size=None, chunk_overlap=None, local_api_url=None,
                 file_no=None, azureopenai_api_version=None, data_type=None):
        load_dotenv()
        self.collection_name = collection_name
        self.content_folder = content_folder
        self.vectordb_folder = vectordb_folder
        self.embeddings_provider = settings.EMBEDDINGS_PROVIDER if embeddings_provider is None else embeddings_provider
        self.embeddings_model = settings.EMBEDDINGS_MODEL if embeddings_model is None else embeddings_model
        self.text_splitter_method = settings.TEXT_SPLITTER_METHOD \
            if text_splitter_method is None else text_splitter_method
        self.vecdb_type = settings.VECDB_TYPE if vecdb_type is None else vecdb_type
        self.chunk_size = settings.CHUNK_SIZE if chunk_size is None else chunk_size
        self.chunk_overlap = settings.CHUNK_OVERLAP if chunk_overlap is None else chunk_overlap
        self.local_api_url = settings.API_URL \
            if local_api_url is None and settings.API_URL is not None else local_api_url
        self.file_no = file_no
        self.azureopenai_api_version = settings.AZUREOPENAI_API_VERSION \
            if azureopenai_api_version is None and settings.AZUREOPENAI_API_VERSION is not None \
            else azureopenai_api_version
        self.data_type = settings.DATA_TYPE if data_type is None else data_type

    def ingest(self) -> None:
        """
        Chooses the right method to ingest the data
        """
        match self.data_type:
            case "woo":
                logger.info("Ingesting woo data")
                self.ingest_woo()
            case _:
                logger.info("Ingesting standard data")
                self.ingest_standard()

    def ingest_standard(self) -> None:
        """
        Creates file parser object and ingestutils object and iterates over all files in the folder
        Checks are done whether vector store needs to be synchronized with folder contents
        """
        file_parser = FileParser()
        ingestutils = IngestUtils(self.chunk_size, self.chunk_overlap, self.file_no, self.text_splitter_method)

        # get embeddings
        embeddings = ut.getEmbeddings(self.embeddings_provider,
                                      self.embeddings_model,
                                      self.local_api_url,
                                      self.azureopenai_api_version)

        # create empty list representing added files
        new_files = []

        if self.vecdb_type == "chromadb":
            # get all relevant files in the folder
            files_in_folder = [f for f in os.listdir(self.content_folder)
                               if os.path.isfile(os.path.join(self.content_folder, f))]
            relevant_files_in_folder = []
            for file in files_in_folder:
                # file_path = os.path.join(self.content_folder, file)
                _, file_extension = os.path.splitext(file)
                if file_extension in [".docx", ".html", ".md", ".pdf", ".txt"]:
                    relevant_files_in_folder.append(file)
                else:
                    logger.info(f"Skipping ingestion of file {file} because it has extension {file[-4:]}")

            # if the vector store already exists, get the set of ingested files from the vector store
            if os.path.exists(self.vectordb_folder):
                # get chroma vector store
                vector_store = ut.get_chroma_vector_store(self.collection_name, embeddings, self.vectordb_folder)
                logger.info(f"Vector store already exists for specified settings and folder {self.content_folder}")
                # determine the files that are added or deleted
                collection = vector_store.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                collection_ids = [int(id) for id in collection['ids']]
                files_in_store = [metadata['filename'] for metadata in collection['metadatas']]
                files_in_store = list(set(files_in_store))
                # check if files were added or removed
                new_files = [file for file in relevant_files_in_folder if file not in files_in_store]
                files_deleted = [file for file in files_in_store if file not in relevant_files_in_folder]
                # delete all chunks from the vector store that belong to files removed from the folder
                if len(files_deleted) > 0:
                    logger.info(f"Files are deleted, so vector store for {self.content_folder} needs to be updated")
                    idx_id_to_delete = []
                    for idx in range(len(collection['ids'])):
                        idx_id = collection['ids'][idx]
                        idx_metadata = collection['metadatas'][idx]
                        if idx_metadata['filename'] in files_deleted:
                            idx_id_to_delete.append(idx_id)
                    vector_store.delete(idx_id_to_delete)
                    logger.info("Deleted files from vectorstore")
                # determine updated maximum id from collection after deletions
                collection = vector_store.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                collection_ids = [int(id) for id in collection['ids']]
                start_id = max(collection_ids) + 1
            # else it needs to be created first
            else:
                logger.info(f"Vector store to be created for folder {self.content_folder}")
                # get chroma vector store
                vector_store = ut.get_chroma_vector_store(self.collection_name, embeddings, self.vectordb_folder)
                collection = vector_store.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                # all files in the folder are to be ingested into the vector store
                new_files = list(relevant_files_in_folder)
                start_id = 0

            # If there are any files to be ingested into the vector store
            if len(new_files) > 0:
                logger.info(f"Files are added, so vector store for {self.content_folder} needs to be updated")
                for file in new_files:
                    file_path = os.path.join(self.content_folder, file)
                    # extract raw text pages and metadata according to file type
                    raw_pages, metadata = file_parser.parse_file(file_path)
                    # convert the raw text to cleaned text chunks
                    documents = ingestutils.clean_text_to_docs(raw_pages, metadata)
                    logger.info(f"Extracted {len(documents)} chunks from {file}")
                    # and add the chunks to the vector store
                    # add id to file chunks for later identification
                    vector_store.add_documents(
                        documents=documents,
                        embedding=embeddings,
                        collection_name=self.collection_name,
                        persist_directory=self.vectordb_folder,
                        ids=[str(id) for id in list(range(start_id, start_id + len(documents)))]
                    )
                    # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                    collection = vector_store.get()
                    collection_ids = [int(id) for id in collection['ids']]
                    start_id = max(collection_ids) + 1
                logger.info("Added files to vectorstore")

            # save updated vector store to disk
            vector_store.persist()

    def ingest_woo(self) -> None:
        woo_parser = WooParser()
        ingestutils = IngestUtils(self.chunk_size, self.chunk_overlap, self.file_no, self.text_splitter_method)

        # Get embeddings
        embeddings = ut.getEmbeddings(self.embeddings_provider, self.embeddings_model, self.local_api_url, self.azureopenai_api_version)
        
        if self.vecdb_type == "chromadb":
            # Set the datatypes for the columns
            dtypes={"id": str, "foi_documentId": str, "foi_dossierId": str, "bodytext_foi_pageNumber": int, "bodytext_foi_bodyText": str, "bodytext_foi_bodyTextOCR": str, "bodytext_foi_hasOCR": bool, "bodytext_foi_redacted": float, "bodytext_foi_nrRedactedRegions": int, "bodytext_foi_contourArea": float, "bodytext_foi_textArea": float, "bodytext_foi_charArea": float, "bodytext_foi_percentageTextAreaRedacted": float, "bodytext_foi_percentageCharAreaRedacted": float, "bodytext_foi_imageArea": int, "bodytext_foi_imageCoversFullPage": int, "bodytext_foi_bodyTextJaccard": float, "documents_dc_title": str, "documents_dc_description": str, "documents_foi_fileName": str, "documents_dc_format": str, "documents_dc_source": str, "documents_dc_type": str, "documents_foi_nrPages": int, "documents_foi_pdfDateCreated": str, "documents_foi_pdfDateModified": str, "documents_foi_pdfCreator": str, "documents_foi_pdfProducer": str, "documents_foi_pdfAuthor": str, "documents_foi_pdfCompany": str, "documents_foi_pdfTitle": str, "documents_foi_pdfSubject": str, "documents_foi_pdfKeywords": str, "documents_foi_fairiscore": int, "dossiers_dc_title": str, "dossiers_dc_description": str, "dossiers_dc_type": str, "dossiers_dc_type_description": str, "dossiers_dc_publisher": str, "dossiers_dc_publisher_name": str, "dossiers_dc_source": str, "dossiers_foi_valuation": str, "dossiers_foi_requestText": str, "dossiers_foi_decisionText": str, "dossiers_foi_isAdjourned": str, "dossiers_foi_requester": str, "dossiers_foi_fairiscore": int, "dossiers_tooiwl_rubriek": str, "dossiers_tooiwl_rubriekCode": str, "dossiers_foi_geoInfo": str}
            woo_data = pd.read_csv(f'{self.content_folder}/woo_merged.csv.gz', parse_dates=['dossiers_foi_publishedDate', 'dossiers_dc_date_year', 'dossiers_foi_requestDate', 'dossiers_foi_decisionDate', 'dossiers_foi_retrievedDate'], dtype=dtypes).set_index('id')
            
            # If the vector store already exists, get the set of ingested files from the vector store
            if os.path.exists(self.vectordb_folder):
                vector_store = ut.get_chroma_vector_store(self.collection_name, embeddings, self.vectordb_folder)
                # Determine the files that are added or deleted
                collection = vector_store.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                collection_ids = [int(id) for id in collection['ids']]
                files_in_store = [metadata['id'] for metadata in collection['metadatas']]
                files_in_store = list(set(files_in_store))
                # Check if there are any deleted items
                files_deleted = [file for file in files_in_store if file not in woo_data.index]
                if len(files_deleted) > 0:
                    logger.info(f"Files are deleted, so vector store for {self.content_folder} needs to be updated")
                    idx_id_to_delete = []
                    for idx in range(len(collection['ids'])):
                        idx_id = collection['ids'][idx]
                        idx_metadata = collection['metadatas'][idx]
                        if idx_metadata['id'] in files_deleted:
                            idx_id_to_delete.append(idx_id)
                    print(idx_id_to_delete)
                    vector_store.delete(idx_id_to_delete)
                    logger.info("Deleted files from vectorstore")
                # Check if there is new data and only keep the new data
                woo_data = woo_data.drop(files_in_store, errors='ignore')
                collection = vector_store.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                collection_ids = [int(id) for id in collection['ids']]
                if len(collection_ids) == 0:
                    start_id = 0
                else:
                    start_id = max(collection_ids) + 1
            # Else it needs to be created first
            else:
                logger.info(f"Vector store to be created for folder {self.content_folder}")
                # Get chroma vector store
                vector_store = ut.get_chroma_vector_store(self.collection_name, embeddings, self.vectordb_folder)
                collection = vector_store.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
                start_id = 0
                
            if len(woo_data) > 0:
                logger.info(f"Files are added, so vector store for {self.content_folder} needs to be updated")
                for index, row in woo_data.reset_index().iterrows():
                    # Extract raw text pages and metadata
                    raw_pages, metadata = woo_parser.parse_woo(row)
                    if raw_pages is None or metadata is None:
                        continue
                    
                    # Convert the raw text to cleaned text chunks
                    documents = ingestutils.clean_text_to_docs(raw_pages, metadata)
                    if len(documents) == 0:
                        continue
                    
                    vector_store.add_documents(
                        documents=documents,
                        embedding=embeddings,
                        collection_name=self.collection_name,
                        persist_directory=self.vectordb_folder,
                        ids=[str(id) for id in list(range(start_id, start_id + len(documents)))]
                    )
                    collection = vector_store.get()
                    collection_ids = [int(id) for id in collection['ids']]
                    start_id = max(collection_ids) + 1
                logger.info("Added files to vectorstore")
                
                # Save updated vector store to disk
                vector_store.persist()
            else:
                logger.warning(f"No new woo documents to be ingested")

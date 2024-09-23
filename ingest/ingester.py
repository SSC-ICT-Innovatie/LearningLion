"""
Ingester class
Creates Ingester object
Also parses files, chunks the files and stores the chunks in vector store
When instantiating without parameters, attributes get values from settings.py
"""
import os
from typing import Tuple, List
import re
from dotenv import load_dotenv
from loguru import logger
from sympy import false

# local imports
import settings
# from ingest.content_iterator import ContentIterator
from ingest.ingest_utils import IngestUtils
from ingest.file_parser import FileParser
import utils as ut
import pandas as pd
import numpy as np


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

    import re

    def get_footer(self, text):

        splitted = text.split(" ")
        footer = []
        splitted.reverse()
        if splitted[0].isdigit():
            splitted.pop(0) # Remove page number
        for split in splitted:
            if "Tweede" in split:
                footer.append(split)
                footer.reverse()
                return " ".join(footer)
            else:
                footer.append(split)
        return ""


    def get_question_and_answer(self, text):

        footnotes = self.extract_footnotes(text)
        footer = self.get_footer(text)
        pages = self.get_amount_of_pages(text,footer)
        text = self.remove_footer_and_pagenumbers(text,footer,pages)
        docspecs = self.get_doc_specs(text)
        text = text.replace(docspecs, "")
        textLen = len(text)
        text = self.normalize_whitespace(text)
        question_pattern = r"(Vraag\s\d+.*?)(?=\s*Antwoord)"
        answer_pattern = r"(Antwoord\s\d+.*?)(?=Vraag|\Z)"

        questions = re.findall(question_pattern, text, re.DOTALL)
        answers = re.findall(answer_pattern, text, re.DOTALL)

        questions = [q.strip() for q in questions]
        answers = [a.strip() for a in answers]

        # Remove footnotes from returns
        questions = [self.remove_footnotes(q, footnotes) for q in questions]
        answers = [self.remove_footnotes(a, footnotes) for a in answers]

        questions = [self.normalize_whitespace(q) for q in questions]
        answers = [self.normalize_whitespace(a) for a in answers]

        return [questions, answers]

    def ingest(self) -> None:
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
                    metadata['filename'] = self.strip_file_path(file_path)
                    # convert the raw text to cleaned text chunks
                    documents = ingestutils.clean_text_to_docs(raw_pages, metadata)
                    logger.info(f"Extracted {len(documents)} chunks from {file}")
                    # and add the chunks to the vector store
                    # add id to file chunks for later identification
                    if(documents != []):
                        combined_text = ''.join([doc.page_content for doc in documents])
                        self.get_question_and_answer(combined_text)
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

    def strip_file_path(self, file_path: str) -> str:
        """
        Strips the file path to the filename
        """
        return os.path.basename(file_path)

    def extract_footnotes(self, text:str):
        footnotePattern = re.compile(r'(\d+)\s+(.*?)(?=\d+\s|$)', re.DOTALL)

        strings_with_numbers = []
        footnotes = []

        # matches = list(footnotePattern.finditer(text))
        # strings_with_numbers.extend(matches)

        # matches = footnotePattern.findall(text)
        matches = list(footnotePattern.finditer(text))
        for match in matches:
            # Group 1 will contain the first part (e.g., "1 Ja")
            # Group 2 will contain the second part (e.g., "1 Trouw 17 december 2011, «meeste crèches krijgen minder klantjes»")
            # strings_with_numbers.append(match.group(1))

            # Group 1 will contain the footnote number (e.g., "1")
            footnote_number = match.group(1)

            # Group 2 will contain the text associated with that footnote (e.g., "Financieel Dagblad ... 24 september 2014")
            footnote_text = match.group(2).strip()

            # Combine the footnote number and text into a single string, if needed
            # combined_text = f"{footnote_number} {footnote_text}"

            # Append to the list
            strings_with_numbers.append(footnote_number)
            strings_with_numbers.append(footnote_text)
        # Now footnotes will contain the extracted pairs
        print(strings_with_numbers)

        footnote_index = 0
        pages = []
        current_page = []
        pattern = re.compile(r'\b' + str(footnote_index + 1) + r'\b')
        for string in strings_with_numbers:
            if string is None:
                continue
            # Check if 's-Gravenhage 2014 is in the string
            if '’s-Gravenhage' in string:
                print(string)
                # If found, add the current page to pages
                pages.append(current_page)
                # Reset current_page for the next page
                current_page = []
            else:
                # Otherwise, keep adding strings to the current page
                current_page.append(string)
        textnexttopattern = re.compile(r'\d+\s+[^\d\s]')

        for page in pages:
            page.reverse()
            passedItems = []
            foundfooternotes = false
            for pageitem in page:
                if foundfooternotes:
                    passedItems.reverse()
                    for passeditem in passedItems:
                        pattern = re.compile(r'\b' + str(footnote_index + 1) + r'(?![\d])')

                        if pattern.search(passeditem):  # Checks if the exact number is in the string
                            footnotes.append(passeditem)
                            footnote_index += 1
                        else:
                            if("ah-tk" in passeditem):
                                break
                            if footnotes[len(footnotes) - 1].endswith("-"):
                                footnotes[len(footnotes) - 1] = f"{footnotes[len(footnotes) - 1]}{passeditem.strip()}".strip()
                            else:
                                footnotes[len(footnotes) - 1] = f"{footnotes[len(footnotes) - 1]} {passeditem.strip()}".strip()

                    break
                if pattern.search(pageitem):  # Checks if the exact number is in the string
                    footnote_index += 1
                    footnotes.append(pageitem)
                    foundfooternotes = True
                else:
                    passedItems.append(pageitem)

        return footnotes

    def remove_footnotes(self, text, footnotes):
        for footnote in footnotes:
            text = text.replace(footnote, "")
        return text.strip()

    def get_amount_of_pages(self, text, footer):
        return text.find(footer)

    def remove_footer(self, text, footer):
        if footer is not None:
            text = text.replace(footer, "")
            return text.strip()
        return text.strip()

    def remove_footer_and_pagenumbers(self, text,footer, amountpages):
        textLength = len(text)
        for number in range(amountpages):
            text = self.remove_footer(text, f"{footer} {str(number + 1)}")
        if(textLength == len(text)):
            for number in range(amountpages):
                text = self.remove_footer(text, footer)
        return text.strip()

    def get_doc_specs(self, text):
        pattern = r"(ah-tk-\d{8}-\d{3} ISSN\s*\d{4}\s*-\s*\d{4}\s*’s-Gravenhage\s*\d{4})"

        match = re.search(pattern, text)

        if match:
            return match.group(1)
        else:
            return "Desired identifiers not found."

    def normalize_whitespace(self, text):
        # Replace multiple spaces with a single space
        return re.sub(r'\s+', ' ', text).strip()


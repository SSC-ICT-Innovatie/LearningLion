import time
import os
import pandas as pd
from loguru import logger

def select_woogle_dump_folders(path:str='./docs') -> str:
    """
    Look for folders containing "WoogleDumps" in their names and return the selected folder.
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        logger.error(f'Path: "{path}" does not exist or is not a directory.')
        return None
    
    # Look for folders containing "woogle_dump" in their names
    folders_with_woogle_dumps = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder)) and "WoogleDumps" in folder]

    print("Folders containing 'WoogleDumps':")
    for idx, folder in enumerate(folders_with_woogle_dumps, start=1):
        print(f"{idx}. {folder}")

    if not folders_with_woogle_dumps:
        logger.error("No folders containing 'WoogleDumps' were found.")
        return None
    
    selection = int(input("Select a folder by number: ")) - 1
    return f"{path}/{folders_with_woogle_dumps[selection]}"

def read_docs(path:str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """"
    Reads the bodytext, dossier and document csv files from the given path and returns them as dataframes.
    """
    # Manually set the correct types
    bodytext_dtypes = {'dc_publisher_name': str, 'dc_publisher': str, 'foi_documentId': str, 'foi_pageNumber': int, 'foi_bodyText': str, 'foi_bodyTextOCR': str, 'foi_hasOCR': bool, 'foi_redacted': float, 'foi_contourArea': float, 'foi_textArea': float, 'foi_charArea': float, 'foi_percentageTextAreaRedacted': float, 'foi_percentageCharAreaRedacted': float, 'foi_nrWords': int, 'foi_nrChars': int, 'foi_nrWordsOCR ': int, 'foi_nrCharsOCR': int}
    dossier_dtypes = {'dc_identifier': str, 'dc_title': str, 'dc_description': str, 'dc_type': str, 'foi_type_description': str, 'dc_publisher_name': str, 'dc_publisher': str, 'dc_source': str, 'foi_valuation': str, 'foi_requestText': str, 'foi_decisionText': str, 'foi_isAdjourned': str, 'foi_requester': str}
    document_dtypes = {'dc_identifier': str, 'foi_dossierId': str, 'dc_title': str, 'foi_fileName': str, 'dc_format': str, 'dc_source': str, 'dc_type': str, 'foi_nrPages': int}
    
    # Start recording the time
    start_time = time.time()
    logger.info(f"Reading data from {path}...")
    
    bodytext_dataframe = pd.read_csv(f'{path}/woo_bodytext.csv.gz', dtype=bodytext_dtypes).set_index('foi_documentId')
    # Manually changes some columns, has to be done seperately due to nan values
    bodytext_dataframe['foi_redacted'] = bodytext_dataframe['foi_redacted'].astype(bool)
    dossier_dataframe = pd.read_csv(f'{path}/woo_dossiers.csv.gz', parse_dates=['foi_publishedDate', 'dc_date_year', 'foi_requestDate', 'foi_decisionDate', 'foi_retrievedDate'], dtype=dossier_dtypes).set_index('dc_identifier')
    document_dataframe = pd.read_csv(f'{path}/woo_documents.csv.gz', dtype=document_dtypes).set_index('dc_identifier')
    
    # Log time it took
    logger.info(f"Data read in {time.time() - start_time:.2f} seconds.")
    
    return bodytext_dataframe, dossier_dataframe, document_dataframe

def save_docs(df:pd.DataFrame, filename:str) -> None:
    """
    Saves the given dataframe to the given filename. If the file already exists, it will not be overwritten.
    """
    if not os.path.exists(filename):
        df.to_csv(filename, compression='gzip')
    else:
        logger.warning(f"Skipping file as it already exists at location: {filename}")

def truncate_merge_docs(length:int=10) -> None:
    """
    Truncates the bodytext, dossier and document dataframes to the given length and saves them in a new directory.
    Also merges the dataframes and saves the result in the new directory.
    """
    path = select_woogle_dump_folders()
    if path is None:
        logger.error("No folder was selected. Exiting...")
        return

    bodytext_dataframe, dossier_dataframe, document_dataframe = read_docs(path)
    
    nr_dossiers, _ = dossier_dataframe.shape
    if length > nr_dossiers:
        logger.error(f"Length is larger than the number of dossiers in the dataset. Exiting...")
        return None

    # Define the new directory based on path and length
    new_directory = f"{path}_{length}"

    # Check if the directory exists, if not, create it
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    # Get the dc_identifier of the first "n = length" dossiers
    dossiers = dossier_dataframe.head(length)
    save_docs(dossiers, f'{new_directory}/woo_dossiers.csv.gz')
    
    # Only use the documents and bodytext that are in the selected dossiers
    documents = document_dataframe[document_dataframe['foi_dossierId'].isin(dossiers.index)]
    save_docs(documents, f'{new_directory}/woo_documents.csv.gz')

    bodytext = bodytext_dataframe[bodytext_dataframe.index.isin(documents.index)]
    save_docs(bodytext, f'{new_directory}/woo_bodytext.csv.gz')
    
    # Write document with all the data joined
    # Create primary key for bodytext

    bodytext.reset_index(inplace=True)
    bodytext.index = bodytext['foi_documentId'] + ".pagina." + bodytext['foi_pageNumber'].astype(str)
    bodytext.index.name = 'id'
    
    # Prefix headers, so you know which columns come from which dataframe
    prefix_bodytext = 'bodytext_'
    exclude_bodytext = 'foi_documentId'
    bodytext.columns = [prefix_bodytext + col if col != exclude_bodytext else col for col in bodytext.columns]

    prefix_documents = 'documents_'
    exclude_documents = 'foi_dossierId'
    documents.columns = [prefix_documents + col if col != exclude_documents else col for col in documents.columns]

    prefix_dossiers = 'dossiers_'
    dossiers.columns = [prefix_dossiers + col for col in dossiers.columns]

    joined_bodytext_documents = bodytext.join(documents, on='foi_documentId')
    result = joined_bodytext_documents.join(dossiers, on='foi_dossierId')
    result = result[result['dossiers_dc_type_description'] == 'Dossier na Woo/Wob-verzoek']
    
    save_docs(result, f'{new_directory}/woo_merged.csv.gz')
    
    logger.info(f"Truncated data successfully saved to {new_directory}.")

if __name__ == "__main__":
    truncate_merge_docs()
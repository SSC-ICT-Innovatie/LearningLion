import os
import random
from loguru import logger
import pandas as pd
from langchain_community.vectorstores.chroma import Chroma


from ingest.file_parser import FileParser
from ingest.ingest_utils import IngestUtils
from ingest.ingester import Ingester, IngestionMode
from query.querier import Querier
from settings import CHUNK_SIZE, TEXT_SPLITTER_METHOD
import utils as ut





def test_retrival_singular(question: str, source_doc, querier: Querier) -> None:
    """
    Test the retrieval of the documents
    """
    documents = querier.get_documents_with_scores(question)
    if(len(documents) <= 0):
        logger.info("No documents found")
        return False
    highest_score_document = documents[0]
    logger.info(f"Highest score: {highest_score_document[1]}")
    if(source_doc == highest_score_document[0].metadata['filename']):
        logger.info("Source document found")
        return True
    else:
        logger.info("Source document not found")
        return False
        
# Get the first question out of the file and retrive the document
def test_retrival(folder_path, ingester: Ingester, querier: Querier, toCSV: bool = False, ingestionMode:IngestionMode = None, addedMetaDataURLCSV:str = None, addContext:bool = None, embeddings_model:str = None, text_splitter_method:str = None, embeddings_provider:str = None, database:str = None, ConcatFiles:bool = False) -> None:
    total_files_checked_questions = 0
    total_files_found_question = 0
    total_files_checked_Answers = 0
    total_files_found_Answers = 0
    file_parser = FileParser()

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            questionsList = []
            answersList = []
            file_path = os.path.join(folder_path, filename)
            
            raw_pages, metadata = file_parser.parse_file(file_path)
            if ConcatFiles:
                concatnated_text = ""
                for doc in raw_pages:
                    concatnated_text += doc[1]
                questions, answers = ingester.get_question_and_answer(concatnated_text)
                if(questions != None and len(questions) > 0):
                    questionsList.append(questions)
                else:
                    continue
                if(answers != None):
                    answersList.append(answers)
            else:
            # Get question to test
                for doc in raw_pages:
                    questions, answers = ingester.get_question_and_answer(doc[1])
                    if(questions != None):
                        questionsList.append(questions)
                    if(answers != None):
                        answersList.append(answers)
            if(len(questionsList) <= 0 or questionsList[0] == None):
                logger.info("No questions found in file")
            else:
                total_files_checked_questions += 1
                randomQuestion = questionsList[0]
                if(len(randomQuestion) < 0):
                    logger.info("No questions found in file")
                else:
                    querier.get_documents_with_scores(randomQuestion[0])
                    if(test_retrival_singular(randomQuestion[0], filename,querier=querier)):
                        total_files_found_question += 1
            if(len(answersList) <= 0 or answersList[0] == None):
                logger.info("No answers found in file")
            else:
                total_files_checked_Answers += 1
                randomAnswer = answersList[0]
                if(len(randomAnswer) <= 0):
                    logger.info("No answers found in file")
                else:
                    querier.get_documents_with_scores(randomAnswer[0])
                    if(test_retrival_singular(randomAnswer[0], filename,querier=querier)):
                        total_files_found_Answers += 1

    logger.info("Questions")
    logger.info(f"Total files checked with questions: {total_files_checked_questions}")
    logger.info(f"Total files found with questions: {total_files_found_question}")
    logger.info(f"Percentage found: {total_files_found_question/total_files_checked_questions*100}%")
    logger.info(f"Average precision: {total_files_found_question/total_files_checked_questions}")
    logger.info("Answers")
    logger.info(f"Total files checked with answers: {total_files_checked_Answers}")
    logger.info(f"Total files found with answers: {total_files_found_Answers}")
    logger.info(f"Percentage found: {total_files_found_Answers/total_files_checked_Answers*100}%")
    logger.info(f"Average precision: {total_files_found_Answers/total_files_checked_Answers}")
    
 # If toCSV is True, handle the DataFrame and CSV export
    if toCSV:
        print("writing to csv")
        # Create a DataFrame with new data
        new_data = pd.DataFrame({
            "Total files checked with questions": [total_files_checked_questions],
            "Total files found with questions": [total_files_found_question],
            "Percentage found questions": [total_files_found_question / total_files_checked_questions * 100],
            "Average precision questions": [total_files_found_question / total_files_checked_questions],
            "Total files checked with answers": [total_files_checked_Answers],
            "Total files found with answers": [total_files_found_Answers],
            "Percentage found answers": [total_files_found_Answers / total_files_checked_Answers * 100],
            "Average precision answers": [total_files_found_Answers / total_files_checked_Answers],
            "ingestionMode": [ingestionMode],
            "addedMetaDataURLCSV": [addedMetaDataURLCSV],
            "addContext": [addContext],
            "embeddings_model": [embeddings_model],
            "text_splitter_method": [text_splitter_method],
            "embeddings_provider": [embeddings_provider],
            "database": [database],
            "concatFiles": [ConcatFiles]
        })
        
        # Check if the CSV file already exists
        file_path = "results_test_retrival.csv"
        if os.path.exists(file_path):
            # If the file exists, read it and concatenate the new data
            existing_data = pd.read_csv(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            # If the file doesn't exist, the new data becomes the updated data
            updated_data = new_data
        
        # Export the updated DataFrame to the CSV file
        updated_data.to_csv(file_path, index=False)
    print("done writing to csv")

def store_questions_and_answers_CSV(folder_path, ingester, concatFiles:bool = False) -> None:
    """Store all the questions and answers in a CSV file"""
    file_parser = FileParser()
    dataList = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            raw_pages, metadata = file_parser.parse_file(file_path)
            questions, answers = [], []
            if concatFiles:
                # for doc in raw_pages:
                concatnated_text = ""
                for doc in raw_pages:
                    concatnated_text += doc[1]
                doc_questions, doc_answers = ingester.get_question_and_answer(concatnated_text)
                questions.extend(doc_questions)
                answers.extend(doc_answers)
            else:
                # Get question to test
                for doc in raw_pages:
                    doc_questions, doc_answers = ingester.get_question_and_answer(doc[1])
                    questions.extend(doc_questions)
                    answers.extend(doc_answers)
            if questions is not None or answers is not None:
                data = {
                    'Filename': filename,
                    'Questions': questions if questions is not None else '',
                    'Answers': answers if answers is not None else ''
                }
                dataList.append(data)
    df = pd.DataFrame(dataList)
    df.to_csv('questions_and_answers.csv', index=False)
    print("done writing to csv")

    
def test_retrival_map_grading(folder_path, ingester: Ingester, querier: Querier, toCSV: bool = False, ingestionMode:IngestionMode = None, addedMetaDataURLCSV:str = None, addContext:bool = None, embeddings_model:str = None, text_splitter_method:str = None, embeddings_provider:str = None, database:str = None, concatFiles:bool = False) -> None:
    """Grade the """
    file_parser = FileParser()
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf") is False:
            continue
        questionsList = []
        answersList = []
        file_path = os.path.join(folder_path, filename)
        raw_pages, metadata = file_parser.parse_file(file_path)
        
        if concatFiles:
            # for doc in raw_pages:
            concatnated_text = ""
            for doc in raw_pages:
                concatnated_text += doc[1]

            questions, answers = ingester.get_question_and_answer(concatnated_text)
            if(questions != None and len(questions) > 0):
                questionsList.append(questions)
            else:
                continue
            if(answers != None):
                answersList.append(answers)
                
        else:
            # Get question to test
            for doc in raw_pages:
                questions, answers = ingester.get_question_and_answer(doc[1])
                if(questions != None):
                    questionsList.append(questions)
                if(answers != None):
                    answersList.append(answers)


        retrieved_page_ids = []
        retrieved_document_ids = []
        scores = []
        if(len(questionsList) <= 0 and questionsList[0] != None and len(questionsList[0]) <= 0):
            logger.info("No questions found in file")
            continue
        
        documents = querier.get_documents_with_scores(question=questionsList[0][0])
        AveragePrecision = 0
        MeanAveragePrecision = 0
        
        for document,score in documents:
            retrieved_page_ids.append(document.metadata['page_number'])
            retrieved_document_ids.append(document.metadata['filename'])
            scores.append(score)
        
        # if len(retrieved_page_ids) != len(raw_pages):
        #     logger.error(f"Length of retrieved pages does not match the length of the raw pages")
        #     return
        
        correct_count = sum(
            (retrieved_document_ids[i] == filename if i < len(retrieved_document_ids) else False) 
            for i in range(100)
        )
        retrieved_count = len(retrieved_page_ids)
        precision = correct_count / retrieved_count if retrieved_count > 0 else 0
        recall = correct_count / len(raw_pages)
        precision_at_k = [
            sum(1 for x in retrieved_document_ids[:i+1] if x == filename) / (i+1)
            for i in range(retrieved_count) if retrieved_document_ids[i] == filename
        ]
        map_score = sum(precision_at_k) / len(precision_at_k) if precision_at_k else 0
        
        # Create a DataFrame with new data
        new_data = pd.DataFrame({
            "Filename": [filename],
            "Correct count": [correct_count],
            "Retrieved count": [retrieved_count],
            "Precision": [precision],
            "Recall": [recall],
            "MAP": [map_score],
            "ingestionMode": [ingestionMode],
            "addedMetaDataURLCSV": [addedMetaDataURLCSV],
            "addContext": [addContext],
            "embeddings_model": [embeddings_model],
            "text_splitter_method": [text_splitter_method],
            "embeddings_provider": [embeddings_provider],
            "database": [database],
            "concatFiles": [concatFiles]
        })
        
        # Check if the CSV file already exists
        file_path = f"results_MAP_grading_'{normilze_param_to_string(ingestionMode.name)}'_embeddingsModel-'{normilze_param_to_string(embeddings_model)}'_textSplitter-'{normilze_param_to_string(text_splitter_method)}'_embeddingsProvider-'{normilze_param_to_string(embeddings_provider)}'_database-'{normilze_param_to_string(database)}'.csv"
        if os.path.exists(file_path):
            # If the file exists, read it and concatenate the new data
            existing_data = pd.read_csv(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            # If the file doesn't exist, the new data becomes the updated data
            updated_data = new_data
        
        # Export the updated DataFrame to the CSV file
        updated_data.to_csv(file_path, index=False)
    print("done writing to csv")

def normilze_param_to_string(param):
    if type(param) != str:
            param = f"{param}"
        
    if param is None:
        return "None"
    param = param.strip("_").replace("/", "_").replace("\"", "_")
    
    return param
        
        
def get_random_sample_ids(folder, sample_size):
    """Get a sample of random ids from the folder"""
    randomsampleids = []
    for sample in range(sample_size):
        randomsampleids.append(random.choice(os.listdir(folder)))
    return randomsampleids

def create_evaluation_sample_questions(folder, ingester: Ingester, destinationCSV: str):
    """Create a sample of questions to evaluate the retrieval"""
    file_parser = FileParser()
    randomsampleids = get_random_sample_ids(folder, 100)
    dataList = []
    
    # Set to hold filenames already added to dataList
    added_filenames = set()
    
    if(os.path.exists(destinationCSV)):
        print("CSV file already exists")
        df = pd.read_csv(destinationCSV)
        
        # Check if context is missing
        if 'context' not in df.columns:
            print("CSV file already exists but does not have context column")
            print("adding context column")
        
            file_parser = FileParser()
            ingestutils = IngestUtils(CHUNK_SIZE, 0, None, TEXT_SPLITTER_METHOD)
            for index, row in df.iterrows():
                if row["context"] is not None:
                    continue
                file = row["Filename"]
                if file.endswith(".pdf"):
                    file_path = os.path.join(folder, file)
                    raw_pages, metadata = file_parser.parse_file(file_path)
                    documents = ingestutils.clean_text_to_docs(raw_pages, metadata)
                    introduction = documents[0].page_content.split("vraag")[0]

                df.at[index, "context"] = introduction
                df.to_csv(destinationCSV, index=False)
            print("done adding context to csv")
            return
            
        if len(df) >= 100:
            print("CSV file already exists and has more than 100 samples")
            return
        return

    while len(dataList) < 100:
        # Pick random file if not enough samples
        randomsampleids.append(random.choice(os.listdir(folder)))
        
        for filename in os.listdir(folder):
            # Break loop if we've already collected 100 items
            if len(dataList) >= 100:
                break

            # Skip if the filename is not in randomsampleids
            if filename not in randomsampleids:
                continue

            # Skip if the filename is already in dataList (checked using the set)
            if filename in added_filenames:
                continue

            if filename.endswith(".pdf"):
                file_path = os.path.join(folder, filename)
                raw_pages, metadata = file_parser.parse_file(file_path)
                
                if len(raw_pages) <= 0:
                    continue
                
                # Concatenate all pages' content
                concats = ""
                for doc in raw_pages:
                    concats += doc[1]
                
                questions, answers = ingester.get_question_and_answer(concats)
                
                introduction = concats.split("vraag")[0]
                
                
                # Ensure questions list is not empty
                if not questions or len(questions) == 0:
                    continue
                randomQuestion = random.choice(questions)
                if randomQuestion is not None:
                    data = {
                        'Filename': filename,
                        'Question': randomQuestion,
                        'context': introduction
                    }
                    dataList.append(data)
                    added_filenames.add(filename)  # Add the filename to the set after adding to dataList

    # Write the data to CSV
    df = pd.DataFrame(dataList)
    df.to_csv(destinationCSV, index=False)
    print("done writing to csv")
    
def evaluate_with_sample_questions(samplequestionsCSVPATH,querier: Querier, toCSV: bool = False, ingestionMode:IngestionMode = None, addedMetaDataURLCSV:str = None, addContext:bool = None, embeddings_model:str = None, text_splitter_method:str = None, embeddings_provider:str = None, database:str = None, concatFiles:bool = False):
    """Evaluate the retrieval with the sample questions"""
    df = pd.read_csv(samplequestionsCSVPATH)
    correct_count = 0
    for index, row in df.iterrows():
        question = f"{row['context']} {row['Question']}"
        documents = querier.get_documents_with_scores(question=row['Question'])
        if len(documents) > 0:
            if documents[0][0].metadata['filename'] == row['Filename']:
                correct_count += 1
                
                
    print(f"Correct count: {correct_count}")
    print(f"Total count: {len(df)}")
    print(f"Percentage: {correct_count/len(df)*100}%")
    print(f"Average precision: {correct_count/len(df)}")
    
    if toCSV:
        print("writing to csv")
        # Create a DataFrame with new data
        new_data = pd.DataFrame({
            "Total files checked with questions": [len(df)],
            "Total files found with questions": [correct_count],
            "Percentage found questions": [correct_count / len(df) * 100],
            "Average precision questions": [correct_count / len(df)],
            "ingestionMode": [ingestionMode],
            "addedMetaDataURLCSV": [addedMetaDataURLCSV],
            "addContext": [addContext],
            "embeddings_model": [embeddings_model],
            "text_splitter_method": [text_splitter_method],
            "embeddings_provider": [embeddings_provider],
            "database": [database],
            "concatFiles": [concatFiles]
        })
        
        # Check if the CSV file already exists
        file_path = "results_test_retrival.csv"
        if os.path.exists(file_path):
            # If the file exists, read it and concatenate the new data
            existing_data = pd.read_csv(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            # If the file doesn't exist, the new data becomes the updated data
            updated_data = new_data
        
        # Export the updated DataFrame to the CSV file
        updated_data.to_csv(file_path, index=False)
    print("done writing to csv")
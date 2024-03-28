import os
from loguru import logger
# local imports
from asr.asr import AutomatedSystematicReview as asr
import utils as ut
import settings

def main():
    # Create instance of Querier once
# Get source folder with docs from user
    content_folder_name = ut.get_content_folder_name(only_check_woo=settings.DATA_TYPE == "woo")

    question_list_name = input('Please insert file name of question list: ') + '.txt'
    # get associated vectordb path
    content_folder, _ = ut.create_vectordb_name(content_folder_name)
    question_list_path = os.path.join(content_folder, "review", question_list_name)

    # If vector store folder does not exist, stop
    if not os.path.exists(content_folder):
        logger.info("This content folder does not exist. Please make sure the spelling is correct")
        ut.exit_program()
    elif not os.path.exists(question_list_path):
        logger.info("This question list does not exist, please make sure this list exists.")
        ut.exit_program()
    else:
        asr(content_folder, question_list_path).conduct_review()


if __name__ == "__main__":
    main()

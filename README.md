# LearningLion

## Description of the project
The project is a study on the use of generative AI to improve the services of SSC-ICT by supporting employees and optimizing internal processes. In particular, the focus is on generative large language models (LLM) because they can have the most significant impact on the daily work of SSC-ICT employees. The assignment (Speech Recognition & AI) has been approved by the SpB and has been running since the beginning of 2023. 

## Repository
The current repository contains a selection of project documents as well as the code to a Proof of Concept (PoC) Chatbot Demo. The demo is an example of Retrieval Augmented Generation (RAG) and allows for the use of Open-Source LLM's for CPU Inference on a local machine. It makes use of Langchain and FAISS libraries among other things to perform document Q&A. A schematic overview of how the application works is shown here: 

![Alt text](project_docs/AI Demo arch.png raw=true "Demo Architecture")


## Acknowledgements
This is a fork of Kenneth Leung's original repository, that adjusts the original code in several ways:
- A streamlit visualisation is available to make it more user-friendly
- Follow-up questions are now possible thanks to memory implementation
- Different models now appear as options for the user
- Multiple other optimalisations 

___
# Running Locally

## Quickstart
- Note: If you want to run this in an offline environment, read the following instructions first: [Using offline embeddings](#using-offline-embeddings)

- Ensure you have downloaded the model of your choice in GGUF format and placed it into the `models/` folder. Some examples:
    - https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF
    - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

- Fill the `data/` folder with .pdf, .doc(x) or .txt files you want to ask questions about

- To build a FAISS database with information regarding your files, launch the terminal from the project directory and run the following command <br>
`python db_build.py`

- To start asking questions about your files, run the following command: <br>
`streamlit run main_st.py`

- Choose which model to use for Q&A and adjust parameters to your liking

![Alt text](assets/qa_output.png)

___
## Using offline embeddings
Necessary word embeddings are usually *downloaded* when running the application. This works for most use cases, but not for those where this application has to be run without any connection to the internet at all.

In those cases, perform the following steps:
1.  Download the desired embedding files from https://sbert.net/models
    - This repo uses `all-MiniLM-L6-v2.zip`
    - Unzip to folder: `sentence-transformers_all-MiniLM-L6-v2/`
    - If you want to use different embeddings, you should adjust the folder name and the reference to it in `db_build.py` (line 74)
2. Go to the `.cache/` folder on your offline machine
    - Can be found in `C:/Users/[User]/` for most Windows machines
3. Within this folder, create `torch/sentence_transformers/` if nonexistent
4. Place embedding folder from step 1 inside of `/sentence_transformers/`

If all steps were performed correctly, the application will find the embeddings locally and will not try to download the embeddings.
___
## Tools
- **LangChain**: Framework for developing applications powered by language models
- **LlamaCPP**: Python bindings for the Transformer models implemented in C/C++
- **FAISS**: Open-source library for efficient similarity search and clustering of dense vectors.
- **Sentence-Transformers (all-MiniLM-L6-v2)**: Open-source pre-trained transformer model for embedding text to a 384-dimensional dense vector space for tasks like clustering or semantic search.
- **Llama-2-7B-Chat**: Open-source fine-tuned Llama 2 model designed for chat dialogue. Leverages publicly available instruction datasets and over 1 million human annotations. 

___
## Files and Content
- `/assets`: Images relevant to the project
- `/config`: Configuration files for LLM application
- `/data`: Dataset used for this project (i.e., Manchester United FC 2022 Annual Report - 177-page PDF document)
- `/models`: Binary file of GGUF quantized LLM model (i.e., Llama-2-7B-Chat) 
- `/src`: Python codes of key components of LLM application, namely `llm.py`, `utils.py`, and `prompts.py`
- `/vectorstore`: FAISS vector store for documents
- `db_build.py`: Python script to ingest dataset and generate FAISS vector store
- `db_clear.py`: Python script to clear the previously built database
- `main_st.py`: Main Python script to launch the streamlit application 
- `main.py`: Python script to launch an older version of the application within the terminal, mainly used for testing purposes
- `requirements.txt`: List of Python dependencies (and version)
___

## References
- https://huggingface.co/TheBloke
- https://github.com/abetlen/llama-cpp-python
- https://python.langchain.com/docs/integrations/llms/llamacpp# Demo-CPU-Inference

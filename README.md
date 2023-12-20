# LearningLion

## Description of the project
The project is a study on the use of generative AI to improve the services of SSC-ICT by supporting employees and optimizing internal processes. In particular, the focus is on generative large language models (LLM) because they can have the most significant impact on the daily work of SSC-ICT employees. The assignment (Speech Recognition & AI) has been approved by the SpB and has been running since the beginning of 2023. 

## Repository
The current repository contains a selection of project documents as well as the code to a Proof of Concept (PoC) Chatbot Demo. The demo is an example of Retrieval Augmented Generation (RAG) and allows for the use of Open-Source LLM's for CPU Inference on a local machine. It makes use of Langchain and FAISS libraries among other things to perform document Q&A. A schematic overview of how the application works is shown here: 

![alt text](https://github.com/SSC-ICT-Innovatie/LearningLion/blob/main/project_docs/images/AI%20Demo%20arch.png)
___
# Running Locally
## Quickstart

- Ensure you have downloaded the model of your choice in GGUF format and placed it into the `models/` folder. Some examples:
    - https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF
    - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

- Fill the `data/` folder with .pdf, .doc(x) or .txt files you want to ask questions about

- To build a vectorstore database of your files, launch the terminal from the project directory and run the following command <br>
`python db_build.py`

- To start the application, run the following command: <br>
`streamlit run main_st.py`

- Use the interface to choose a model and adjust the parameters

- You can now start asking questions about your files

![Alt text](Placeholder screenshot of app)
___
## Complete walkthrough (work in progress)
### 1. Clone Repository
- Open a terminal

- Navigate to the location where you want the cloned directory to be

- Input the git clone command using the LearningLion repository link in the terminal
```
git clone https://github.com/SSC-ICT-Innovatie/LearningLion.git
```

- Press enter to create your local clone

### 2. Download your models
- There are numerous open source models available to download on [Huggingface](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard). When you run an LLM on a personal machine, you will probably use smaller models (max 7/13B parameters).

- If you are running on a CPU, look for models in GGUF format. These models are quantized, which means the weiths of the model are converted to lower precision datatypes. This makes them less computationally heavy to run, but it also means they are less accurate and stable.

- Some example of GGUF models
    - https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF
    - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF
    - https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF
    - https://huggingface.co/TheBloke/Llama-2-13B-Chat-Dutch-GGUF

- Most models have different versions. Make sure you select one that meets your system requirements. For example, listed here are several quantized versions of the Mistral 7B model. 

![alt text](https://github.com/SSC-ICT-Innovatie/LearningLion/blob/main/project_docs/images/model%20quantization%20screenshot.png)

- Download the models you want and place them in the `models/` folder

### 3. Input files for your database
- Choose the files you want to include in your RAG knowledge base and place them in the `data/` folder, the model will use these files to answer questions

- Use .pdf, .docx, or .txt files

### 4. Install requirements
- Create a virtual environment using conda or venv

- Install the required packages and libraries to your virtual environment using the pip install command

```
pip install -r requirements.txt
```

### 4. Build your vectorstore database
- Run the db_build file in the terminal to build your vectorstore
```
python db_build.py
```
- Wait for the function to finsih, this may take up to several minutes depending on the size of your `data/` folder

### 5. Run the application
- Start the application using Streamlit
```
streamlit run main_st.py
```
- The application will automatically start your browser. You can also access it in a different browser using http://localhost:8501

### 6. Adjust your settings
- Using the panel on the left side of the interface you can adjust your settings

- The first setting allows you to select a **model** from the `/models` folder

- The **temperature** setting controls the 'creativity' or randomness of the model
    - Low temperature *(0)* = deterministic, precise, focused
    - High temperature *(1)* = diverse, creative

- **max_length** sets the amount of tokens a model is allowed to use in a response
    - A token is a chunk of text that a model reads or generates; a general introduction by [OpenAI](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
    - A model will not always use every available token but in general allowing a model to use more tokens will lead to longer responses and longer required time to generate an answer
    - This setting is also useful when using commercial models, where you often pay per token
 
- **n_sources** how many document chunks will be fed to the model to generate an answer
    - Using more sources will also lead to more input context and a longer runtime

- **prompt** in this window you can adjust the system prompt 

### 8. Asking questions
- Now you're all set to use the application

- You can use the `clear history` button to clear the chat history
    - The application has a memory function, meaning that it will use the previous questions and answers as context to answer follow-up questions
    - This also means that with every question, the context size increases, so the runtime increases

- To shut down the application access the terminal and press <kbd>Ctrl</kbd> + <kbd>C</kbd>

### 9. Adding files to your database
delete db
create new db


> [!NOTE]
> If you want to run this in an offline environment, read the following instructions first: [Using offline embeddings](#using-offline-embeddings)

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
- `/data`: Dataset used for this project
- `/models`: Binary files of GGUF quantized LLM model (i.e., Llama-2-7B-Chat) 
- `/src`: Python codes of key components of LLM application, namely `llm.py` and `utils.py`
- `/vectorstore`: FAISS vector store for documents
- `db_build.py`: Python script to ingest dataset and generate FAISS vector store
- `db_clear.py`: Python script to clear the previously built database
- `main_st.py`: Main Python script to launch the streamlit application 
- `requirements.txt`: List of Python dependencies (and version)
___
## Acknowledgements
This is a fork of [Kenneth Leung's original repository](https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference/tree/main), and also gratefully makes use of [Dennis V's](https://github.com/Vlassie/Llama-2-CPU-Inference) work. 

## References
- https://huggingface.co/TheBloke
- https://github.com/abetlen/llama-cpp-python
- https://python.langchain.com/docs/integrations/llms/llamacpp# Demo-CPU-Inference

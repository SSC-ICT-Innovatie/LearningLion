# LearningLion

## Description of the project
The project is a study on the use of generative AI to improve the services of SSC-ICT by supporting employees and optimizing internal processes. In particular, the focus is on generative large language models (LLM), in the form of Retrieval Augmented Generation (RAG), because they can have the most significant impact on the daily work of SSC-ICT employees. The assignment (Speech Recognition & AI) has been approved by the SpB and has been running since the beginning of 2023. 

## Repository
The current repository is based on the repository made by PBL under the direction of Stefan Troost (https://github.com/pbl-nl/appl-docchat), changed for our specific use cases. The demo is an example of Retrieval Augmented Generation (RAG) and allows for the use and evaluation of both Open and Closed-Source LLM's. It makes use of Langchain, Chroma and Streamlit among other things to perform document Q&A. Right now it is mostly a clone with some additions (to make running it locally easier for example) and it contains additional project documents (in project_docs) that provide background information about this project, the decisions we made and the research we conducted. 

A schematic overview of how the application works is shown here:

![RAG flow design](https://github.com/SSC-ICT-Innovatie/LearningLion/blob/main/project_docs/images/RAG%20flow%20design.png)

## How to use this repo
! This repo is tested on a Windows platform
The instructions as written assume you have Anaconda and Python installed. 
If not, download python (https://www.python.org/downloads/) and follow this installation guides:
https://docs.anaconda.com/free/anaconda/install/windows/ 

### Preparation
1. Open your terminal (e.g. anaconda powershell prompt) and open the folder in which you want to install this repository, for example make a folder called Repositories and open it in your terminal (you can use the command cd to go to the necessary folder, for example cd windows/users/repositories)
2. Clone this repo with the command <br><code> git clone https://github.com/SSC-ICT-Innovatie/LearningLion.git </code><br>
3. Create a subfolder vector_stores in the root folder of the cloned repo
  
### Conda virtual environment setup
1. Open an Anaconda prompt or other command prompt
2. Go to the root folder of the project and create a Python environment with conda using commandline command<br>
<code>conda env create -f learninglion.yml</code><br>
NB: The name of the environment is learninglion by default. It can be changed to a name of your choice in the first line of the yml file
3. Activate this environment using commandline command<br>
<code>conda activate learninglion</code>

### Pip virtual environment setup
1. Open an Anaconda prompt or other command prompt
2. Go to the root folder of the project and create a Python environment with pip using commandline command<br>
<code>python -m venv venv</code><br>
This will create a basic virtual environment folder named venv in the root of your project folder
NB: The chosen name of the environment is here learninglion. It can be changed to a name of your choice
3. Activate this environment using commandline command<br>
<code>venv\Scripts\activate</code>
4. All required packages can now be installed with command line command<br>
<code>pip install -r requirements.txt</code>

### Setting parameters
The file settings_template.py contains all parameters that can be used and needs to be copied to settings.py. In settings.py, fill in the parameter values you want to use for your use case. 
Examples and restrictions for parameter values are given in the comment lines. Among other things you need to decide what models you want to use and if you want to run them locally (on your own hardware) or externally (using the hardware from for example OpenAI or Huggingface by using an API key). 

If you want to run this locally you will need to do the following:

1. Download Ollama: https://ollama.com/
2. In settings choice LLM_TYPE = "local_llm"
3. Go to models and choose a model you want to use, we recommend mistral-openorca especially when working in non-english languages, but you can experiment with different models yourself.
* set LLM_MODEL_TYPE = model_name so in our example LLM_MODEL_TYPE = mistral-openorca
4. In settings choice EMBEDDING_PROVIDER = "local_embeddings", choice an embeddings model from: https://huggingface.co/models?library=sentence-transformers&sort=trending een embedding-model and set EMBEDDINGS_MODEL = "jegormeister/bert-base-dutch-cased"

If you want to do the latter and use the LLM's or Embedding models provided by OpenAI (GPT3.5 / GPT4 / Text-Embeddings-Ada-002) you will need to do the following:

1. Go to [https://platform.openai.com/docs/overview ](https://auth0.openai.com/u/signup/identifier?state=hKFo2SAxWUNzRWVLbFJfWnFkYzAyNm5oTFRkbF8xZ2NJNkhSV6Fur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDJBaFhUNTB6RWx1VkRaSXZ6U3JLQ2NDaUdwY255Mjlao2NpZNkgRFJpdnNubTJNdTQyVDNLT3BxZHR3QjNOWXZpSFl6d0Q) and either login or sign up, this option costs money (a fraction of a cent per question)
2. Create a file .env and enter your OpenAI API key in the first line of this file :<br>
OPENAI_API_KEY="sk-....."<br> 
Save and close the .env file<br>
* In case you don't have an OpenAI API key yet, you can obtain one here: https://platform.openai.com/account/api-keys
* Click on + Create new secret key
* Enter an identifier name (optional) and click on Create secret key

If you want to use one of the many open source models on Huggingface and use their hardware (so run it externally):

* register at https://huggingface.co/join
* When registered and logged in, you can get your API key in your Hugging Face profile settings
* Enter your Hugging Face API key in the second line of the .env file :<br>
HUGGINGFACEHUB_API_TOKEN="hf_....."<br>


### Ingesting documents
The file ingest.py can be used to vectorize all documents in a chosen folder and store the vectors and texts in a vector database for later use.<br>
Execution is done in the activated virtual environment using commandline command:<br>
<code>python ingest.py</code>

### Querying documents
The file query.py can be used to query any folder with documents, provided that the associated vector database exists.<br>
Execution is done in the activated virtual environment using commandline command:<br>
<code>python query.py</code>

### Querying multiple documents with multiple questions in batch
The file review.py uses the standard question-answer technique but allows you to ask multiple questions to each document in a folder. 
All the results are gathered in a .csv file.<br>
<code>python review.py</code>

### Ingesting and querying documents through a Streamlit User Interface
The functionalities described above can also be used through a User Interface.<br>
The UI can be started by using commandline command:<br>
<code>streamlit run streamlit_app.py</code><br>
When this command is used, a browser session will open automatically


### Evaluation of Question Answer results
The file evaluate.py can be used to evaluate the generated answers for a list of questions, provided that the file eval.json exists, containing 
not only the list of questions but also the related list of desired answers (ground truth).<br>
Evaluation is done at folder level in the activated virtual environment using commandline command:<br>
<code>python evaluate.py</code><br>
It is also possible to run an evaluation over all folders with <code>python evaluate_all.py</code>

### Monitoring the evaluation results through a Streamlit User Interface
All evaluation results can be viewed by using a dedicated User Interface.<br>
This evaluation UI can be started by using commandline command:<br>
<code>streamlit run streamlit_evaluate.py</code><br>
When this command is used, a browser session will open automatically


### Ingesting and querying documents through a Flask User Interface
The functionalities described above can also be used through a Flask User Interface.<br>
The flask UI can be started in the activated virtual environment using commandline command:<br>
<code>python flask_app.py</code>
The Flask UI is tailored for future use in production and contains more insight into the chunks (used) and also contains user admin functionality among others.<br>
For a more detailed description and installation, see the readme file in the  flask_app folder

## Tools
- **LangChain**: Framework for developing applications powered by language models
- **LlamaCPP**: Python bindings for the Transformer models implemented in C/C++
- **FAISS**: Open-source library for efficient similarity search and clustering of dense vectors.
- **Sentence-Transformers (all-MiniLM-L6-v2)**: Open-source pre-trained transformer model for embedding text to a 384-dimensional dense vector space for tasks like clustering or semantic search.
- **Llama-2-7B-Chat**: Open-source fine-tuned Llama 2 model designed for chat dialogue. Leverages publicly available instruction datasets and over 1 million human annotations. 

## Acknowledgements
This is a fork of [appl-docchat from Planbureau voor de Leefomgeving](https://github.com/pbl-nl/appl-docchat).

## References
This repo is mainly inspired by:
- https://docs.streamlit.io/
- https://docs.langchain.com/docs/
- https://blog.langchain.dev/tutorial-chatgpt-over-your-data/
- https://github.com/PatrickKalkman/python-docuvortex/tree/master
- https://blog.langchain.dev/evaluating-rag-pipelines-with-ragas-langsmith/
- https://github.com/explodinggradients/ragas

# LearningLion
This is the English version of the LearningLion project for the Dutch version see: https://github.com/JitseGoutbeek/LerendeLeeuw

## Description of the project
The project is a study on the use of generative AI to improve the services of SSC-ICT by supporting employees and optimizing internal processes. In particular, the focus is on generative large language models (LLM), in the form of Retrieval Augmented Generation (RAG), because they can have the most significant impact on the daily work of SSC-ICT employees. The assignment (Speech Recognition & AI) has been approved by the SpB and has been running since the beginning of 2023. 

## Repository
The current repository is based on the repository made by PBL under the direction of Stefan Troost (https://github.com/pbl-nl/appl-docchat), changed for our specific use cases. The demo is an example of Retrieval Augmented Generation (RAG) and allows for the use and evaluation of both Open and Closed-Source LLM's. It makes use of Langchain, Chroma and Streamlit among other things to perform document Q&A. Right now it is mostly a clone with some additions (to make running it locally easier for example) and it contains additional project documents (in project_docs) that provide background information about this project, the decisions we made and the research we conducted. 

A schematic overview of how the application works is shown here:

![RAG flow design](https://github.com/SSC-ICT-Innovatie/LearningLion/blob/main/project_docs/images/RAG%20flow%20design.png)

## How to use this repo
This repo is tested on a Windows platform.
The instructions as written assume you have Anaconda and Python installed. 
If not, download Python (https://www.python.org/downloads/) and follow this installation guide for Anaconda:
https://docs.anaconda.com/free/anaconda/install/windows/.

## Preparation
1. Open your terminal (e.g. anaconda powershell prompt) and open the folder in which you want to install this repository, for example make a folder called Repositories and open it in your terminal (you can use the command cd to go to the necessary folder, for example `cd windows/users/repositories`).
2. Clone this repo with the command <br><code>git clone https://github.com/SSC-ICT-Innovatie/LearningLion.git</code><br>
3. Create a subfolder vector_stores in the root folder of the cloned repo
  
### Conda virtual environment setup
1. Open an Anaconda prompt or other command prompt
2. Go to the root folder of the project and create a Python environment with conda using commandline command<br>
<code>conda env create -f learninglion.yml</code><br>
NB: The name of the environment is learninglion by default. It can be changed to a name of your choice in the first line of the yml file
3. Activate this environment using commandline command<br>
<code>conda activate learninglion</code><br>
4. All required packages can now be installed with command line command<br>
<code>pip install -r requirements.txt</code><br> (skip this if you rather work in a virtual environment)

### Pip virtual environment setup
! You don't need to set up a pip virtual environment, if you already have your conda environment set up.
1. Open an Anaconda prompt or other command prompt
2. Go to the root folder of the project and create a Python environment with pip using commandline command<br>
<code>python -m venv venv</code><br>
This will create a basic virtual environment folder named venv in the root of your project folder<br>
NB: The chosen name of the environment is here venv. It can be changed to a name of your choice.
3. Activate this environment using commandline command<br>
<code>venv\Scripts\activate</code><br>
4. All required packages can now be installed with command line command<br>
<code>pip install -r requirements.txt</code><br>

## Choosing your parameters
The file settings_template.py contains all parameters that can be used and needs to be copied to settings.py. In settings.py, fill in the parameter values you want to use for your use case. 
Examples and restrictions for parameter values are given in the comment lines. Among other things you need to decide what models you want to use and if you want to run them locally (on your own hardware) or externally (using the hardware from for example OpenAI or Huggingface by using an API key). 

If you want to run this locally using Ollama you will need to do the following:

1. Download Ollama: https://ollama.com/
2. In settings choice `LLM_TYPE = "local_llm"`
3. Go to models and choose a model you want to use, we recommend zephyr and mistral-openorca especially when working in non-english languages, if you have the memory Mixtral can also be a good choice (this model is 26 GB compared to 4 GB for mistral-openorca, but should perform better) you can experiment with different models yourself. Set `LLM_MODEL_TYPE = <model_name>`. So in our example `LLM_MODEL_TYPE = "mistral-openorca"`.
4. download the model on your device by typing <code> ollama pull model_name </code> in your terminal, e.g. <code> ollama pull mistral-openorce </code>
5. In settings choice `EMBEDDING_PROVIDER = "local_embeddings"`, choose an embeddings model from: https://huggingface.co/models?library=sentence-transformers&sort=trending. In the settings, set the embedding-model to that name `EMBEDDINGS_MODEL = "jegormeister/bert-base-dutch-cased"`.

If you want to do the latter and use the LLM's or Embedding models provided by OpenAI (GPT-3.5 / GPT-4 / Text-Embeddings-Ada-002) you will need to do the following:

1. Go to [https://platform.openai.com/docs/overview](https://auth0.openai.com/u/signup/identifier?state=hKFo2SAxWUNzRWVLbFJfWnFkYzAyNm5oTFRkbF8xZ2NJNkhSV6Fur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDJBaFhUNTB6RWx1VkRaSXZ6U3JLQ2NDaUdwY255Mjlao2NpZNkgRFJpdnNubTJNdTQyVDNLT3BxZHR3QjNOWXZpSFl6d0Q) and either login or sign up, this option costs money (a fraction of a cent per question).
2. Create a file `.env` and enter your OpenAI API key in the first line of this file :<br>
<code>OPENAI_API_KEY="sk-....."</code><br> 
Save and close the `.env` file.<br>
* In case you don't have an OpenAI API key yet, you can obtain one here: https://platform.openai.com/account/api-keys.
* Click on + Create new secret key.
* Enter an identifier name (optional) and click on Create secret key.

If you want to use one of the many open source models on Huggingface and use their hardware (so run it externally):

* Register at https://huggingface.co/join.
* When registered and logged in, you can get your API key in your Hugging Face profile settings.
* Enter your Hugging Face API key in the second line of the `.env` file:<br>
<code>HUGGINGFACEHUB_API_TOKEN="hf_....."</code><br>

You also need to decide how you want to 'chunk' your documents. Before embedding a document it is split up in pieces of text of a certain length and these pieces are subsequently vectorized and the most relevant (highest similarity score) of them retrieved and used as input by the LLM. In settings you can choose roughly how long you want to make the chunks and how many of them you want to retrieve.
* Chunk-Size specifies the number of tokens a chunk should roughly be a token tends to be a bit less than a word so the standard 1000 tokens is roughly 700 words, the code chunks the text in a way where the entirety of a paragraph is within the same chunk. It usually takes the maximimum number of paragraphs together in one chunk that together are still smaller than the chunk size.
* chunk_k is the number of chunks retrieved
* chunk_overlap specifies how long the overlap between chunks should be, it is often useful to have some overlap since the paragraph before can provide crucial context for the paragraph that follows and vice versa, having larger overlap makes it more likely units of text that are crucial for understanding each other accurately are in the same chunk.
In general when choosing these parameters there are a couple of things to consider. Firstly the product of chunk-size and number of chunks should be lower than the context window of the LLM you are using, gpt-35 for example has a context window of 4097 tokens so chunk_size*chunk_k < 4097. Furthermore a large chunk-size or a large number of chunks can cause a 'lost in the middle problem' where when the LLM is provided more context than needed it makes it less likely that it answers based on the truly most relevant context and therefore can make it less accurate. However, it should be provided with enough context to answer the type of questions you are asking well. If your documents contain for example a long explanation of something and you want the RAG application to be able to find that explanation and summarise it in its entirety, the context-size needs to be at least as long as that explanation. If you want to ask questions to which the answer isn't found in one place in one document but instead requires a lot of information that is difused over many documents the number of chunks needs to be at least as high as this number of documents. Furthermore, more chunks and a bigger chunk_size allows the embedding model more room for error, it might not have correctly identified the most relevant chunk, but maybe it still thought the chunk with the answer was the 4th most relevant which can be good enough with a chunk_k of 4.
* Score_threshold contains a value between 0 and 1 that stipulates how similar a chunk needs to be in order to be provided as context, in theory this can be used to combat the lost in the middle problem by making a pre-selection where less than chunk_k chunks are given if not enough relevant enough chunks are found. The closer to 1 the more rigorous the selection. 
* This score_threshold is only used if search_type is set to similarity_score_threshold, if search_type is similarity it will always retrieve chunk_k chunks, which is equivalent to a score_threshold of 0.

The rest of the settings are not that important for the functioning of the application, you can just leave them as is, a lot of them are about the way the interface looks for example. 


## Using the repository

In order to use this repository you need to be in the right folder and right virtual environment. If you are not in the right virtual environment you need to activate your virtual environment:
<br><code>conda activate learninglion</code><br>
If you are not in the right folder (LearningLion) you need to move to that folder, with the command cd you can move to the right folder, for example:
<br><code> cd windows/users/repositories/LearningLion </code><br> ofcourse if you have cloned the LearningLion repository to a different path you need to adjust to go to where you saved it.

This allows a couple of functionalities: 
* You can launch a user interface in which you can select a document folder and ask questions about it
* You can also embed your documents and ask questions through your command terminal, additionally through the command terminal you can automatically ask a larger set of questions and save the answers or automatically evaluate the answers.
We will walk through how to use these different options below, remember to choose the right settings before using a functionality.

### Asking questions about your documents through a User Interface
With the commandline command: `streamlit run streamlit_app.py` you can start an interface. When this command is used, a browser session will open automatically. In this browser you can ask questions about documents you put in the docs fodler, there is a little explainer on the left side of the screen that should be read the first time using the online interface.

### Ingesting documents
We can also ask questions, either 1 at a time or in multiples, through the command terminal. In this case we need to vectorize the documents we want to ask questions about first.
For this ingest.py is used. To do this first make a subfolder in the docs folder containing the documents you want to ask questions about, give the folder a recognizable name with only lower case letters. Subsequently type `python ingest.py` in an activated virtual environment. This asks you which folder you want to vectorize and you can type the name of the folder with the relevant documents.

### Querying documents
To ask questions about documents in your virtual environment you can use the file query.py (the necessary folder needs to be ingested). In order to do so just type `python query.py` in your activated virtual environment, and type in the name of the folder containing the documents you want to ask questions about. 

### Querying multiple documents with multiple questions in batch
You can also ask multiple questions at the same time, the code will run each question through your RAG pipeline and save the relevant questions and answers in a `.csv` file. To do this go to the folder containing the relevant documents in docs, make a subfolder named "review" and make a `.txt` file in that folder containing the relevant questions. Now type in your command window:
`python review.py` and type in the name of the folder containing the documents your questions are about. If you do this locally and the `.txt` file contains a lot of questions it might take a while, but at the end a `.csv` file should be saved in the review folder containing the questions and automatically generated answers. 

### Evaluation of Question Answer results
The file evaluate.py can be used to evaluate the generated answers for a list of questions, provided that the file eval.json exists, containing not only the list of questions but also the related list of desired answers (ground truth).<br>
Evaluation is done at folder level in the activated virtual environment using commandline command:`python evaluate.py` It is also possible to run an evaluation over all folders with `python evaluate_all.py`. The results will be generated in a `.tsv` file. Which can be opened in Microsoft Excel to have a clear overview of the results. More info on the metrics shown in the results can be found here: https://docs.ragas.io/en/stable/getstarted/evaluation.html#metrics/.

#### Generating test data for evaluation
TODO

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

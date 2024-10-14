# LearningLion - Kamervragen
Welcome to the git repo of the use case 'Kamervragen'. Here, we document our progress regarding our feasibility study into RAG for supporting the process of answering questions from members of parliament.  

## Description of the project
The project is a study on the use of generative AI to improve the services of SSC-ICT by supporting employees and optimizing internal processes. In particular, the focus is on generative large language models (LLM), in the form of Retrieval Augmented Generation (RAG), because they can have the most significant impact on the daily work of SSC-ICT employees. The assignment (Speech Recognition & AI) has been approved by the SpB and has been running since the beginning of 2023.

## The original Learning Lion Repository
The Learning Lion repository is based on the repository made by PBL under the direction of Stefan Troost (https://github.com/pbl-nl/appl-docchat), changed for the specific use cases of SSC-ICT-Innovatie. It is an example of Retrieval Augmented Generation (RAG) and allows for the use and evaluation of both Open and Closed-Source LLM's. It makes use of Langchain, Chroma and Streamlit among other things to perform document Q&A. Right now it is mostly a clone with some additions (to make running it locally easier for example) and it contains additional project documents (in project_docs) that provide background information about this project, the decisions we made and the research we conducted.
![Original Git](https://github.com/SSC-ICT-Innovatie/LearningLion)

## Current repository
The repository is a work in progress of streamlining the larger original Learning Lion Repository and making it more accessible, simple and transparent (for developers and the public) for the current use case.
Elements from the original repo are reused. However, we also took the liberty of using newer functions and methods if this would support these higher level goals.

The archive is where the original repo is archived.
The jupyter notebook is where we mainly experiment.
Later on, we will integrate and abstract the core elements into classes to be reusable and where we will be able to integrate it into (micro-)services.

## How to use this repo
The instructions as written assume you have Anaconda and Python installed. 
If not, download Python (https://www.python.org/downloads/) and follow this installation guide for Anaconda:
https://docs.anaconda.com/free/anaconda/install/windows/.

## Preparation
1. Open your terminal (e.g. anaconda powershell prompt) and open the folder in which you want to install this repository, for example make a folder called Repositories and open it in your terminal (you can use the command cd to go to the necessary folder, for example `cd windows/users/repositories`).
2. Clone this repo with the command <br><code>git clone https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen.git</code><br>
3. Setup your virtual environment
   
### Conda virtual environment setup
1. Open an Anaconda prompt or other command prompt
2. Go to the root folder of the project and create a Python environment with conda using commandline command<br>
<code>conda env create -f learninglionkamervragen.yml</code><br>
NB: The name of the environment is learninglionkamervragen by default. It can be changed to a name of your choice in the first line of the yml file
3. Activate this environment using commandline command<br>
<code>conda activate learninglion</code><br>
4. All required packages can now be installed with command line command<br>
<code>pip install -r requirements.txt</code><br> (skip this if you rather work in a virtual environment)

### Execute some cells in the newPipe.ipynb
3. Start playing around (execute some cells in the newPipe.ipynb) to see how our pipeline behaves.

## Tools
- **LangChain**: Framework for developing applications powered by language models
- **LlamaCPP**: Python bindings for the Transformer models implemented in C/C++
- **FAISS**: Open-source library for efficient similarity search and clustering of dense vectors.
- **Sentence-Transformers (all-MiniLM-L6-v2)**: Open-source pre-trained transformer model for embedding text to a 384-dimensional dense vector space for tasks like clustering or semantic search.
- **Llama-2-7B-Chat**: Open-source fine-tuned Llama 2 model designed for chat dialogue. Leverages publicly available instruction datasets and over 1 million human annotations. 

## Acknowledgements
This is a fork of ![Original Git](https://github.com/SSC-ICT-Innovatie/LearningLion) which is a fork of 
[appl-docchat from Planbureau voor de Leefomgeving](https://github.com/pbl-nl/appl-docchat).

## References
This repo is mainly inspired by:
- https://docs.streamlit.io/
- https://docs.langchain.com/docs/
- https://blog.langchain.dev/tutorial-chatgpt-over-your-data/
- https://github.com/PatrickKalkman/python-docuvortex/tree/master
- https://blog.langchain.dev/evaluating-rag-pipelines-with-ragas-langsmith/
- https://github.com/explodinggradients/ragas

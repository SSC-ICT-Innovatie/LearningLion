# relative filepath of logo in user interface, e.g. "./images/nmdc_logo.png"
APP_LOGO = "./images/bzk-logo.png"

# relative filepath of text file with content for application explanation in Streamlit UI, e.g. "./info/explanation.txt"
APP_INFO = "./info/explanation.txt"

# header in Streamlit UI, e.g. "ChatNMDC: chat with your documents"
APP_HEADER = "SSC-ICT RAG demo"

# relative filepath of folder with input documents, e.g. "./docs"
DOC_DIR = "./docs"

# relative filepath of folder with chunkss, e.g. "./chunks"
CHUNK_DIR = "./chunks"

# relative filepath of persistent vector databases, e.g. "./vector_stores"
VECDB_DIR = "./vector_stores"

# relative filepath of evaluation results folder, e.g. "./evaluate"
EVAL_DIR = "./evaluate"

# header in Streamlit evaluation UI, e.g. "ChatNMDC: evaluation"
EVAL_APP_HEADER = "Evaluation"

# content for evaluation explanation in evaluation user interface, e.g. "./info/evaluation_explanation.txt"
EVAL_APP_INFO = "./info/evaluation_explanation.txt"

# filename of json file with question and answer lists, e.g. "eval.json"
EVAL_FILE_NAME = "eval.json"

# CHAIN_VERBOSITY must be boolean. When set to True, the standalone question that is conveyed to LLM is shown
CHAIN_VERBOSITY = False

# ######### THE SETTINGS BELOW CAN BE USED FOR TESTING AND CUSTOMIZED TO YOUR PREFERENCE ##########
# LLM_TYPE must be one of: "chatopenai", "huggingface", "local_llm", "azureopenai"
LLM_TYPE = "local_llm"

# - LLM_MODEL_TYPE must be one of: "gpt35", "gpt35_16", "gpt4" if LLM_TYPE is "chatopenai". Default is "gpt35"
#   Context window sizes are currently: "gpt35": 4097 tokens (equivalent to ~3000 words), "gpt35_16": 16385 tokens, "gpt4": 8192 tokens
# - LLM_MODEL_TYPE must be one of: "llama2", "GoogleFlan" if LLM_TYPE is "huggingface"
#   "llama2" requires Huggingface Pro Account and access to the llama2 model https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
#   note: llama2 is not fully tested, the last step was not undertaken, because no HF Pro account was available for the developer
#   Context window sizes are currently: "GoogleFlan": ? tokens, "llama2": ? tokens
# - LLM_MODEL_TYPE must be one of the Ollama downloaded models, e.g. "llama2" "mini-orca" or "zephyr". See also https://ollama.ai/library
# - LLM_MODEL_TYPE must be the deployment name if LLM_TYPE is "azureopenai"
LLM_MODEL_TYPE = "mistral-openorca"

# API_URL must be the URL to your (local) API
# If LLM_TYPE is "local_llm" and model is run on your local machine, API_URL should be "localhost:11434" by default
# If run on Azure virtual machine, use "http://127.0.0.1:11434"
API_URL = "http://127.0.0.1:11434"

# AZUREOPENAI_API_VERSION must be the API version used for AzureOpenAI, e.g. "2023-08-01-preview"
# NB: this only needs to be set when LLM_TYPE = "azureopenai" and/or EMBEDDINGS_PROVIDER = "azureopenai"
AZUREOPENAI_API_VERSION = "2023-08-01-preview"

# EMBEDDINGS_PROVIDER must be one of: "openai", "huggingface", "local_embeddings", "azureopenai"
EMBEDDINGS_PROVIDER = "local_embeddings"

# - EMBEDDINGS_MODEL must be one of: "text-embedding-ada-002" if EMBEDDINGS_PROVIDER is "openai"
# - EMBEDDINGS_MODEL must be one of: "all-mpnet-base-v2" if EMBEDDINGS_PROVIDER is "huggingface"
# - EMBEDDINGS_MODEL must be a model name from here https://huggingface.co/models?pipeline_tag=sentence-similarity&library=sentence-transformers&sort=trending"
# - EMBEDDINGS_MODEL must be the embeddings deployment name if EMBEDDINGS_PROVIDER is "azureopenai"
EMBEDDINGS_MODEL = "textgain/allnli-GroNLP-bert-base-dutch-cased"

# TEXT_SPLITTER_METHOD represents the way in which raw text chunks are created, must be one of:
# "RecursiveCharacterTextSplitter" (split text to fixed size chunks) or
# "NLTKTextSplitter" (keep full sentences even if chunk size is exceeded)
TEXT_SPLITTER_METHOD = "NLTKTextSplitter"

# CHAIN_NAME must be one of: "conversationalretrievalchain",
CHAIN_NAME = "conversationalretrievalchain"

# CHAIN_TYPE must be one of: "stuff",
CHAIN_TYPE = "stuff"

# SEARCH_TYPE must be one of: "similarity", "similarity_score_threshold"
SEARCH_TYPE = "similarity"

# SCORE_THRESHOLD represents the similarity value that chunks must exceed to qualify for the context, value must be between 0.0 and 1.0, e.g. 0.8
# This value is only relevant when SEARCH_TYPE has been set to "similarity_score_threshold"
SCORE_THRESHOLD = 0.5

# VECDB_TYPE must be one of: "chromadb",
VECDB_TYPE = "chromadb"

# CHUNK_SIZE represents the maximum allowed size of text chunks, value must be integer
CHUNK_SIZE = 1024

# CHUNK_K represents the number of chunks that is returned from the vector database as input for the LLM, value must be integer (>=1)
# NB: CHUNK_SIZE and CHUNK_K are related, make sure that CHUNK_K * CHUNK_SIZE < LLM window size
CHUNK_K = 4

# CHUNK_OVERLAP represents the overlap between 2 sequential text chunks, value must be integer (>=0 and < CHUNK_SIZE)
CHUNK_OVERLAP = 256

# RETRIEVAL_METHOD must be one of "regular" or "answer_and_question"
# "regular" use the similarity search only based on the question
# "answer_and_question" use the similarity search based on the question and the answer and combines these
# The setting "answer_and_question" is based on the literature of the paper https://arxiv.org/abs/2212.10496
RETRIEVAL_METHOD = "regular"

# This is a standard set of instructions the LLM will be given. You can update this through trial and erorr to fir your use case in the most optimal way.
SYSTEM_PROMPT = """
### OBJECTIVE ###
Je bent een assistent voor de rijksoverheid. Jouw taak is om vragen te beantwoorden in het Nederlands. Zorg ervoor dat je alleen antwoord geeft op basis van de beschikbare context en dat je daar ook naar verwijst in je antwoord.

### AUDIENCE ###
De doelgroep van jouw antwoorden zijn ambtenaren. Geef alle relevante informatie uit de context, antwoord in het Nederlands leg in maximaal 100 woorden zoveel mogelijk uit.

### GUARDRAILS ###
Indien de context onvoldoende informatie bevat om de vraag te beantwoorden, verzin dan geen informatie maar geef aan dat er onvoldoende informatie beschikbaar is.

### INSTRUCTIONS ###
- Beantwoord de vraag altijd in het Nederlands, zelfs als de context in het Engels is gesteld.
- Vermijd het herhalen van de vraag in het antwoord en het herhalen van de instructies. Voer de instructies uit en geef een concreet antwoord op de gestelde vraag.
- Geef een stapsgewijze redenering bij het beantwoorden van de vraag en refereer naar specifieke zinnen uit de context die hebben bijgedragen aan het antwoord.
- Houd je antwoord nauw verbonden met de context en vermijd het toevoegen van informatie die niet expliciet in de context wordt vermeld.

### QUESTION ### \n
"""

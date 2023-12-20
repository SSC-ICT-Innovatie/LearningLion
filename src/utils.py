'''
===========================================
        Module: Util functions
===========================================
'''
import box
import yaml
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from src.llm import build_llm
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

memory = ConversationBufferMemory(memory_key='chat_history', input_key='question', output_key='answer', 
                                  return_messages=True)

def build_retrieval_qa(llm, prompt, vectordb, n_sources, clear):
    if clear:
        memory.clear()
    dbqa = ConversationalRetrievalChain.from_llm(llm, 
                                                 retriever=vectordb.as_retriever(search_kwargs={'k': n_sources}),
                                                 return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
                                                 condense_question_prompt=prompt, 
                                                 memory=memory,
                                                 )
    return dbqa


def setup_dbqa(prompt, model_path, length, temp, n_sources, gpu_layers, clear=False, chat_box=None):
    embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS_MODEL_NAME,
                                       model_kwargs={'device': 'cpu'})
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    llm = build_llm(model_path, length, temp, gpu_layers, chat_box)
    qa_prompt = PromptTemplate.from_template(prompt)
    dbqa = build_retrieval_qa(llm, qa_prompt, vectordb, n_sources, clear)

    return dbqa
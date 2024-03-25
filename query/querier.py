from dotenv import load_dotenv
from typing import Dict, Tuple, List, Any
from langchain_core.documents import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import AIMessage
from langchain.schema import HumanMessage
from loguru import logger
# local imports
import settings
import utils as ut
from llm_class.llm_class import LLM
from langchain.prompts import PromptTemplate


class Querier:
    '''
    When parameters are read from settings.py, object is initiated without parameter settings
    When parameters are read from GUI, object is initiated with parameter settings listed
    '''
    def __init__(self, llm_type=None, llm_model_type=None, embeddings_provider=None, embeddings_model=None,
                 vecdb_type=None, chain_name=None, chain_type=None, chain_verbosity=None, search_type=None,
                 score_threshold=None, chunk_k=None, local_api_url=None, azureopenai_api_version=None):
        load_dotenv()
        self.llm_type = settings.LLM_TYPE if llm_type is None else llm_type
        self.llm_model_type = settings.LLM_MODEL_TYPE if llm_model_type is None else llm_model_type
        self.embeddings_provider = settings.EMBEDDINGS_PROVIDER if embeddings_provider is None else embeddings_provider
        self.embeddings_model = settings.EMBEDDINGS_MODEL if embeddings_model is None else embeddings_model
        self.vecdb_type = settings.VECDB_TYPE if vecdb_type is None else vecdb_type
        self.chain_name = settings.CHAIN_NAME if chain_name is None else chain_name
        self.chain_type = settings.CHAIN_TYPE if chain_type is None else chain_type
        self.chain_verbosity = settings.CHAIN_VERBOSITY if chain_verbosity is None else chain_verbosity
        self.search_type = settings.SEARCH_TYPE if search_type is None else search_type
        self.score_threshold = settings.SCORE_THRESHOLD if score_threshold is None else score_threshold
        self.chunk_k = settings.CHUNK_K if chunk_k is None else chunk_k
        self.local_api_url = settings.API_URL \
            if local_api_url is None and settings.API_URL is not None else local_api_url
        self.chat_history = []
        self.vector_store = None
        self.azureopenai_api_version = settings.AZUREOPENAI_API_VERSION \
            if azureopenai_api_version is None and settings.AZUREOPENAI_API_VERSION is not None \
            else azureopenai_api_version
        self.embeddings = ut.getEmbeddings(self.embeddings_provider,
                                           self.embeddings_model,
                                           self.local_api_url,
                                           self.azureopenai_api_version)

        # define llm
        self.llm = LLM(self.llm_type, self.llm_model_type, self.local_api_url, self.azureopenai_api_version).get_llm()
        self.chain = None
        self.chain_hallucinated = None

    def make_agent(self, input_folder, vectordb_folder):
        """
        Create a langchain agent with selected llm and tools
        """
        #
        # TODO
        #   - generalise code from make_chain
        #   - implement sample tools (wikipedia (standard), geocoder, soilgrids)
        #       see:
        #           https://python.langchain.com/docs/integrations/tools/wikipedia
        #           https://python.langchain.com/docs/integrations/tools/requests
        #           https://python.langchain.com/docs/modules/agents/tools/custom_tools (<-)
        #   - implement dynamic tool selection mechanism
        #   - create llm, tools, and initialise agent
        #   - add __init__ parameters for agent (maybe rename some chain related params?)
        #   - see usages of make_chain where to select between using chain and agent
        #   - add evaluation questions and answers, e.g. based on detailed spatial location context
        #
        return

    def make_chain(self, input_folder, vectordb_folder, search_filter=None) -> None:
        self.input_folder = input_folder
        self.vectordb_folder = vectordb_folder

        # get chroma vector store
        if self.vecdb_type == "chromadb":
            self.vector_store = ut.get_chroma_vector_store(self.input_folder, self.embeddings, self.vectordb_folder)
            # get retriever with some search arguments
            # maximum number of chunks to retrieve
            search_kwargs = {"k": self.chunk_k}
            # filter, if set
            if search_filter is not None:
                logger.info(f"querying vector store with filter {search_filter}")
                search_kwargs["filter"] = search_filter
            if self.search_type == "similarity_score_threshold":
                search_kwargs["score_threshold"] = self.score_threshold
            retriever = self.vector_store.as_retriever(search_type=self.search_type, search_kwargs=search_kwargs)
            logger.info(f"Loaded chromadb from folder {self.vectordb_folder}")

        if self.chain_name == "conversationalretrievalchain":
            # TODO: For me, the condense_question_prompt does not work and it does not change anything.
            base_prompt = "Answer the question in dutch. Answer the question between the triple dashes: ---{question}---"
            if settings.RETRIEVAL_METHOD == "answer_and_question":
                from langchain_custom_chain.base import CustomConversationalRetrievalChain
                logger.info("Using custom chain")
                self.chain = CustomConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    chain_type=self.chain_type,
                    verbose=self.chain_verbosity,
                    return_source_documents=True,
                    condense_question_prompt=PromptTemplate.from_template(base_prompt)
                )
            else:
                self.chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    chain_type=self.chain_type,
                    verbose=self.chain_verbosity,
                    return_source_documents=True,
                    condense_question_prompt=PromptTemplate.from_template(base_prompt)
                )
        logger.info("Executed Querier.make_chain")
        
    def get_documents_with_scores(self, question: str) -> List[Tuple[Document, float]]:
        most_similar_docs = self.vector_store.similarity_search_with_relevance_scores(question, k=self.chunk_k)
        logger.info(f"Topscore most similar docs: {most_similar_docs[0][1]}")
        
        if settings.RETRIEVAL_METHOD == "regular":
            return most_similar_docs
        # Else retrieval method is "answer_and_question
        hallucinated_prompt = f"""Please write a passage to answer the question. The passage should be short, concise, and answer in dutch and in maximum 50 words.
        Question: {question}
        Passage:"""
        hallucinated_answer = self.llm.invoke(hallucinated_prompt)
        logger.info(f"Hallucinated answer: {hallucinated_answer}")
        most_similar_docs_hallucinated = self.vector_store.similarity_search_with_relevance_scores(hallucinated_answer.content, k=self.chunk_k)
        logger.info(f"Topscore most similar docs hallucinated: {most_similar_docs_hallucinated[0][1]}")

        # Add the retrieval method of the docs to the metadata
        for document, _ in most_similar_docs:
            document.metadata['retrieval_method'] = "Embedded Question"
        for document, _ in most_similar_docs_hallucinated:
            document.metadata['retrieval_method'] = "Embedded Hallucinated Answer"
            
        # Merge the two lists
        merged_list = most_similar_docs + most_similar_docs_hallucinated
        
        # Remove duplicates based on the score of each tuple
        unique_documents = {}
        for document, score in merged_list:
            if document.page_content not in unique_documents or unique_documents[document.page_content][1] < score:
                unique_documents[document.page_content] = (document, score)
        return sorted(unique_documents.values(), key=lambda x: x[1], reverse=True)

    def ask_question(self, question: str) -> Tuple[Dict[str, Any], List[float]]:
        """"
        Finds most similar docs to prompt in vectorstore and determines the response
        If the closest doc found is not similar enough to the prompt, any answer from the LM is overruled by a message
        """
        prompt_helper = """Answer the following question in Dutch with he corresponding documents. If the answer is not in the documents, just say that the data is not in the documents."""
        documents = self.get_documents_with_scores(question)
        
        if settings.GENERATION_METHOD == "document_only":
            return {"source_documents": documents}
        
        if settings.RETRIEVAL_METHOD == "answer_and_question":
            # Uses the custom chain
            response = self.chain.invoke({"question": f"{prompt_helper} {question}", "chat_history": self.chat_history}, custom_documents=documents)
        else:
            # Uses the regular Langchain chain
            response = self.chain.invoke({"question": f"{prompt_helper} {question}", "chat_history": self.chat_history})
            # Overwrite their documents with the ones we found
            # This should be the same, but only with the scores added
            response["source_documents"] = documents
            
        # If no chunk qualifies, overrule any answer generated by the LLM with message below
        _, first_score = response["source_documents"][0]
        if first_score < self.score_threshold:
            response["answer"] = "I don't know because there is no relevant context containing the answer"
        else:
            logger.info(f"Topscore: {first_score}")

        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response["answer"]))
        return response

    def clear_history(self) -> None:
        """"
        Clears the chat history
        Used by "Clear Conversation" button in streamlit_app.py  
        """
        self.chat_history = []

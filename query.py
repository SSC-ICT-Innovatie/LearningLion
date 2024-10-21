from langchain.retrievers import EnsembleRetriever
import database
class Query:
    ensemble_retriever = None

    def __init__(self):
        print("Query class initialized")

    def setup_querier(self, database: database.Database):
        chroma_retriever = database.get_vector_store().as_retriever()
        bm25_retriever = database.get_bm25_retriever()
        
        if bm25_retriever is None:
            raise ValueError("BM25 retriever is not set in the database")
        if chroma_retriever is None:
            raise ValueError("Chroma retriever is not set in the database")
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever],
            weights=[0.5, 0.5], # TODO: tune these weights
        )
    def query(self, query_text):
        return self.ensemble_retriever.invoke(query_text)

    def get_ensemble_retriever(self):
        return self.ensemble_retriever
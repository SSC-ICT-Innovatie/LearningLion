from langchain.retrievers import EnsembleRetriever
import database
class Query:
    ensemble_retriever = None

    def __init__(self):
        print("Query class initialized")

    def setup_querier(self, database: database.Database):
        print("Setting up ensemble retriever")
        chroma_retriever = database.get_vector_store()
        if(chroma_retriever is None):
            raise ValueError("Chroma retriever is not set in the database")
        chroma_retriever = chroma_retriever.as_retriever()
        bm25_retriever = database.get_bm25_retriever()
        
        if bm25_retriever is None:
            raise ValueError("BM25 retriever is not set in the database")
        if chroma_retriever is None:
            raise ValueError("Chroma retriever is not set in the database")
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever],
            weights=[0.5, 0.5], # TODO: tune these weights
        )
        print("Ensemble retriever set up")
        
    def query(self, query_text):
        print(f"Querying: {query_text}")
        results = self.ensemble_retriever.invoke(query_text)
        print(f"Got {len(results)} results")
        print(f"Results: {results}")
        
        # Convert each result to a JSON-serializable format
        json_ready_results = []
        for result in results:
            # Assuming fields like `text` and `metadata` exist in `Document`
            json_ready_results.append({
                "text": getattr(result, "page_content", ""),  # Replace with the actual text attribute
                "metadata": getattr(result, "metadata", {})  # Replace with the actual metadata attribute
            })
        
        return json_ready_results

    def get_ensemble_retriever(self):
        return self.ensemble_retriever
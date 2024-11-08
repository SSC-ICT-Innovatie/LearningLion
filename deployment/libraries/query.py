from langchain.retrievers import EnsembleRetriever

from deployment.libraries import database
# import database
class Query:
    ensemble_retriever = None

    def __init__(self):
        print("Query class initialized")

    def setup_querier(self, database: database.Database):
        print("Setting up ensemble retriever")

        # Retrieve the Chroma vector store
        chroma_vectorstore = database.get_vector_store()
        if chroma_vectorstore is None:
            raise ValueError("Chroma vector store is not set in the database")
        chroma_retriever = chroma_vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5,"score_threshold": 0.9})
        # Retrieve the BM25 retriever
        bm25_retriever = database.get_bm25_retriever()
        if bm25_retriever is None:
            raise ValueError("BM25 retriever is not set in the database")

        # Create the ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever],
            weights=[0.5, 0.5], # TODO: tune these weights
        )

        print("Ensemble retriever set up")
            
    def query(self, query_text):
        print(f"Querying: {query_text}")
        results = self.ensemble_retriever.invoke(query_text)
        for doc in results:
            score = doc.metadata.get('score', None)
            print(f"Document: {doc.page_content}, Score: {score}")
        if results is None:
            return []
        print(f"Got {len(results)} results")
        # print(f"Results: {results}")
        
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
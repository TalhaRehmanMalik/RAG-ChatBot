from langchain_pinecone import PineconeVectorStore
from chatbot.embeddings.hf_embeddings import HFEmbeddings
from chatbot.config.settings import settings

class RAGRetriever:
    def __init__(self, top_k=5):
        self.top_k = top_k
        self.embeddings = HFEmbeddings().langchain_embeddings
        self.vector_store = PineconeVectorStore.from_existing_index(
            index_name=settings.PINECONE_INDEX_NAME,
            embedding=self.embeddings
        )

    def retrieve(self, query: str):
        results = self.vector_store.similarity_search(query, k=self.top_k)
        return results

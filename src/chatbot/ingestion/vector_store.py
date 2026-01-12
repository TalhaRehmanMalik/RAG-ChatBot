from pinecone import Pinecone, ServerlessSpec
from chatbot.config.settings import settings
from chatbot.embeddings.hf_embeddings import HFEmbeddings
from langchain_pinecone import PineconeVectorStore

class PineconeIngestor:
    def __init__(self, index_name: str = settings.PINECONE_INDEX_NAME):
        # Create a Pinecone client instance
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = index_name
        self.embeddings = HFEmbeddings().langchain_embeddings

        # Create index if not exists
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=self.embeddings.embed_dim,  # automatically get dimension from embeddings
                metric='cosine', 
                spec=ServerlessSpec(cloud='aws', region='us-west-2')
            )

    def upsert_documents(self, documents):
        PineconeVectorStore.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=self.index_name
        )

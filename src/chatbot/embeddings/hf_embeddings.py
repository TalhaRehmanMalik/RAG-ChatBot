from langchain_huggingface import HuggingFaceEmbeddings

from chatbot.config.settings import settings

class HFEmbeddings:
    def __init__(self):
        self.langchain_embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME
        )
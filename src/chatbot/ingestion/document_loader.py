from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from chatbot.config.settings import settings

class DocumentLoader:
    def __init__(self, data_dir: Path = settings.DATA_PATH):
        self.data_dir = data_dir

    def load_all_pdfs(self):
        documents = []

        for pdf_file in self.data_dir.glob("*.pdf"):
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()

            for d in docs:
                d.metadata["source"] = pdf_file.name

            documents.extend(docs)

        return documents

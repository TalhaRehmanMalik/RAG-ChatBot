from chatbot.ingestion.document_loader import DocumentLoader
from chatbot.ingestion.chunker import DocumentChunker
from chatbot.ingestion.vector_store import PineconeIngestor
from chatbot.config.logger import setup_logger

logger = setup_logger(__name__)

def run_ingestion():
    logger.info("📄 Loading PDFs...")
    loader = DocumentLoader()
    documents = loader.load_all_pdfs()

    logger.info(f"Loaded {len(documents)} pages")

    logger.info("✂️ Chunking documents...")
    chunker = DocumentChunker()
    chunks = chunker.chunk_documents(documents)

    logger.info(f"Created {len(chunks)} chunks")

    logger.info("📌 Uploading to Pinecone...")
    ingestor = PineconeIngestor()
    ingestor.upsert_documents(chunks)

    logger.info("✅ Ingestion complete!")

if __name__ == "__main__":
    run_ingestion()

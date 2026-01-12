from dotenv import load_dotenv
import os
from pathlib import Path
from .logger import setup_logger 

logger = setup_logger(__name__)

# Load .env from project root
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)
logger.debug(".env loaded")  

class Settings:
    BASE_DIR = Path(__file__).resolve().parents[3]
    DATA_PATH = BASE_DIR / "data"

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    PINECONE_INDEX_NAME = "research-assistant"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

settings = Settings()

logger.info(f"PINECONE_API_KEY loaded: {settings.PINECONE_API_KEY}")
logger.info(f"GROQ_API_KEY loaded: {settings.GROQ_API_KEY}")

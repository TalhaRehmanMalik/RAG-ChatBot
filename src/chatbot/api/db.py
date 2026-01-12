# src/chatbot/api/db.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from src.chatbot.config.logger import setup_logger
import os
from dotenv import load_dotenv

logger = setup_logger(__name__)

# Load Mongo URI from environment
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Singleton objects
client = None
db = None
chat_collection = None


try:
    # Connect with timeout
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ping')
    logger.info("✅ MongoDB connected successfully")
    
    # Database and collection
    db = client["rag_chatbot"]
    chat_collection = db["chats"]
    
    logger.info(f"✅ Database: {db.name}")
    logger.info(f"✅ Collection: {chat_collection.name}")
    
except ConnectionFailure:
    logger.error("❌ MongoDB connection failed - Server not reachable")
    raise
except ServerSelectionTimeoutError:
    logger.error("❌ MongoDB connection timeout - Check MONGO_URI")
    raise
except Exception as e:
    logger.error(f"❌ MongoDB error: {str(e)}")
    raise

# Export explicitly
__all__ = ["client", "db", "chat_collection"]

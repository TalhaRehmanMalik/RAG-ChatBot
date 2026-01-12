from typing import List
from src.chatbot.config.logger import setup_logger
from ..schemas import Message        
from ..db import chat_collection
from ...rag_pipeline import rag_query  


logger = setup_logger(__name__)

class ChatManager:

    def create_chat(self, session_id: str, user_message: str) -> List[Message]:
        # Fetch existing chat
        chat = chat_collection.find_one({"session_id": session_id})

        if not chat:
            chat = {"session_id": session_id, "history": []}
            logger.info(f"Creating new chat session: {session_id}")
        else:
            chat.setdefault("history", [])

        # Append user message
        chat["history"].append({"role": "user", "content": user_message})
        logger.info(f"User message added to session {session_id}")

        # Generate RAG response
        answer = rag_query(user_message)
        chat["history"].append({"role": "assistant", "content": answer})
        logger.info(f"Assistant response generated for session {session_id}")

        # Upsert into MongoDB
        result = chat_collection.update_one(
            {"session_id": session_id},
            {"$set": {"session_id": session_id, "history": chat["history"]}},
            upsert=True
        )
        logger.info(f"MongoDB upsert result: {result.raw_result}")

        return [Message(**msg) for msg in chat["history"]]

    def get_chat(self, session_id: str) -> List[Message]:
        chat = chat_collection.find_one({"session_id": session_id})
        if not chat or "history" not in chat:
            logger.warning(f"No chat found for session {session_id}")
            return []
        return [Message(**msg) for msg in chat["history"]]

    def delete_chat(self, session_id: str) -> bool:
        result = chat_collection.delete_one({"session_id": session_id})
        if result.deleted_count > 0:
            logger.info(f"Deleted chat session {session_id}")
            return True
        else:
            logger.warning(f"Tried to delete non-existent session {session_id}")
            return False

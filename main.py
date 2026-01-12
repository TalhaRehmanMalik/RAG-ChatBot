from fastapi import FastAPI
from src.chatbot.api.routes.chat import router as chat_router
app = FastAPI(title="RAG Chatbot API")

app.include_router(chat_router)

@app.get("/")
def health_check():
    return {"status": "API running"}

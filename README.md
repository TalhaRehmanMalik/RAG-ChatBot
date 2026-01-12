# 🤖 RAG Chatbot - AI-Powered Research Assistant

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot built with **FastAPI**, **LangChain**, **Pinecone**, **MongoDB Atlas**, and **Gradio**. This system allows users to query PDF documents intelligently with context-aware responses and persistent chat history.

---

## ✨ Features

- 🔍 **Smart Document Retrieval** - Semantic search using Pinecone vector database
- 💬 **Interactive Chat Interface** - Beautiful Gradio UI with streaming responses
- 🗄️ **Persistent Chat History** - MongoDB Atlas integration for session management
- 🚀 **RESTful API** - FastAPI backend with comprehensive endpoints
- 📚 **PDF Document Processing** - Automatic chunking and embedding of research papers
- 🎯 **Context-Aware Responses** - LLM-powered answers with source citations
- ⚡ **Streaming Support** - Real-time response generation

---

## 🏗️ Architecture

```
┌─────────────┐
│   Gradio UI │ (Frontend)
└──────┬──────┘
       │
┌──────▼───────────┐
│   FastAPI Server │ (Backend)
└──────┬───────────┘
       │
       ├─────────────► MongoDB Atlas (Chat History)
       │
       ├─────────────► Pinecone (Vector Store)
       │
       └─────────────► Groq LLM (AI Responses)
```

---

## 📁 Project Structure


ChatBot/ 
├── logs/                          # All logs stored here
│   └── app.log                    # Rotating file logs (DEBUG + INFO)
│
├── main.py                        # CLI entry point (logger replaces prints)
│
├── src/
│   └── chatbot/
│       ├── api/                    # FastAPI Application
│       │
│       │   ├── db.py            # MongoDB connection (logger replaces prints)
│       │   ├── schemas.py         # Pydantic models
│       │   ├── routes/
│       │   │   └── chat.py        # Chat endpoints (logger optional for requests/errors)
│       │   └── services/
│       │       └── chat_manager.py # Business logic (logger optional)
│       │
│       ├── ingestion/             # Document Processing
│       │   ├── document_loader.py # PDF loading (logger replaces prints)
│       │   ├── chunker.py         # Text splitting (no changes)
│       │   └── vector_store.py    # Pinecone ingestion (logger optional)
│       │
│       ├── embeddings/            # Embedding Models
│       │   └── hf_embeddings.py   # HuggingFace embeddings (logger optional)
│       │
│       ├── config/                # Configuration
│       │   ├── logger.py          # Centralized logger (NEW)
│       │   └── settings.py        # Environment variables (prints → logger)
│       │
│       ├── qa_chain.py            # RAG chain logic (logger optional)
│       ├── rag_pipeline.py        # Main pipeline (logger optional)
│       ├── retriever.py           # Vector search (logger optional)
│       └── gradio_ui.py           # Web interface (optional logger)
│
├── data/                          # PDF documents
├── .env                           # Environment variables
├── requirements.txt               # Dependencies
└── README.md                      # Documentation

---

## 🚀 Quick Start

### 1. **Prerequisites**

- Python 3.9+
- MongoDB Atlas account
- Pinecone account
- Groq API key

### 2. **Installation**

```bash
# Clone the repository
git clone https://github.com/TalhaRehmanMalik/rag-chatbot.git
cd rag-chatbot

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. **Environment Setup**

Create a `.env` file in the project root:

```env
# MongoDB Configuration
MONGO_URI= Mongo_URI

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-chatbot-index

# Groq API
GROQ_API_KEY=your_groq_api_key

# Embedding Model
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Paths
DATA_PATH=./data
```

### 4. **Document Ingestion**

Place your PDF files in the `data/` folder, then run:

```bash
python main_ingest.py
```

This will:
- Load all PDFs from `data/` directory
- Split documents into chunks
- Generate embeddings
- Upload to Pinecone vector database

### 5. **Run the Application**

#### Option A: FastAPI Server

```bash
# Start FastAPI backend
python -m uvicorn src.chatbot.api.main:app --reload

# Server runs at: http://127.0.0.1:8000
```

#### Option B: Gradio Interface

```bash
# Start Gradio UI
python gradio_ui.py

# Interface opens at: http://127.0.0.1:7860
```

---

## 📡 API Documentation

### Endpoints

#### 1. **Health Check**
```http
GET /
```
**Response:**
```json
{
  "status": "API running"
}
```

#### 2. **Create/Update Chat**
```http
POST /chat/create
Content-Type: application/json

{
  "session_id": "user123",
  "message": "What are the main findings in the research papers?"
}
```

**Response:**
```json
{
  "session_id": "user123",
  "history": [
    {
      "role": "user",
      "content": "What are the main findings in the research papers?"
    },
    {
      "role": "assistant",
      "content": "Based on the documents, the main findings include..."
    }
  ]
}
```

#### 3. **Get Chat History**
```http
GET /chat/{session_id}
```

**Response:**
```json
{
  "session_id": "user123",
  "history": [...]
}
```

#### 4. **Delete Chat**
```http
DELETE /chat/{session_id}
```

**Response:**
```json
{
  "message": "Chat deleted successfully"
}
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI |
| **Vector Database** | Pinecone |
| **Database** | MongoDB Atlas |
| **LLM** | Groq (Llama 3.1) |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) |
| **Orchestration** | LangChain |
| **Frontend** | Gradio |
| **PDF Processing** | PyPDF |

---

## 🔧 Configuration

### MongoDB Atlas Setup

1. Create a cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database user
3. Whitelist your IP (or use `0.0.0.0/0` for all IPs)
4. Copy connection string to `.env`

### Pinecone Setup

1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create a new index
3. Set dimension to `384` (for all-MiniLM-L6-v2)
4. Choose `cosine` similarity metric
5. Copy API key to `.env`

### Groq API Setup

1. Get API key from [Groq Console](https://console.groq.com/)
2. Add to `.env` file

---

## 📊 Usage Examples

### Command Line Interface

```bash
python main.py
```

```
📚 RAG Research Assistant
Type 'exit' to quit

❓ Enter your question: What are the benefits of renewable energy?

💡 Answer:
Renewable energy investments have led to significant job growth...
[World Energy Outlook 2022]
```

### API Request (cURL)

```bash
curl -X POST "http://127.0.0.1:8000/chat/create" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo",
    "message": "Summarize the key findings"
  }'
```

### Python Client

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat/create",
    json={
        "session_id": "python_client",
        "message": "What is mentioned about climate change?"
    }
)

print(response.json())
```

---

## 🎨 Gradio Interface Features

- **Streaming Responses** - Word-by-word AI response animation
- **Session Management** - Persistent chat history per user
- **Modern UI** - Clean, colorful, and responsive design
- **Easy Interaction** - Type and press Enter or click Submit

---

## 🧪 Testing

### Test Document Ingestion

```bash
python -c "from chatbot.ingestion.document_loader import DocumentLoader; \
           loader = DocumentLoader(); \
           docs = loader.load_all_pdfs(); \
           print(f'Loaded {len(docs)} pages')"
```

### Test RAG Pipeline

```bash
python -c "from rag_pipeline import rag_query; \
           print(rag_query('What is AI?'))"
```

### Test MongoDB Connection

```bash
python -c "from src.chatbot.api.db import chat_collection; \
           print('MongoDB Connected:', chat_collection.name)"
```

---

## 🐛 Troubleshooting

### Issue: MongoDB Connection Failed
**Solution:** Check your `MONGO_URI` and network access settings in MongoDB Atlas

### Issue: Pinecone Index Not Found
**Solution:** Run `python main_ingest.py` to create and populate the index

### Issue: Import Errors
**Solution:** Ensure you're running from the project root and virtual environment is activated

### Issue: API Not Starting
**Solution:** Check if port 8000 is already in use:
```bash
# Windows
netstat -ano | findstr :8000
# Linux/Mac
lsof -i :8000
```

---

## 📈 Performance Optimization

- **Chunking Strategy**: Adjust `chunk_size` and `chunk_overlap` in `chunker.py`
- **Retrieval**: Modify `top_k` parameter for more/fewer context documents
- **LLM Temperature**: Lower values (0.1) for factual, higher (0.7) for creative responses
- **Connection Pooling**: MongoDB client uses connection pooling by default

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use environment variables** for all secrets
3. **Enable MongoDB authentication**
4. **Restrict API access** with CORS in production
5. **Use HTTPS** for production deployment

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.chatbot.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment (Railway/Render)

1. Connect GitHub repository
2. Set environment variables in dashboard
3. Deploy with auto-scaling

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Talha Rehman**
- GitHub: [@TalhaRehmanMalik](https://github.com/TalhaRehmanMalik)
- LinkedIn: [Talha Rehman](https://www.linkedin.com/in/talha-rehman-7a3178221/)
- Email: talharehman41061@gmail.com

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for RAG orchestration
- [Pinecone](https://www.pinecone.io/) for vector database
- [Groq](https://groq.com/) for fast LLM inference
- [MongoDB Atlas](https://www.mongodb.com/atlas) for database hosting
- [Gradio](https://gradio.app/) for UI framework

---

## 📞 Support

For issues and questions:
- 🐛 [Open an Issue](https://github.com/TalhaRehmanMalik/rag-chatbot/issues)
- 💬 [Discussions](https://github.com/TalhaRehmanMalik/rag-chatbot/discussions)
- 📧 Email: talharehman41061@gmail.com

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [Talha Rehman](https://github.com/TalhaRehmanMalik)

</div>#   R a g - C h a t B o t  
 
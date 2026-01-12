#Retrieval + LLM generation
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq

from chatbot.config.settings import settings


class RAGRetriever:
    def __init__(self, top_k=5):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        vectorstore = PineconeVectorStore(
            index_name=settings.PINECONE_INDEX_NAME,
            embedding=embeddings
        )

        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )

    def retrieve(self, query: str):
        # ✅ ONLY correct method that works across versions
        return self.retriever.invoke(query)


class RAGQA:
    def __init__(self, top_k=5, temperature=0.1):
        self.llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=temperature
        )

        self.retriever = RAGRetriever(top_k=top_k)

        self.prompt = PromptTemplate(
    input_variables=["query", "context"],
    template="""
You are a research assistant. Use ONLY the provided context to answer the user query.

Question:
{query}

Context:
{context}

Instructions:
- If the user asks a question, provide a concise answer with citations like [source, page].
- If the user asks for a summary, respond in a  well-structured paragraph.
- Always include citations from metadata in square brackets [source, page].
- Do NOT hallucinate, guess, or add information not in the context.

Answer:
"""
)


        # ✅ Modern replacement of LLMChain
        self.chain = self.prompt | self.llm

    def run(self, query: str):
        docs = self.retriever.retrieve(query)

        context = ""
        for d in docs:
            context += (
                f"{d.page_content}\n"
                f"[{d.metadata.get('source')}, page {d.metadata.get('page')}]\n\n"
            )

        return self.chain.invoke(
            {
                "query": query,
                "context": context
            }
        )

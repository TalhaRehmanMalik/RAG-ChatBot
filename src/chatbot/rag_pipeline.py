# src/chatbot/rag_pipeline.py

from chatbot.qa_chain import RAGQA


class RAGPipeline:
    def __init__(self, top_k: int = 5, temperature: float = 0.1, mode: str = "qa"):
        """
        mode: "qa" for general Q&A
              "summary" for research summary
        """
        self.rag = RAGQA(top_k=top_k, temperature=temperature)
        self.mode = mode

    def run(self, user_query: str) -> str:
        if not user_query or not user_query.strip():
            return "⚠️ Please enter a valid question."

        try:
            # Depending on mode, you can tweak prompt or behavior
            if self.mode == "summary":
                prompt = f"Provide a concise structured summary for this question:\n{user_query}"
            else:
                prompt = user_query  # General Q&A

            response = self.rag.run(prompt)

            if hasattr(response, "content"):
                return response.content
            return str(response)

        except Exception as e:
            return f"❌ RAG Pipeline Error: {str(e)}"


_pipeline = RAGPipeline()

def rag_query(query: str, mode: str = "qa") -> str:
    _pipeline.mode = "summary" if mode == "summary" else "qa"
    return _pipeline.run(query)

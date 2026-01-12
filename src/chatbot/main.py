from chatbot.qa_chain import RAGQA
from chatbot.config.logger import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("📚 RAG Research Assistant")
    logger.info("Type 'exit' to quit\n")

    # Initialize RAG bot
    rag_bot = RAGQA(top_k=5, temperature=0.1)

    while True:
        query = input("❓ Enter your question: ").strip()

        if query.lower() in ["exit", "quit"]:
            logger.info("👋 Goodbye!")
            break

        if not query:
            logger.warning("⚠️ Please enter a valid question\n")
            continue

        try:
            response = rag_bot.run(query)

            logger.info("\n💡 Answer:\n")
            # ChatGroq returns AIMessage
            answer = response.content if hasattr(response, "content") else response
            logger.info(answer)

        except Exception as e:
            logger.error("❌ Error: %s", str(e))

        logger.info("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()

import time
import gradio as gr
from src.chatbot.rag_pipeline import rag_query

# ----------------------
# Chat function (STREAMING + DICT FORMAT)
# ----------------------
def chat_fn(user_input, history):
    if history is None:
        history = []

    if not user_input.strip():
        history.append({"role": "assistant", "content": "⚠️ Please enter a question."})
        yield history
        return

    # user message
    history.append({"role": "user", "content": user_input})
    # empty assistant message (for streaming)
    history.append({"role": "assistant", "content": ""})
    yield history

    # get response from your RAG pipeline
    full_response = rag_query(user_input)

    # stream word by word
    streamed_text = ""
    for word in full_response.split():
        streamed_text += word + " "
        history[-1]["content"] = streamed_text
        yield history
        time.sleep(0.03)  # small delay for streaming effect

# ----------------------
# CSS for light theme + colored buttons
# ----------------------
custom_css = """
#chatbot {
    height: 500px;
    border: 2px solid #7B68EE;
    border-radius: 15px;
    background-color: #F8F8FF;
}
#submit-btn { 
    background-color: #7B68EE !important; /* Purple submit button */
    color: white !important; 
    border-radius: 8px !important; 
    padding: 6px 15px !important; 
}
#clear-btn { 
    background-color: #FF4500 !important; /* Orange clear button */
    color: white !important; 
    border-radius: 8px !important; 
    padding: 6px 15px !important; 
}
"""

# ----------------------
# Gradio UI
# ----------------------
with gr.Blocks(title="🌟 RAG Chat Assistant") as app:

    gr.Markdown(
        "<h1>🌟 RAG Chat Assistant</h1>"
        "<p>Streaming responses with session-based chat</p>"
    )

    chatbot = gr.Chatbot(
        elem_id="chatbot",
        label="Chat"
    )

    user_msg = gr.Textbox(
        placeholder="Type your question here...",
        lines=3
    )

    with gr.Row():
        submit_btn = gr.Button("Submit", elem_id="submit-btn")
        clear_btn = gr.Button("Clear", elem_id="clear-btn")

    # Submit button and Enter key trigger chat_fn
    submit_btn.click(chat_fn, [user_msg, chatbot], chatbot)
    user_msg.submit(chat_fn, [user_msg, chatbot], chatbot)

    # Clear input after submit
    submit_btn.click(lambda: "", None, user_msg)
    clear_btn.click(lambda: [], None, chatbot)

# Launch app with custom CSS
app.launch(css=custom_css)










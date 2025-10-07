import gradio as gr

from customer_support_bot import chatbot_response

# Create Gradio interface
interface = gr.Interface(
    fn=chatbot_response,
    inputs=gr.Textbox(lines=2, placeholder="Ask your customer support question..."),
    outputs=gr.Textbox(label="Chatbot Response"),
    title="AI-Powered Customer Support Chatbot",
    description="Ask a question, and the AI will respond with the best-matching FAQ answer."
)

# Launch the web app
if __name__ == "__main__":
    interface.launch()
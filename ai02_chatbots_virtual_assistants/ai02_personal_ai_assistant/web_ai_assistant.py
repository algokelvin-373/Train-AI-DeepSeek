import gradio as gr

from ai_assistant import ai_assistant

# Create Gradio interface
interface = gr.Interface(
    fn=ai_assistant,
    inputs=gr.Textbox(lines=3, placeholder="Ask anything..."),
    outputs="text",
    title="AI-Powered Personal Assistant",
    description="Type a query or use voice commands to interact with the assistant.",
    live=True
)


# Launch the web app
if __name__ == "__main__":
    interface.launch()
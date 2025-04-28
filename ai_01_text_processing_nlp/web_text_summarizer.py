import gradio as gr
from text_summarizer import summarize_text

# Create Gradio interface
interface = gr.Interface(
    fn=summarize_text,
    inputs=gr.Textbox(lines=10, placeholder="Enter text to summarize"),
    outputs=gr.Textbox(label="Summarized Text"),
    title="AI-Powered Text Summarizer",
    description="Enter a long text and DeepSeek AI will generate a concise summary."
)

# Launch the web app
if __name__ == "__main__":
    interface.launch()
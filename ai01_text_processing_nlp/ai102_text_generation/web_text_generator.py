import gradio as gr
from text_generator import generate_text

interface = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(lines=3, placeholder="Enter your prompt here"),
        gr.Slider(50, 500, step=50, label="Word Limit"),
        gr.Button("Regenerate")
    ],
    outputs="text",
    title="AI-Powered Text Generator",
    description="Enter a prompt, select word limit, and generate AI-written content."
)


# Launch the web app
if __name__ == "__main__":
    interface.launch()
import gradio as gr

from extract_ner import extract_ner

interface = gr.Interface(
    fn=extract_ner,
    inputs=gr.Textbox(lines=5, placeholder="Enter text for entity recognition"),
    outputs=gr.Textbox(label="Extracted Entities"),
    title="AI-Powered Named Entity Recognition (NER)",
    description="Enter a paragraph and DeepSeek AI will extract persons, locations, and dates."
)


# Launch the web app
if __name__ == "__main__":
    interface.launch()
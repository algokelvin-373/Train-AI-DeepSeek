import gradio as gr

from grammar_spell_checker import correct_grammar

interface = gr.Interface(
    fn=correct_grammar,
    inputs=gr.Textbox(lines=5, placeholder="Enter text with grammar or spelling mistakes"),
    outputs=gr.Textbox(label="Corrected Text"),
    title="AI-Powered Grammar and Spell Checker",
    description="Enter text, and AI DeepSeeks Will Be Correct"
)


# Launch the web app
if __name__ == "__main__":
    interface.launch()
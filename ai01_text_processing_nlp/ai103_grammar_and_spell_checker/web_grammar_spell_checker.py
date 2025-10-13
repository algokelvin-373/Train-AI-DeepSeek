import gradio as gr
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def correct_grammar(text: str) -> str:
    print(f'Correcting: {text[:50]}...')
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Correct the grammar and spelling of the following text:\n\n{text}",
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=3000)
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        return result if result else "No correction generated."
    except Exception as e:
        return f"Error: {str(e)}"

interface = gr.Interface(
    fn=correct_grammar,
    inputs=gr.Textbox(lines=25, placeholder="Enter text with grammar or spelling mistakes"),
    outputs=gr.Textbox(lines=25, label="Corrected Text"),
    title="AI-Powered Grammar and Spell Checker",
    description="Enter text, and AI will correct grammar and spelling."
)

if __name__ == "__main__":
    interface.launch()
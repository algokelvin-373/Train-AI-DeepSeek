from fastapi import FastAPI
import requests

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/extract_entities/")
def extract_ner(text: str):
    payload = {"model": "deepseek-r1", "prompt": f"Extract Entities:\n\n{text}", "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No entities detected.")
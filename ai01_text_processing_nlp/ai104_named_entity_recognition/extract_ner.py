import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_ner(text):
    prompt = f"Extract all named entities (persons, organization, location, dates) from the following text:\n\n{text}"

    payload = {
        "model": "deepseek-r1",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No entities detected.")
    else:
        return f"Error: {response.text}"


if __name__ == "__main__":
    sample_text = "Google was founded by Larry Page and Sergey Brin in September 1988 at Stanford University."
    print("### Extracted Entities ###")
    print(extract_ner(sample_text))
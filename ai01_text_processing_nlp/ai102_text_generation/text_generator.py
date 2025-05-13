import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_text(prompt, word_limit=100, language="English"):
    full_prompt = f"Write a {language}-language text to Generate a response within {word_limit} words:\n\n{prompt}"

    payload = {
        "model": "deepseek-r1",
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No content generated.")
    else:
        return f"Error: {response.text}"


if __name__ == "__main__":
    prompt = "Write an introduction for an article about the future of AI."
    print("### AI-Generated Content ###")
    print(generate_text(prompt))
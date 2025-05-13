import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_sentiment(text):
    prompt = f"Classify the sentiment of the following text as Positive, Negative, or Neutral:\n\n{text}"

    payload = {
        "model": "deepseek-r1",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No sentiment detected.")
    else:
        return f"Error: {response.text}"


if __name__ == "__main__":
    sample_text = "The movie was absolutely fantastic! I enjoyed every minute of it."
    sample_text_2 = "The service was terrible. I waited an hour, and my order was wrong."
    print("### Sentiment Analyze Result ###")
    print(analyze_sentiment(sample_text_2))
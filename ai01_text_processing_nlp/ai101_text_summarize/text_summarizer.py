import requests

# Define API URL (Ollama runs locally on port 11434)
OLLAMA_URL = "http://localhost:11434/api/generate"

def summarize_text(text):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Summarize the following text in **3 bullet points**:\n\n{text}",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No summary generated.")
    else:
        return f"Error: {response.text}"

# # Test Summarization
if __name__ == "__main__":
    sample_text = """
    Artificial Intelligence is transforming industries across the world. AI models like DeepSeek-R1 enable businesses to automate tasks,
    analyze large datasets, and enhance productivity. With advancements in AI, applications range from virtual assistants to predictive analytics
    and personalized recommendations.
    """
    print("### Summary ###")
    print(summarize_text(sample_text))

import requests
import json

API_KEY = "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"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer <API_KEY>",
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>",
        "X-Title": "<YOUR_SITE_NAME>",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ],

    })
)

print("Response:")
print(response)
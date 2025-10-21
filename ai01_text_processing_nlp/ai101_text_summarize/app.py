from fastapi import FastAPI
import requests
import time

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/summarize/")
def summarize_text(text: str):
    start_time = time.time()
    try:
        payload = {
            "model": "deepseek-r1",
            "prompt": f"Summarize this text in Indonesian:\n\n{text}",
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        processing_time = round(time.time() - start_time, 2)

        if response.status_code == 200:
            result = response.json()
            summary = result.get("response", "").strip()

            return {
                "status": "success",
                "summary": summary,
                "metrics": {
                    "processing_time_seconds": processing_time,
                    "original_length": len(text),
                    "summary_length": len(summary),
                    "compression_ratio": f"{round(len(summary) / len(text) * 100, 1)}%" if text else "0%"
                },
                "model_info": {
                    "name": "deepseek-r1",
                    "provider": "ollama"
                }
            }
        else:
            return {
                "status": "error",
                "error": {
                    "code": response.status_code,
                    "message": "Failed to process request",
                    "details": response.text[:200]  # Limit error details length
                },
                "metrics": {
                    "processing_time_seconds": processing_time
                }
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": {
                "code": "timeout",
                "message": "Request timeout - Ollama service took too long to respond"
            },
            "metrics": {
                "processing_time_seconds": round(time.time() - start_time, 2)
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": {
                "code": "internal_error",
                "message": "An unexpected error occurred",
                "details": str(e)
            },
            "metrics": {
                "processing_time_seconds": round(time.time() - start_time, 2)
            }
        }
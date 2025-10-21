from fastapi import FastAPI, HTTPException
import requests
import time
from pydantic import BaseModel

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"


# Request Model
class SummaryRequest(BaseModel):
    text: str
    model: str = "deepseek-r1"


# Response Model
class SummaryResponse(BaseModel):
    success: bool
    summary: str
    processing_time: float
    original_length: int
    summary_length: int


@app.post("/summarize/", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    """
    Summarize text using Ollama
    """
    start_time = time.time()

    try:
        # Prepare the payload for Ollama
        payload = {
            "model": request.model,
            "prompt": f"Buatlah ringkasan yang jelas dan padat dari teks berikut:\n\n{request.text}",
            "stream": False
        }

        # Send request to Ollama
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        if response.status_code == 200:
            result = response.json()
            summary = result.get("response", "").strip()

            if not summary:
                raise HTTPException(status_code=500, detail="Model returned empty summary")

            processing_time = round(time.time() - start_time, 2)

            return SummaryResponse(
                success=True,
                summary=summary,
                processing_time=processing_time,
                original_length=len(request.text),
                summary_length=len(summary)
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ollama API error: {response.status_code}"
            )

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
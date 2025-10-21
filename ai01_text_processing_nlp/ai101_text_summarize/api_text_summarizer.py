from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
API_KEY = os.getenv('OPENROUTER_API_KEY', 'your_default_api_key_here')

"""
    Fungsi untuk meringkas teks menggunakan OpenRouter API

    Parameters:
    - text: Teks yang akan diringkas
    - api_key: API key OpenRouter Anda
    - model: Model yang digunakan (default: deepseek/deepseek-r1:free)
    - max_length: Panjang maksimal ringkasan (dalam tokens/karakter)
"""
def summarize_text(text, api_key, model="deepseek/deepseek-r1:free", max_length=1000):
    system_prompt = """Anda adalah asisten yang ahli dalam meringkas teks. 
    Buatlah ringkasan yang padat, informatif, dan mudah dipahami dari teks yang diberikan.
    Pertahankan poin-poin penting dan inti dari teks asli."""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Tolong ringkas teks berikut:\n\n{text}\n\nRingkasan:"
                    }
                ],
                "max_tokens": max_length,
                "temperature": 0.3,
            })
        )

        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content']
            return {
                "success": True,
                "summary": summary.strip(),
                "model_used": model
            }
        else:
            return {
                "success": False,
                "error": f"API Error: {response.status_code}",
                "details": response.text
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Exception occurred: {str(e)}"
        }


@app.route('/')
def home():
    """Home endpoint with information API"""
    return jsonify({
        "message": "Text Summarizer API",
        "version": "1.0",
        "endpoints": {
            "POST /summarize": "Meringkas teks",
            "GET /health": "Check API status"
        },
        "usage": "Send POST request to /summarize with JSON body containing 'text'"
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Text Summarizer API"
    })


@app.route('/summarize', methods=['POST'])
def summarize_api():
    """
    Endpoint untuk meringkas teks
    Expected JSON payload:
    {
        "text": "Teks yang akan diringkas...",
        "model": "deepseek/deepseek-r1:free" (optional),
        "max_length": 1000 (optional)
    }
    """
    # Check content type
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    # Get JSON data
    data = request.get_json()

    # Validate required fields
    if not data or 'text' not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'text' field in request body"
        }), 400

    text = data['text']
    model = data.get('model', 'deepseek/deepseek-r1:free')
    max_length = data.get('max_length', 1000)

    # Validate text
    if not text or not text.strip():
        return jsonify({
            "success": False,
            "error": "Text cannot be empty"
        }), 400

    if len(text.strip()) < 10:
        return jsonify({
            "success": False,
            "error": "Text too short for summarization"
        }), 400

    # Process summarization
    result = summarize_text(text, API_KEY, model, max_length)

    # Add metadata
    result["timestamp"] = datetime.now().isoformat()
    result["original_text_length"] = len(text)

    if result["success"]:
        result["summary_length"] = len(result["summary"])
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@app.route('/summarize/batch', methods=['POST'])
def batch_summarize():
    """
    Endpoint untuk meringkas multiple teks sekaligus
    Expected JSON payload:
    {
        "texts": [
            "Teks pertama...",
            "Teks kedua...",
            ...
        ],
        "model": "deepseek/deepseek-r1:free" (optional),
        "max_length": 1000 (optional)
    }
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    if not data or 'texts' not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'texts' field in request body"
        }), 400

    texts = data['texts']
    model = data.get('model', 'deepseek/deepseek-r1:free')
    max_length = data.get('max_length', 1000)

    if not isinstance(texts, list) or len(texts) == 0:
        return jsonify({
            "success": False,
            "error": "'texts' must be a non-empty array"
        }), 400

    # Process each text
    results = []
    for i, text in enumerate(texts):
        if not text or not text.strip():
            results.append({
                "success": False,
                "error": f"Text at index {i} is empty",
                "index": i
            })
            continue

        result = summarize_text(text, API_KEY, model, max_length)
        result["index"] = i
        result["original_text_length"] = len(text)
        if result["success"]:
            result["summary_length"] = len(result["summary"])

        results.append(result)

    return jsonify({
        "success": True,
        "results": results,
        "total_processed": len(results),
        "timestamp": datetime.now().isoformat()
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
import requests
from requests import RequestException

from config import MAX_TOKENS, OLLAMA_MODEL, OLLAMA_URL, REQUEST_TIMEOUT_SECONDS


def query_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": MAX_TOKENS,
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except RequestException as exc:
        return f"Ollama request failed: {exc}. Please ensure Ollama is running locally."

    try:
        data = response.json()
    except ValueError:
        return "Ollama returned a non-JSON response."

    return data.get("response", "No response returned by Ollama.").strip()
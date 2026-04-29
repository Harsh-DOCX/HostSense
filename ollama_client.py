import asyncio

import aiohttp

from config import (
    MAX_TOKENS,
    OLLAMA_MODEL,
    OLLAMA_NUM_CTX,
    OLLAMA_NUM_THREAD,
    OLLAMA_TEMPERATURE,
    OLLAMA_URL,
    REQUEST_TIMEOUT_SECONDS,
)


async def query_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": MAX_TOKENS,
            "num_ctx": OLLAMA_NUM_CTX,
            "num_thread": OLLAMA_NUM_THREAD,
            "temperature": OLLAMA_TEMPERATURE,
        },
    }

    try:
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_SECONDS)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(OLLAMA_URL, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        return f"Ollama request failed: {exc}. Please ensure Ollama is running locally."
    except ValueError:
        return "Ollama returned a non-JSON response."

    return data.get("response", "No response returned by Ollama.").strip()

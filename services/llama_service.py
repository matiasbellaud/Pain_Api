import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_llama(prompt: str, model: str = "llama3"):
    payload = {"model": model, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data.get("response", "")
    else:
        raise Exception(f"Erreur Ollama: {response.status_code} - {response.text}")

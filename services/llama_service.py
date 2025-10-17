import requests
import json
from typing import Tuple, Dict, Any, List
from services.resource_monitor import ResourceMonitor
from prompts.system_prompt import build_recipe_prompt, build_general_cooking_prompt, CUISINE_SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_llama(prompt: str, model: str = "llama3", force_json: bool = False) -> Tuple[str, Dict[str, Any]]:
    monitor = ResourceMonitor()
    monitor.start_monitoring()

    try:
        payload = {"model": model, "prompt": prompt, "stream": False}

        if force_json:
            payload["format"] = "json"

        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")
            metrics = monitor.stop_monitoring()
            return answer, metrics
        else:
            raise Exception(f"Erreur Ollama: {response.status_code} - {response.text}")
    except Exception as e:
        metrics = monitor.stop_monitoring() if monitor.start_time else {}
        raise e


def generate_recipes(ingredients: List[str], number_of_recipes: int = 1,
                     dietary_restrictions: List[str] = None,
                     model: str = "llama3") -> Tuple[str, Dict[str, Any]]:
    prompt = build_recipe_prompt(ingredients, number_of_recipes, dietary_restrictions)
    return query_llama(prompt, model, force_json=True)


def ask_cooking_question(question: str, model: str = "llama3") -> Tuple[str, Dict[str, Any]]:
    prompt = build_general_cooking_prompt(question)
    return query_llama(prompt, model, force_json=False)

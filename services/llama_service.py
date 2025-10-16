import requests
import json
from typing import Tuple, Dict, Any
from services.resource_monitor import ResourceMonitor

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_llama(prompt: str, model: str = "llama3") -> Tuple[str, Dict[str, Any]]:
    """
    Envoie une requête à Ollama et mesure les ressources utilisées.

    Returns:
        Tuple contenant (réponse, métriques_ressources)
    """
    monitor = ResourceMonitor()
    monitor.start_monitoring()

    try:
        payload = {"model": model, "prompt": prompt, "stream": False}
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")

            # Récupérer les métriques
            metrics = monitor.stop_monitoring()

            return answer, metrics
        else:
            raise Exception(f"Erreur Ollama: {response.status_code} - {response.text}")
    except Exception as e:
        # En cas d'erreur, on récupère quand même les métriques
        metrics = monitor.stop_monitoring() if monitor.start_time else {}
        raise e

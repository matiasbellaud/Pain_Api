from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models.request_model import PromptRequest
from models.response_model import LlamaResponse, ResourceMetrics
from services.llama_service import query_llama
from services.resource_monitor import get_system_stats
from services.websocket_service import metrics_streamer

router = APIRouter(prefix="/api", tags=["LLaMA"])

@router.post("/ask", response_model=LlamaResponse)
def ask_llama(request: PromptRequest):
    """Envoie un prompt au modèle LLaMA via Ollama avec monitoring des ressources."""
    answer, metrics = query_llama(request.prompt)

    return LlamaResponse(
        response=answer,
        energy_usage=metrics.get("estimated_energy_wh", 0.0),
        metrics=ResourceMetrics(**metrics)
    )

@router.get("/system-stats")
def system_stats():
    """Retourne les statistiques système actuelles."""
    return get_system_stats()

@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """
    WebSocket endpoint pour streamer les métriques système en temps réel.

    Se connecte via: ws://localhost:4000/api/ws/metrics
    Envoie les métriques toutes les secondes.
    """
    await metrics_streamer.connect(websocket)
    try:
        # Envoyer un message de bienvenue
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "Streaming des métriques démarré"
        })

        # Streamer les métriques en continu
        await metrics_streamer.stream_metrics(websocket, interval=1.0)
    except WebSocketDisconnect:
        metrics_streamer.disconnect(websocket)
        print("Client WebSocket déconnecté")
    except Exception as e:
        print(f"Erreur WebSocket: {e}")
        metrics_streamer.disconnect(websocket)

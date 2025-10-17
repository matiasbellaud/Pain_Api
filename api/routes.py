from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from models.request_model import PromptRequest
from models.response_model import LlamaResponse, ResourceMetrics
from models.recipe_model import RecipeRequest, RecipeResponse, Recipe
from services.llama_service import query_llama, generate_recipes, ask_cooking_question
from services.resource_monitor import get_system_stats
from services.websocket_service import metrics_streamer
import json

router = APIRouter(prefix="/api", tags=["LLaMA"])

@router.post("/ask", response_model=LlamaResponse)
def ask_llama(request: PromptRequest):
    answer, metrics = ask_cooking_question(request.prompt)

    return LlamaResponse(
        response=answer,
        energy_usage=metrics.get("estimated_energy_wh", 0.0),
        metrics=ResourceMetrics(**metrics)
    )

@router.post("/recipe", response_model=RecipeResponse)
def generate_recipe(request: RecipeRequest):
    try:
        response_text, metrics = generate_recipes(
            ingredients=request.ingredients,
            number_of_recipes=request.number_of_recipes,
            dietary_restrictions=request.dietary_restrictions
        )

        try:
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()

            recipe_data = json.loads(cleaned_response)
            recipes = [Recipe(**recipe) for recipe in recipe_data.get("recipes", [])]

            if not recipes:
                raise ValueError("Aucune recette générée")

            return RecipeResponse(
                recipes=recipes,
                energy_usage=metrics.get("estimated_energy_wh", 0.0),
                metrics=metrics
            )

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur de parsing JSON de la réponse IA : {str(e)}. Réponse brute : {response_text[:200]}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors du traitement de la recette : {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de la recette : {str(e)}"
        )


@router.get("/system-stats")
def system_stats():
    return get_system_stats()

@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    await metrics_streamer.connect(websocket)
    try:
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "Streaming des métriques démarré"
        })

        await metrics_streamer.stream_metrics(websocket, interval=1.0)
    except WebSocketDisconnect:
        metrics_streamer.disconnect(websocket)
        print("Client WebSocket déconnecté")
    except Exception as e:
        print(f"Erreur WebSocket: {e}")
        metrics_streamer.disconnect(websocket)

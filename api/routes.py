from fastapi import APIRouter
from models.request_model import PromptRequest
from models.response_model import LlamaResponse
from services.llama_service import query_llama

router = APIRouter(prefix="/api", tags=["LLaMA"])

@router.post("/ask", response_model=LlamaResponse)
def ask_llama(request: PromptRequest):
    """Envoie un prompt au modèle LLaMA via Ollama."""
    answer = query_llama(request.prompt)

    return LlamaResponse(
        response=answer
    )

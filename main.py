from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Local LLaMA API",
    description="API locale pour interagir avec un modèle LLaMA via Ollama",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API LLaMA locale 👋"}

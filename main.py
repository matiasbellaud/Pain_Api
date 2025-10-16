from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router
import os

app = FastAPI(
    title="Local LLaMA API",
    description="API locale pour interagir avec un modèle LLaMA via Ollama",
    version="1.0.0"
)

app.include_router(router)

# Servir les fichiers statiques si le dossier existe
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API LLaMA locale 👋"}

@app.get("/demo")
def demo():
    """Page de démonstration du WebSocket de monitoring."""
    return FileResponse("static/websocket-demo.html")

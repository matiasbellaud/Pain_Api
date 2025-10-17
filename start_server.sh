#!/bin/bash

# Script de démarrage du serveur API avec support WebSocket

echo "🚀 Démarrage du serveur API LLaMA avec WebSocket..."
echo ""

# Arrêter le serveur existant si présent
pkill -f "uvicorn main:app" 2>/dev/null
sleep 1

# Démarrer le serveur
echo "📡 Serveur démarré sur http://localhost:4000"
echo "🔌 WebSocket disponible sur ws://localhost:4000/api/ws/metrics"
echo "🎨 Page de démo: http://localhost:4000/demo"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer uvicorn
uvicorn main:app --reload --port 4000

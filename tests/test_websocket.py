"""
Script de test pour le WebSocket de streaming des métriques.
Usage: python tests/test_websocket.py
"""
import asyncio
import json

try:
    import websockets
except ImportError:
    print("❌ Module 'websockets' non trouvé. Installation...")
    import subprocess
    subprocess.check_call(["pip", "install", "websockets"])
    import websockets


async def test_websocket():
    """Test de connexion au WebSocket et réception des métriques."""
    uri = "ws://localhost:4000/api/ws/metrics"

    print(f"🔌 Connexion au WebSocket: {uri}")

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connecté au WebSocket!")

            # Recevoir le message de bienvenue
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"\n📨 Message de bienvenue: {welcome_data}")

            # Recevoir 5 messages de métriques
            print("\n📊 Réception des métriques en temps réel...\n")

            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)

                print(f"--- Message #{i+1} ---")
                print(f"  CPU: {data['cpu']['percent_total']:.1f}%")
                print(f"  Mémoire: {data['memory']['percent']:.1f}% "
                      f"({data['memory']['used_mb']:.0f} MB utilisés)")
                print(f"  Disque: {data['disk']['percent']:.1f}%")
                print(f"  Processus actuel: {data['process']['memory_mb']:.1f} MB")
                print()

            print("✅ Test réussi! WebSocket fonctionne correctement.")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(test_websocket())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")

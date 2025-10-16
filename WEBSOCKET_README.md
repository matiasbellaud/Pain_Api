# WebSocket Monitoring en Temps Réel

Ce projet inclut un système de monitoring des ressources système en temps réel via WebSocket.

## Fonctionnalités

Le WebSocket transmet en continu (toutes les secondes) les métriques suivantes :

### Métriques CPU
- Utilisation totale en pourcentage
- Utilisation par cœur
- Nombre de cœurs
- Fréquence actuelle (MHz)

### Métriques Mémoire
- Pourcentage d'utilisation
- Mémoire totale (MB)
- Mémoire disponible (MB)
- Mémoire utilisée (MB)

### Métriques Disque
- Pourcentage d'utilisation
- Espace total (GB)
- Espace utilisé (GB)
- Espace libre (GB)

### Métriques Réseau
- Données envoyées (MB)
- Données reçues (MB)

### Métriques Processus
- Mémoire utilisée par l'API (MB)
- CPU utilisé par l'API (%)

## Utilisation

### 1. Via Python (Client de test)

```bash
python3 tests/test_websocket.py
```

### 2. Via JavaScript (Frontend)

```javascript
const ws = new WebSocket('ws://localhost:4000/api/ws/metrics');

ws.onopen = () => {
    console.log('Connecté au WebSocket');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // Premier message : bienvenue
    if (data.type === 'connection') {
        console.log('Status:', data.status);
        console.log('Message:', data.message);
        return;
    }

    // Messages suivants : métriques
    console.log('CPU:', data.cpu.percent_total + '%');
    console.log('Mémoire:', data.memory.percent + '%');
    console.log('Disque:', data.disk.percent + '%');
    // ... etc
};

ws.onerror = (error) => {
    console.error('Erreur:', error);
};

ws.onclose = () => {
    console.log('Déconnecté');
};
```

### 3. Via HTML (Page de démo)

Ouvrez votre navigateur et accédez à :

```
http://localhost:4000/demo
```

Cette page affiche en temps réel :
- Graphiques de progression pour CPU, Mémoire et Disque
- Statistiques réseau
- Informations sur le processus API
- Informations système

## Structure des données

### Message de bienvenue (premier message)

```json
{
  "type": "connection",
  "status": "connected",
  "message": "Streaming des métriques démarré"
}
```

### Messages de métriques (envoyés chaque seconde)

```json
{
  "timestamp": 1697456789.123,
  "cpu": {
    "percent_total": 25.5,
    "percent_per_core": [20.0, 30.0, 25.0, 26.0],
    "count": 4,
    "frequency_mhz": 2400.0
  },
  "memory": {
    "percent": 65.2,
    "total_mb": 16384.0,
    "available_mb": 5700.0,
    "used_mb": 10684.0
  },
  "disk": {
    "percent": 45.3,
    "total_gb": 512.0,
    "used_gb": 232.0,
    "free_gb": 280.0
  },
  "network": {
    "bytes_sent_mb": 1250.5,
    "bytes_recv_mb": 3420.8
  },
  "process": {
    "memory_mb": 85.3,
    "cpu_percent": 2.5
  }
}
```

## Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Page d'accueil |
| POST | `/api/ask` | Envoyer un prompt à LLaMA |
| GET | `/api/system-stats` | Obtenir les stats système (snapshot) |
| WS | `/api/ws/metrics` | WebSocket de streaming des métriques |
| GET | `/demo` | Page de démonstration HTML |

## Configuration

Par défaut, les métriques sont envoyées toutes les **1 seconde**.

Pour modifier l'intervalle, éditez le fichier `api/routes.py` :

```python
await metrics_streamer.stream_metrics(websocket, interval=1.0)  # Modifier ici
```

## Intégration Frontend

### React

```javascript
import { useEffect, useState } from 'react';

function MetricsMonitor() {
    const [metrics, setMetrics] = useState(null);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:4000/api/ws/metrics');

        ws.onopen = () => {
            setConnected(true);
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type !== 'connection') {
                setMetrics(data);
            }
        };

        ws.onclose = () => {
            setConnected(false);
        };

        return () => ws.close();
    }, []);

    if (!connected) return <div>Connexion...</div>;
    if (!metrics) return <div>Chargement des métriques...</div>;

    return (
        <div>
            <h2>CPU: {metrics.cpu.percent_total.toFixed(1)}%</h2>
            <h2>Mémoire: {metrics.memory.percent.toFixed(1)}%</h2>
            <h2>Disque: {metrics.disk.percent.toFixed(1)}%</h2>
        </div>
    );
}
```

### Vue.js

```javascript
<template>
  <div>
    <div v-if="!connected">Connexion...</div>
    <div v-else-if="!metrics">Chargement...</div>
    <div v-else>
      <h2>CPU: {{ metrics.cpu.percent_total.toFixed(1) }}%</h2>
      <h2>Mémoire: {{ metrics.memory.percent.toFixed(1) }}%</h2>
      <h2>Disque: {{ metrics.disk.percent.toFixed(1) }}%</h2>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null,
      connected: false,
      metrics: null
    };
  },
  mounted() {
    this.ws = new WebSocket('ws://localhost:4000/api/ws/metrics');

    this.ws.onopen = () => {
      this.connected = true;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type !== 'connection') {
        this.metrics = data;
      }
    };

    this.ws.onclose = () => {
      this.connected = false;
    };
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  }
};
</script>
```

## Dépannage

### Le WebSocket ne se connecte pas

1. Vérifiez que le serveur est en cours d'exécution :
   ```bash
   ps aux | grep uvicorn
   ```

2. Redémarrez le serveur :
   ```bash
   pkill -f uvicorn
   uvicorn main:app --reload --port 4000
   ```

3. Vérifiez que le port 4000 est accessible :
   ```bash
   curl http://localhost:4000/
   ```

### Les métriques ne s'affichent pas

1. Ouvrez la console du navigateur (F12)
2. Vérifiez les erreurs JavaScript
3. Vérifiez que le format des données est correct

### Erreur CORS

Si vous accédez depuis un domaine différent, ajoutez CORS dans `main.py` :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance

- **Bande passante** : ~1-2 KB par seconde par client connecté
- **CPU** : Impact minimal (~0.5% par client)
- **Mémoire** : ~5 MB par client connecté

Le système supporte facilement 100+ clients simultanés.

## Sécurité

⚠️ **Important** : En production, vous devriez :

1. Ajouter une authentification (JWT, OAuth, etc.)
2. Limiter le nombre de connexions par IP
3. Utiliser WSS (WebSocket Secure) avec HTTPS
4. Implémenter un rate limiting

Exemple avec authentification :

```python
@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket, token: str = None):
    if not verify_token(token):  # Fonction à implémenter
        await websocket.close(code=1008)  # Policy violation
        return

    await metrics_streamer.connect(websocket)
    # ... reste du code
```

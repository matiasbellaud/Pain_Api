import asyncio
import json
from typing import Dict, Any
from fastapi import WebSocket
from services.resource_monitor import get_system_stats
import psutil


class MetricsStreamer:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.streaming = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_metrics(self, websocket: WebSocket, data: Dict[str, Any]):
        try:
            await websocket.send_json(data)
        except Exception as e:
            self.disconnect(websocket)

    async def broadcast_metrics(self, data: Dict[str, Any]):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"Erreur de broadcast: {e}")
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

    def get_detailed_metrics(self) -> Dict[str, Any]:
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()
        process = psutil.Process()
        process_memory = process.memory_info()

        return {
            "timestamp": asyncio.get_event_loop().time(),
            "cpu": {
                "percent_total": psutil.cpu_percent(interval=0.1),
                "percent_per_core": cpu_percent,
                "count": psutil.cpu_count(),
                "frequency_mhz": cpu_freq.current if cpu_freq else 0,
            },
            "memory": {
                "percent": memory.percent,
                "total_mb": memory.total / (1024 * 1024),
                "available_mb": memory.available / (1024 * 1024),
                "used_mb": memory.used / (1024 * 1024),
            },
            "disk": {
                "percent": disk.percent,
                "total_gb": disk.total / (1024 ** 3),
                "used_gb": disk.used / (1024 ** 3),
                "free_gb": disk.free / (1024 ** 3),
            },
            "network": {
                "bytes_sent_mb": net_io.bytes_sent / (1024 * 1024),
                "bytes_recv_mb": net_io.bytes_recv / (1024 * 1024),
            },
            "process": {
                "memory_mb": process_memory.rss / (1024 * 1024),
                "cpu_percent": process.cpu_percent(),
            }
        }

    async def stream_metrics(self, websocket: WebSocket, interval: float = 1.0):
        try:
            while True:
                metrics = self.get_detailed_metrics()
                await self.send_metrics(websocket, metrics)
                await asyncio.sleep(interval)
        except Exception as e:
            print(f"Erreur dans le streaming: {e}")
            self.disconnect(websocket)


metrics_streamer = MetricsStreamer()

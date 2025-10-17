import psutil
import time
from typing import Dict, Any


class ResourceMonitor:
    def __init__(self):
        self.process = psutil.Process()
        self.start_time = None
        self.start_cpu_time = None
        self.start_memory = None

    def start_monitoring(self):
        self.start_time = time.time()
        self.start_cpu_time = self.process.cpu_times()
        self.start_memory = self.process.memory_info().rss / (1024 * 1024)

    def stop_monitoring(self) -> Dict[str, Any]:
        if self.start_time is None:
            raise ValueError("Le monitoring n'a pas été démarré")

        elapsed_time = time.time() - self.start_time

        end_cpu_time = self.process.cpu_times()
        cpu_time_used = (end_cpu_time.user - self.start_cpu_time.user) + \
                       (end_cpu_time.system - self.start_cpu_time.system)
        cpu_percent = (cpu_time_used / elapsed_time) * 100 if elapsed_time > 0 else 0

        end_memory = self.process.memory_info().rss / (1024 * 1024)
        memory_used = end_memory - self.start_memory

        estimated_energy_joules = (cpu_percent * elapsed_time * 15) / 100
        estimated_energy_wh = estimated_energy_joules / 3600

        return {
            "elapsed_time_seconds": round(elapsed_time, 3),
            "cpu_percent": round(cpu_percent, 2),
            "cpu_time_seconds": round(cpu_time_used, 3),
            "memory_used_mb": round(memory_used, 2),
            "memory_current_mb": round(end_memory, 2),
            "estimated_energy_joules": round(estimated_energy_joules, 4),
            "estimated_energy_wh": round(estimated_energy_wh, 6)
        }


def get_system_stats() -> Dict[str, Any]:
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "cpu_count": psutil.cpu_count(),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_available_mb": psutil.virtual_memory().available / (1024 * 1024),
        "memory_total_mb": psutil.virtual_memory().total / (1024 * 1024)
    }

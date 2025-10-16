from pydantic import BaseModel
from typing import Optional, Dict, Any

class ResourceMetrics(BaseModel):
    """Métriques de ressources système."""
    elapsed_time_seconds: float
    cpu_percent: float
    cpu_time_seconds: float
    memory_used_mb: float
    memory_current_mb: float
    estimated_energy_joules: float
    estimated_energy_wh: float

class LlamaResponse(BaseModel):
    response: str
    energy_usage: float  # En Wh pour compatibilité
    metrics: Optional[ResourceMetrics] = None

from pydantic import BaseModel

class LlamaResponse(BaseModel):
    response: str
    energy_usage: float

from pydantic import BaseModel
from typing import List, Dict, Any

class RespuestaSnapshot(BaseModel):
    """
    DTO para snapshot de grafo (vertices y aristas).
    """
    vertices: List[Dict[str, Any]]
    aristas: List[Dict[str, Any]]
    dirigido: bool = False

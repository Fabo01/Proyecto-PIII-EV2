from typing import Dict, Any
from pydantic import BaseModel

class RespuestaHashMap(BaseModel):
    """
    DTO genérico para exponer un hashmap de objetos (ID o clave → objeto serializable).
    """
    hashmap: Dict[str, Any]

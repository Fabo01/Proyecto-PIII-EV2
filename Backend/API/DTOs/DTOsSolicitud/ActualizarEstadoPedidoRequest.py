"""
DTO para solicitud de actualización de estado de pedido.
"""
from pydantic import BaseModel, validator
from typing import Optional

class ActualizarEstadoPedidoRequest(BaseModel):
    """DTO para actualizar el estado de un pedido."""
    nuevo_status: str
    comentario: Optional[str] = None
    
    @validator('nuevo_status')
    def validar_status(cls, v):
        estados_validos = ['pendiente', 'en_ruta', 'entregado']
        if v not in estados_validos:
            raise ValueError(f'Estado inválido: {v}. Estados válidos: {estados_validos}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "nuevo_status": "entregado",
                "comentario": "Entregado exitosamente al cliente"
            }
        }

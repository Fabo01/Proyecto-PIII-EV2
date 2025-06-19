from fastapi import APIRouter, HTTPException
from typing import List

from Backend.API.DTOs.Dtos1 import RecargaResponse
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService

router = APIRouter(prefix="/recargas", tags=["Recargas"])

@router.get("/", response_model=List[RecargaResponse])
def listar_recargas():
    recargas = SimulacionAplicacionService.listar_recargas()
    if recargas is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not recargas:
        raise HTTPException(status_code=404, detail="No hay estaciones de recarga registradas")
    return recargas

@router.get("/{id}", response_model=RecargaResponse)
def obtener_recarga(id: int):
    try:
        recarga = SimulacionAplicacionService.obtener_recarga(id)
        if recarga is None:
            raise HTTPException(status_code=404, detail="Estación de recarga no encontrada")
        return recarga
    except Exception:
        raise HTTPException(status_code=404, detail="Estación de recarga no encontrada")

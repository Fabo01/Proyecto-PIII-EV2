from fastapi import APIRouter, HTTPException
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.Dtos1 import AlmacenamientoResponse
from typing import List

router = APIRouter(prefix="/almacenamientos", tags=["Almacenamientos"])

@router.get("/", response_model=List[AlmacenamientoResponse])
def listar_almacenamientos():
    almacenamientos = SimulacionAplicacionService.listar_almacenamientos()
    if almacenamientos is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not almacenamientos:
        raise HTTPException(status_code=404, detail="No hay almacenamientos registrados")
    return almacenamientos

@router.get("/{id}", response_model=AlmacenamientoResponse)
def obtener_almacenamiento(id: int):
    try:
        almacen = SimulacionAplicacionService.obtener_almacenamiento(id)
        if almacen is None:
            raise HTTPException(status_code=404, detail="Almacenamiento no encontrado")
        return almacen
    except Exception:
        raise HTTPException(status_code=404, detail="Almacenamiento no encontrado")

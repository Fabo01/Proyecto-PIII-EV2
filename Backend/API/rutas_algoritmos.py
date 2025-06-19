from fastapi import APIRouter, HTTPException, Query
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.Dtos1 import RutaResponse
from typing import List
import time

router = APIRouter(prefix="/rutas", tags=["Rutas"])

@router.get("/camino", response_model=RutaResponse)
def calcular_camino(
    origen: int = Query(..., description="ID del nodo origen"),
    destino: int = Query(..., description="ID del nodo destino"),
    algoritmo: str = Query("dijkstra", description="Algoritmo a utilizar: bfs, dfs, topological, dijkstra, floyd_warshall"),
    id_pedido: int = Query(None, description="ID del pedido (opcional)")
):
    """
    Calcula la ruta entre dos nodos usando el algoritmo seleccionado.
    Si se especifica id_pedido, calcula la ruta para ese pedido.
    Retorna el camino, el costo y el tiempo de cálculo.
    """
    t0 = time.time()
    try:
        if id_pedido is not None:
            ruta = SimulacionAplicacionService.calcular_ruta_pedido(id_pedido, algoritmo)
        else:
            ruta = SimulacionAplicacionService.calcular_camino_entre_nodos(origen, destino, algoritmo)
        t1 = time.time()
        if ruta is None:
            raise HTTPException(status_code=404, detail="No existe una ruta posible entre los nodos seleccionados")
        if isinstance(ruta, dict):
            ruta['tiempo_respuesta'] = round(t1-t0, 4)
            return ruta
        # Si es DTO, convertir a dict y agregar tiempo
        data = ruta.model_dump() if hasattr(ruta, 'model_dump') else dict(ruta)
        data['tiempo_respuesta'] = round(t1-t0, 4)
        return data
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException, Query, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from typing import List
import time

def get_simulacion_service():
    return SimulacionAplicacionService

router = APIRouter(prefix="/rutas", tags=["Rutas"])

@router.get("/camino", response_model=RespuestaRuta)
def calcular_camino(
    origen: int = Query(..., description="ID del vertice origen"),
    destino: int = Query(..., description="ID del vertice destino"),
    algoritmo: str = Query("dijkstra", description="Algoritmo a utilizar: bfs, dfs, topological, dijkstra, floyd_warshall"),
    id_pedido: int = Query(None, description="ID del pedido (opcional)"),
    service=Depends(get_simulacion_service)
):
    """
    Calcula la ruta entre dos vertices usando el algoritmo seleccionado.
    Si se especifica id_pedido, calcula la ruta para ese pedido.
    Retorna el camino, el costo y el tiempo de cálculo.
    """
    t0 = time.time()
    try:
        if id_pedido is not None:
            ruta = service.calcular_ruta_pedido(id_pedido, algoritmo)
        else:
            ruta = service.calcular_camino_entre_vertices(origen, destino, algoritmo)
        t1 = time.time()
        if ruta is None:
            raise HTTPException(status_code=404, detail="No existe una ruta posible entre los vertices seleccionados")
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

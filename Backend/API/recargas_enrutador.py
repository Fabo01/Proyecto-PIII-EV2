from fastapi import APIRouter, HTTPException, Depends
from typing import List
from Backend.API.DTOs.DTOsRespuesta.RespuestaRecarga import RespuestaRecarga
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.Mapeadores.MapeadorRecarga import MapeadorRecarga

router = APIRouter(prefix="/recargas", tags=["Recargas"])

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.get("/", response_model=List[RespuestaRecarga])
def listar_recargas(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de recargas registradas en la simulación.
    """
    recargas = service.obtener_recargas()
    if recargas is None:
        raise HTTPException(status_code=404, detail="No hay recargas registradas")
    return MapeadorRecarga.lista_a_dto(recargas)

@router.get("/hashmap", response_model=dict)
def recargas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de recargas (ID → Objeto Recarga serializable plano).
    """
    recargas = service.obtener_recargas()
    return {r.id_recarga: MapeadorRecarga.a_hashmap(r) for r in recargas}

@router.get("/hashmap/lista", response_model=List[dict])
def recargas_hashmap_lista(service=Depends(get_simulacion_service)):
    """
    Devuelve una lista de objetos de recarga en formato hashmap para depuración avanzada.
    """
    recargas = service.obtener_recargas()
    return MapeadorRecarga.lista_a_hashmap(recargas)

@router.get("/{id}", response_model=RespuestaRecarga)
def obtener_recarga(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una estación de recarga por su id, usando el servicio y mapeador.
    """
    recarga = service.obtener_recarga(id)
    if recarga is None:
        raise HTTPException(status_code=404, detail="Recarga no encontrada")
    return MapeadorRecarga.a_dto(recarga)

@router.get("/{id}/hashmap", response_model=dict)
def obtener_recarga_hashmap(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una estación de recarga por su id en formato hashmap, para obtener
    todos sus atributos de forma plana.
    """
    recarga = service.obtener_recarga(id)
    if recarga is None:
        raise HTTPException(status_code=404, detail="Recarga no encontrada")
    return MapeadorRecarga.a_hashmap(recarga)

@router.post("/crear", response_model=RespuestaRecarga)
def crear_recarga(dto: dict, service=Depends(get_simulacion_service)):
    """
    Crea una nueva estación de recarga a partir de los datos recibidos.
    """
    try:
        recarga = service.crear_recarga(dto)
        return MapeadorRecarga.a_dto(recarga)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear recarga: {str(e)}")

@router.patch("/{id}", response_model=RespuestaRecarga)
def actualizar_recarga(id: int, dto: dict, service=Depends(get_simulacion_service)):
    """
    Actualiza los datos de una estación de recarga existente.
    """
    try:
        recarga = service.actualizar_recarga(id, dto)
        return MapeadorRecarga.a_dto(recarga)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar recarga: {str(e)}")

@router.delete("/{id}", response_model=dict)
def eliminar_recarga(id: int, service=Depends(get_simulacion_service)):
    """
    Elimina una estación de recarga por su id.
    """
    try:
        service.eliminar_recarga(id)
        return {"mensaje": "Recarga eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar recarga: {str(e)}")



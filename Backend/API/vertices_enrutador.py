from fastapi import APIRouter, HTTPException, Depends
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.API.DTOs.DTOsRespuesta.RespuestaVertice import RespuestaVertice
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.Infraestructura.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.Infraestructura.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.Infraestructura.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.Infraestructura.Mapeadores.MapeadorVertice import MapeadorVertice
from typing import List
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService

router = APIRouter(prefix="/vertices", tags=["Vertices"])

def get_simulacion_service():
    return SimulacionAplicacionService


@router.get("/", response_model=List[RespuestaVertice])
def listar_vertices():
    """
    Devuelve todos los vertices (clientes, almacenamientos, recargas) de la red como objetos RespuestaVertice.
    """
    vertices = RepositorioVertices().todos()
    if not vertices:
        raise HTTPException(status_code=404, detail="No hay vertices registrados")
    try:
        vertices = []
        for v in vertices:
            elem = v.elemento() if hasattr(v, 'elemento') else v
            tipo = getattr(elem, 'tipo_elemento', '')
            if tipo == 'cliente':
                vertices.append(MapeadorCliente.a_dto(elem, incluir_pedidos=False))
            elif tipo == 'almacenamiento':
                vertices.append(MapeadorAlmacenamiento.a_dto(elem, incluir_pedidos=False))
            elif tipo == 'recarga':
                vertices.append(MapeadorRecarga.a_dto(elem))
            else:
                vertices.append(RespuestaVertice(id=getattr(elem, 'id', 0), tipo=tipo, nombre=getattr(elem, 'nombre', '')))
        return vertices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_vertices_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de vértices (ID → Objeto Vertice serializable).
    """
    hashmap = service.obtener_vertices_hashmap()
    from Backend.Infraestructura.Mapeadores.MapeadorVertice import MapeadorVertice
    hashmap_dto = {str(k): MapeadorVertice.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)

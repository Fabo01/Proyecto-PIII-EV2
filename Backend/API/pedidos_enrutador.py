from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
from typing import List

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.get("/", response_model=List[RespuestaPedido])
def listar_pedidos(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de pedidos registrados en la simulación.
    """
    pedidos = service.obtener_pedidos()
    if pedidos is None:
        raise HTTPException(status_code=404, detail="No hay pedidos registrados")
    return [MapeadorPedido.a_dto(p) for p in pedidos]

@router.get("/hashmap", response_model=RespuestaHashMap)
def pedidos_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de pedidos (ID → Objeto Pedido serializable).
    """
    hashmap = service.obtener_pedidos_hashmap()
    if hashmap is None:
        raise HTTPException(status_code=404, detail="No hay pedidos en el sistema")
    hashmap_dto = {str(k): MapeadorPedido.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)

@router.get("/{id}", response_model=RespuestaPedido)
def obtener_pedido(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un pedido por su id.
    """
    pedido = service.buscar_pedido(id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return MapeadorPedido.a_dto(pedido)

@router.post("/crear", response_model=RespuestaPedido)
def crear_pedido(dto: dict, service=Depends(get_simulacion_service)):
    """
    Crea un nuevo pedido a partir de los datos recibidos.
    """
    try:
        pedido = service.crear_pedido(dto)
        return MapeadorPedido.a_dto(pedido)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear pedido: {str(e)}")

@router.post("/{id}/ruta", response_model=RespuestaRuta)
def calcular_ruta_pedido(id: int, service=Depends(get_simulacion_service)):
    """
    Calcula la ruta óptima para el pedido indicado.
    """
    ruta = service.calcular_ruta_pedido(id)
    if ruta is None:
        raise HTTPException(status_code=404, detail="No se pudo calcular la ruta para el pedido")
    return MapeadorRuta.a_dto(ruta)

@router.patch("/{id}/estado", response_model=RespuestaPedido)
def actualizar_estado_pedido(id: int, nuevo_estado: str, service=Depends(get_simulacion_service)):
    """
    Actualiza el estado de un pedido (pendiente, en_ruta, entregado, etc).
    """
    try:
        pedido = service.actualizar_estado_pedido(id, nuevo_estado)
        return MapeadorPedido.a_dto(pedido)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar estado: {str(e)}")

@router.delete("/{id}", response_model=dict)
def eliminar_pedido(id: int, service=Depends(get_simulacion_service)):
    """
    Elimina un pedido por su id.
    """
    try:
        service.eliminar_pedido(id)
        return {"mensaje": "Pedido eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar pedido: {str(e)}")

@router.get("/por_cliente/{id_cliente}", response_model=List[RespuestaPedido])
def pedidos_por_cliente(id_cliente: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos asociados a un cliente específico.
    """
    pedidos = service.obtener_pedidos_por_cliente(id_cliente)
    if pedidos is None:
        raise HTTPException(status_code=404, detail="No hay pedidos para el cliente especificado")
    return [MapeadorPedido.a_dto(p) for p in pedidos]

@router.get("/en_almacen/{id_almacen}", response_model=List[RespuestaPedido])
def pedidos_en_almacen(id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos en un almacenamiento específico.
    """
    pedidos = service.obtener_pedidos_en_almacen(id_almacen)
    if pedidos is None:
        raise HTTPException(status_code=404, detail="No hay pedidos en el almacenamiento especificado")
    return [MapeadorPedido.a_dto(p) for p in pedidos]



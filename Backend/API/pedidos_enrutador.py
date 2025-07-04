from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
from typing import List
import logging

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
    return MapeadorPedido.lista_a_dto(pedidos)

@router.get("/hashmap", response_model=dict)
def pedidos_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de pedidos (objetos reales para debug).
    """
    try:
        from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
        repo = RepositorioPedidos()
        return {"pedidos": repo.obtener_hashmap()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo hashmap de pedidos: {str(e)}")

@router.get("/{id}", response_model=RespuestaPedido)
def obtener_pedido(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un pedido por su id (DTO plano).
    """
    pedido = service.obtener_pedido(id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return MapeadorPedido.a_dto(pedido)

@router.get("/hashmap/{id}", response_model=dict)
def obtener_pedido_hashmap(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un pedido por su id (objeto real para debug).
    """
    pedido = service.obtener_pedido(id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"pedido": MapeadorPedido.a_hashmap(pedido)}

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
    pedidos = service.obtener_por_cliente(id_cliente)
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



from fastapi import APIRouter, HTTPException, Depends
from typing import List
from Backend.API.DTOs.DTOsRespuesta.RespuestaCliente import RespuestaCliente
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_simulacion_service():
    return SimulacionAplicacionService

@router.get("/", response_model=List[RespuestaCliente])
def listar_clientes(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de clientes registrados en la simulación.
    """
    clientes = service.listar_clientes()
    if clientes is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not clientes:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    try:
        return [MapeadorCliente.a_dto(c) for c in clientes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/{id}", response_model=RespuestaCliente)
def obtener_cliente(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un cliente por su id, usando el servicio y mapeador.
    """
    try:
        cliente = service.obtener_cliente(id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return MapeadorCliente.a_dto(cliente)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cliente no encontrado: {str(e)}")

@router.get("/con_pedidos/{id_almacen}", response_model=List[RespuestaCliente])
def clientes_con_pedidos_en_almacen(id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los clientes que tienen al menos un pedido cuyo almacenamiento de origen es el dado.
    """
    clientes = service.listar_clientes()
    pedidos = service.listar_pedidos()
    clientes_filtrados = []
    for cliente in clientes:
        tiene_pedido = any(
            getattr(p, 'id_almacenamiento', None) == id_almacen and getattr(p, 'id_cliente', None) == getattr(cliente, 'id_cliente', None)
            for p in pedidos
        )
        if tiene_pedido:
            clientes_filtrados.append(cliente)
    try:
        return [MapeadorCliente.a_dto(c) for c in clientes_filtrados]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/{id_cliente}/pedidos_en_almacen/{id_almacen}", response_model=List[RespuestaPedido])
def pedidos_cliente_en_almacen(id_cliente: int, id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos de un cliente en un almacenamiento específico.
    """
    pedidos = service.listar_pedidos()
    pedidos_filtrados = [p for p in pedidos if getattr(p, 'id_cliente', None) == id_cliente and getattr(p, 'id_almacenamiento', None) == id_almacen]
    try:
        return [MapeadorPedido.a_dto(p) for p in pedidos_filtrados]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_clientes_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de clientes (ID → Objeto Cliente serializable).
    """
    hashmap = service.obtener_clientes_hashmap()
    hashmap_dto = {str(k): MapeadorCliente.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)

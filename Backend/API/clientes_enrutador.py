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
    return SimulacionAplicacionService()

@router.get("/", response_model=List[RespuestaCliente])
def listar_clientes(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de clientes registrados en la simulación.
    """
    clientes = service.obtener_clientes()
    if clientes is None:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    return MapeadorCliente.lista_a_dto(clientes)

@router.get("/hashmap", response_model=dict)
def clientes_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de clientes (ID → Objeto Cliente serializable plano).
    """
    clientes = service.obtener_clientes()
    # Devuelve objetos reales para debug avanzado
    return {c.id_cliente: MapeadorCliente.a_hashmap(c) for c in clientes}

@router.get("/hashmap/lista", response_model=List[dict])
def clientes_hashmap_lista(service=Depends(get_simulacion_service)):
    """
    Devuelve una lista de hashes de clientes para debug avanzado.
    """
    clientes = service.obtener_clientes()
    return MapeadorCliente.lista_a_hashmap(clientes)

@router.get("/{id}", response_model=RespuestaCliente)
def obtener_cliente(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un cliente por su id, usando el servicio y mapeador.
    """
    cliente = service.obtener_cliente(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return MapeadorCliente.a_dto(cliente)

@router.get("/{id}/hashmap", response_model=dict)
def obtener_cliente_hashmap(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un cliente por su id como un objeto hash para debug avanzado.
    """
    cliente = service.obtener_cliente(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return MapeadorCliente.a_hashmap(cliente)

@router.get("/con_pedidos/{id_almacen}", response_model=List[RespuestaCliente])
def clientes_con_pedidos_en_almacen(id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los clientes que tienen al menos un pedido cuyo almacenamiento de origen es el dado.
    """
    clientes = service.clientes_con_pedidos_en_almacen(id_almacen)
    return [MapeadorCliente.a_dto(c) for c in clientes]

@router.get("/{id_cliente}/pedidos", response_model=List[RespuestaPedido])
def pedidos_por_cliente(id_cliente: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos asociados a un cliente específico.
    """
    pedidos = service.obtener_por_cliente(id_cliente)
    if pedidos is None:
        return []
    return [MapeadorPedido.a_dto(p) for p in pedidos]

@router.get("/{id_cliente}/pedidos_en_almacen/{id_almacen}", response_model=List[RespuestaPedido])
def pedidos_cliente_en_almacen(id_cliente: int, id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos de un cliente en un almacenamiento específico.
    """
    pedidos = service.pedidos_cliente_en_almacen(id_cliente, id_almacen)
    return [MapeadorPedido.a_dto(p) for p in pedidos]

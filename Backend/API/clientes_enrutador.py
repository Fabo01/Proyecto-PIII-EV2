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
    return [MapeadorCliente.a_dto(c) for c in clientes]

@router.get("/hashmap", response_model=RespuestaHashMap)
def clientes_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de clientes (ID → Objeto Cliente serializable).
    """
    hashmap = service.obtener_clientes_hashmap()
    if hashmap is None:
        raise HTTPException(status_code=404, detail="No hay clientes en el sistema")
    return RespuestaHashMap(hashmap=hashmap)

@router.get("/{id}", response_model=RespuestaCliente)
def obtener_cliente(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un cliente por su id, usando el servicio y mapeador.
    """
    cliente = service.buscar_cliente(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return MapeadorCliente.a_dto(cliente)

@router.post("/crear", response_model=RespuestaCliente)
def crear_cliente(dto: dict, service=Depends(get_simulacion_service)):
    """
    Crea un nuevo cliente a partir de los datos recibidos.
    """
    try:
        cliente = service.crear_cliente(dto)
        return MapeadorCliente.a_dto(cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear cliente: {str(e)}")

@router.patch("/{id}", response_model=RespuestaCliente)
def actualizar_cliente(id: int, dto: dict, service=Depends(get_simulacion_service)):
    """
    Actualiza los datos de un cliente existente.
    """
    try:
        cliente = service.actualizar_cliente(id, dto)
        return MapeadorCliente.a_dto(cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar cliente: {str(e)}")

@router.delete("/{id}", response_model=dict)
def eliminar_cliente(id: int, service=Depends(get_simulacion_service)):
    """
    Elimina un cliente por su id.
    """
    try:
        service.eliminar_cliente(id)
        return {"mensaje": "Cliente eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar cliente: {str(e)}")

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
    pedidos = service.obtener_pedidos_por_cliente(id_cliente)
    if pedidos is None:
        raise HTTPException(status_code=404, detail="No hay pedidos para el cliente especificado")
    return [MapeadorPedido.a_dto(p) for p in pedidos]

@router.get("/{id_cliente}/pedidos_en_almacen/{id_almacen}", response_model=List[RespuestaPedido])
def pedidos_cliente_en_almacen(id_cliente: int, id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos de un cliente en un almacenamiento específico.
    """
    pedidos = service.pedidos_cliente_en_almacen(id_cliente, id_almacen)
    return [MapeadorPedido.a_dto(p) for p in pedidos]

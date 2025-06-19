from fastapi import APIRouter, HTTPException
from typing import List

from Backend.API.DTOs.Dtos1 import ClienteResponse
from Backend.API.DTOs.Dtos1 import PedidoResponse
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes():
    clientes = SimulacionAplicacionService.listar_clientes()
    if clientes is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not clientes:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    return clientes

@router.get("/{id}", response_model=ClienteResponse)
def obtener_cliente(id: int):
    try:
        cliente = SimulacionAplicacionService.obtener_cliente(id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente
    except Exception:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.get("/con_pedidos/{id_almacen}", response_model=List[ClienteResponse])
def clientes_con_pedidos_en_almacen(id_almacen: int):
    """
    Devuelve los clientes que tienen al menos un pedido cuyo almacenamiento de origen es el dado.
    La consulta se realiza sobre la fuente de verdad de pedidos de la simulación, siguiendo separación de responsabilidades.
    """
    clientes = SimulacionAplicacionService.listar_clientes()
    pedidos = SimulacionAplicacionService.listar_pedidos()
    clientes_filtrados = []
    for cliente in clientes:
        # Buscar si el cliente tiene al menos un pedido con el almacenamiento como origen
        tiene_pedido = any(
            (getattr(p, 'origen', None) == id_almacen or getattr(p, 'id_almacenamiento', None) == id_almacen)
            and (getattr(p, 'destino', None) == getattr(cliente, 'id', None) or getattr(p, 'id_cliente', None) == getattr(cliente, 'id', None))
            for p in pedidos
        )
        if tiene_pedido:
            clientes_filtrados.append(cliente)
    # No lanzar error, devolver lista vacía si no hay clientes con pedidos en este almacén
    return clientes_filtrados

@router.get("/{id_cliente}/pedidos_en_almacen/{id_almacen}", response_model=List[PedidoResponse])
def pedidos_cliente_en_almacen(id_cliente: int, id_almacen: int):
    """
    Devuelve los pedidos de un cliente asociados a un almacenamiento específico.
    """
    cliente = SimulacionAplicacionService.obtener_cliente(id_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    pedidos = getattr(cliente, 'obtener_pedidos', lambda: [])()
    pedidos_filtrados = [p for p in pedidos if getattr(p, 'id_almacenamiento', None) == id_almacen or getattr(p, 'origen', None) == id_almacen]
    # No lanzar error, devolver lista vacía si no hay pedidos
    return pedidos_filtrados

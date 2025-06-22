"""
ObserverPedidos: Observador para eventos relacionados con pedidos en la simulacion logistica de drones.
Audita y reacciona ante creacion, actualizacion y entrega de pedidos.
"""
from Backend.Dominio.Interfaces.IntObs.IObserver import IObserver
import logging

class ObserverPedidos(IObserver):
    def __init__(self):
        self.logger = logging.getLogger("ObserverPedidos")

    def actualizar(self, evento, sujeto=None, datos=None):
        """
        Maneja los eventos relevantes de pedidos.
        :param evento: Nombre del evento.
        :param sujeto: Objeto que notifica (opcional).
        :param datos: Datos asociados al evento.
        """
        if evento == "simulacion_iniciada":
            self.logger.info(f"[Pedidos] Simulacion iniciada. Total pedidos: {len(datos.get('pedidos', [])) if datos else 0}")
        elif evento == "calculo_ruta":
            pedido_id = datos.get("pedido") if datos else None
            self.logger.info(f"[Pedidos] Ruta calculada para pedido {pedido_id}.")
        elif evento == "entrega_pedido":
            pedido_id = datos.get("pedido") if datos else None
            self.logger.info(f"[Pedidos] Pedido entregado: {pedido_id}.")
        elif evento == "simulacion_reiniciada":
            self.logger.info("[Pedidos] Simulacion reiniciada. Todos los pedidos han sido limpiados.")
        elif evento == "nuevo_pedido":
            pedido_id = datos.get("pedido") if datos else None
            self.logger.info(f"[Pedidos] Nuevo pedido creado: {pedido_id}.")
        elif evento == "actualizacion_pedido":
            pedido_id = datos.get("pedido") if datos else None
            estado = datos.get("estado") if datos else None
            self.logger.info(f"[Pedidos] Pedido {pedido_id} actualizado a estado: {estado}.")
        else:
            self.logger.debug(f"[Pedidos] Evento no manejado: {evento} | Datos: {datos}")

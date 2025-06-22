"""
ObserverEstadisticas: Observador para eventos de estadisticas en la simulacion logistica de drones.
Audita y actualiza estadisticas clave de la simulacion en tiempo real.
"""
from Backend.Dominio.Interfaces.IntObs.IObserver import IObserver
import logging
import os

class ObserverEstadisticas(IObserver):
    def __init__(self, servicio_estadisticas=None):
        self.logger = logging.getLogger("ObserverEstadisticas")
        self.servicio_estadisticas = servicio_estadisticas  # Puede ser None o un servicio real

    def actualizar(self, evento, sujeto=None, datos=None):
        """
        Maneja los eventos relevantes para estadisticas.
        :param evento: Nombre del evento.
        :param sujeto: Objeto que notifica (opcional).
        :param datos: Datos asociados al evento.
        """
        if evento == "simulacion_iniciada":
            total_vertices = len(datos.get('vertices', [])) if datos else 0
            total_aristas = len(datos.get('aristas', [])) if datos else 0
            total_pedidos = len(datos.get('pedidos', [])) if datos else 0
            self.logger.info(f"[Estadisticas] Simulacion iniciada. Vertices: {total_vertices}, Aristas: {total_aristas}, Pedidos: {total_pedidos}")
            if self.servicio_estadisticas:
                self.servicio_estadisticas.registrar_inicio(total_vertices, total_aristas, total_pedidos)
        elif evento == "entrega_pedido":
            pedido_id = datos.get("pedido") if datos else None
            self.logger.info(f"[Estadisticas] Pedido entregado: {pedido_id}.")
            if self.servicio_estadisticas:
                self.servicio_estadisticas.registrar_entrega(pedido_id)
        elif evento == "calculo_ruta":
            pedido_id = datos.get("pedido") if datos else None
            costo = datos.get("costo") if datos else None
            self.logger.info(f"[Estadisticas] Ruta calculada para pedido {pedido_id} con costo {costo}.")
            if self.servicio_estadisticas:
                self.servicio_estadisticas.registrar_ruta(pedido_id, costo)
        elif evento == "simulacion_reiniciada":
            self.logger.info("[Estadisticas] Simulacion reiniciada. Estadisticas reseteadas.")
            if self.servicio_estadisticas:
                self.servicio_estadisticas.reiniciar()
        else:
            self.logger.debug(f"[Estadisticas] Evento no manejado: {evento} | Datos: {datos}")

# Configuración global de logging para la simulación
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
log_file = os.path.join(log_dir, 'simulacion.log')
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
else:
    # Si ya hay handlers, asegurarse de que el archivo esté incluido
    root_logger = logging.getLogger()
    file_handler_exists = any(isinstance(h, logging.FileHandler) and h.baseFilename == log_file for h in root_logger.handlers)
    if not file_handler_exists:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s'))
        root_logger.addHandler(file_handler)

"""
FabricaPedidos: Fábrica centralizada para la creación y validación de pedidos en la simulación logística de drones.
Cumple SOLID, patrones de diseño y requisitos del proyecto.
"""
from Backend.Dominio.Dominio_Pedido import Pedido
from datetime import datetime
import logging

class FabricaPedidos:
    def __init__(self):
        self.errores = []  # Lista de errores de creación para auditoría
        self.logger = logging.getLogger("FabricaPedidos")
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def crear_pedido(self, id_pedido, vertice_cliente, vertice_almacen, prioridad, fecha_creacion=None):
        self.logger.info(f"Intentando crear pedido {id_pedido}:")
        self.logger.info(f"  vertice_cliente: {vertice_cliente}")
        self.logger.info(f"  vertice_cliente.elemento: {getattr(vertice_cliente, 'elemento', lambda: None)() if vertice_cliente else None}")
        self.logger.info(f"  vertice_almacen: {vertice_almacen}")
        self.logger.info(f"  vertice_almacen.elemento: {getattr(vertice_almacen, 'elemento', lambda: None)() if vertice_almacen else None}")
        self.logger.info(f"  prioridad: {prioridad}")
        self.logger.info(f"  fecha_creacion: {fecha_creacion}")
        # Validación robusta
        if vertice_cliente is None or not hasattr(vertice_cliente, 'elemento') or getattr(vertice_cliente.elemento(), 'tipo_elemento', None) != 'cliente':
            self.logger.warning(f"Pedido {id_pedido}: vertice_cliente inválido -> {vertice_cliente}")
            self.errores.append({
                'id_pedido': id_pedido,
                'error': 'Vertice cliente inválido',
                'cliente': vertice_cliente,
                'almacen': vertice_almacen,
                'fecha': fecha_creacion,
                'prioridad': prioridad
            })
            return None
        if vertice_almacen is None or not hasattr(vertice_almacen, 'elemento') or getattr(vertice_almacen.elemento(), 'tipo_elemento', None) != 'almacenamiento':
            self.logger.warning(f"Pedido {id_pedido}: vertice_almacen inválido -> {vertice_almacen}")
            self.errores.append({
                'id_pedido': id_pedido,
                'error': 'Vertice almacen inválido',
                'cliente': vertice_cliente,
                'almacen': vertice_almacen,
                'fecha': fecha_creacion,
                'prioridad': prioridad
            })
            return None
        if fecha_creacion is not None and not isinstance(fecha_creacion, datetime):
            self.logger.warning(f"Pedido {id_pedido}: fecha_creacion inválida -> {fecha_creacion}")
            self.errores.append({
                'id_pedido': id_pedido,
                'error': 'Fecha de creación inválida',
                'cliente': vertice_cliente,
                'almacen': vertice_almacen,
                'fecha': fecha_creacion,
                'prioridad': prioridad
            })
            return None
        try:
            pedido = Pedido(
                id_pedido=id_pedido,
                cliente_v=vertice_cliente,
                origen_v=vertice_almacen,
                destino_v=vertice_cliente,
                prioridad=prioridad,
                fecha_creacion=fecha_creacion or datetime.now()
            )
            self.logger.info(f"Pedido {id_pedido} creado correctamente: {pedido}")
            self.logger.info(f"  Pedido.origen: {pedido.origen}, Pedido.destino: {pedido.destino}, Pedido.fecha_creacion: {pedido.fecha_creacion}")
            return pedido
        except Exception as e:
            self.logger.error(f"Excepción al crear pedido {id_pedido}: {e}")
            self.errores.append({
                'id_pedido': id_pedido,
                'error': f'Excepción al crear pedido: {e}',
                'cliente': vertice_cliente,
                'almacen': vertice_almacen,
                'fecha': fecha_creacion,
                'prioridad': prioridad
            })
            return None

    def obtener_errores(self):
        return self.errores

    # Métodos protegidos para extensión de reglas de validación
    def _validar_regla_personalizada(self, *args, **kwargs):
        pass

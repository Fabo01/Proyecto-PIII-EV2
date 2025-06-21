"""
Clase Pedido para representar un pedido en la simulación logística de drones.
"""

from datetime import datetime
import logging

class Pedido:
    """
    Representa un pedido realizado por un cliente.
    La gestión de pedidos es independiente de la lógica de Cliente y Vertice.
    Almacena referencias a los vértices del grafo (no a los elementos).
    Puede ser usado como DTO para transferir datos entre capas.
    Requisitos de atributos:
    - origen: Debe ser un vértice válido de tipo almacenamiento.
    - destino: Debe ser un vértice válido de tipo cliente.
    - fecha_creacion: Debe ser datetime válido.
    Si algún atributo es inválido, se lanza una excepción.
    """
    def __init__(self, id_pedido, cliente_v, origen_v, destino_v, prioridad, fecha_creacion=None):
        logger = logging.getLogger("Pedido")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[Pedido.__init__] Creando pedido {id_pedido}:")
        logger.info(f"  cliente_v: {cliente_v}")
        logger.info(f"  cliente_v.elemento: {getattr(cliente_v, 'elemento', lambda: None)() if cliente_v else None}")
        logger.info(f"  origen_v: {origen_v}")
        logger.info(f"  origen_v.elemento: {getattr(origen_v, 'elemento', lambda: None)() if origen_v else None}")
        logger.info(f"  destino_v: {destino_v}")
        logger.info(f"  destino_v.elemento: {getattr(destino_v, 'elemento', lambda: None)() if destino_v else None}")
        logger.info(f"  prioridad: {prioridad}")
        logger.info(f"  fecha_creacion: {fecha_creacion}")
        if origen_v is None or not hasattr(origen_v, 'elemento') or getattr(origen_v.elemento(), 'tipo_elemento', None) != 'almacenamiento':
            logger.warning(f"[Pedido.__init__] Origen inválido para pedido {id_pedido}: {origen_v}")
            raise ValueError("El vértice de origen debe ser un almacenamiento válido.")
        if destino_v is None or not hasattr(destino_v, 'elemento') or getattr(destino_v.elemento(), 'tipo_elemento', None) != 'cliente':
            logger.warning(f"[Pedido.__init__] Destino inválido para pedido {id_pedido}: {destino_v}")
            raise ValueError("El vértice de destino debe ser un cliente válido.")
        if fecha_creacion is not None and not isinstance(fecha_creacion, datetime):
            logger.warning(f"[Pedido.__init__] Fecha de creación inválida para pedido {id_pedido}: {fecha_creacion}")
            raise ValueError("La fecha de creación debe ser un objeto datetime válido.")
        self.id_pedido = id_pedido
        self.cliente = cliente_v  # Vértice del grafo (cliente)
        self.origen = origen_v    # Vértice del grafo (almacenamiento)
        self.destino = destino_v  # Vértice del grafo (cliente)
        self.prioridad = prioridad
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.ruta = None
        self.peso_total = None
        self.status = 'pendiente'
        self.fecha_entrega = None
        logger.info(f"[Pedido.__init__] Pedido {id_pedido} creado con self.origen: {self.origen}, self.destino: {self.destino}, self.fecha_creacion: {self.fecha_creacion}")

    def obtener_cliente(self):
        """
        Retorna el objeto cliente asociado a este pedido a través del vértice.
        """
        logger = logging.getLogger("Pedido")
        cliente = self.cliente.elemento() if self.cliente and hasattr(self.cliente, 'elemento') else None
        logger.info(f"[Pedido.obtener_cliente] Pedido {self.id_pedido} retorna cliente: {cliente}")
        return cliente

    def obtener_origen(self):
        """
        Retorna el vértice de origen (almacenamiento) asociado a este pedido.
        Siempre retorna la referencia única del objeto Vertice.
        """
        logger = logging.getLogger("Pedido")
        origen = self.origen.elemento() if self.origen and hasattr(self.origen, 'elemento') else None
        logger.info(f"[Pedido.obtener_origen] Pedido {self.id_pedido} retorna origen: {origen}")
        return self.origen

    def obtener_destino(self):
        """
        Retorna el vértice de destino (cliente) asociado a este pedido.
        Siempre retorna la referencia única del objeto Vertice.
        """
        logger = logging.getLogger("Pedido")
        destino = self.destino.elemento() if self.destino and hasattr(self.destino, 'elemento') else None
        logger.info(f"[Pedido.obtener_destino] Pedido {self.id_pedido} retorna destino: {destino}")
        return self.destino

    def asignar_ruta(self, ruta, peso_total):
        logger = logging.getLogger("Pedido")
        logger.info(f"[Pedido.asignar_ruta] Pedido {self.id_pedido} asignando ruta: {ruta}, peso_total: {peso_total}")
        self.ruta = ruta
        self.peso_total = peso_total
        self.status = 'enviado'
        logger.info(f"[Pedido.asignar_ruta] Pedido {self.id_pedido} status actualizado a: {self.status}")

    def marcar_entregado(self):
        logger = logging.getLogger("Pedido")
        logger.info(f"[Pedido.marcar_entregado] Pedido {self.id_pedido} marcado como entregado.")
        self.status = 'entregado'
        self.fecha_entrega = datetime.now()
        logger.info(f"[Pedido.marcar_entregado] Pedido {self.id_pedido} fecha_entrega: {self.fecha_entrega}")

    def es_pendiente(self):
        logger = logging.getLogger("Pedido")
        logger.info(f"[Pedido.es_pendiente] Pedido {self.id_pedido} status: {self.status}")
        return self.status == 'pendiente'

    def es_enviado(self):
        logger = logging.getLogger("Pedido")
        logger.info(f"[Pedido.es_enviado] Pedido {self.id_pedido} status: {self.status}")
        return self.status == 'enviado'

    def es_entregado(self):
        logger = logging.getLogger("Pedido")
        logger.info(f"[Pedido.es_entregado] Pedido {self.id_pedido} status: {self.status}")
        return self.status == 'entregado'

    def validar_origen_destino(self, origen, destino):
        logger = logging.getLogger("Pedido")
        logger.info(f"[Pedido.validar_origen_destino] Pedido {self.id_pedido} origen: {origen}, destino: {destino}")
        resultado = (self.origen is origen and self.destino is destino) or \
               (getattr(self.origen.elemento(), 'id_almacenamiento', None) == getattr(origen.elemento(), 'id_almacenamiento', None) and
                getattr(self.destino.elemento(), 'id_cliente', None) == getattr(destino.elemento(), 'id_cliente', None))
        logger.info(f"[Pedido.validar_origen_destino] Pedido {self.id_pedido} resultado: {resultado}")
        return resultado

    def __str__(self):
        logger = logging.getLogger("Pedido")
        cliente_nombre = self.obtener_cliente().nombre if self.obtener_cliente() else 'N/A'
        logger.info(f"[Pedido.__str__] Pedido {self.id_pedido} - Cliente: {cliente_nombre} - Estado: {self.status}")
        return f"Pedido {self.id_pedido} - Cliente: {cliente_nombre} - Estado: {self.status}"

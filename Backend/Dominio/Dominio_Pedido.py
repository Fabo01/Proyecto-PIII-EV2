"""
Clase Pedido para representar un pedido en la simulacion logistica de drones.
Incluye soporte para observadores de eventos de dominio.
"""

from datetime import datetime

class Pedido:
    """
    Representa un pedido realizado por un cliente.
    La gestion de pedidos es independiente de la logica de Cliente y Vertice.
    Permite agregar observadores para auditar eventos de negocio.
    """
    def __init__(self, id_pedido, cliente_v, origen_v, destino_v, prioridad, fecha_creacion=None):
        self.id_pedido = id_pedido
        self.cliente = cliente_v
        self.origen = origen_v
        self.destino = destino_v
        self.prioridad = prioridad
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.ruta = None
        self.peso_total = None
        self.status = 'pendiente'
        self.fecha_entrega = None
        self._observadores = set()
        self.notificar_observadores('pedido_creado', {'id_pedido': id_pedido, 'cliente': cliente_v, 'origen': origen_v, 'destino': destino_v, 'prioridad': prioridad, 'fecha_creacion': self.fecha_creacion})

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def obtener_cliente(self):
        """
        Retorna el cliente asociado a este pedido.
        """
        return self.cliente.elemento if self.cliente and hasattr(self.cliente, 'elemento') else None

    def obtener_origen(self):
        """
        Retorna el vertice de origen (almacenamiento) asociado a este pedido.
        Siempre retorna la referencia única del objeto Vertice.
        """
        return self.origen.elemento if self.origen and hasattr(self.origen, 'elemento') else None

    def obtener_destino(self):
        """
        Retorna el vertice de destino (cliente) asociado a este pedido.
        Siempre retorna la referencia única del objeto Vertice.
        """
        return self.destino.elemento if self.destino and hasattr(self.destino, 'elemento') else None

    def asignar_ruta(self, ruta, peso_total):
        self.ruta = ruta
        self.peso_total = peso_total
        self.status = 'enviado'
        self.notificar_observadores('pedido_ruta_asignada', {'ruta': ruta, 'peso_total': peso_total})

    def marcar_entregado(self):
        self.status = 'entregado'
        self.fecha_entrega = datetime.now()
        self.notificar_observadores('pedido_entregado', {'fecha_entrega': self.fecha_entrega})

    def es_pendiente(self):
        return self.status == 'pendiente'

    def es_enviado(self):
        return self.status == 'enviado'

    def es_entregado(self):
        return self.status == 'entregado'

    def validar_origen_destino(self, origen, destino):
        resultado = (self.origen is origen and self.destino is destino) or \
               (getattr(self.origen.elemento, 'id_almacenamiento', None) == getattr(origen.elemento, 'id_almacenamiento', None) and
                getattr(self.destino.elemento, 'id_cliente', None) == getattr(destino.elemento, 'id_cliente', None))
        return resultado

    def serializar(self):
        self.notificar_observadores('pedido_serializado', None)
        return {'id_pedido': self.id_pedido, 'cliente': str(self.cliente), 'origen': str(self.origen), 'destino': str(self.destino), 'prioridad': self.prioridad, 'status': self.status}

    def __str__(self):
        cliente_nombre = self.obtener_cliente().nombre if self.obtener_cliente() else 'N/A'
        return f"Pedido {self.id_pedido} - Cliente: {cliente_nombre} - Estado: {self.status}"

"""
Clase Almacenamiento para representar un vertice de almacenamiento en la simulación logística de drones.
Incluye soporte para observadores de eventos de dominio.
"""

class Almacenamiento:
    """
    Representa un vertice de almacenamiento. Permite asociar y consultar pedidos como objetos completos.
    Permite agregar observadores para auditar eventos de negocio.
    """
    def __init__(self, id_almacenamiento, nombre):
        """
        Inicializa un almacenamiento con su identificador y nombre. Crea la lista interna de pedidos.
        """
        self.id_almacenamiento = id_almacenamiento
        self.nombre = nombre
        self.tipo_elemento = 'almacenamiento'
        self._pedidos = []  # Lista de objetos Pedido asociados a este almacenamiento
        self._observadores = set()
        self.notificar_observadores('almacenamiento_creado', {'id_almacenamiento': id_almacenamiento, 'nombre': nombre})

    def agregar_observador(self, observador):
        """
        Agrega un observador para recibir notificaciones de eventos de negocio.
        """
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        """
        Quita un observador de la lista de receptores de notificaciones.
        """
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores registrados sobre un evento de negocio.
        """
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar_pedido(self, pedido):
        """
        Agrega un pedido (objeto completo) a la lista de pedidos del almacenamiento, validando unicidad.
        Notifica a los observadores sobre el nuevo pedido agregado.
        """
        if pedido not in self._pedidos:
            self._pedidos.append(pedido)
            self.notificar_observadores('almacenamiento_pedido_agregado', {'pedido': pedido})

    def obtener_pedidos(self):
        """
        Retorna la lista completa de pedidos asociados.
        """
        return list(self._pedidos)

    def total_pedidos(self):
        """
        Retorna la cantidad de pedidos que tiene el almacenamiento.
        """
        return len(self._pedidos)

    def limpiar_pedidos(self):
        """
        Vacia la lista interna de pedidos.
        Notifica a los observadores que los pedidos han sido limpiados.
        """
        self._pedidos.clear()
        self.notificar_observadores('almacenamiento_pedidos_limpiados', None)

    def serializar(self):
        """
        Prepara los datos del almacenamiento para ser serializados.
        Notifica a los observadores que el almacenamiento ha sido serializado.
        """
        self.notificar_observadores('almacenamiento_serializado', None)
        return {'id_almacenamiento': self.id_almacenamiento, 'nombre': self.nombre, 'total_pedidos': self.total_pedidos()}

    def __str__(self):
        return f"Almacenamiento {self.id_almacenamiento}: {self.nombre} (Pedidos: {self.total_pedidos()})"

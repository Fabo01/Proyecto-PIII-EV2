"""
Clase Cliente para representar un cliente en la simulación logística de drones.
Incluye soporte para observadores de eventos de dominio.
"""

class Cliente:
    """
    Representa un cliente con identificador, nombre y tipo_elemento. Maneja sus propios pedidos como objetos completos.
    Permite agregar observadores para auditar eventos de negocio.
    """
    def __init__(self, id_cliente, nombre):
        """
        Inicializa un cliente con su identificador y nombre. Crea la lista interna de pedidos.
        """
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.tipo_elemento = 'cliente'
        self._pedidos = []  # Lista de objetos Pedido asociados a este cliente
        self._observadores = set()
        self.notificar_observadores('cliente_creado', {'id_cliente': id_cliente, 'nombre': nombre})

    def agregar_observador(self, observador):
        """
        Agrega un observador para recibir notificaciones de eventos de negocio.
        """
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        """
        Quita un observador, dejando de notificarle sobre eventos futuros.
        """
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores registrados sobre un evento.
        """
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar_pedido(self, pedido):
        """
        Agrega un pedido a la lista interna y notifica a los observadores.
        """
        self._pedidos.append(pedido)
        self.notificar_observadores('cliente_pedido_agregado', {'pedido': pedido})

    def eliminar_pedido(self, pedido):
        """
        Elimina el pedido si existe en la lista interna.
        Notifica a los observadores sobre la eliminación del pedido.
        """
        if pedido in self._pedidos:
            self._pedidos.remove(pedido)
            self.notificar_observadores('cliente_pedido_eliminado', {'pedido': pedido})

    def limpiar_pedidos(self):
        """
        Vacia la lista de pedidos por completo.
        Notifica a los observadores que los pedidos han sido limpiados.
        """
        self._pedidos.clear()
        self.notificar_observadores('cliente_pedidos_limpiados', None)

    def obtener_pedidos(self):
        """
        Retorna la lista completa de pedidos asociados.
        """
        return list(self._pedidos)

    def total_pedidos(self):
        """
        Retorna la cantidad de pedidos que tiene el cliente.
        """
        return len(self._pedidos)

    def serializar(self):
        """
        Prepara los datos del cliente para su almacenamiento o transmisión.
        Notifica a los observadores que el cliente ha sido serializado.
        """
        self.notificar_observadores('cliente_serializado', None)
        return {'id_cliente': self.id_cliente, 'nombre': self.nombre, 'total_pedidos': self.total_pedidos()}

    def __str__(self):
        return f"Cliente {self.id_cliente}: {self.nombre} (Pedidos: {self.total_pedidos()})"

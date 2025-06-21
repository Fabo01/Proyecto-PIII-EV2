"""
Clase Cliente para representar un cliente en la simulación logística de drones.
"""

class Cliente:
    """
    Representa un cliente con identificador, nombre y tipo_elemento. Maneja sus propios pedidos como objetos completos.
    No depende de la estructura del grafo ni de la lógica de simulación.
    """
    def __init__(self, id_cliente, nombre):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.tipo_elemento = 'cliente'
        self.pedidos = []  # Lista de objetos Pedido asociados a este cliente

    def agregar_pedido(self, pedido):
        """
        Agrega un pedido (objeto completo) a la lista de pedidos del cliente.
        """
        self.pedidos.append(pedido)

    def eliminar_pedido(self, pedido):
        """
        Elimina un pedido (objeto completo) de la lista de pedidos del cliente.
        """
        if pedido in self.pedidos:
            self.pedidos.remove(pedido)

    def limpiar_pedidos(self):
        """
        Elimina todos los pedidos asociados a este cliente.
        """
        self.pedidos.clear()

    def obtener_pedidos(self):
        """
        Retorna la lista de pedidos (objetos completos) asociados a este cliente, ordenados por prioridad (de mayor a menor).
        """
        prioridad_orden = {
            'emergencia': 6,
            'muy alto': 5,
            'alto': 4,
            'medio': 3,
            'bajo': 2,
            'muy bajo': 1
        }
        return sorted(self.pedidos, key=lambda p: prioridad_orden.get(p.prioridad, 0), reverse=True)

    def total_pedidos(self):
        """
        Retorna el número total de pedidos asociados a este cliente.
        """
        return len(self.pedidos)

    def __str__(self):
        return f"Cliente {self.id_cliente}: {self.nombre}"

"""
Clase Almacenamiento para representar un nodo de almacenamiento en la simulación logística de drones.
"""

class Almacenamiento:
    """
    Representa un nodo de almacenamiento. Permite asociar y consultar pedidos.
    """
    def __init__(self, id_almacenamiento, nombre):
        self.id_almacenamiento = id_almacenamiento
        self.nombre = nombre
        self.tipo_elemento = 'almacenamiento'
        self._pedidos = []

    def agregar_pedido(self, pedido):
        self._pedidos.append(pedido)

    def obtener_pedidos(self):
        return self._pedidos

    def total_pedidos(self):
        return len(self._pedidos)

    def limpiar_pedidos(self):
        self._pedidos.clear()

    def __str__(self):
        return f"Almacenamiento {self.id_almacenamiento}: {self.nombre}"

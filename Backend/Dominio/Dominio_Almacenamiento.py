"""
Clase Almacenamiento para representar un vertice de almacenamiento en la simulación logística de drones.
"""

class Almacenamiento:
    """
    Representa un vertice de almacenamiento. Permite asociar y consultar pedidos como objetos completos.
    """
    def __init__(self, id_almacenamiento, nombre):
        self.id_almacenamiento = id_almacenamiento
        self.nombre = nombre
        self.tipo_elemento = 'almacenamiento'
        self._pedidos = []  # Lista de objetos Pedido asociados a este almacenamiento

    def agregar_pedido(self, pedido):
        """
        Agrega un pedido (objeto completo) a la lista de pedidos del almacenamiento.
        """
        self._pedidos.append(pedido)

    def obtener_pedidos(self):
        """
        Retorna la lista de pedidos (objetos completos) asociados a este almacenamiento.
        """
        return self._pedidos

    def total_pedidos(self):
        """
        Retorna el número total de pedidos asociados a este almacenamiento.
        """
        return len(self._pedidos)

    def limpiar_pedidos(self):
        """
        Elimina todos los pedidos asociados a este almacenamiento.
        """
        self._pedidos.clear()

    def __str__(self):
        return f"Almacenamiento {self.id_almacenamiento}: {self.nombre}"

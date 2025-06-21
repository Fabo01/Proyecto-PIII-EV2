"""
Clase Recarga para representar una estación de recarga en la simulación logística de drones.
"""

class Recarga:
    """
    Representa una estación de recarga en la red de drones.
    Puede ser referenciada por un vértice para mantener la posición.
    """
    def __init__(self, id_recarga, nombre):
        self.id_recarga = id_recarga
        self.nombre = nombre
        self.tipo_elemento = 'recarga'

    def __str__(self):
        return f"Recarga {self.id_recarga}: {self.nombre}"

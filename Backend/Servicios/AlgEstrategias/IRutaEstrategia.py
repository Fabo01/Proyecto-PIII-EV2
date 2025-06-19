"""
Interfaz para estrategias de cálculo de rutas (patrón Estrategia).
"""
from abc import ABC, abstractmethod

class IRutaEstrategia(ABC):
    @abstractmethod
    def calcular_ruta(self, origen, destino, grafo):
        """
        Calcula la ruta entre dos nodos en el grafo.
        Retorna una tupla (camino, peso_total) o lanza excepción si no existe ruta.
        """
        pass

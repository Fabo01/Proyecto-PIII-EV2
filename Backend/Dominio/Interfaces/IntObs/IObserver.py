"""
Interfaz Observer para el patron observer en la simulacion logistica de drones.
"""
from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def actualizar(self, evento, datos=None):
        """
        Metodo llamado cuando se publica un evento.
        :param evento: Nombre del evento.
        :param datos: Datos asociados al evento.
        """
        pass

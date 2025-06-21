"""
Interfaz Observer para el patrón observer en la simulación logística de drones.
"""
from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def actualizar(self, evento, datos=None):
        """
        Método llamado cuando se publica un evento.
        :param evento: Nombre del evento.
        :param datos: Datos asociados al evento.
        """
        pass

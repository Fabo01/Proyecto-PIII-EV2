"""
Interfaz Observer para el patron observer en la simulacion logistica de drones.
"""
from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def actualizar(self, evento, sujeto=None, datos=None):
        """
        Metodo llamado cuando se publica un evento.
        :param evento: Nombre del evento.
        :param sujeto: Objeto que notifica (opcional).
        :param datos: Datos asociados al evento.
        """
        pass

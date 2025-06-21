"""
Interfaz Sujeto para el patrón observer en la simulación logística de drones.
"""
from abc import ABC, abstractmethod

class ISujeto(ABC):
    @abstractmethod
    def agregar_observador(self, observador):
        """
        Agrega un observador a la lista de observadores.
        """
        pass

    @abstractmethod
    def quitar_observador(self, observador):
        """
        Quita un observador de la lista de observadores.
        """
        pass

    @abstractmethod
    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores registrados sobre un evento.
        """
        pass

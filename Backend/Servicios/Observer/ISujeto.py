"""
Interfaz Sujeto para el patrón observer en la simulación logística de drones.
"""
from abc import ABC, abstractmethod

class ISujeto(ABC):
    @abstractmethod
    def agregar_observador(self, observador):
        pass

    @abstractmethod
    def quitar_observador(self, observador):
        pass

    @abstractmethod
    def notificar_observadores(self, evento, datos=None):
        pass

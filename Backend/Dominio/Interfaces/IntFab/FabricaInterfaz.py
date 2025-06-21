"""
FabricaInterfaz: Interfaz abstracta común para todas las fábricas del sistema.
Define los métodos esenciales que deben implementar todas las fábricas, asegurando cohesión, escalabilidad y cumplimiento de SOLID.
"""
from abc import ABC, abstractmethod

class FabricaInterfaz(ABC):
    @abstractmethod
    def crear(self, *args, **kwargs):
        """
        Crea una nueva instancia de la entidad correspondiente y la registra si no existe.
        Los argumentos dependen de la entidad concreta.
        """
        pass

    @abstractmethod
    def obtener(self, clave):
        """
        Obtiene una instancia existente a partir de la clave única.
        """
        pass

    @abstractmethod
    def todos(self):
        """
        Retorna todas las instancias registradas en la fábrica.
        """
        pass

    @abstractmethod
    def limpiar(self):
        """
        Limpia el repositorio y el estado interno de la fábrica, eliminando referencias y reseteando estructuras.
        """
        pass

    @abstractmethod
    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de entidades.
        """
        pass

from abc import ABC, abstractmethod

class IRepositorioRutas(ABC):
    @abstractmethod
    def agregar(self, ruta, clave):
        """Agrega una ruta al repositorio."""
        pass

    @abstractmethod
    def obtener(self, clave):
        """Obtiene una ruta del repositorio."""
        pass

    @abstractmethod
    def eliminar(self, clave):
        """Elimina una ruta del repositorio."""
        pass

    @abstractmethod
    def todos(self):
        """Retorna todas las rutas."""
        pass

    @abstractmethod
    def limpiar(self):
        """Limpia el repositorio de rutas."""
        pass

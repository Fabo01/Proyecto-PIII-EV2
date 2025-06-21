"""
FabricaAristas: Fábrica centralizada para la creación y validación de aristas.
Garantiza unicidad y registro de errores.
"""
from Backend.Infraestructura.Modelos.Dominio_Arista import Arista
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
import logging
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaAristas(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaAristas")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, origen, destino, peso):
        """
        Crea una arista entre dos vértices y la registra en el repositorio si no existe.
        """
        clave = (
            getattr(origen.elemento(), 'id_cliente', None) or getattr(origen.elemento(), 'id_almacenamiento', None) or getattr(origen.elemento(), 'id_recarga', None),
            getattr(destino.elemento(), 'id_cliente', None) or getattr(destino.elemento(), 'id_almacenamiento', None) or getattr(destino.elemento(), 'id_recarga', None)
        )
        repo = RepositorioAristas()
        existente = repo.obtener(clave)
        if existente:
            self.logger.info(f"Arista {clave} ya existe, retornando instancia existente.")
            return existente
        try:
            arista = Arista(origen, destino, peso)
            repo.agregar(arista, clave)
            return arista
        except Exception as e:
            self.logger.error(f"Error creando arista {clave}: {e}")
            self.errores.append({'clave': clave, 'error': str(e)})
            return None

    def obtener(self, clave):
        """
        Obtiene una arista existente del repositorio.
        """
        return RepositorioAristas().obtener(clave)

    def todos(self):
        """
        Retorna todas las aristas registradas en el repositorio.
        """
        return RepositorioAristas().todos()

    def limpiar(self):
        """
        Limpia el repositorio de aristas y los errores registrados.
        """
        RepositorioAristas().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de aristas.
        """
        return self.errores

"""
FabricaRecargas: Fábrica centralizada para la creación y validación de recargas.
Garantiza unicidad y registro de errores.
"""
from Backend.Dominio.Dominio_Recarga import Recarga
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
import logging
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaRecargas(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaRecargas")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, id_recarga, nombre):
        """
        Crea una recarga y la registra en el repositorio si no existe.
        """
        repo = RepositorioRecargas()
        existente = repo.obtener(id_recarga)
        if existente:
            self.logger.info(f"Recarga {id_recarga} ya existe, retornando instancia existente.")
            return existente
        try:
            recarga = Recarga(id_recarga, nombre)
            repo.agregar(recarga)
            return recarga
        except Exception as e:
            self.logger.error(f"Error creando recarga {id_recarga}: {e}")
            self.errores.append({'id_recarga': id_recarga, 'error': str(e)})
            return None

    def obtener(self, clave):
        """
        Obtiene una recarga existente del repositorio.
        """
        return RepositorioRecargas().obtener(clave)

    def todos(self):
        """
        Retorna todas las recargas registradas en el repositorio.
        """
        return RepositorioRecargas().todos()

    def limpiar(self):
        """
        Limpia el repositorio de recargas y los errores registrados.
        """
        RepositorioRecargas().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de recargas.
        """
        return self.errores

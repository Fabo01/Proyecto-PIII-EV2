"""
FabricaAlmacenamientos: Fábrica centralizada para la creación y validación de almacenamientos.
Garantiza unicidad y registro de errores.
"""
from Backend.Dominio.Dominio_Almacenamiento import Almacenamiento
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
import logging
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaAlmacenamientos(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaAlmacenamientos")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, id_almacenamiento, nombre):
        """
        Crea un almacenamiento y lo registra en el repositorio si no existe.
        """
        repo = RepositorioAlmacenamientos()
        existente = repo.obtener(id_almacenamiento)
        if existente:
            self.logger.info(f"Almacenamiento {id_almacenamiento} ya existe, retornando instancia existente.")
            return existente
        try:
            almacen = Almacenamiento(id_almacenamiento, nombre)
            repo.agregar(almacen)
            return almacen
        except Exception as e:
            self.logger.error(f"Error creando almacenamiento {id_almacenamiento}: {e}")
            self.errores.append({'id_almacenamiento': id_almacenamiento, 'error': str(e)})
            return None

    def obtener(self, clave):
        """
        Obtiene un almacenamiento del repositorio.
        """
        return RepositorioAlmacenamientos().obtener(clave)

    def todos(self):
        """
        Retorna todos los almacenamientos registrados.
        """
        return RepositorioAlmacenamientos().todos()

    def limpiar(self):
        """
        Limpia el repositorio de almacenamientos y los errores registrados.
        """
        RepositorioAlmacenamientos().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de almacenamientos.
        """
        return self.errores

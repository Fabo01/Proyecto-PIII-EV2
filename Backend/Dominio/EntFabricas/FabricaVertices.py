"""
FabricaVertices: Fábrica centralizada para la creación y validación de vértices.
Garantiza unicidad y registro de errores.
"""
from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
import logging
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaVertices(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaVertices")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, elemento):
        """
        Crea un vértice para el elemento dado y lo registra en el repositorio si no existe.
        """
        # Obtener identificador sin descartar valores 0
        id_cliente = getattr(elemento, 'id_cliente', None)
        id_almacenamiento = getattr(elemento, 'id_almacenamiento', None)
        id_recarga = getattr(elemento, 'id_recarga', None)
        id_elemento = id_cliente if id_cliente is not None else id_almacenamiento if id_almacenamiento is not None else id_recarga
        if id_elemento is None:
            self.logger.warning(f"Intento de crear vértice con ID None para elemento: {elemento}. Creación abortada.")
            return None
        repo = RepositorioVertices()
        existente = repo.obtener(id_elemento)
        if existente:
            self.logger.info(f"Vertice para elemento {id_elemento} ya existe, retornando instancia existente.")
            return existente
        try:
            vertice = Vertice(elemento)
            repo.agregar(vertice, id_elemento)
            return vertice
        except Exception as e:
            self.logger.error(f"Error creando vertice para elemento {id_elemento}: {e}")
            self.errores.append({'id_elemento': id_elemento, 'error': str(e)})
            return None

    def obtener(self, clave):
        """
        Obtiene un vértice existente del repositorio.
        """
        return RepositorioVertices().obtener(clave)

    def todos(self):
        """
        Retorna todos los vértices registrados en el repositorio.
        """
        return RepositorioVertices().todos()

    def limpiar(self):
        """
        Limpia el repositorio de vértices y los errores registrados.
        """
        RepositorioVertices().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de vértices.
        """
        return self.errores

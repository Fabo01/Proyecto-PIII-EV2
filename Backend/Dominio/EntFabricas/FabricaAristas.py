"""
FabricaAristas: Fábrica centralizada para la creación y validación de aristas.
Garantiza unicidad y registro de errores.
"""
from Backend.Infraestructura.TDA.TDA_Arista import Arista
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
        # Obtener identificadores sin descartar valores 0
        id_cliente_ori = getattr(origen.elemento, 'id_cliente', None)
        id_alm_ori = getattr(origen.elemento, 'id_almacenamiento', None)
        id_rec_ori = getattr(origen.elemento, 'id_recarga', None)
        id_origen = id_cliente_ori if id_cliente_ori is not None else id_alm_ori if id_alm_ori is not None else id_rec_ori
        id_cliente_dest = getattr(destino.elemento, 'id_cliente', None)
        id_alm_dest = getattr(destino.elemento, 'id_almacenamiento', None)
        id_rec_dest = getattr(destino.elemento, 'id_recarga', None)
        id_destino = id_cliente_dest if id_cliente_dest is not None else id_alm_dest if id_alm_dest is not None else id_rec_dest
        if id_origen is None or id_destino is None:
            self.logger.warning(f"Intento de crear arista con ID None: origen={id_origen}, destino={id_destino}. Creación abortada.")
            return None
        clave = (id_origen, id_destino)
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

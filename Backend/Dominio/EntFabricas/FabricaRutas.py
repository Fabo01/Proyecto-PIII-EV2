"""
FabricaRutas: Fábrica centralizada para la creación y validación de rutas.
Garantiza unicidad y registro de errores.
Utiliza FabricaVertices y FabricaAristas para componentes internos.
"""
from Backend.Dominio.Dominio_Ruta import Ruta
from Backend.Dominio.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
import logging
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaRutas(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        # Singleton con repositorio de rutas
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaRutas")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, origen, destino, camino, peso_total, algoritmo, tiempo_calculo=None):
        """
        Crea o retorna una ruta única entre origen y destino y la registra en el repositorio.
        """
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        repo = RepositorioRutas()
        clave = (
            getattr(origen.elemento(), 'id_cliente', None) or getattr(origen.elemento(), 'id_almacenamiento', None) or getattr(origen.elemento(), 'id_recarga', None),
            getattr(destino.elemento(), 'id_cliente', None) or getattr(destino.elemento(), 'id_almacenamiento', None) or getattr(destino.elemento(), 'id_recarga', None),
            algoritmo
        )
        existente = repo.obtener(clave)
        if existente:
            self.logger.info(f"Ruta {clave} ya existe, retornando instancia existente.")
            return existente
        try:
            fabrica_vertices = FabricaVertices()
            # Convertir vertices del camino a vértices únicos
            camino_vertices = [fabrica_vertices.crear(n.elemento()) for n in camino]
            ruta = Ruta(origen, destino, camino_vertices, peso_total, algoritmo, tiempo_calculo)
            repo.agregar(ruta, clave)
            return ruta
        except Exception as e:
            self.logger.error(f"Error creando ruta {clave}: {e}")
            self.errores.append({'clave': clave, 'error': str(e)})
            return None

    def obtener(self, clave):
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        return RepositorioRutas().obtener(clave)

    def todos(self):
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        return RepositorioRutas().todos()

    def limpiar(self):
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        RepositorioRutas().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de rutas.
        """
        return self.errores

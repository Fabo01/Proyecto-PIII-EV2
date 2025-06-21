"""
RepositorioRutas: Acceso centralizado y único a instancias de Ruta.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Infraestructura.Repositorios.RepoInterfaces.IRepositorioRutas import IRepositorioRutas
import logging

class RepositorioRutas(IRepositorioRutas):
    """
    Repositorio para gestionar instancias únicas de Ruta.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._rutas = HashMap()
            cls._instancia.logger = logging.getLogger("Ruta")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def agregar(self, ruta, clave):
        self.logger.info(f"[RepositorioRutas.agregar] Agregando ruta con clave {clave}")
        self._rutas.insertar(clave, ruta)
        self.logger.info(f"[RepositorioRutas.agregar] Ruta agregada exitosamente: {ruta}")

    def obtener(self, clave):
        self.logger.info(f"[RepositorioRutas.obtener] Buscando ruta con clave {clave}")
        ruta = self._rutas.buscar(clave)
        if ruta:
            self.logger.info(f"[RepositorioRutas.obtener] Ruta encontrada: {ruta}")
        else:
            self.logger.warning(f"[RepositorioRutas.obtener] Ruta no encontrada para clave {clave}")
        return ruta

    def eliminar(self, clave):
        self.logger.info(f"[RepositorioRutas.eliminar] Eliminando ruta con clave {clave}")
        self._rutas.eliminar(clave)
        self.logger.info(f"[RepositorioRutas.eliminar] Ruta eliminada (si existía) para clave {clave}")

    def todos(self):
        rutas = list(self._rutas.valores())
        self.logger.info(f"[RepositorioRutas.todos] Total de rutas registradas: {len(rutas)}")
        return rutas

    def limpiar(self):
        self.logger.info(f"[RepositorioRutas.limpiar] Limpiando todas las rutas del repositorio")
        self._rutas.limpiar()
        self.logger.info(f"[RepositorioRutas.limpiar] Repositorio de rutas limpiado exitosamente")

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de rutas (clave → Objeto Ruta).
        """
        return dict(self._rutas.items())

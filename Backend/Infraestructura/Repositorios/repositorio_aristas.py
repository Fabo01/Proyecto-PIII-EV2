"""
RepositorioAristas: Acceso centralizado y único a instancias de Arista.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioAristas import IRepositorioAristas

class RepositorioAristas(IRepositorioAristas):
    """
    Repositorio para gestionar instancias únicas de Arista.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._aristas = HashMap()
        return cls._instancia

    def agregar(self, arista, clave=None):
        # clave puede ser una tupla (id_origen, id_destino)
        if clave is None:
            clave = (getattr(arista.origen.elemento(), 'id_cliente', None) or getattr(arista.origen.elemento(), 'id_almacenamiento', None) or getattr(arista.origen.elemento(), 'id_recarga', None),
                     getattr(arista.destino.elemento(), 'id_cliente', None) or getattr(arista.destino.elemento(), 'id_almacenamiento', None) or getattr(arista.destino.elemento(), 'id_recarga', None))
        self._aristas.insertar(clave, arista)

    def obtener(self, clave):
        return self._aristas.buscar(clave)

    def eliminar(self, clave):
        self._aristas.eliminar(clave)

    def todos(self):
        return list(self._aristas.valores())

    def limpiar(self):
        self._aristas.limpiar()

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de aristas (clave → Objeto Arista).
        """
        return dict(self._aristas.items())

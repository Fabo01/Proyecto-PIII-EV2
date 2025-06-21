"""
Clase Grafo para modelar el grafo base de la red de drones.
Basado en Docs/graph.py y plan de mejora 4.4 (unicidad de instancias).
"""
from Backend.Infraestructura.Modelos.Dominio_Vertice import Vertice
from Backend.Infraestructura.Modelos.Dominio_Arista import Arista
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Servicios.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Servicios.EntFabricas.FabricaAristas import FabricaAristas

class Grafo:
    """
    Representa un grafo dirigido o no dirigido.
    Solo modela la estructura de red, no contiene lógica de negocio ni de simulación.
    Garantiza unicidad de instancias de vértices y aristas usando repositorios centralizados.
    """
    def __init__(self, dirigido=False):
        self._dirigido = dirigido
        self._repositorio_vertices = RepositorioVertices()
        self._repositorio_aristas = RepositorioAristas()

    def es_dirigido(self):
        return self._dirigido

    def insertar_vertice(self, elemento):
        """
        Inserta un vértice único para el elemento dado, usando la fábrica y el repositorio centralizado.
        Si ya existe, retorna la instancia existente.
        """
        id_elemento = getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_recarga', None)
        vertice = self._repositorio_vertices.obtener(id_elemento)
        if vertice is None:
            vertice = FabricaVertices().crear(elemento)
            self._repositorio_vertices.agregar(vertice, id_elemento)
        return vertice

    def buscar_vertice_por_elemento(self, elemento):
        id_elemento = getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_recarga', None)
        return self._repositorio_vertices.obtener(id_elemento)

    def insertar_arista(self, u, v, peso):
        """
        Inserta una arista única entre los vértices u y v, usando la fábrica y el repositorio centralizado.
        Si ya existe, retorna la instancia existente.
        """
        self._validar_origen_destino(u, v)
        clave = (self._id_vertice(u), self._id_vertice(v))
        arista = self._repositorio_aristas.obtener(clave)
        if arista is None:
            arista = FabricaAristas().crear(u, v, peso)
            self._repositorio_aristas.agregar(arista, clave)
        return arista
    
    def eliminar_arista(self, u, v):
        self._validar_origen_destino(u, v)
        clave = (self._id_vertice(u), self._id_vertice(v))
        self._repositorio_aristas.eliminar(clave)

    def eliminar_vertice(self, v):
        # Validar que v sea un vertice existente
        if not isinstance(v, Vertice):
            raise TypeError("v debe ser instancia de Vertice")
        id_v = self._id_vertice(v)
        self._repositorio_vertices.eliminar(id_v)
        # Eliminar aristas asociadas
        aristas_a_eliminar = [a for a in self.aristas() if a.origen == v or a.destino == v]
        for arista in aristas_a_eliminar:
            clave = (self._id_vertice(arista.origen), self._id_vertice(arista.destino))
            self._repositorio_aristas.eliminar(clave)

    def obtener_arista(self, u, v):
        self._validar_origen_destino(u, v)
        clave = (self._id_vertice(u), self._id_vertice(v))
        return self._repositorio_aristas.obtener(clave)
    
    def vertices(self):
        return self._repositorio_vertices.todos()

    def aristas(self):
        return self._repositorio_aristas.todos()

    def vecinos(self, v):
        vecinos = []
        for arista in self.aristas():
            if arista.origen == v:
                vecinos.append(arista.destino)
            elif not self._dirigido and arista.destino == v:
                vecinos.append(arista.origen)
        return vecinos

    def grado(self, v, salientes=True):
        if self._dirigido:
            if salientes:
                return len([a for a in self.aristas() if a.origen == v])
            else:
                return len([a for a in self.aristas() if a.destino == v])
        else:
            return len([a for a in self.aristas() if a.origen == v or a.destino == v])

    def aristas_incidentes(self, v, salientes=True):
        if self._dirigido:
            if salientes:
                return [a for a in self.aristas() if a.origen == v]
            else:
                return [a for a in self.aristas() if a.destino == v]
        else:
            return [a for a in self.aristas() if a.origen == v or a.destino == v]

    def _validar_origen_destino(self, origen, destino):
        if origen is None or destino is None:
            raise ValueError("Origen y destino no pueden ser None")
        if not isinstance(origen, Vertice) or not isinstance(destino, Vertice):
            raise TypeError("Origen y destino deben ser instancias de Vertice")

    def _id_vertice(self, v):
        if hasattr(v, 'id_elemento'):
            return v.id_elemento()
        return getattr(v, 'id_cliente', None) or getattr(v, 'id_almacenamiento', None) or getattr(v, 'id_recarga', None)
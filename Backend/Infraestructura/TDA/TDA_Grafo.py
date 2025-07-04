"""
Clase Grafo para modelar el grafo base de la red de drones.
Basado en Docs/graph.py y plan de mejora 4.4 (unicidad de instancias).
"""
from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
from Backend.Infraestructura.TDA.TDA_Arista import Arista
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Dominio.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas

class Grafo:
    """
    Grafo dirigido/no dirigido con soporte para observadores.
    Notifica en insercion/eliminacion de vertices/aristas y serializacion.
    """
    def __init__(self, dirigido=False):
        self._dirigido = dirigido
        self._repositorio_vertices = RepositorioVertices()
        self._repositorio_aristas = RepositorioAristas()
        self._observadores = set()
        self.notificar_observadores('grafo_creado', {'dirigido': dirigido})

    def es_dirigido(self):
        return self._dirigido

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def insertar_vertice(self, elemento):
        """
        Inserta un vértice único para el elemento dado, usando la fábrica y el repositorio centralizado.
        Si ya existe, retorna la instancia existente.
        """
        # Obtener identificador sin descartar valores 0
        id_cliente = getattr(elemento, 'id_cliente', None)
        id_almacenamiento = getattr(elemento, 'id_almacenamiento', None)
        id_recarga = getattr(elemento, 'id_recarga', None)
        id_elemento = id_cliente if id_cliente is not None else id_almacenamiento if id_almacenamiento is not None else id_recarga
        vertice = self._repositorio_vertices.obtener(id_elemento)
        if vertice is None:
            vertice = FabricaVertices().crear(elemento)
            self._repositorio_vertices.agregar(vertice, id_elemento)
            self.notificar_observadores('vertice_insertado', {'vertice': vertice})
            if hasattr(vertice, 'agregar_observador'):
                for obs in self._observadores:
                    vertice.agregar_observador(obs)
        return vertice

    def buscar_vertice_por_elemento(self, elemento):
        # Obtener identificador sin descartar valores 0
        id_cliente = getattr(elemento, 'id_cliente', None)
        id_almacenamiento = getattr(elemento, 'id_almacenamiento', None)
        id_recarga = getattr(elemento, 'id_recarga', None)
        id_elemento = id_cliente if id_cliente is not None else id_almacenamiento if id_almacenamiento is not None else id_recarga
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
            self.notificar_observadores('arista_insertada', {'arista': arista})
            if hasattr(arista, 'agregar_observador'):
                for obs in self._observadores:
                    arista.agregar_observador(obs)
        return arista
    
    def eliminar_arista(self, u, v):
        """
        Elimina la arista entre los vértices u y v si existe.
        Notifica a los observadores sobre la eliminación.
        """
        self._validar_origen_destino(u, v)
        clave = (self._id_vertice(u), self._id_vertice(v))
        self._repositorio_aristas.eliminar(clave)
        self.notificar_observadores('arista_eliminada', {'origen': u, 'destino': v})

    def eliminar_vertice(self, v):
        """
        Elimina el vértice v y todas las aristas asociadas a él.
        Notifica a los observadores sobre la eliminación.
        """
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
        self.notificar_observadores('vertice_eliminado', {'vertice': v})

    def obtener_arista(self, u, v):
        """
        Obtiene la arista entre los vértices u y v si existe.
        """
        self._validar_origen_destino(u, v)
        clave = (self._id_vertice(u), self._id_vertice(v))
        return self._repositorio_aristas.obtener(clave)
    
    def vertices(self):
        """
        Retorna todos los vértices del grafo.
        """
        return self._repositorio_vertices.todos()

    def aristas(self):
        """
        Retorna todas las aristas del grafo.
        """
        return self._repositorio_aristas.todos()

    def vecinos(self, v):
        """
        Retorna los vecinos del vértice v.
        Si el grafo es no dirigido, también considera a v como destino.
        """
        vecinos = []
        for arista in self.aristas():
            if arista.origen == v:
                vecinos.append(arista.destino)
            elif not self._dirigido and arista.destino == v:
                vecinos.append(arista.origen)
        return vecinos

    def grado(self, v, salientes=True):
        """
        Retorna el grado del vértice v.
        En grafos dirigidos, puede ser el grado de salida (salientes=True) o de entrada (salientes=False).
        """
        if self._dirigido:
            if salientes:
                return len([a for a in self.aristas() if a.origen == v])
            else:
                return len([a for a in self.aristas() if a.destino == v])
        else:
            return len([a for a in self.aristas() if a.origen == v or a.destino == v])

    def aristas_incidentes(self, v, salientes=True):
        """
        Retorna las aristas incidentes al vértice v.
        En grafos dirigidos, puede retornar las de salida (salientes=True) o las de entrada (salientes=False).
        """
        if self._dirigido:
            if salientes:
                return [a for a in self.aristas() if a.origen == v]
            else:
                return [a for a in self.aristas() if a.destino == v]
        else:
            return [a for a in self.aristas() if a.origen == v or a.destino == v]

    def _validar_origen_destino(self, origen, destino):
        """
        Valida que los vértices de origen y destino no sean None y sean instancias de Vertice.
        """
        if origen is None or destino is None:
            raise ValueError("Origen y destino no pueden ser None")
        if not isinstance(origen, Vertice) or not isinstance(destino, Vertice):
            raise TypeError("Origen y destino deben ser instancias de Vertice")

    def _id_vertice(self, v):
        """
        Retorna el ID del vértice v.
        Intenta usar el método id_elemento() si está disponible, sino usa los atributos id_cliente, id_almacenamiento o id_recarga.
        """
        if hasattr(v, 'id_elemento'):
            return v.id_elemento()
        # Obtener identificador sin descartar valores 0
        id_cliente = getattr(v, 'id_cliente', None)
        id_almacenamiento = getattr(v, 'id_almacenamiento', None)
        id_recarga = getattr(v, 'id_recarga', None)
        return id_cliente if id_cliente is not None else id_almacenamiento if id_almacenamiento is not None else id_recarga

    def serializar(self):
        """
        Serializa el grafo, notificando a los observadores.
        """
        self.notificar_observadores('grafo_serializado', None)
        return {
            'vertices': [v.serializar() for v in self.vertices()],
            'aristas': [a.serializar() for a in self.aristas()],
            'dirigido': self._dirigido
        }

    def snapshot(self):
        """
        Devuelve un snapshot serializado del grafo actual (vertices y aristas).
        """
        return {
            'vertices': [v.serializar() if hasattr(v, 'serializar') else str(v) for v in self.vertices()],
            'aristas': [a.serializar() if hasattr(a, 'serializar') else str(a) for a in self.aristas()],
            'dirigido': self._dirigido
        }
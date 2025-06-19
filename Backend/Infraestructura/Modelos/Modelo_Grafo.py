"""
Clase Grafo para modelar el grafo base de la red de drones.
Basado en Docs/graph.py
"""
from Backend.Infraestructura.Modelos.Modelo_Vertice import Vertice
from Backend.Infraestructura.Modelos.Modelo_Arista import Arista
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas

class Grafo:
    """
    Representa un grafo dirigido o no dirigido.
    Solo modela la estructura de red, no contiene lógica de negocio ni de simulación.
    Garantiza unicidad de instancias de vértices y aristas usando repositorios.
    """
    def __init__(self, dirigido=False):
        self._dirigido = dirigido
        self._adyacentes = {}  # vertice: set de aristas salientes
        self._entrantes = {} if dirigido else self._adyacentes
        self._repo_vertices = RepositorioVertices()
        self._repo_aristas = RepositorioAristas()

    def es_dirigido(self):
        return self._dirigido

    def insertar_vertice(self, elemento):
        """
        Inserta un vértice único para el elemento dado. Si ya existe, lo retorna.
        """
        id_elem = None
        for attr in ['id_cliente', 'id_almacenamiento', 'id_recarga']:
            if hasattr(elemento, attr):
                id_elem = getattr(elemento, attr)
                break
        if id_elem is None:
            raise ValueError("Elemento sin identificador único")
        vertice = self._repo_vertices.obtener(id_elem)
        if vertice is not None:
            return vertice
        vertice = Vertice(elemento)
        self._repo_vertices.agregar(vertice, id_elem)
        self._adyacentes[vertice] = set()
        if self._dirigido:
            self._entrantes[vertice] = set()
        return vertice

    def buscar_vertice_por_elemento(self, elemento):
        id_elem = None
        for attr in ['id_cliente', 'id_almacenamiento', 'id_recarga']:
            if hasattr(elemento, attr):
                id_elem = getattr(elemento, attr)
                break
        if id_elem is None:
            return None
        return self._repo_vertices.obtener(id_elem)

    def insertar_arista(self, u, v, peso):
        """
        Inserta una arista única entre u y v. Si ya existe, la retorna.
        """
        clave = (u.id_elemento(), v.id_elemento())
        arista = self._repo_aristas.obtener(clave)
        if arista is not None:
            return arista
        arista = Arista(u, v, peso)
        self._repo_aristas.agregar(arista, clave)
        self._adyacentes[u].add(arista)
        if self._dirigido:
            self._entrantes[v].add(arista)
        else:
            self._adyacentes[v].add(arista)
        return arista

    def eliminar_arista(self, u, v):
        clave = (u.id_elemento(), v.id_elemento())
        arista = self._repo_aristas.obtener(clave)
        if arista:
            self._adyacentes[u].discard(arista)
            if self._dirigido:
                self._entrantes[v].discard(arista)
            else:
                self._adyacentes[v].discard(arista)
            self._repo_aristas.eliminar(clave)

    def eliminar_vertice(self, v):
        id_elem = v.id_elemento()
        if v in self._adyacentes:
            for arista in list(self._adyacentes[v]):
                self.eliminar_arista(arista.origen, arista.destino)
            del self._adyacentes[v]
        if self._dirigido and v in self._entrantes:
            del self._entrantes[v]
        self._repo_vertices.eliminar(id_elem)

    def obtener_arista(self, u, v):
        clave = (u.id_elemento(), v.id_elemento())
        return self._repo_aristas.obtener(clave)

    def vertices(self):
        return list(self._adyacentes.keys())

    def aristas(self):
        return list(self._repo_aristas.todos())

    def vecinos(self, v):
        return [arista.opuesto(v) for arista in self._adyacentes.get(v, set())]

    def grado(self, v, salientes=True):
        if self._dirigido:
            return len(self._adyacentes[v]) if salientes else len(self._entrantes[v])
        return len(self._adyacentes[v])

    def aristas_incidentes(self, v, salientes=True):
        if self._dirigido:
            return self._adyacentes[v] if salientes else self._entrantes[v]
        return self._adyacentes[v]

    def _validar_origen_destino(self, origen, destino):
        if origen not in self._adyacentes or destino not in self._adyacentes:
            raise ValueError("Origen o destino no existen en el grafo")
        if not (hasattr(origen.elemento(), 'tipo_elemento') and hasattr(destino.elemento(), 'tipo_elemento')):
            raise ValueError("Los vértices deben tener tipo_elemento.")
        if origen.elemento().tipo_elemento != 'almacenamiento' or destino.elemento().tipo_elemento != 'cliente':
            raise ValueError("Solo se permiten rutas de almacenamiento a cliente.")

    # Métodos de algoritmos (kruskal, dijkstra, etc.) deben usar 'peso' de la arista
    def dijkstra_camino_minimo(self, origen, destino, max_peso=50, forzar_recarga=True):
        import heapq
        try:
            self._validar_origen_destino(origen, destino)
        except ValueError as e:
            return None, str(e)
        visitados = set()
        heap = [(0, [origen], False)]  # (costo, camino, recarga_usada)
        while heap:
            costo, camino, recarga_usada = heapq.heappop(heap)
            actual = camino[-1]
            if actual == destino:
                # Si el costo supera el max_peso, debe haber pasado por recarga
                if costo > max_peso and not recarga_usada:
                    continue
                return {'camino': camino, 'peso_total': costo}, None
            if actual in visitados:
                continue
            visitados.add(actual)
            if actual not in self._adyacentes:
                continue
            for vecino in self.vecinos(actual):
                if vecino in visitados:
                    continue
                arista = self.obtener_arista(actual, vecino)
                if not arista:
                    continue
                nuevo_costo = costo + arista.peso
                nuevo_camino = camino + [vecino]
                nuevo_recarga = recarga_usada or (hasattr(vecino.elemento(), 'tipo_elemento') and vecino.elemento().tipo_elemento == 'recarga')
                heapq.heappush(heap, (nuevo_costo, nuevo_camino, nuevo_recarga))
        return None, "No existe una ruta posible entre almacenamiento y cliente."

    def bfs_camino(self, origen, destino, max_peso=50, forzar_recarga=True):
        from collections import deque
        try:
            self._validar_origen_destino(origen, destino)
        except ValueError as e:
            return None, str(e)
        visitados = set()
        cola = deque([(origen, [origen], 0, False)])
        while cola:
            actual, camino, costo, recarga_usada = cola.popleft()
            if actual == destino:
                if costo > max_peso and forzar_recarga and not recarga_usada:
                    continue
                return {'camino': camino, 'peso_total': costo}, None
            if actual in visitados:
                continue
            visitados.add(actual)
            for vecino in self.vecinos(actual):
                if vecino in visitados:
                    continue
                arista = self.obtener_arista(actual, vecino)
                if not arista:
                    continue
                nuevo_costo = costo + arista.peso
                nuevo_camino = camino + [vecino]
                nuevo_recarga = recarga_usada or (hasattr(vecino.elemento(), 'tipo_elemento') and vecino.elemento().tipo_elemento == 'recarga')
                cola.append((vecino, nuevo_camino, nuevo_costo, nuevo_recarga))
        return None, "No existe una ruta posible entre almacenamiento y cliente."

    def dfs_camino(self, origen, destino, max_peso=50, forzar_recarga=True):
        try:
            self._validar_origen_destino(origen, destino)
        except ValueError as e:
            return None, str(e)
        visitados = set()
        stack = [(origen, [origen], 0, False)]
        while stack:
            actual, camino, costo, recarga_usada = stack.pop()
            if actual == destino:
                if costo > max_peso and forzar_recarga and not recarga_usada:
                    continue
                return {'camino': camino, 'peso_total': costo}, None
            if actual in visitados:
                continue
            visitados.add(actual)
            for vecino in self.vecinos(actual):
                if vecino in visitados:
                    continue
                arista = self.obtener_arista(actual, vecino)
                if not arista:
                    continue
                nuevo_costo = costo + arista.peso
                nuevo_camino = camino + [vecino]
                nuevo_recarga = recarga_usada or (hasattr(vecino.elemento(), 'tipo_elemento') and vecino.elemento().tipo_elemento == 'recarga')
                stack.append((vecino, nuevo_camino, nuevo_costo, nuevo_recarga))
        return None, "No existe una ruta posible entre almacenamiento y cliente."

    def topological_sort_camino(self, origen, destino, max_peso=50, forzar_recarga=True):
        if not self._dirigido:
            return None, "El grafo no es dirigido."
        try:
            self._validar_origen_destino(origen, destino)
        except ValueError as e:
            return None, str(e)
        grado_entrada = {v: 0 for v in self.vertices()}
        for v in self.vertices():
            for vecino in self.vecinos(v):
                grado_entrada[vecino] += 1
        from collections import deque
        cola = deque([v for v in self.vertices() if grado_entrada[v] == 0])
        orden_topologico = []
        while cola:
            actual = cola.popleft()
            orden_topologico.append(actual)
            for vecino in self.vecinos(actual):
                grado_entrada[vecino] -= 1
                if grado_entrada[vecino] == 0:
                    cola.append(vecino)
        distancias = {v: float('inf') for v in self.vertices()}
        predecesores = {v: None for v in self.vertices()}
        distancias[origen] = 0
        for v in orden_topologico:
            if distancias[v] != float('inf'):
                for vecino in self.vecinos(v):
                    arista = self.obtener_arista(v, vecino)
                    if arista:
                        nueva_distancia = distancias[v] + arista.peso
                        if nueva_distancia < distancias[vecino]:
                            if nueva_distancia > max_peso and forzar_recarga:
                                if (hasattr(vecino.elemento(), 'tipo_elemento') and (vecino.elemento().tipo_elemento == 'recarga' or vecino == destino)):
                                    distancias[vecino] = nueva_distancia
                                    predecesores[vecino] = v
                            else:
                                distancias[vecino] = nueva_distancia
                                predecesores[vecino] = v
        if distancias[destino] == float('inf'):
            return None, "No existe una ruta posible entre almacenamiento y cliente."
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
        camino.reverse()
        return {'camino': camino, 'peso_total': distancias[destino]}, None

    def kruskal_arbol_expansion_minima(self):
        # Algoritmo de Kruskal para árbol de expansión mínima
        parent = {}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            parent[find(u)] = find(v)
        aristas = list(self.aristas())
        aristas.sort(key=lambda a: a.peso())
        for v in self.vertices():
            parent[v] = v
        mst = []
        for arista in aristas:
            u, v = arista.extremos()
            if find(u) != find(v):
                mst.append(arista)
                union(u, v)
            if len(mst) == len(self._adyacentes) - 1:
                break
        return mst

    def obtener_vertices_por_tipo(self, tipo):
        """
        Retorna una lista de vértices cuyo elemento es del tipo dado.
        """
        return [v for v in self.vertices() if v.es_tipo(tipo)]

    def obtener_aristas_por_tipo(self, tipo_origen, tipo_destino):
        """
        Retorna una lista de aristas que conectan tipos de vértices dados.
        """
        return [a for a in self.aristas() if a.es_conexion(tipo_origen, tipo_destino)]

    def floyd_warshall_todos_los_caminos(self, max_peso=50, forzar_recarga=True):
        """
        Calcula las distancias mínimas y predecesores entre todos los pares de nodos usando Floyd-Warshall.
        Considera el peso máximo (autonomía) y la necesidad de recarga.
        Retorna dos diccionarios: distancias y predecesores.
        """
        vertices = list(self.vertices())
        n = len(vertices)
        idx_map = {v: i for i, v in enumerate(vertices)}
        dist = [[float('inf')] * n for _ in range(n)]
        pred = [[None] * n for _ in range(n)]
        # Inicializar distancias directas
        for i, u in enumerate(vertices):
            dist[i][i] = 0
            for v in self.vecinos(u):
                j = idx_map[v]
                arista = self.obtener_arista(u, v)
                if arista:
                    dist[i][j] = arista.peso
                    pred[i][j] = u
        # Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        # Si se fuerza recarga, solo permitir caminos válidos
                        if forzar_recarga and dist[i][k] + dist[k][j] > max_peso:
                            # Solo permitir si el nodo intermedio es de recarga
                            if hasattr(vertices[k].elemento(), 'tipo_elemento') and vertices[k].elemento().tipo_elemento == 'recarga':
                                dist[i][j] = dist[i][k] + dist[k][j]
                                pred[i][j] = pred[k][j]
                        else:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            pred[i][j] = pred[k][j]
        # Convertir a diccionarios para acceso por vértice
        dist_dict = {}
        pred_dict = {}
        for i, u in enumerate(vertices):
            dist_dict[u] = {}
            pred_dict[u] = {}
            for j, v in enumerate(vertices):
                dist_dict[u][v] = dist[i][j]
                pred_dict[u][v] = pred[i][j]
        return dist_dict, pred_dict

    def calcular_camino_entre_nodos(self, origen, destino, algoritmo):
        """
        Calcula el camino entre dos nodos usando el algoritmo especificado.
        Retorna una tupla (camino, peso_total).
        """
        if algoritmo == 'bfs':
            return self.bfs_camino(origen, destino)
        elif algoritmo == 'dfs':
            return self.dfs_camino(origen, destino)
        elif algoritmo == 'topological':
            return self.topological_sort_camino(origen, destino)
        elif algoritmo == 'dijkstra':
            return self.dijkstra_camino_minimo(origen, destino)
        elif algoritmo == 'floyd_warshall':
            distancias, caminos = self.floyd_warshall_todos_los_caminos()
            key = (getattr(origen.elemento(), 'id', None), getattr(destino.elemento(), 'id', None))
            return (caminos.get(key, []), distancias.get(key, float('inf')))
        else:
            raise ValueError("Algoritmo de ruta no soportado")

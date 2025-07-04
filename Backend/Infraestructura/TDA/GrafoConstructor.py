import logging
from Backend.Infraestructura.TDA.TDA_Grafo import Grafo
from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
from Backend.Infraestructura.TDA.TDA_Arista import Arista
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Dominio.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
from typing import List, Tuple, Dict, Any
import random
from collections import deque

class GrafoConstructor:
    """
    Clase responsable de construir grafos válidos y persistir snapshots de sus estados (n-1 y m_aristas).
    Inyecta dependencias y utiliza las fábricas y repositorios del sistema.
    """
    def __init__(self, n_vertices: int = None, m_aristas: int = None, roles_vertices: List[str] = None, aristas_candidatas: List[Tuple[int, int, int]] = None,
                 dirigido=False, repositorio_vertices=None, repositorio_aristas=None,
                 fabrica_vertices=None, fabrica_aristas=None, elementos: List[Any] = None):
        self.n_vertices = n_vertices
        self.m_aristas = m_aristas
        self.roles_vertices = roles_vertices  # Lista de roles por índice
        self.aristas_candidatas = aristas_candidatas  # (u, v, peso)
        self.elementos = elementos  # Lista de entidades de dominio opcional
        self.grafo_n1 = None
        self.grafo_m = None
        self.snapshots = {}
        self._dirigido = dirigido
        self._repositorio_vertices = repositorio_vertices or RepositorioVertices()
        self._repositorio_aristas = repositorio_aristas or RepositorioAristas()
        self._fabrica_vertices = fabrica_vertices or FabricaVertices()
        self._fabrica_aristas = fabrica_aristas or FabricaAristas()
        import logging
        self.logger = logging.getLogger("GrafoConstructor")
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def construir(self):
        """
        Construye el grafo válido, generando dos snapshots:
        - n-1: árbol de expansión mínimo válido (con segmentación)
        - m_aristas: grafo final con la cantidad de aristas solicitada
        """
        # Inicio de construcción con segmentación de autonomía y presupuesto real de aristas
        self.logger.info(f"[INICIO] Construcción de grafo: n_vertices={self.n_vertices}, m_aristas presupuestadas={self.m_aristas}")
        # Iniciar grafo y limpiar repositorios para nueva simulación
        grafo = Grafo(dirigido=self._dirigido)
        grafo._repositorio_vertices = self._repositorio_vertices
        grafo._repositorio_aristas = self._repositorio_aristas
        # Insertar todos los vértices de dominio
        vertices = []
        for elem in self.elementos:
            vert = grafo.insertar_vertice(elem)
            vertices.append(vert)
        self.logger.info(f"[VERTICES] Insertados {len(vertices)} vértices en el grafo: {[getattr(v.elemento, 'nombre', str(v)) for v in vertices]}")
        # Filtrar aristas candidatas según peso individual <= autonomía
        valid_aristas = [(u, v, w) for u, v, w in self.aristas_candidatas if w <= 50]
        self.logger.info(f"[ARISTAS] Candidatas filtradas por peso<=50: {len(valid_aristas)} de {len(self.aristas_candidatas)}")
        # Generar árbol mínimo segmentado (MST) con Kruskal sobre aristas válidas
        parent = {i: i for i in range(self.n_vertices)}
        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        def union(a, b):
            parent[find(a)] = find(b)
        sorted_edges = sorted(valid_aristas, key=lambda x: x[2])
        arbol_edges = []
        for u_idx, v_idx, peso in sorted_edges:
            if find(u_idx) != find(v_idx):
                union(u_idx, v_idx)
                arbol_edges.append((u_idx, v_idx, peso))
                if len(arbol_edges) == self.n_vertices - 1:
                    break
        # Construir grafo_n1 separado con solo arbol_edges
        grafo_n1 = Grafo(dirigido=self._dirigido)
        grafo_n1._repositorio_vertices = self._repositorio_vertices
        grafo_n1._repositorio_aristas = self._repositorio_aristas
        # Insertar vértices en grafo_n1
        for v in vertices:
            grafo_n1.insertar_vertice(v.elemento)
        # Insertar aristas del MST
        for u_idx, v_idx, peso in arbol_edges:
            grafo_n1.insertar_arista(vertices[u_idx], vertices[v_idx], peso)
        # Guardar snapshot n-1 con arbol_edges únicamente
        self.grafo_n1 = grafo_n1
        snapshot_n1 = grafo_n1.snapshot()
        self.snapshots['n-1'] = snapshot_n1
        self.logger.info(f"[SNAPSHOT] Guardado snapshot n-1: vértices={len(snapshot_n1['vertices'])}, aristas={len(snapshot_n1['aristas'])}")
        # Construir grafo final (grafo_m) con m_aristas aristas válidas
        grafo_final = Grafo(dirigido=self._dirigido)
        grafo_final._repositorio_vertices = self._repositorio_vertices
        grafo_final._repositorio_aristas = self._repositorio_aristas
        # Insertar vértices en grafo_final
        for v in vertices:
            grafo_final.insertar_vertice(v.elemento)
        # Insertar todas las aristas del MST en grafo_final
        for u_idx, v_idx, peso in arbol_edges:
            grafo_final.insertar_arista(vertices[u_idx], vertices[v_idx], peso)
        # Agregar aristas adicionales hasta alcanzar m_aristas, evitando duplicados
        adicionales = [e for e in valid_aristas if e not in arbol_edges]
        random.shuffle(adicionales)
        count = len(arbol_edges)
        seen = set((u, v, w) for u, v, w in arbol_edges)
        for u_idx, v_idx, peso in adicionales:
            if count >= self.m_aristas:
                break
            key = (u_idx, v_idx, peso)
            if key not in seen:
                grafo_final.insertar_arista(vertices[u_idx], vertices[v_idx], peso)
                seen.add(key)
                count += 1
                self.logger.debug(f"[GRAFO] Arista extra agregada: ({u_idx}, {v_idx}, peso={peso})")
        # Validar conectividad final
        if not self._validar_segmentacion_total(grafo_final, vertices):
            self.logger.error("[GRAFO] El grafo final no cumple la segmentación ni la conectividad requerida.")
            raise Exception("El grafo final no cumple la segmentación ni la conectividad requerida")
        # Guardar snapshot m_aristas desde grafo_final
        self.grafo_m = grafo_final
        snapshot_m = grafo_final.snapshot()
        self.snapshots['m_aristas'] = snapshot_m
        self.logger.info(f"[SNAPSHOT] Guardado snapshot m_aristas con vértices={len(snapshot_m['vertices'])}, aristas={len(snapshot_m['aristas'])}")
        self.logger.info("[FIN] Construcción de grafo completa y válida")
        # Limpiar referencias a instancias temporales
        del grafo_n1, grafo_final, vertices

    def construir_grafo(self, vertices_data, aristas_data):
        """
        Construye un grafo a partir de listas de datos de vértices y aristas.
        vertices_data: lista de entidades de dominio (almacen, recarga, cliente)
        aristas_data: lista de tuplas (id_origen, id_destino, peso)
        """
        self.logger.info("Construyendo grafo desde datos externos...")
        grafo = Grafo(dirigido=self._dirigido)
        grafo._repositorio_vertices = self._repositorio_vertices
        grafo._repositorio_aristas = self._repositorio_aristas
        id_to_vertice = {}
        for elemento in vertices_data:
            id_elemento = getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_recarga', None)
            if id_elemento is None:
                self.logger.warning(f"[ADVERTENCIA] Vértice inválido no importado: {elemento}")
                continue
            vertice = self._fabrica_vertices.crear(elemento)
            if vertice is not None:
                id_to_vertice[id_elemento] = vertice
                self.logger.info(f"Vértice importado: {id_elemento}")
            else:
                self.logger.warning(f"[ADVERTENCIA] No se pudo crear vértice: {elemento}")
        for (id_u, id_v, peso) in aristas_data:
            u = id_to_vertice.get(id_u)
            v = id_to_vertice.get(id_v)
            if u is None or v is None:
                self.logger.warning(f"[ADVERTENCIA] Arista con vértices no encontrados: ({id_u}, {id_v})")
                continue
            arista = self._fabrica_aristas.crear(u, v, peso)
            if arista is not None:
                self._repositorio_aristas.agregar(arista, (id_u, id_v))
                grafo.insertar_arista(u, v, peso)
                self.logger.info(f"Arista importada: ({id_u}, {id_v}, peso={peso})")
            else:
                self.logger.warning(f"[ADVERTENCIA] No se pudo crear arista: ({id_u}, {id_v}, peso={peso})")
        self.logger.info("Grafo construido desde datos externos.")
        return grafo

    def snapshot(self, tipo: str) -> Dict[str, Any]:
        self.logger.info(f"Obteniendo snapshot: {tipo}")
        return self.snapshots.get(tipo, {})

    def snapshot_grafo(self, grafo):
        self.logger.info("Snapshot de grafo solicitado.")
        return grafo.snapshot()

    def snapshot_n_1(self, vertices_data, aristas_data_n_1):
        self.logger.info("Snapshot n-1 solicitado desde datos.")
        return self.construir_grafo(vertices_data, aristas_data_n_1).snapshot()

    def snapshot_m_aristas(self, vertices_data, aristas_data_m):
        self.logger.info("Snapshot m_aristas solicitado desde datos.")
        return self.construir_grafo(vertices_data, aristas_data_m).snapshot()

    def _generar_arbol_minimo_segmentado(self, vertices: List[Vertice]) -> List[Tuple[int, int, int]]:
        self.logger.info("Generando árbol mínimo segmentado...")
        parent = {}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            parent[find(u)] = find(v)
        # Inicializar parent solo para IDs válidos
        for v in vertices:
            id_v = getattr(v.elemento, 'id_cliente', None) or getattr(v.elemento, 'id_almacenamiento', None) or getattr(v.elemento, 'id_recarga', None)
            parent[id_v] = id_v
        aristas_utiles = []
        for (u, v, peso) in sorted(self.aristas_candidatas, key=lambda x: x[2]):
            if u not in parent or v not in parent:
                continue
            if find(u) != find(v):
                # Aquí se puede agregar validación de segmentación si es necesario
                union(u, v)
                aristas_utiles.append((u, v, peso))
            if len(aristas_utiles) == len(vertices) - 1:
                break
        if len(aristas_utiles) < len(vertices) - 1:
            self.logger.error("[ERROR] No se pudo construir árbol mínimo segmentado: no hay suficientes aristas válidas para conectividad mínima.")
        return aristas_utiles

    def _validar_segmentacion_parcial(self, aristas: List[Tuple[int, int, int]], vertices: List[Vertice]) -> bool:
        self.logger.info("[VALIDACION] Validando segmentación parcial (placeholder)")
        return True

    def _validar_segmentacion_total(self, grafo: Grafo, vertices: List[Vertice]) -> bool:
        self.logger.info("[VALIDACION] Validando segmentación total para todos los pares (almacén, cliente)...")
        def obtener_tipo(elemento):
            if isinstance(elemento, dict):
                return elemento.get('tipo', None)
            return getattr(elemento, 'tipo', None)
        def obtener_id(elemento):
            if isinstance(elemento, dict):
                return elemento.get('id', None)
            return getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_recarga', None)
        idxs_almacen = [i for i, v in enumerate(vertices) if obtener_tipo(v.elemento) == 'almacenamiento']
        idxs_cliente = [i for i, v in enumerate(vertices) if obtener_tipo(v.elemento) == 'cliente']
        idxs_recarga = set(i for i, v in enumerate(vertices) if obtener_tipo(v.elemento) == 'recarga')
        for i in idxs_almacen:
            for j in idxs_cliente:
                origen = vertices[i]
                destino = vertices[j]
                if not self._camino_segmentado(grafo, origen, destino, idxs_recarga, obtener_id=obtener_id):
                    self.logger.warning(f"[VALIDACION] No existe camino segmentado válido entre almacén {obtener_id(origen.elemento)} y cliente {obtener_id(destino.elemento)}")
                    return False
        self.logger.info("[VALIDACION] Todos los pares (almacén, cliente) tienen camino segmentado válido")
        return True

    def _camino_segmentado(self, grafo: Grafo, origen: Vertice, destino: Vertice, recarga_idxs: set, obtener_id=None) -> bool:
        visitados = set()
        cola = deque()
        cola.append((origen, 0))
        def extraer_id(vertice):
            elemento = vertice.elemento
            if obtener_id is not None:
                return obtener_id(elemento)
            if isinstance(elemento, dict):
                return elemento.get('id')
            return getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_recarga', None)
        while cola:
            actual, peso_actual = cola.popleft()
            if actual == destino:
                self.logger.info(f"[CAMINO] Camino segmentado válido encontrado de {self._obtener_id_debug(origen)} a {self._obtener_id_debug(destino)}")
                return True
            visitados.add((actual, peso_actual))
            for vecino in grafo.vecinos(actual):
                arista = grafo.obtener_arista(actual, vecino)
                if hasattr(arista, 'peso'):
                    peso = arista.peso
                elif isinstance(arista.elemento, dict):
                    peso = arista.elemento.get('peso', 1)
                else:
                    peso = 1
                # Validar ANTES de tomar la arista: si el peso de la arista o la suma supera 50, no se puede tomar
                if peso > 50 or (peso_actual + peso) > 50:
                    continue  # No es válido, supera el máximo permitido antes de llegar
                id_vecino = extraer_id(vecino)
                if id_vecino in recarga_idxs:
                    nuevo_peso = 0  # Reinicio por recarga
                else:
                    nuevo_peso = peso_actual + peso
                if (vecino, nuevo_peso) not in visitados:
                    cola.append((vecino, nuevo_peso))
        self.logger.warning(f"[CAMINO] No existe camino segmentado válido de {self._obtener_id_debug(origen)} a {self._obtener_id_debug(destino)}")
        return False

    def _obtener_id_debug(self, vertice):
        elemento = getattr(vertice, 'elemento', vertice)
        if isinstance(elemento, dict):
            return elemento.get('id', None)
        return getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_recarga', None)

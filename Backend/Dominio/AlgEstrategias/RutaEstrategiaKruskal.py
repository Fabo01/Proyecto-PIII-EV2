"""
Estrategia de árbol de expansión mínima usando Kruskal.
Retorna el árbol de expansión mínima como lista de aristas y el peso total.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
import logging

class RutaEstrategiaKruskal(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaKruskal")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[Kruskal] Iniciando cálculo de árbol de expansión mínima: origen={origen}, destino={destino}")
        """
        Calcula el árbol de expansión mínima usando Kruskal, garantizando unicidad de vértices y aristas.
        Solo opera sobre objetos Vertice y Arista únicos del grafo/repositorio.
        """
        # Validación de unicidad de vértices
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        aristas = sorted(grafo.aristas(), key=lambda a: a.peso)
        parent = {}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            pu, pv = find(u), find(v)
            if pu != pv:
                parent[pu] = pv
                return True
            return False
        for v in grafo.vertices():
            parent[v] = v
        mst = []
        peso_total = 0
        for arista in aristas:
            logger.info(f"[Kruskal] Evaluando arista: {arista}")
            # Validación de unicidad de aristas
            assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
            if union(arista.origen, arista.destino):
                mst.append(arista)
                peso_total += arista.peso
        logger.info(f"[Kruskal] Árbol de expansión mínima calculado: {mst}, peso total: {peso_total}")
        return mst, peso_total

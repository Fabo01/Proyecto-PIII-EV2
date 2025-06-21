"""
Estrategia de ruta usando Topological Sort (para grafos dirigidos acíclicos).
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
import logging

class RutaEstrategiaTopologicalSort(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo):
        logger = logging.getLogger("RutaEstrategiaTopologicalSort")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[TopologicalSort] Iniciando cálculo de ruta: origen={origen}, destino={destino}")
        # Validación de unicidad de vértices
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        visitados = set()
        stack = []
        prev = {}
        def dfs(u):
            logger.info(f"[TopologicalSort] Visitando vertice: {u}")
            visitados.add(u)
            for arista in grafo.aristas_incidentes(u, salientes=True):
                logger.info(f"[TopologicalSort] Evaluando arista: {arista}")
                v = arista.destino
                if v not in visitados:
                    prev[v] = u
                    dfs(v)
            stack.append(u)
        dfs(origen)
        stack.reverse()
        if destino not in prev and origen != destino:
            logger.warning(f"[TopologicalSort] No existe ruta posible entre {origen} y {destino}")
            raise ValueError("No existe una ruta posible entre los vertices seleccionados")
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = prev.get(actual, None) if actual != origen else None
        camino.reverse()
        logger.info(f"[TopologicalSort] Ruta calculada: {camino}, costo total: {len(camino)-1}")
        return camino, len(camino)-1

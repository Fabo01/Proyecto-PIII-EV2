"""
Estrategia de ruta usando Dijkstra.
"""
from Backend.Servicios.AlgEstrategias.IRutaEstrategia import IRutaEstrategia
import heapq

class RutaEstrategiaDijkstra(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo):
        # Implementación básica de Dijkstra sobre el grafo del sistema
        dist = {v: float('inf') for v in grafo.vertices()}
        prev = {v: None for v in grafo.vertices()}
        dist[origen] = 0
        heap = [(0, origen)]
        while heap:
            d, u = heapq.heappop(heap)
            if u == destino:
                break
            for arista in grafo.aristas_incidentes(u, salientes=True):
                v = arista.destino
                peso = arista.peso
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    prev[v] = u
                    heapq.heappush(heap, (dist[v], v))
        # Reconstruir camino
        if dist[destino] == float('inf'):
            raise ValueError("No existe una ruta posible entre los nodos seleccionados")
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = prev[actual]
        camino.reverse()
        return camino, dist[destino]

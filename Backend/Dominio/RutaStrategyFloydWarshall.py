"""
Estrategia de ruta usando Floyd-Warshall (para todos los pares, pero aquí solo reconstruye una ruta).
"""
from Backend.Dominio.IRutaStrategy import IRutaStrategy

class RutaStrategyFloydWarshall(IRutaStrategy):
    def calcular_ruta(self, origen, destino, grafo):
        vertices = list(grafo.vertices())
        n = len(vertices)
        idx = {v: i for i, v in enumerate(vertices)}
        dist = [[float('inf')]*n for _ in range(n)]
        next_v = [[None]*n for _ in range(n)]
        for i, v in enumerate(vertices):
            dist[i][i] = 0
            next_v[i][i] = v
        for arista in grafo.aristas():
            i, j = idx[arista.origen], idx[arista.destino]
            dist[i][j] = arista.peso
            next_v[i][j] = arista.destino
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_v[i][j] = next_v[i][k]
        i, j = idx[origen], idx[destino]
        if dist[i][j] == float('inf'):
            raise ValueError("No existe una ruta posible entre los nodos seleccionados")
        # Reconstruir camino
        camino = [origen]
        while origen != destino:
            origen = next_v[idx[origen]][j]
            camino.append(origen)
        return camino, dist[i][j]

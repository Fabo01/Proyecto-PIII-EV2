"""
Estrategia de ruta usando BFS.
"""
from Backend.Dominio.IRutaStrategy import IRutaStrategy
from collections import deque

class RutaStrategyBFS(IRutaStrategy):
    def calcular_ruta(self, origen, destino, grafo):
        visitados = set()
        prev = {origen: None}
        queue = deque([origen])
        while queue:
            u = queue.popleft()
            if u == destino:
                break
            for arista in grafo.aristas_incidentes(u, salientes=True):
                v = arista.destino
                if v not in visitados:
                    visitados.add(v)
                    prev[v] = u
                    queue.append(v)
        if destino not in prev:
            raise ValueError("No existe una ruta posible entre los nodos seleccionados")
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = prev[actual]
        camino.reverse()
        return camino, len(camino)-1

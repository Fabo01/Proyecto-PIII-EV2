"""
Estrategia de ruta usando DFS.
"""
from Backend.Dominio.IRutaStrategy import IRutaStrategy

class RutaStrategyDFS(IRutaStrategy):
    def calcular_ruta(self, origen, destino, grafo):
        visitados = set()
        prev = {}
        stack = [origen]
        while stack:
            u = stack.pop()
            if u == destino:
                break
            if u not in visitados:
                visitados.add(u)
                for arista in grafo.aristas_incidentes(u, salientes=True):
                    v = arista.destino
                    if v not in visitados:
                        prev[v] = u
                        stack.append(v)
        if destino not in prev and origen != destino:
            raise ValueError("No existe una ruta posible entre los nodos seleccionados")
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = prev.get(actual, None) if actual != origen else None
        camino.reverse()
        return camino, len(camino)-1

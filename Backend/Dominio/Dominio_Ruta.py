"""
Clase Ruta para representar una ruta en la simulación logística de drones.
"""

class Ruta:
    """
    Representa una ruta entre dos nodos, incluyendo el camino y el costo total.
    """
    def __init__(self, origen, destino, camino, peso_total, algoritmo):
        self.origen = origen
        self.destino = destino
        self.camino = camino  # Lista de nodos
        self.peso_total = peso_total
        self.algoritmo = algoritmo  # 'kruskal', 'dijkstra', 'bfs', 'dfs', etc.

    def es_valida(self):
        return bool(self.camino) and self.peso_total is not None

    def __str__(self):
        return f"Ruta de {self.origen} a {self.destino} por {self.algoritmo} (Costo: {self.peso_total})"

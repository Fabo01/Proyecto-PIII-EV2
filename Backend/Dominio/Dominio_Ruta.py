"""
Clase Ruta para representar una ruta en la simulación logística de drones.
"""
import logging

class Ruta:
    """
    Representa una ruta entre dos vertices (vértices), incluyendo el camino (lista de vértices), el costo total y el tiempo de cálculo.
    """
    def __init__(self, origen, destino, camino, peso_total, algoritmo, tiempo_calculo=None):
        self.logger = logging.getLogger("Ruta")
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.info(f"[Ruta.__init__] Creando ruta:")
        self.logger.info(f"  origen: {origen}")
        self.logger.info(f"  destino: {destino}")
        self.logger.info(f"  camino: {camino}")
        self.logger.info(f"  peso_total: {peso_total}")
        self.logger.info(f"  algoritmo: {algoritmo}")
        self.logger.info(f"  tiempo_calculo: {tiempo_calculo}")
        self.origen = origen  # Vértice de origen (objeto completo)
        self.destino = destino  # Vértice de destino (objeto completo)
        self.camino = camino  # Lista de vértices (objetos completos)
        self.peso_total = peso_total
        self.algoritmo = algoritmo  # 'kruskal', 'dijkstra', 'bfs', 'dfs', etc.
        self.tiempo_calculo = tiempo_calculo  # Tiempo en segundos

    def es_valida(self):
        self.logger.info(f"[Ruta.es_valida] Validando ruta de {self.origen} a {self.destino} (camino: {self.camino})")
        return bool(self.camino) and self.peso_total is not None

    def __str__(self):
        return f"Ruta de {self.origen} a {self.destino} por {self.algoritmo} (Costo: {self.peso_total}, Tiempo: {self.tiempo_calculo})"

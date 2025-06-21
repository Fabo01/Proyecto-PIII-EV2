"""
Estrategia de ruta usando Floyd-Warshall (para todos los pares, pero aquí solo reconstruye una ruta).
"""
from Backend.Aplicacion.AlgEstrategias.IRutaEstrategia import IRutaEstrategia
import logging

class RutaEstrategiaFloydWarshall(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaFloydWarshall")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[FloydWarshall] Iniciando cálculo de ruta: origen={origen}, destino={destino}, autonomia={autonomia}")
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        vertices = list(grafo.vertices())
        n = len(vertices)
        idx = {v: i for i, v in enumerate(vertices)}
        dist = [[float('inf')]*n for _ in range(n)]
        next_v = [[None]*n for _ in range(n)]
        for i, v in enumerate(vertices):
            dist[i][i] = 0
            next_v[i][i] = v
        for arista in grafo.aristas():
            logger.info(f"[FloydWarshall] Evaluando arista: {arista}")
            assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
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
            logger.warning(f"[FloydWarshall] No existe ruta posible entre {origen} y {destino}")
            raise ValueError("No existe una ruta posible entre los vertices seleccionados")
        camino = [origen]
        while origen != destino:
            origen = next_v[idx[origen]][j]
            camino.append(origen)
        logger.info(f"[FloydWarshall] Ruta calculada: {camino}, costo total: {dist[i][j]}")
        if autonomia is not None and estaciones_recarga is not None:
            camino, _ = self._insertar_recargas_si_necesario(camino, grafo, autonomia, estaciones_recarga)
        return camino, dist[i][j]

    def _insertar_recargas_si_necesario(self, camino, grafo, autonomia, estaciones_recarga):
        if not estaciones_recarga:
            return camino, False
        nuevo_camino = []
        acumulado = 0
        for i in range(len(camino)-1):
            u, v = camino[i], camino[i+1]
            arista = next((a for a in grafo.aristas_incidentes(u, salientes=True) if a.destino == v), None)
            if arista is None:
                raise ValueError("Arista no encontrada en el grafo entre los vértices únicos.")
            peso = arista.peso
            acumulado += peso
            nuevo_camino.append(u)
            if acumulado > autonomia:
                recarga = self._buscar_estacion_recarga(u, estaciones_recarga, grafo)
                if recarga:
                    nuevo_camino.append(recarga)
                    acumulado = 0
        nuevo_camino.append(camino[-1])
        return nuevo_camino, True

    def _buscar_estacion_recarga(self, vertice, estaciones_recarga, grafo):
        for recarga in estaciones_recarga:
            if recarga in grafo.vecinos(vertice):
                return recarga
        return None

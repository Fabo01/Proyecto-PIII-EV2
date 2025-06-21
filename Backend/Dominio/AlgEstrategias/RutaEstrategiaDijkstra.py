"""
Estrategia de ruta usando Dijkstra.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
import heapq
import logging

class RutaEstrategiaDijkstra(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaDijkstra")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[Dijkstra] Iniciando cálculo de ruta: origen={origen}, destino={destino}, autonomia={autonomia}")
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        dist = {v: float('inf') for v in grafo.vertices()}
        prev = {v: None for v in grafo.vertices()}
        dist[origen] = 0
        heap = [(0, origen)]
        while heap:
            d, u = heapq.heappop(heap)
            logger.info(f"[Dijkstra] Visitando vertice: {u}, distancia acumulada: {d}")
            if u == destino:
                logger.info(f"[Dijkstra] vertice destino alcanzado: {destino}")
                break
            for arista in grafo.aristas_incidentes(u, salientes=True):
                logger.info(f"[Dijkstra] Evaluando arista: {arista}")
                assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
                v = arista.destino
                peso = arista.peso
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    prev[v] = u
                    heapq.heappush(heap, (dist[v], v))
        if dist[destino] == float('inf'):
            logger.warning(f"[Dijkstra] No existe ruta posible entre {origen} y {destino}")
            raise ValueError("No existe una ruta posible entre los vertices seleccionados")
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = prev[actual]
        camino.reverse()
        logger.info(f"[Dijkstra] Ruta calculada: {camino}, costo total: {dist[destino]}")
        if autonomia is not None and estaciones_recarga is not None:
            camino, _ = self._insertar_recargas_si_necesario(camino, grafo, autonomia, estaciones_recarga)
        return camino, dist[destino]

    def _insertar_recargas_si_necesario(self, camino, grafo, autonomia, estaciones_recarga):
        """
        Inserta vertices de recarga en el camino si la autonomía se excede.
        """
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
                # Buscar estación de recarga más cercana
                recarga = self._buscar_estacion_recarga(u, estaciones_recarga, grafo)
                if recarga:
                    nuevo_camino.append(recarga)
                    acumulado = 0
        nuevo_camino.append(camino[-1])
        return nuevo_camino, True

    def _buscar_estacion_recarga(self, vertice, estaciones_recarga, grafo):
        """
        Busca la estación de recarga más cercana al vértice dado.
        """
        for recarga in estaciones_recarga:
            if recarga in grafo.vecinos(vertice):
                return recarga
        return None

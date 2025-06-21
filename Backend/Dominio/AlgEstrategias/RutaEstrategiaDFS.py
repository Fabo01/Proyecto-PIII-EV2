"""
Estrategia de ruta usando DFS.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
import logging

class RutaEstrategiaDFS(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaDFS")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[DFS] Iniciando cálculo de ruta: origen={origen}, destino={destino}, autonomia={autonomia}")
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        visitados = set()
        prev = {}
        stack = [origen]
        while stack:
            u = stack.pop()
            logger.info(f"[DFS] Visitando vertice: {u}")
            if u == destino:
                logger.info(f"[DFS] vertice destino alcanzado: {destino}")
                break
            if u not in visitados:
                visitados.add(u)
                for arista in grafo.aristas_incidentes(u, salientes=True):
                    logger.info(f"[DFS] Evaluando arista: {arista}")
                    assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
                    v = arista.destino
                    if v not in visitados:
                        prev[v] = u
                        stack.append(v)
        if destino not in prev and origen != destino:
            logger.warning(f"[DFS] No existe ruta posible entre {origen} y {destino}")
            raise ValueError("No existe una ruta posible entre los vertices seleccionados")
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = prev.get(actual, None) if actual != origen else None
        camino.reverse()
        logger.info(f"[DFS] Ruta calculada: {camino}, costo total: {len(camino)-1}")
        if autonomia is not None and estaciones_recarga is not None:
            camino, _ = self._insertar_recargas_si_necesario(camino, grafo, autonomia, estaciones_recarga)
        return camino, len(camino)-1

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

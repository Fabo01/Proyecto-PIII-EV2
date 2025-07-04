"""
Estrategia de ruta usando Dijkstra.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia

class RutaEstrategiaDijkstra(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        import heapq
        import logging
        logger = logging.getLogger("RutaEstrategiaDijkstra")
        logger.info(f"[Dijkstra] Iniciando cálculo de ruta: origen={origen}, destino={destino}, autonomia={autonomia}")
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'dijkstra', 'origen': origen, 'destino': destino})
        vertices_grafo = grafo.vertices()
        logger.debug(f"[Dijkstra] Vértices en grafo: {[str(v) for v in vertices_grafo]}")
        assert origen in vertices_grafo, f"El vértice de origen no es único o no existe en el grafo: {origen}"
        assert destino in vertices_grafo, f"El vértice de destino no es único o no existe en el grafo: {destino}"

        dist = dict()  # (vertice, energia_restante) -> distancia_total
        prev = dict()  # (vertice, energia_restante) -> (predecesor, energia_previa)
        heap = []  # (distancia_total, energia_restante, vertice)

        energia_inicial = autonomia
        heapq.heappush(heap, (0, energia_inicial, origen))
        dist[(origen, energia_inicial)] = 0
        prev[(origen, energia_inicial)] = (None, None)

        while heap:
            distancia_actual, energia_actual, vertice_actual = heapq.heappop(heap)
            logger.debug(f"[Dijkstra] Visitando: {vertice_actual} | Dist: {distancia_actual} | Energia: {energia_actual}")

            # Si llegamos al destino, reconstruimos el camino
            if vertice_actual == destino:
                logger.info(f"[Dijkstra] Destino alcanzado: {destino} con distancia {distancia_actual}")
                break

            # Si es un vértice de recarga, reiniciar energía
            tipo_elemento = getattr(getattr(vertice_actual, 'elemento', None), 'tipo_elemento', None)
            if tipo_elemento == 'recarga':
                energia_actual = autonomia
                logger.debug(f"[Dijkstra] Recarga en {vertice_actual}, energía reiniciada a {autonomia}")

            for arista in grafo.aristas_incidentes(vertice_actual, salientes=True):
                v = arista.destino
                peso_arista = arista.peso
                # No permitir tomar una arista si el peso excede la autonomía máxima
                if peso_arista > autonomia:
                    continue
                # Solo permitir si la energía actual alcanza para llegar
                if energia_actual < peso_arista:
                    continue
                energia_siguiente = energia_actual - peso_arista
                tipo_destino = getattr(getattr(v, 'elemento', None), 'tipo_elemento', None)
                # Si el destino es recarga, al llegar se reinicia la energía
                if tipo_destino == 'recarga':
                    energia_siguiente = autonomia
                distancia_siguiente = distancia_actual + peso_arista
                estado_siguiente = (v, energia_siguiente)
                if estado_siguiente not in dist or distancia_siguiente < dist[estado_siguiente]:
                    dist[estado_siguiente] = distancia_siguiente
                    prev[estado_siguiente] = (vertice_actual, energia_actual)
                    heapq.heappush(heap, (distancia_siguiente, energia_siguiente, v))
                    logger.debug(f"[Dijkstra] Relajando arista {vertice_actual}->{v} | Peso: {peso_arista} | Nueva dist: {distancia_siguiente} | Nueva energia: {energia_siguiente}")

        # Buscar el mejor estado final en el destino
        estados_destino = [(k, v) for k, v in dist.items() if k[0] == destino]
        if not estados_destino:
            logger.warning(f"[Dijkstra] No se encontró ruta de {origen} a {destino}")
            raise Exception(f"No existe ruta de {origen} a {destino} respetando autonomía y recargas.")
        # Elegir el estado con menor distancia
        (destino_final, energia_final), peso_total = min(estados_destino, key=lambda x: x[1])

        # Reconstruir el camino de vértices
        camino = []
        estado = (destino_final, energia_final)
        while estado in prev and prev[estado][0] is not None:
            vertice, energia = estado
            camino.append(vertice)
            estado = prev[estado]
        camino.append(origen)
        camino = camino[::-1]

        # Reconstruir el camino de aristas
        aristas_camino = []
        for i in range(len(camino) - 1):
            u = camino[i]
            v = camino[i+1]
            arista_uv = next((a for a in grafo.aristas_incidentes(u, salientes=True) if a.destino == v), None)
            assert arista_uv is not None, f"No se encontró arista entre {u} y {v}"
            aristas_camino.append(arista_uv)

        logger.info(f"[Dijkstra] Ruta final: {[str(a) for a in aristas_camino]}, peso_total: {peso_total}")
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('ruta_calculada', {'algoritmo': 'dijkstra', 'camino': aristas_camino, 'peso_total': peso_total})
        return aristas_camino, peso_total

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

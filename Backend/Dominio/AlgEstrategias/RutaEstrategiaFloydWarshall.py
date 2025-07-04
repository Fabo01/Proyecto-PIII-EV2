"""
Estrategia de ruta usando Floyd-Warshall (para todos los pares, pero aquí solo reconstruye una ruta).
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
from collections import deque
import logging

class RutaEstrategiaFloydWarshall(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaFloydWarshall")
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'floydwarshall', 'origen': origen, 'destino': destino})
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
        # Solo considerar aristas que cumplen autonomía
        for arista in grafo.aristas():
            assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
            i, j = idx[arista.origen], idx[arista.destino]
            if arista.peso <= autonomia:
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
            logger.error(f"No existe una ruta posible entre {origen} y {destino}")
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'floydwarshall', 'origen': origen, 'destino': destino, 'error': 'No existe una ruta posible'})
            return [], float('inf')
        # Reconstruir camino_vertices y validar autonomía/recargas
        camino_vertices = [origen]
        actual = origen
        energia_actual = autonomia
        valido = True
        while actual != destino:
            siguiente = next_v[idx[actual]][j]
            if siguiente is None:
                valido = False
                break
            arista = next((a for a in grafo.aristas_incidentes(actual, salientes=True) if a.destino == siguiente), None)
            if arista is None:
                valido = False
                break
            peso = arista.peso
            if peso > autonomia:
                valido = False
                break
            if energia_actual < peso:
                # Intentar recargar en el actual
                es_recarga = hasattr(actual.elemento, 'tipo_elemento') and getattr(actual.elemento, 'tipo_elemento', None) == 'recarga'
                if es_recarga:
                    energia_actual = autonomia
                else:
                    valido = False
                    break
            energia_actual -= peso
            camino_vertices.append(siguiente)
            # Si llegamos a una recarga, reiniciar energía
            es_recarga = hasattr(siguiente.elemento, 'tipo_elemento') and getattr(siguiente.elemento, 'tipo_elemento', None) == 'recarga'
            if es_recarga:
                energia_actual = autonomia
            actual = siguiente
        if not valido:
            logger.error(f"No existe ruta posible entre {origen} y {destino} respetando autonomía y recargas.")
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'floydwarshall', 'origen': origen, 'destino': destino, 'error': 'No existe ruta posible con autonomía y recargas'})
            return [], float('inf')
        # reconstruir lista de aristas y calcular peso_total
        aristas_camino = []
        peso_total = 0
        for k in range(len(camino_vertices) - 1):
            u = camino_vertices[k]
            v = camino_vertices[k+1]
            arista_uv = next((a for a in grafo.aristas_incidentes(u, salientes=True) if a.destino == v), None)
            assert arista_uv is not None, f"No se encontró arista entre {u} y {v} en FloydWarshall"
            aristas_camino.append(arista_uv)
            peso_total += arista_uv.peso
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('ruta_calculada', {'algoritmo': 'floydwarshall', 'camino': aristas_camino, 'peso_total': peso_total})
        logger.info(f"Ruta FloydWarshall calculada: aristas={aristas_camino}, peso_total={peso_total}")
        return aristas_camino, peso_total

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

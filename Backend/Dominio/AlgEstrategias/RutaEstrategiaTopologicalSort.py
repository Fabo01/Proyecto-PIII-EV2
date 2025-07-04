"""
Estrategia de ruta usando Topological Sort (para grafos dirigidos acíclicos).
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
import logging

class RutaEstrategiaTopologicalSort(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaTopologicalSort")
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'topologicalsort', 'origen': origen, 'destino': destino})
        # Validación de unicidad de vértices
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        # Topological sort clásico para obtener orden
        visitados = set()
        stack = []
        def dfs(u):
            visitados.add(u)
            for arista in grafo.aristas_incidentes(u, salientes=True):
                v = arista.destino
                if v not in visitados:
                    dfs(v)
            stack.append(u)
        dfs(origen)
        stack.reverse()
        # Ahora, para cada camino posible desde origen a destino en el orden topológico, buscar respetando autonomía
        from collections import deque
        queue = deque()
        queue.append((origen, autonomia, [origen]))
        # visitados: vertice -> energia_maxima_alcanzada
        visitados = dict()
        visitados[origen] = autonomia
        encontrado = False
        camino_final = None
        while queue:
            vertice_actual, energia_actual, camino_actual = queue.popleft()
            if vertice_actual == destino:
                encontrado = True
                camino_final = list(camino_actual)
                break
            for arista in grafo.aristas_incidentes(vertice_actual, salientes=True):
                v = arista.destino
                peso = arista.peso
                if peso > autonomia:
                    continue
                es_recarga = hasattr(v.elemento, 'tipo_elemento') and getattr(v.elemento, 'tipo_elemento', None) == 'recarga'
                if energia_actual >= peso:
                    energia_nueva = energia_actual - peso
                    if es_recarga:
                        energia_nueva = autonomia
                    energia_max_previa = visitados.get(v, -1)
                    if energia_nueva <= energia_max_previa:
                        continue
                    visitados[v] = energia_nueva
                    if v not in camino_actual:  # evitar ciclos
                        queue.append((v, energia_nueva, camino_actual + [v]))
        try:
            if not encontrado:
                if hasattr(self, 'notificar_observadores'):
                    self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'topologicalsort', 'origen': origen, 'destino': destino, 'error': 'No existe una ruta posible'})
                logger.error(f"TopologicalSort no encontró ruta entre {origen} y {destino}")
                return [], float('inf')
            camino_vertices = camino_final
            # reconstruir lista de aristas y calcular peso_total
            aristas_camino = []
            peso_total = 0
            for i in range(len(camino_vertices) - 1):
                u = camino_vertices[i]
                v = camino_vertices[i+1]
                arista_uv = next((a for a in grafo.aristas_incidentes(u, salientes=True) if a.destino == v), None)
                assert arista_uv is not None, f"No se encontró arista entre {u} y {v}"
                aristas_camino.append(arista_uv)
                peso_total += arista_uv.peso
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('ruta_calculada', {'algoritmo': 'topologicalsort', 'camino': aristas_camino, 'peso_total': peso_total})
            logger.info(f"Ruta TopologicalSort calculada: aristas={aristas_camino}, peso_total={peso_total}")
            return aristas_camino, peso_total
        except Exception as e:
            logger.error(f"Error en TopologicalSort: {str(e)}", exc_info=True)
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'topologicalsort', 'origen': origen, 'destino': destino, 'error': str(e)})
            return [], float('inf')

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

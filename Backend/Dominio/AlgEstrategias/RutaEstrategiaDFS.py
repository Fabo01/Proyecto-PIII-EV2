"""
Estrategia de ruta usando DFS.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
import logging

class RutaEstrategiaDFS(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaDFS")
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'dfs', 'origen': origen, 'destino': destino})
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."

        stack = [(origen, autonomia)]
        prev = dict()  # (vertice, energia_restante) -> (predecesor, energia_previa, arista)
        # visitados: vertice -> energia_maxima_alcanzada
        visitados = dict()
        prev[(origen, autonomia)] = (None, None, None)
        visitados[origen] = autonomia

        encontrado = False
        estado_final = None

        while stack:
            vertice_actual, energia_actual = stack.pop()
            if vertice_actual == destino:
                encontrado = True
                estado_final = (vertice_actual, energia_actual)
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
                    prev[(v, energia_nueva)] = (vertice_actual, energia_actual, arista)
                    visitados[v] = energia_nueva
                    stack.append((v, energia_nueva))
        try:
            if not encontrado:
                if hasattr(self, 'notificar_observadores'):
                    self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'dfs', 'origen': origen, 'destino': destino, 'error': 'No existe una ruta posible'})
                logger.error(f"DFS no encontró ruta entre {origen} y {destino}")
                raise ValueError("No existe una ruta posible entre los vertices seleccionados")
            # Reconstruir camino de vértices y aristas
            camino_vertices = []
            aristas_camino = []
            estado = estado_final
            while estado and prev[estado][0] is not None:
                v, energia = estado
                camino_vertices.append(v)
                predecesor, energia_previa, arista = prev[estado]
                if arista is not None:
                    aristas_camino.append(arista)
                estado = (predecesor, energia_previa)
            camino_vertices.append(origen)
            camino_vertices.reverse()
            aristas_camino = aristas_camino[::-1]
            peso_total = sum(a.peso for a in aristas_camino)
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('ruta_calculada', {'algoritmo': 'dfs', 'camino': aristas_camino, 'peso_total': peso_total})
            logger.info(f"Ruta DFS calculada: aristas={aristas_camino}, peso_total={peso_total}")
            return aristas_camino, peso_total
        except Exception as e:
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'dfs', 'origen': origen, 'destino': destino, 'error': str(e)})
            raise
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

"""
Estrategia de ruta usando DFS.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia

class RutaEstrategiaDFS(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'dfs', 'origen': origen, 'destino': destino})
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
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
                    assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
                    v = arista.destino
                    if v not in visitados:
                        prev[v] = u
                        stack.append(v)
        try:
            if destino not in prev and origen != destino:
                if hasattr(self, 'notificar_observadores'):
                    self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'dfs', 'origen': origen, 'destino': destino, 'error': 'No existe una ruta posible'})
                raise ValueError("No existe una ruta posible entre los vertices seleccionados")
            camino = []
            actual = destino
            while actual is not None:
                camino.append(actual)
                actual = prev.get(actual, None) if actual != origen else None
            camino.reverse()
            if autonomia is not None and estaciones_recarga is not None:
                camino, _ = self._insertar_recargas_si_necesario(camino, grafo, autonomia, estaciones_recarga)
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('ruta_calculada', {'algoritmo': 'dfs', 'camino': camino})
            return camino
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

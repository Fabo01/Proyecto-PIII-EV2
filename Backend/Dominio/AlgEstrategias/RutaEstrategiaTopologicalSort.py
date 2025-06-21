"""
Estrategia de ruta usando Topological Sort (para grafos dirigidos acíclicos).
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia

class RutaEstrategiaTopologicalSort(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo):
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'topologicalsort', 'origen': origen, 'destino': destino})
        # Validación de unicidad de vértices
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
        visitados = set()
        stack = []
        prev = {}
        def dfs(u):
            visitados.add(u)
            for arista in grafo.aristas_incidentes(u, salientes=True):
                v = arista.destino
                if v not in visitados:
                    prev[v] = u
                    dfs(v)
            stack.append(u)
        dfs(origen)
        stack.reverse()
        try:
            if destino not in prev and origen != destino:
                if hasattr(self, 'notificar_observadores'):
                    self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'topologicalsort', 'origen': origen, 'destino': destino, 'error': 'No existe una ruta posible'})
                raise ValueError("No existe una ruta posible entre los vertices seleccionados")
            camino = []
            actual = destino
            while actual is not None:
                camino.append(actual)
                actual = prev.get(actual, None) if actual != origen else None
            camino.reverse()
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('ruta_calculada', {'algoritmo': 'topologicalsort', 'camino': camino})
            return camino
        except Exception as e:
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'topologicalsort', 'origen': origen, 'destino': destino, 'error': str(e)})
            raise

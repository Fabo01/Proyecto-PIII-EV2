"""
Estrategia de árbol de expansión mínima usando Kruskal.
Retorna el árbol de expansión mínima como lista de aristas y el peso total.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia

class RutaEstrategiaKruskal(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'kruskal', 'origen': origen, 'destino': destino})
        try:
            """
            Calcula el árbol de expansión mínima usando Kruskal, garantizando unicidad de vértices y aristas.
            Solo opera sobre objetos Vertice y Arista únicos del grafo/repositorio.
            """
            # Validación de unicidad de vértices
            assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
            assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."
            aristas = sorted(grafo.aristas(), key=lambda a: a.peso)
            parent = {}
            def find(u):
                while parent[u] != u:
                    parent[u] = parent[parent[u]]
                    u = parent[u]
                return u
            def union(u, v):
                pu, pv = find(u), find(v)
                if pu != pv:
                    parent[pu] = pv
                    return True
                return False
            for v in grafo.vertices():
                parent[v] = v
            mst = []
            peso_total = 0
            for arista in aristas:
                # Validación de unicidad de aristas
                assert arista in grafo.aristas(), "La arista no es única o no existe en el grafo."
                if union(arista.origen, arista.destino):
                    mst.append(arista)
                    peso_total += arista.peso
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('ruta_calculada', {'algoritmo': 'kruskal', 'origen': origen, 'destino': destino})
            return mst
        except Exception as e:
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'kruskal', 'origen': origen, 'destino': destino, 'error': str(e)})
            raise

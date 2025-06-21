"""
Clase Ruta para representar una ruta en la simulación logística de drones.
Incluye soporte para observadores de eventos de dominio.
"""

class Ruta:
    """
    Representa una ruta entre dos vertices (vértices), incluyendo el camino (lista de vértices), el costo total y el tiempo de cálculo.
    Permite agregar observadores para auditar eventos de negocio.
    """
    def __init__(self, origen, destino, camino, peso_total, algoritmo, tiempo_calculo=None):
        """
        Inicializa una ruta con origen, destino, camino, peso total, algoritmo y tiempo de calculo.
        Notifica a los observadores la creación de la ruta.
        """
        self.origen = origen  # Vértice de origen (objeto completo)
        self.destino = destino  # Vértice de destino (objeto completo)
        self.camino = camino  # Lista de vértices (objetos completos)
        self.peso_total = peso_total
        self.algoritmo = algoritmo  # 'kruskal', 'dijkstra', 'bfs', 'dfs', etc.
        self.tiempo_calculo = tiempo_calculo  # Tiempo en segundos
        self._observadores = set()
        # Notificar a los observadores la creación de la ruta
        self.notificar_observadores('ruta_creada', {'origen': origen, 'destino': destino, 'camino': camino, 'peso_total': peso_total, 'algoritmo': algoritmo, 'tiempo_calculo': tiempo_calculo})

    def agregar_observador(self, observador):
        """
        Agrega un observador para recibir notificaciones de eventos de la ruta.
        """
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        """
        Quita un observador para dejar de recibir notificaciones de eventos de la ruta.
        """
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores registrados sobre un evento ocurrido en la ruta.
        """
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def es_valida(self):
        """
        Verifica si la ruta es valida segun las reglas de negocio (peso maximo, conectividad, etc).
        Notifica a los observadores si la ruta no es válida.
        """
        if self.peso_total is None or self.peso_total > 50:
            self.notificar_observadores('error_ruta', {'origen': self.origen, 'destino': self.destino, 'error': 'Peso total excede el máximo permitido.'})
            return False
        if not self.camino or self.origen != self.camino[0] or self.destino != self.camino[-1]:
            self.notificar_observadores('error_ruta', {'origen': self.origen, 'destino': self.destino, 'error': 'Camino inválido.'})
            return False
        return True

    def serializar(self):
        """
        Serializa la ruta en un diccionario.
        Notifica a los observadores que la ruta ha sido serializada.
        """
        self.notificar_observadores('ruta_serializada', None)
        return {'origen': str(self.origen), 'destino': str(self.destino), 'camino': [str(v) for v in self.camino], 'peso_total': self.peso_total, 'algoritmo': self.algoritmo}

    def __str__(self):
        return f"Ruta {self.origen} -> {self.destino} (Peso: {self.peso_total}, Algoritmo: {self.algoritmo})"

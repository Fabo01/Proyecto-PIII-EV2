"""
Observer concreto para actualizar estadísticas en tiempo real.
"""
from Backend.Dominio.Interfaces.IntObs.IObserver import IObserver

class ObserverEstadisticas(IObserver):
    def __init__(self, servicio_estadisticas):
        self.servicio_estadisticas = servicio_estadisticas

    def actualizar(self, evento, datos=None):
        if evento == "pedido_entregado":
            self.servicio_estadisticas.registrar_entrega(datos)
        elif evento == "ruta_calculada":
            self.servicio_estadisticas.registrar_ruta(datos)
        # Agregar más eventos según sea necesario

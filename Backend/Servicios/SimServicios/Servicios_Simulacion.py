from Backend.Dominio.Interfaces.IntSim.ISimulacionDominioService import ISimulacionDominioService
from Backend.Dominio.Simulacion_dominio import Simulacion

class SimulacionDominioService(ISimulacionDominioService):
    """
    Servicio de dominio para la simulacion.
    Orquesta la logica de negocio usando la instancia de Simulacion inyectada.
    """
    def __init__(self, simulacion: Simulacion):
        self._sim = simulacion

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int) -> None:
        self._sim.iniciar_simulacion(n_vertices, m_aristas, n_pedidos)

    def obtener_vertices(self):
        return self._sim.obtener_vertices()

    def obtener_aristas(self):
        return self._sim.obtener_aristas()

    def obtener_clientes(self):
        return self._sim.obtener_clientes()

    def obtener_almacenamientos(self):
        return self._sim.obtener_almacenamientos()

    def obtener_recargas(self):
        return self._sim.obtener_recargas()

    def obtener_pedidos(self):
        return self._sim.obtener_pedidos()

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = None):
        return self._sim.calcular_ruta_pedido(id_pedido, algoritmo)

    def marcar_pedido_entregado(self, id_pedido: int):
        return self._sim.marcar_pedido_entregado(id_pedido)

    def buscar_pedido(self, id_pedido: int):
        return self._sim.buscar_pedido(id_pedido)

    def obtener_cliente(self, id_cliente: int):
        return self._sim.repo_clientes.obtener(id_cliente)

    def obtener_almacenamiento(self, id_almacenamiento: int):
        return self._sim.repo_almacenamientos.obtener(id_almacenamiento)

    def obtener_recarga(self, id_recarga: int):
        return self._sim.repo_recargas.obtener(id_recarga)

    def obtener_pedido(self, id_pedido: int):
        return self._sim.repo_pedidos.obtener(id_pedido)

    def obtener_ruta(self, id_ruta: int):
        return self._sim.repo_rutas.obtener(id_ruta)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        return self._sim.obtener_rutas_mas_frecuentes(top)

    def obtener_rutas_hashmap(self):
        return self._sim.obtener_rutas_hashmap()

    def obtener_vertices_hashmap(self):
        return self._sim.obtener_vertices_hashmap()

    def obtener_aristas_hashmap(self):
        return self._sim.obtener_aristas_hashmap()

    def obtener_clientes_hashmap(self):
        return self._sim.obtener_clientes_hashmap()

    def obtener_almacenamientos_hashmap(self):
        return self._sim.obtener_almacenamientos_hashmap()

    def obtener_recargas_hashmap(self):
        return self._sim.obtener_recargas_hashmap()

    def obtener_pedidos_hashmap(self):
        return self._sim.obtener_pedidos_hashmap()

    def obtener_estadisticas(self):
        rutas_freq = self.obtener_rutas_mas_frecuentes()
        vertices_visitados = {}
        return {
            "rutas_mas_frecuentes": rutas_freq,
            "vertices_mas_visitados": vertices_visitados,
            "tiempo_respuesta": 0.0
        }

    def set_estrategia_ruta(self, estrategia):
        self._sim.set_estrategia_ruta(estrategia)

    def notificar_evento(self, evento, datos=None):
        self._sim.notificar_observadores(evento, datos)

    def reiniciar_todo(self):
        self._sim.reiniciar_todo()


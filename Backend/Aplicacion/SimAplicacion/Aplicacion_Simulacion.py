from Backend.Dominio.Interfaces.ISimulacionAplicacionService import ISimulacionAplicacionService
from Backend.Servicios.SimServicios.Servicios_Simulacion import SimulacionDominioService

class SimulacionAplicacionService(ISimulacionAplicacionService):
    """
    Capa de aplicación para la simulación, delega todas las acciones al servicio de dominio.
    """
    def __init__(self, dominio_service: SimulacionDominioService):
        self._serv = dominio_service

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int, estrategia_ruta: str = None):
        return self._serv.iniciar_simulacion(n_vertices, m_aristas, n_pedidos)

    def reiniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int):
        return self._serv.iniciar_simulacion(n_vertices, m_aristas, n_pedidos)

    def obtener_vertices(self):
        return self._serv.obtener_vertices()

    def obtener_aristas(self):
        return self._serv.obtener_aristas()

    def obtener_clientes(self):
        return self._serv.obtener_clientes()

    def obtener_almacenamientos(self):
        return self._serv.obtener_almacenamientos()

    def obtener_recargas(self):
        return self._serv.obtener_recargas()

    def obtener_pedidos(self):
        return self._serv.obtener_pedidos()

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = None):
        return self._serv.calcular_ruta_pedido(id_pedido, algoritmo)

    def marcar_pedido_entregado(self, id_pedido: int):
        return self._serv.marcar_pedido_entregado(id_pedido)

    def buscar_pedido(self, id_pedido: int):
        return self._serv.buscar_pedido(id_pedido)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        return self._serv.obtener_rutas_mas_frecuentes(top)

    def obtener_rutas_hashmap(self):
        return self._serv.obtener_rutas_hashmap()

    def obtener_vertices_hashmap(self):
        return self._serv.obtener_vertices_hashmap()

    def obtener_aristas_hashmap(self):
        return self._serv.obtener_aristas_hashmap()

    def obtener_clientes_hashmap(self):
        return self._serv.obtener_clientes_hashmap()

    def obtener_almacenamientos_hashmap(self):
        return self._serv.obtener_almacenamientos_hashmap()

    def obtener_recargas_hashmap(self):
        return self._serv.obtener_recargas_hashmap()

    def obtener_pedidos_hashmap(self):
        return self._serv.obtener_pedidos_hashmap()


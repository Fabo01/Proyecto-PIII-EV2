from Backend.Interfaces.ISimulacionDominioService import ISimulacionDominioService
from Backend.Dominio.Simulacion_dominio import Simulacion
from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.Dominio.Dominio_Almacenamiento import Almacenamiento
from Backend.Dominio.Dominio_Recarga import Recarga
from Backend.Dominio.Dominio_Pedido import Pedido
from Backend.Dominio.Dominio_Ruta import Ruta
from Backend.Infraestructura.Modelos.Modelo_Vertice import Vertice

class SimulacionDominioService(ISimulacionDominioService):
    """
    Servicio de dominio para la simulación, accede siempre a la instancia Singleton de Simulacion.
    """
    def iniciar_simulacion(self, n_nodos: int, m_aristas: int, n_pedidos: int):
        Simulacion.reiniciar_instancia(n_nodos, m_aristas, n_pedidos)
        return Simulacion.obtener_instancia()

    def _check_simulacion(self):
        if Simulacion._instancia is None:
            raise Exception("Simulación no iniciada")

    def obtener_nodos(self):
        self._check_simulacion()
        return list(Simulacion.obtener_instancia().grafo.vertices())

    def obtener_aristas(self):
        self._check_simulacion()
        return list(Simulacion.obtener_instancia().grafo.aristas())

    def obtener_clientes(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().clientes

    def obtener_almacenamientos(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().almacenamientos

    def obtener_recargas(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().estaciones_recarga

    def obtener_pedidos(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().pedidos

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str):
        self._check_simulacion()
        return Simulacion.obtener_instancia().calcular_ruta_pedido(id_pedido, algoritmo)

    def marcar_pedido_entregado(self, id_pedido: int):
        self._check_simulacion()
        pedido = Simulacion.obtener_instancia().obtener_pedido(id_pedido)
        pedido.marcar_entregado()
        return pedido

    def buscar_pedido(self, id_pedido: int):
        self._check_simulacion()
        return Simulacion.obtener_instancia().obtener_pedido(id_pedido)

    def obtener_rutas_mas_frecuentes(self, top=5):
        self._check_simulacion()
        return Simulacion.obtener_instancia().rutas_mas_frecuentes(top)

    def obtener_estadisticas(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().obtener_estadisticas()

    def obtener_todos_los_caminos_floyd_warshall(self):
        """
        Retorna los resultados de Floyd-Warshall (distancias y caminos) desde la simulación.
        """
        sim = Simulacion.obtener_instancia()
        return sim.calcular_todos_los_caminos_floyd_warshall()

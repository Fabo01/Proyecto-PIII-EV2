from Backend.Dominio.Interfaces.IntSim.ISimulacionAplicacionService import ISimulacionAplicacionService
from Backend.Servicios.SimServicios.Servicios_Simulacion import SimulacionDominioService
from Backend.Dominio.Simulacion_dominio import Simulacion
from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas

class SimulacionAplicacionService(ISimulacionAplicacionService):
    """
    Capa de aplicacion para la simulacion, delega todas las acciones al servicio de dominio.
    """
    def __init__(self, dominio_service: SimulacionDominioService = None):
        if dominio_service is None:
            simulacion = Simulacion(
                RepositorioClientes(), RepositorioAlmacenamientos(),
                RepositorioRecargas(), RepositorioVertices(),
                RepositorioAristas(), RepositorioPedidos(), RepositorioRutas()
            )
            dominio_service = SimulacionDominioService(simulacion)
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

    def set_estrategia_ruta(self, estrategia):
        return self._serv.set_estrategia_ruta(estrategia)

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = None):
        return self._serv.calcular_ruta_pedido(id_pedido, algoritmo)

    def marcar_pedido_entregado(self, id_pedido: int):
        return self._serv.marcar_pedido_entregado(id_pedido)

    def buscar_pedido(self, id_pedido: int):
        return self._serv.buscar_pedido(id_pedido)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        return self._serv.obtener_rutas_mas_frecuentes(top)

    def obtener_rutas_hashmap(self):
        orig = self._serv.obtener_rutas_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def obtener_vertices_hashmap(self):
        orig = self._serv.obtener_vertices_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def obtener_aristas_hashmap(self):
        orig = self._serv.obtener_aristas_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def obtener_clientes_hashmap(self):
        orig = self._serv.obtener_clientes_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def obtener_almacenamientos_hashmap(self):
        orig = self._serv.obtener_almacenamientos_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def obtener_recargas_hashmap(self):
        orig = self._serv.obtener_recargas_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def obtener_pedidos_hashmap(self):
        orig = self._serv.obtener_pedidos_hashmap()
        return {str(k): v for k, v in (orig or {}).items()}

    def estado_actual(self):
        return {
            "clientes": self.listar_clientes(),
            "almacenamientos": self.listar_almacenamientos(),
            "recargas": self.listar_recargas(),
            "pedidos": self.listar_pedidos(),
            "rutas": self.listar_rutas(),
            "estado": "iniciada",
            "mensaje": None
        }

    def listar_clientes(self):
        return self.obtener_clientes()

    def listar_almacenamientos(self):
        return self.obtener_almacenamientos()

    def listar_recargas(self):
        return self.obtener_recargas()

    def listar_pedidos(self):
        return self.obtener_pedidos()

    def listar_rutas(self):
        try:
            return self._serv.obtener_rutas_mas_frecuentes()
        except Exception:
            return []

    def obtener_estadisticas(self):
        return self._serv.obtener_estadisticas()

    def obtener_cliente(self, id_cliente: int):
        return self._serv.obtener_cliente(id_cliente)

    def obtener_almacenamiento(self, id_almacenamiento: int):
        return self._serv.obtener_almacenamiento(id_almacenamiento)

    def obtener_recarga(self, id_recarga: int):
        return self._serv.obtener_recarga(id_recarga)

    def obtener_pedido(self, id_pedido: int):
        return self._serv.obtener_pedido(id_pedido)

    def obtener_ruta(self, id_ruta: int):
        return self._serv.obtener_ruta(id_ruta)

    def notificar_evento(self, evento, datos=None):
        return self._serv.notificar_evento(evento, datos)

    def reiniciar_todo(self):
        return self._serv.reiniciar_todo()


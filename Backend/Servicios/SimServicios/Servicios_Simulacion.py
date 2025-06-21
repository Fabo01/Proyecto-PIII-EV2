from Backend.Servicios.SimServicios.ISimulacionDominioService import ISimulacionDominioService
from Backend.Dominio.Simulacion_dominio import Simulacion
from Backend.Infraestructura.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.Infraestructura.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.Infraestructura.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.Infraestructura.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.Infraestructura.Mapeadores.MapeadorRuta import MapeadorRuta

class SimulacionDominioService(ISimulacionDominioService):
    """
    Servicio de dominio para la simulación, accede siempre a la instancia Singleton de Simulacion.
    Permite inyectar la estrategia de ruta y cambiarla dinámicamente.
    Maneja errores y casos extremos, y desacopla la lógica de DTOs del dominio.
    """
    def __init__(self, estrategia_ruta=None):
        self.estrategia_ruta = estrategia_ruta
        if Simulacion._instancia is not None and estrategia_ruta is not None:
            Simulacion._instancia.set_estrategia_ruta(estrategia_ruta)
        self.simulacion = Simulacion.obtener_instancia()

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int, estrategia_ruta=None):
        Simulacion.reiniciar_instancia(n_vertices, m_aristas, n_pedidos)
        if estrategia_ruta:
            Simulacion._instancia.set_estrategia_ruta(estrategia_ruta)
        elif self.estrategia_ruta:
            Simulacion._instancia.set_estrategia_ruta(self.estrategia_ruta)
        return Simulacion.obtener_instancia()

    def set_estrategia_ruta(self, nombre_estrategia):
        self.estrategia_ruta = nombre_estrategia
        if Simulacion._instancia is not None:
            Simulacion._instancia.set_estrategia_ruta(nombre_estrategia)

    def _check_simulacion(self):
        if Simulacion._instancia is None:
            raise Exception("La simulación no ha sido inicializada")

    def obtener_vertices(self):
        self._check_simulacion()
        return list(Simulacion.obtener_instancia().grafo.vertices())

    def obtener_aristas(self):
        self._check_simulacion()
        return list(Simulacion.obtener_instancia().grafo.aristas())

    def obtener_clientes(self, incluir_pedidos: bool = True):
        self._check_simulacion()
        clientes = Simulacion.obtener_instancia().clientes
        return [MapeadorCliente.a_dto(cliente, incluir_pedidos=incluir_pedidos) for cliente in clientes]

    def obtener_almacenamientos(self, incluir_pedidos: bool = True):
        self._check_simulacion()
        almacenamientos = Simulacion.obtener_instancia().almacenamientos
        return [MapeadorAlmacenamiento.a_dto(almacen, incluir_pedidos=incluir_pedidos) for almacen in almacenamientos]

    def obtener_recargas(self):
        self._check_simulacion()
        recargas = Simulacion.obtener_instancia().estaciones_recarga
        return [MapeadorRecarga.a_dto(recarga) for recarga in recargas]

    def obtener_pedidos(self, incluir_cliente: bool = True, incluir_almacenamiento: bool = True):
        self._check_simulacion()
        pedidos = Simulacion.obtener_instancia().pedidos
        return [MapeadorPedido.a_dto(pedido, incluir_cliente=incluir_cliente, incluir_almacenamiento=incluir_almacenamiento) for pedido in pedidos]

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = None):
        import logging
        logger = logging.getLogger("SimulacionDominioService")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[SimulacionDominioService.calcular_ruta_pedido] Solicitando cálculo de ruta para pedido {id_pedido} con algoritmo {algoritmo}")
        self._check_simulacion()
        resultado = Simulacion.obtener_instancia().calcular_ruta_pedido(id_pedido, algoritmo)
        logger.info(f"[SimulacionDominioService.calcular_ruta_pedido] Resultado DTO: {resultado}")
        return resultado

    def marcar_pedido_entregado(self, id_pedido: int):
        self._check_simulacion()
        pedido = Simulacion.obtener_instancia().buscar_pedido(id_pedido)
        if pedido is None:
            raise Exception(f"Pedido {id_pedido} no encontrado")
        pedido.marcar_entregado()
        return pedido

    def buscar_pedido(self, id_pedido: int, incluir_cliente: bool = True, incluir_almacenamiento: bool = True):
        self._check_simulacion()
        pedido = Simulacion.obtener_instancia().buscar_pedido(id_pedido)
        if pedido is None:
            return None
        return MapeadorPedido.a_dto(pedido, incluir_cliente=incluir_cliente, incluir_almacenamiento=incluir_almacenamiento)

    def obtener_rutas_mas_frecuentes(self, top=5):
        self._check_simulacion()
        return Simulacion.obtener_instancia().obtener_rutas_mas_frecuentes(top)

    def obtener_estadisticas(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().obtener_estadisticas()

    def obtener_todos_los_caminos_floyd_warshall(self):
        self._check_simulacion()
        return Simulacion.obtener_instancia().obtener_todos_los_caminos_floyd_warshall()

    def obtener_clientes_hashmap(self):
        """
        Retorna el hashmap de clientes (ID → Objeto Cliente).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_clientes.obtener_hashmap()

    def obtener_almacenamientos_hashmap(self):
        """
        Retorna el hashmap de almacenamientos (ID → Objeto Almacenamiento).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_almacenamientos.obtener_hashmap()

    def obtener_recargas_hashmap(self):
        """
        Retorna el hashmap de recargas (ID → Objeto Recarga).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_recargas.obtener_hashmap()

    def obtener_pedidos_hashmap(self):
        """
        Retorna el hashmap de pedidos (ID → Objeto Pedido).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_pedidos.obtener_hashmap()

    def obtener_vertices_hashmap(self):
        """
        Retorna el hashmap de vértices (ID → Objeto Vertice).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_vertices.obtener_hashmap()
    
    def obtener_aristas_hashmap(self):
        """
        Retorna el hashmap de aristas (ID → Objeto Arista).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_aristas.obtener_hashmap()
    
    def obtener_rutas_hashmap(self):
        """
        Retorna el hashmap de rutas (ID → Objeto Ruta).
        """
        self._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.repositorio_rutas.obtener_hashmap()


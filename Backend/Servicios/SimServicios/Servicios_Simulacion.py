from Backend.Dominio.Interfaces.IntSim.ISimulacionDominioService import ISimulacionDominioService
from Backend.Dominio.Simulacion_dominio import Simulacion

class SimulacionDominioService(ISimulacionDominioService):
    """
    Servicio de dominio para la simulación.
    Orquesta la lógica de negocio usando la instancia de Simulacion inyectada.
    """
    def __init__(self, simulacion: Simulacion):
        # Inyección de la instancia de dominio
        self._sim = simulacion

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int) -> None:
        # Lógica de inicialización delegada a repositorios
        # Ejemplo: poblar repositorios de vértices y aristas
        self._sim.repo_vertices.limpiar()
        self._sim.repo_aristas.limpiar()
        self._sim.repo_clientes.limpiar()
        self._sim.repo_almacenamientos.limpiar()
        self._sim.repo_recargas.limpiar()
        self._sim.repo_pedidos.limpiar()
        self._sim.repo_rutas.limpiar()
        # ... lógica para generar vértices y aristas usando repositorios ...
        # generar pedidos a través de repo_pedidos ...

    def obtener_vertices(self):
        return self._sim.repo_vertices.todos()

    def obtener_aristas(self):
        return self._sim.repo_aristas.todos()

    def obtener_clientes(self):
        return self._sim.repo_clientes.todos()

    def obtener_almacenamientos(self):
        return self._sim.repo_almacenamientos.todos()

    def obtener_recargas(self):
        return self._sim.repo_recargas.todos()

    def obtener_pedidos(self):
        return self._sim.repo_pedidos.todos()

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str):
        pedido = self._sim.repo_pedidos.obtener(id_pedido)
        # Delegar cálculo de ruta estratégico al grafo por repositorio de rutas
        ruta = self._sim.repo_rutas.obtener(id_pedido)
        return ruta

    def marcar_pedido_entregado(self, id_pedido: int):
        pedido = self._sim.repo_pedidos.obtener(id_pedido)
        pedido.marcar_entregado()
        # Persistir estado
        self._sim.repo_pedidos.agregar(pedido)

    def buscar_pedido(self, id_pedido: int):
        return self._sim.repo_pedidos.obtener(id_pedido)
    
    def obtener_cliente(self, id_cliente: int):
        """Obtiene un cliente específico del repositorio."""
        return self._sim.repo_clientes.obtener(id_cliente)

    def obtener_almacenamiento(self, id_almacenamiento: int):
        """Obtiene un almacenamiento específico del repositorio."""
        return self._sim.repo_almacenamientos.obtener(id_almacenamiento)

    def obtener_recarga(self, id_recarga: int):
        """Obtiene una recarga específica del repositorio."""
        return self._sim.repo_recargas.obtener(id_recarga)

    def obtener_pedido(self, id_pedido: int):
        """Obtiene un pedido específico del repositorio."""
        return self._sim.repo_pedidos.obtener(id_pedido)

    def obtener_ruta(self, id_ruta: int):
        """Obtiene una ruta específica del repositorio."""
        return self._sim.repo_rutas.obtener(id_ruta)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        # Suponiendo repositorio de rutas almacena frecuencias
        return self._sim.repo_rutas.todos()[:top]

    def obtener_rutas_hashmap(self):
        return self._sim.repo_rutas.obtener_hashmap()

    def obtener_vertices_hashmap(self):
        return self._sim.repo_vertices.obtener_hashmap()

    def obtener_aristas_hashmap(self):
        return self._sim.repo_aristas.obtener_hashmap()

    def obtener_clientes_hashmap(self):
        return self._sim.repo_clientes.obtener_hashmap()

    def obtener_almacenamientos_hashmap(self):
        return self._sim.repo_almacenamientos.obtener_hashmap()

    def obtener_recargas_hashmap(self):
        return self._sim.repo_recargas.obtener_hashmap()

    def obtener_pedidos_hashmap(self):
        return self._sim.repo_pedidos.obtener_hashmap()

    def obtener_estadisticas(self):
        """Calcula estadísticas básicas de la simulación."""
        rutas_freq = self.obtener_rutas_mas_frecuentes()
        # Placeholder para vertices más visitados; se puede extender según necesidad
        vertices_visitados = {}
        return {
            "rutas_mas_frecuentes": rutas_freq,
            "vertices_mas_visitados": vertices_visitados,
            "tiempo_respuesta": 0.0
        }


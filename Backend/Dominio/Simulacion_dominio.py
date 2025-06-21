from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas

class Simulacion:
    """
    Singleton que mantiene una única instancia de la simulación.
    Repositorios inyectados y expuestos como propiedades de solo lectura.
    Solo contiene lógica de dominio básica usando repositorios.
    """
    _instancia = None

    def __new__(cls, repo_clientes=None, repo_almacenamientos=None,
                repo_recargas=None, repo_vertices=None,
                repo_aristas=None, repo_pedidos=None,
                repo_rutas=None):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Inicializar solo una vez
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self, repo_clientes: RepositorioClientes,
                 repo_almacenamientos: RepositorioAlmacenamientos,
                 repo_recargas: RepositorioRecargas,
                 repo_vertices: RepositorioVertices,
                 repo_aristas: RepositorioAristas,
                 repo_pedidos: RepositorioPedidos,
                 repo_rutas: RepositorioRutas):
        # Configuración de repositorios inyectados en la primera inicialización
        if not getattr(self, '_inicializado', False):
            self._repo_clientes = repo_clientes
            self._repo_almacenamientos = repo_almacenamientos
            self._repo_recargas = repo_recargas
            self._repo_vertices = repo_vertices
            self._repo_aristas = repo_aristas
            self._repo_pedidos = repo_pedidos
            self._repo_rutas = repo_rutas
            self._inicializado = True

    @property
    def repo_clientes(self) -> RepositorioClientes:
        """Acceso de solo lectura al repositorio de clientes."""
        return self._repo_clientes

    @property
    def repo_almacenamientos(self) -> RepositorioAlmacenamientos:
        """Acceso de solo lectura al repositorio de almacenamientos."""
        return self._repo_almacenamientos

    @property
    def repo_recargas(self) -> RepositorioRecargas:
        """Acceso de solo lectura al repositorio de recargas."""
        return self._repo_recargas

    @property
    def repo_vertices(self) -> RepositorioVertices:
        """Acceso de solo lectura al repositorio de vértices."""
        return self._repo_vertices

    @property
    def repo_aristas(self) -> RepositorioAristas:
        """Acceso de solo lectura al repositorio de aristas."""
        return self._repo_aristas

    @property
    def repo_pedidos(self) -> RepositorioPedidos:
        """Acceso de solo lectura al repositorio de pedidos."""
        return self._repo_pedidos

    @property
    def repo_rutas(self) -> RepositorioRutas:
        """Acceso de solo lectura al repositorio de rutas."""
        return self._repo_rutas

    # Métodos para exponer hashmaps de entidades delegando a repositorios
    def obtener_clientes_hashmap(self):
        return self._repo_clientes.obtener_hashmap()

    def obtener_almacenamientos_hashmap(self):
        return self._repo_almacenamientos.obtener_hashmap()

    def obtener_recargas_hashmap(self):
        return self._repo_recargas.obtener_hashmap()

    def obtener_vertices_hashmap(self):
        return self._repo_vertices.obtener_hashmap()

    def obtener_aristas_hashmap(self):
        return self._repo_aristas.obtener_hashmap()

    def obtener_pedidos_hashmap(self):
        return self._repo_pedidos.obtener_hashmap()

    def obtener_rutas_hashmap(self):
        return self._repo_rutas.obtener_hashmap()

    # Aquí solo se incluirá lógica de dominio pura usando repositorios (p.ej. generar pedidos, rutas, etc.)
    # Métodos de negocio delegan siempre en repositorios. Ejemplo:
    # def generar_pedido(self, datos_pedido):
    #     pedido = self._repo_pedidos.crear(datos_pedido)
    #     self._repo_clientes.asociar_pedido(pedido.id, pedido)
    #     return pedido

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int):
        """
        Inicializa la simulación: genera vértices, aristas y pedidos siguiendo los requisitos.
        """
        # Limpiar repositorios
        self.repo_vertices.limpiar()
        self.repo_aristas.limpiar()
        self.repo_clientes.limpiar()
        self.repo_almacenamientos.limpiar()
        self.repo_recargas.limpiar()
        self.repo_pedidos.limpiar()
        self.repo_rutas.limpiar()
        # Generación de vértices con proporciones: 20% almacenamiento, 20% recarga, 60% clientes
        from Backend.Dominio.EntFabricas.FabricaAlmacenamientos import FabricaAlmacenamientos
        from Backend.Dominio.EntFabricas.FabricaRecargas import FabricaRecargas
        from Backend.Dominio.EntFabricas.FabricaClientes import FabricaClientes
        fa = FabricaAlmacenamientos()
        fr = FabricaRecargas()
        fc = FabricaClientes()
        n_alm = max(1, int(n_vertices * 0.2))
        n_rec = max(1, int(n_vertices * 0.2))
        n_cli = n_vertices - n_alm - n_rec
        for i in range(n_alm): fa.crear(i+1, f"Almacen {i+1}")
        for i in range(n_rec): fr.crear(i+1, f"Recarga {i+1}")
        for i in range(n_cli): fc.crear(i+1, f"Cliente {i+1}")
        # Generar aristas asegurando conectividad y aleatoriedad
        import random
        all_vertices = list(self.repo_vertices.todos())
        # Conexión en cadena mínima
        for u, v in zip(all_vertices, all_vertices[1:]):
            peso = random.uniform(1, 10)
            from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
            fae = FabricaAristas()
            fae.crear(u, v, peso)
        # Aristas adicionales hasta m_aristas
        existentes = len(all_vertices) - 1
        posibles = [(u, v) for u in all_vertices for v in all_vertices if u != v]
        while existentes < m_aristas and posibles:
            u, v = random.choice(posibles)
            posibles.remove((u, v))
            peso = random.uniform(1, 10)
            fae.crear(u, v, peso)
            existentes += 1
        # Generar pedidos entre almacenamientos y clientes
        from Backend.Dominio.EntFabricas.FabricaPedidos import FabricaPedidos
        fp = FabricaPedidos()
        almacenes = list(self.repo_almacenamientos.todos())
        clientes = list(self.repo_clientes.todos())
        prioridades = ['alta', 'media', 'baja']
        for j in range(1, n_pedidos + 1):
            origen = random.choice(almacenes)
            destino = random.choice(clientes)
            prioridad = random.choice(prioridades)
            pedido = fp.crear(j, origen, destino, prioridad)
            # Asociar pedido a cliente y almacen
            cliente_elem = self.repo_clientes.obtener(destino.id_cliente)
            almacen_elem = self.repo_almacenamientos.obtener(origen.id_almacenamiento)
            cliente_elem.agregar_pedido(pedido)
            almacen_elem.agregar_pedido(pedido)
        return None

    def obtener_vertices(self):
        return list(self.repo_vertices.todos())

    def obtener_aristas(self):
        return list(self.repo_aristas.todos())

    def obtener_clientes(self):
        return list(self.repo_clientes.todos())

    def obtener_almacenamientos(self):
        return list(self.repo_almacenamientos.todos())

    def obtener_recargas(self):
        return list(self.repo_recargas.todos())

    def obtener_pedidos(self):
        return list(self.repo_pedidos.todos())

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = 'BFS'):
        # Buscar pedido y delegar cálculo de ruta según algoritmo
        pedido = self.repo_pedidos.obtener(id_pedido)
        # Aquí se debería invocar la estrategia concreta (vía fábrica o repositorio de rutas)
        raise NotImplementedError("Lógica de cálculo de ruta no implementada en dominio")

    def marcar_pedido_entregado(self, id_pedido: int):
        pedido = self.repo_pedidos.obtener(id_pedido)
        pedido.marcar_entregado()
        self.repo_pedidos.agregar(pedido)

    def buscar_pedido(self, id_pedido: int):
        return self.repo_pedidos.obtener(id_pedido)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        # Delegar al repositorio de rutas (asumiendo persistencia de frecuencias)
        return list(self.repo_rutas.todos())[:top]

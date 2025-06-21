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

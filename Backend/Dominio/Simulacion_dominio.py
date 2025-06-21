from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
from Backend.Servicios.Observer.SujetoObservable import SujetoObservable
from Backend.Servicios.Observer.ObserverEstadisticas import ObserverEstadisticas
from Backend.Infraestructura.TDA.TDA_AVL import AVL
import logging

class Simulacion(SujetoObservable):
    """
    Singleton que mantiene una unica instancia de la simulacion.
    Integra repositorios, logica de negocio, estrategias de ruta y observadores.
    """
    _instancia = None

    def __new__(cls, repo_clientes=None, repo_almacenamientos=None,
                repo_recargas=None, repo_vertices=None,
                repo_aristas=None, repo_pedidos=None,
                repo_rutas=None):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self, repo_clientes, repo_almacenamientos, repo_recargas, repo_vertices, repo_aristas, repo_pedidos, repo_rutas):
        if not getattr(self, '_inicializado', False):
            super().__init__()  # SujetoObservable
            self._repo_clientes = repo_clientes
            self._repo_almacenamientos = repo_almacenamientos
            self._repo_recargas = repo_recargas
            self._repo_vertices = repo_vertices
            self._repo_aristas = repo_aristas
            self._repo_pedidos = repo_pedidos
            self._repo_rutas = repo_rutas
            self._estrategia_ruta = None
            self._avl_rutas = AVL()
            self._logger = logging.getLogger("Simulacion")
            if not self._logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)
            # Observador de estadisticas
            self._observer_estadisticas = ObserverEstadisticas(self)
            self.agregar_observador(self._observer_estadisticas)
            self._inicializado = True

    @property
    def repo_clientes(self) -> RepositorioClientes:
        return self._repo_clientes

    @property
    def repo_almacenamientos(self) -> RepositorioAlmacenamientos:
        return self._repo_almacenamientos

    @property
    def repo_recargas(self) -> RepositorioRecargas:
        return self._repo_recargas

    @property
    def repo_vertices(self) -> RepositorioVertices:
        return self._repo_vertices

    @property
    def repo_aristas(self) -> RepositorioAristas:
        return self._repo_aristas

    @property
    def repo_pedidos(self) -> RepositorioPedidos:
        return self._repo_pedidos

    @property
    def repo_rutas(self) -> RepositorioRutas:
        return self._repo_rutas

    @property
    def repositorios(self):
        """Devuelve todos los repositorios como un diccionario."""
        return {
            'clientes': self._repo_clientes,
            'almacenamientos': self._repo_almacenamientos,
            'recargas': self._repo_recargas,
            'vertices': self._repo_vertices,
            'aristas': self._repo_aristas,
            'pedidos': self._repo_pedidos,
            'rutas': self._repo_rutas
        }

    @property
    def fabricas(self):
        """Devuelve todas las fabricas como un diccionario."""
        from Backend.Dominio.EntFabricas.FabricaClientes import FabricaClientes
        from Backend.Dominio.EntFabricas.FabricaAlmacenamientos import FabricaAlmacenamientos
        from Backend.Dominio.EntFabricas.FabricaRecargas import FabricaRecargas
        from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
        from Backend.Dominio.EntFabricas.FabricaPedidos import FabricaPedidos
        from Backend.Dominio.EntFabricas.FabricaRutas import FabricaRutas
        return {
            'clientes': FabricaClientes(),
            'almacenamientos': FabricaAlmacenamientos(),
            'recargas': FabricaRecargas(),
            'aristas': FabricaAristas(),
            'pedidos': FabricaPedidos(),
            'rutas': FabricaRutas()
        }

    @property
    def grafo(self):
        """Devuelve el grafo desde el repositorio de vertices si existe."""
        if hasattr(self._repo_vertices, 'grafo'):
            return self._repo_vertices.grafo
        return None

    @property
    def hashmaps(self):
        """Devuelve los hashmaps de cada repositorio si existen."""
        return {
            'clientes': self._repo_clientes.obtener_hashmap() if hasattr(self._repo_clientes, 'obtener_hashmap') else None,
            'almacenamientos': self._repo_almacenamientos.obtener_hashmap() if hasattr(self._repo_almacenamientos, 'obtener_hashmap') else None,
            'recargas': self._repo_recargas.obtener_hashmap() if hasattr(self._repo_recargas, 'obtener_hashmap') else None,
            'vertices': self._repo_vertices.obtener_hashmap() if hasattr(self._repo_vertices, 'obtener_hashmap') else None,
            'aristas': self._repo_aristas.obtener_hashmap() if hasattr(self._repo_aristas, 'obtener_hashmap') else None,
            'pedidos': self._repo_pedidos.obtener_hashmap() if hasattr(self._repo_pedidos, 'obtener_hashmap') else None,
            'rutas': self._repo_rutas.obtener_hashmap() if hasattr(self._repo_rutas, 'obtener_hashmap') else None
        }

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

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int):
        """
        Inicializa la simulacion: genera vertices, aristas y pedidos siguiendo los requisitos.
        """
        # Limpiar repositorios
        self.repo_vertices.limpiar()
        self.repo_aristas.limpiar()
        self.repo_clientes.limpiar()
        self.repo_almacenamientos.limpiar()
        self.repo_recargas.limpiar()
        self.repo_pedidos.limpiar()
        self.repo_rutas.limpiar()
        self._avl_rutas = AVL()
        # Generacion de vertices con proporciones: 20% almacenamiento, 20% recarga, 60% clientes
        from Backend.Dominio.EntFabricas.FabricaAlmacenamientos import FabricaAlmacenamientos
        from Backend.Dominio.EntFabricas.FabricaRecargas import FabricaRecargas
        from Backend.Dominio.EntFabricas.FabricaClientes import FabricaClientes
        fa = FabricaAlmacenamientos()
        fr = FabricaRecargas()
        fc = FabricaClientes()
        n_alm = max(1, int(n_vertices * 0.2))
        n_rec = max(1, int(n_vertices * 0.2))
        n_cli = n_vertices - n_alm - n_rec
        for i in range(n_alm):
            alm = fa.crear(f"A{i+1}", f"Almacenamiento {i+1}")
            self.repo_almacenamientos.agregar(alm)
            self.repo_vertices.agregar(alm)
        for i in range(n_rec):
            rec = fr.crear(f"R{i+1}", f"Recarga {i+1}")
            self.repo_recargas.agregar(rec)
            self.repo_vertices.agregar(rec)
        for i in range(n_cli):
            cli = fc.crear(f"C{i+1}", f"Cliente {i+1}")
            self.repo_clientes.agregar(cli)
            self.repo_vertices.agregar(cli)
        # Generar aristas asegurando conectividad y aleatoriedad
        all_vertices = list(self.repo_vertices.todos())
        from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
        fae = FabricaAristas()
        # Conexion en cadena minima
        for u, v in zip(all_vertices, all_vertices[1:]):
            arista = fae.crear(u, v)
            self.repo_aristas.agregar(arista)
        # Aristas adicionales hasta m_aristas
        existentes = len(all_vertices) - 1
        posibles = [(u, v) for u in all_vertices for v in all_vertices if u != v]
        import random
        while existentes < m_aristas and posibles:
            u, v = random.choice(posibles)
            if not self.repo_aristas.existe(u, v):
                arista = fae.crear(u, v)
                self.repo_aristas.agregar(arista)
                existentes += 1
        # Generar pedidos entre almacenamientos y clientes
        from Backend.Dominio.EntFabricas.FabricaPedidos import FabricaPedidos
        fp = FabricaPedidos()
        almacenes = list(self.repo_almacenamientos.todos())
        clientes = list(self.repo_clientes.todos())
        prioridades = ['alta', 'media', 'baja']
        for j in range(1, n_pedidos + 1):
            import random
            origen = random.choice(almacenes)
            destino = random.choice(clientes)
            prioridad = random.choice(prioridades)
            pedido = fp.crear(f"P{j}", origen, destino, prioridad)
            self.repo_pedidos.agregar(pedido)
            destino.agregar_pedido(pedido)
        self.notificar_observadores("simulacion_iniciada", {
            "n_vertices": n_vertices,
            "m_aristas": m_aristas,
            "n_pedidos": n_pedidos
        })
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

    def set_estrategia_ruta(self, estrategia):
        """
        Permite inyectar una estrategia de rutas (BFS, DFS, Topological, etc.)
        """
        self._estrategia_ruta = estrategia
        self._logger.info(f"[Simulacion] Estrategia de ruta configurada: {type(estrategia).__name__}")
        self.notificar_observadores("cambio_estrategia", {"estrategia": type(estrategia).__name__})

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = 'BFS'):
        """
        Calcula la ruta para un pedido usando la estrategia de ruta seleccionada.
        """
        pedido = self.repo_pedidos.obtener(id_pedido)
        if self._estrategia_ruta is None:
            raise Exception("No hay estrategia de ruta configurada")
        origen = pedido.origen_v
        destino = pedido.destino_v
        grafo = self.repo_vertices.grafo  # Se asume que el grafo esta accesible desde el repositorio de vertices
        ruta, costo, recargas = self._estrategia_ruta.calcular_ruta(origen, destino, grafo, autonomia=50)
        pedido.asignar_ruta(ruta, costo)
        self._avl_rutas.insertar(ruta, costo)
        self.notificar_observadores("calculo_ruta", {"pedido": id_pedido, "ruta": ruta, "costo": costo, "recargas": recargas})
        return ruta, costo, recargas

    def marcar_pedido_entregado(self, id_pedido: int):
        pedido = self.repo_pedidos.obtener(id_pedido)
        pedido.actualizar_status("entregado")
        self.notificar_observadores("entrega_pedido", {"pedido": id_pedido})
        return pedido

    def buscar_pedido(self, id_pedido: int):
        return self.repo_pedidos.obtener(id_pedido)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        return self._avl_rutas.obtener_mas_frecuentes(top)

    def notificar_observadores(self, evento, datos=None):
        self.notificar(evento, datos)

    def reiniciar_todo(self):
        self.repo_vertices.limpiar()
        self.repo_aristas.limpiar()
        self.repo_clientes.limpiar()
        self.repo_almacenamientos.limpiar()
        self.repo_recargas.limpiar()
        self.repo_pedidos.limpiar()
        self.repo_rutas.limpiar()
        self._avl_rutas = AVL()
        self.notificar_observadores("simulacion_reiniciada", {})

    def reiniciar(self):
        """Alias para reiniciar_todo, por compatibilidad con los tests."""
        self.reiniciar_todo()

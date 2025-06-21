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
import random

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
            # LOG: Verificar tipo antes de agregar al repositorio de vértices
            logging.debug(f"[AGREGAR_VERTICE] Intentando agregar almacenamiento al repo_vertices: {alm} (type={type(alm)})")
            if not hasattr(alm, 'id_almacenamiento'):
                logging.error(f"[AGREGAR_VERTICE] El objeto no tiene id_almacenamiento: {alm}")
            # Si no es Vertice, envolverlo
            from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
            if not isinstance(alm, Vertice):
                vertice_alm = Vertice(alm)
                logging.debug(f"[AGREGAR_VERTICE] Envolviendo almacenamiento en Vertice: {vertice_alm} (type={type(vertice_alm)})")
            else:
                vertice_alm = alm
            self.repo_vertices.agregar(vertice_alm, getattr(alm, 'id_almacenamiento', None))
            logging.debug(f"[AGREGAR_VERTICE] Estado actual de repo_vertices: {[str(v) + ' type=' + str(type(v)) for v in self.repo_vertices.todos()]}")
        for i in range(n_rec):
            rec = fr.crear(f"R{i+1}", f"Recarga {i+1}")
            self.repo_recargas.agregar(rec)
            logging.debug(f"[AGREGAR_VERTICE] Intentando agregar recarga al repo_vertices: {rec} (type={type(rec)})")
            if not hasattr(rec, 'id_recarga'):
                logging.error(f"[AGREGAR_VERTICE] El objeto no tiene id_recarga: {rec}")
            if not isinstance(rec, Vertice):
                vertice_rec = Vertice(rec)
                logging.debug(f"[AGREGAR_VERTICE] Envolviendo recarga en Vertice: {vertice_rec} (type={type(vertice_rec)})")
            else:
                vertice_rec = rec
            self.repo_vertices.agregar(vertice_rec, getattr(rec, 'id_recarga', None))
            logging.debug(f"[AGREGAR_VERTICE] Estado actual de repo_vertices: {[str(v) + ' type=' + str(type(v)) for v in self.repo_vertices.todos()]}")
        for i in range(n_cli):
            cli = fc.crear(f"C{i+1}", f"Cliente {i+1}")
            self.repo_clientes.agregar(cli)
            logging.debug(f"[AGREGAR_VERTICE] Intentando agregar cliente al repo_vertices: {cli} (type={type(cli)})")
            if not hasattr(cli, 'id_cliente'):
                logging.error(f"[AGREGAR_VERTICE] El objeto no tiene id_cliente: {cli}")
            if not isinstance(cli, Vertice):
                vertice_cli = Vertice(cli)
                logging.debug(f"[AGREGAR_VERTICE] Envolviendo cliente en Vertice: {vertice_cli} (type={type(vertice_cli)})")
            else:
                vertice_cli = cli
            self.repo_vertices.agregar(vertice_cli, getattr(cli, 'id_cliente', None))
            logging.debug(f"[AGREGAR_VERTICE] Estado actual de repo_vertices: {[str(v) + ' type=' + str(type(v)) for v in self.repo_vertices.todos()]}")
        # Asegurar que all_vertices solo contenga instancias de Vertice únicas del repositorio
        all_vertices = list(self.repo_vertices.todos())
        logging.info(f"[ALL_VERTICES] Contenido de all_vertices tras poblar: {[str(v) + ' type=' + str(type(v)) for v in all_vertices]}")
        for idx, v in enumerate(all_vertices):
            if not (hasattr(v, 'elemento') and callable(getattr(v, 'elemento', None))):
                import traceback
                logging.error(f"[ALL_VERTICES] Elemento en all_vertices no es Vertice: idx={idx}, v={v}, type={type(v)}\nStack trace:\n{traceback.format_exc()}")
                raise TypeError(f"[ALL_VERTICES] Se esperaba Vertice en all_vertices, recibido: idx={idx}, type={type(v)}")
        logging.info(f"[ALL_VERTICES] Todos los elementos en all_vertices son instancias de Vertice. Total: {len(all_vertices)}")
        # Generar aristas asegurando conectividad y aleatoriedad
        from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
        fae = FabricaAristas()
        # Conexion en cadena minima
        for u, v in zip(all_vertices, all_vertices[1:]):
            logging.debug(f"Creando arista: u={u} (type={type(u)}), v={v} (type={type(v)})")
            if not (hasattr(u, 'elemento') and hasattr(v, 'elemento')):
                logging.error(f"[ARISTA-CHAIN] Uno de los objetos no es Vertice: u={u} (type={type(u)}), v={v} (type={type(v)})")
                raise TypeError(f"[ARISTA-CHAIN] Se esperaba Vertice, recibido: u={type(u)}, v={type(v)}")
            peso = random.randint(1, 50)
            arista = fae.crear(u, v, peso)
            self.repo_aristas.agregar(arista)
        # Aristas adicionales hasta m_aristas
        existentes = len(all_vertices) - 1
        posibles = [(u, v) for u in all_vertices for v in all_vertices if u != v]
        while existentes < m_aristas and posibles:
            u, v = random.choice(posibles)
            logging.debug(f"Creando arista extra: u={u} (type={type(u)}), v={v} (type={type(v)})")
            if not (hasattr(u, 'elemento') and hasattr(v, 'elemento')):
                logging.error(f"[ARISTA-EXTRA] Uno de los objetos no es Vertice: u={u} (type={type(u)}), v={v} (type={type(v)})")
                raise TypeError(f"[ARISTA-EXTRA] Se esperaba Vertice, recibido: u={type(u)}, v={type(v)}")
            if not self.repo_aristas.existe(u, v):
                peso = random.randint(1, 50)
                arista = fae.crear(u, v, peso)
                self.repo_aristas.agregar(arista)
                existentes += 1
        # Generar pedidos entre almacenamientos y clientes
        from Backend.Dominio.EntFabricas.FabricaPedidos import FabricaPedidos
        fp = FabricaPedidos()
        almacenes = list(self.repo_almacenamientos.todos())
        clientes = list(self.repo_clientes.todos())
        prioridades = ['alta', 'media', 'baja']
        for j in range(1, n_pedidos + 1):
            almacen = random.choice(almacenes)
            cliente = random.choice(clientes)
            # Buscar los vértices correspondientes
            origen = self.repo_vertices.obtener(getattr(almacen, 'id_almacenamiento', None))
            destino = self.repo_vertices.obtener(getattr(cliente, 'id_cliente', None))
            logging.debug(f"Creando pedido: almacen={almacen} (type={type(almacen)}), cliente={cliente} (type={type(cliente)}), origen={origen} (type={type(origen)}), destino={destino} (type={type(destino)})")
            if not (hasattr(origen, 'elemento') and hasattr(destino, 'elemento')):
                logging.error(f"[PEDIDO] Origen o destino no es Vertice: origen={origen} (type={type(origen)}), destino={destino} (type={type(destino)})")
                raise TypeError(f"[PEDIDO] Se esperaba Vertice para origen/destino, recibido: origen={type(origen)}, destino={type(destino)}")
            prioridad = random.choice(prioridades)
            pedido = fp.crear(f"P{j}", destino, origen, destino, prioridad)  # cliente_v, origen_v, destino_v, prioridad
            self.repo_pedidos.agregar(pedido)
            # Agregar el pedido al elemento cliente (no al vértice)
            if hasattr(destino, 'elemento'):
                elem_cliente = destino.elemento()
                if hasattr(elem_cliente, 'agregar_pedido'):
                    elem_cliente.agregar_pedido(pedido)
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

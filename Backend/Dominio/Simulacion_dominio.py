from Backend.API.DTOs.Dtos1 import *
from Backend.Infraestructura.Modelos.Modelo_Grafo import Grafo
from Backend.Infraestructura.Modelos.Modelo_Vertice import Vertice
from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.Dominio.Dominio_Almacenamiento import Almacenamiento
from Backend.Dominio.Dominio_Recarga import Recarga
from Backend.Dominio.Dominio_Pedido import Pedido
from Backend.Dominio.FabricaPedidos import FabricaPedidos
from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Servicios.AlgEstrategias.RutaEstrategiaDijkstra import RutaEstrategiaDijkstra
from Backend.Servicios.AlgEstrategias.RutaEstrategiaBFS import RutaEstrategiaBFS
from Backend.Servicios.AlgEstrategias.RutaEstrategiaDFS import RutaEstrategiaDFS
from Backend.Servicios.AlgEstrategias.RutaEstrategiaFloydWarshall import RutaEstrategiaFloydWarshall
import random
import time
import logging

class Simulacion:
    """
    Clase Singleton que representa la simulación logística de drones.
    Utiliza el patrón Singleton para asegurar una única instancia global.
    """
    _instancia = None

    def __new__(cls, n_nodos=None, m_aristas=None, n_pedidos=None):
        if cls._instancia is None:
            cls._instancia = super(Simulacion, cls).__new__(cls)
            cls._instancia._ya_inicializada = False
        return cls._instancia

    @classmethod
    def obtener_instancia(cls):
        """Devuelve la instancia única de la simulación."""
        if cls._instancia is None:
            raise Exception("La simulación no ha sido inicializada")
        return cls._instancia

    @classmethod
    def reiniciar_instancia(cls, n_nodos, m_aristas, n_pedidos):
        """Reinicia la instancia única de la simulación con nuevos parámetros."""
        cls._instancia = None
        return cls(n_nodos, m_aristas, n_pedidos)

    @classmethod
    def limpiar_instancia(cls):
        """Limpia la instancia única de la simulación."""
        cls._instancia = None

    def __init__(self, n_nodos, m_aristas, n_pedidos):
        if getattr(self, '_ya_inicializada', False):
            return
        if n_nodos is None or m_aristas is None or n_pedidos is None or n_nodos <= 0 or m_aristas <= 0 or n_pedidos < 0:
            raise ValueError("Parámetros inválidos para inicializar la simulación")
        self.n_nodos = n_nodos
        self.m_aristas = m_aristas
        self.n_pedidos = n_pedidos
        self.grafo = Grafo()
        self.clientes = []
        self.almacenamientos = []
        self.estaciones_recarga = []
        self.pedidos = []
        self.hash_pedidos = {}
        self.rutas = []
        self.rutas_avl = None  # Debe inicializarse con el TDA AVL correspondiente
        self.fabrica_pedidos = FabricaPedidos()  # Fábrica centralizada de pedidos
        self._generar_nodos()
        self._generar_aristas()
        self._generar_pedidos()
        self._ya_inicializada = True

    def serializar_estado(self):
        return simulacion_estado_a_dto(self)

    def obtener_estadisticas(self):
        t0 = time.time()
        # ...calculo de estadisticas...
        t1 = time.time()
        return estadisticas_a_dto(self, tiempo_respuesta=round(t1-t0, 4))

    def _generar_nodos(self):
        n_clientes = max(1, int(self.n_nodos * 0.6))
        n_almacenamientos = max(1, int(self.n_nodos * 0.2))
        n_recargas = self.n_nodos - n_clientes - n_almacenamientos
        if n_recargas < 1:
            n_recargas = 1
        self.clientes = []
        self.almacenamientos = []
        self.estaciones_recarga = []
        repo_clientes = RepositorioClientes()
        repo_almacenamientos = RepositorioAlmacenamientos()
        repo_recargas = RepositorioRecargas()
        repo_vertices = RepositorioVertices()
        repo_clientes.limpiar()
        repo_almacenamientos.limpiar()
        repo_recargas.limpiar()
        repo_vertices.limpiar()
        for i in range(n_clientes):
            cliente = Cliente(i, f"Cliente_{i}")
            self.clientes.append(cliente)
            repo_clientes.agregar(cliente)
            v = Vertice(cliente)
            repo_vertices.agregar(v, cliente.id_cliente)
            self.grafo.insertar_vertice(cliente)
        for i in range(n_almacenamientos):
            almacen = Almacenamiento(i + n_clientes, f"Almacen_{i}")
            self.almacenamientos.append(almacen)
            repo_almacenamientos.agregar(almacen)
            v = Vertice(almacen)
            repo_vertices.agregar(v, almacen.id_almacenamiento)
            self.grafo.insertar_vertice(almacen)
        for i in range(n_recargas):
            recarga = Recarga(i + n_clientes + n_almacenamientos, f"Recarga_{i}")
            self.estaciones_recarga.append(recarga)
            repo_recargas.agregar(recarga)
            v = Vertice(recarga)
            repo_vertices.agregar(v, recarga.id_recarga)
            self.grafo.insertar_vertice(recarga)

    def _generar_aristas(self):
        repo_aristas = RepositorioAristas()
        repo_aristas.limpiar()
        vertices = list(self.grafo.vertices())
        n = len(vertices)
        if n < 2:
            return
        indices = list(range(n))
        random.shuffle(indices)
        conectados = set([indices[0]])
        aristas = set()
        # Árbol generador mínimo para asegurar conectividad
        while len(conectados) < n:
            posibles = [i for i in indices if i not in conectados]
            nuevo = random.choice(posibles)
            conectado = random.choice(list(conectados))
            u, v = vertices[conectado], vertices[nuevo]
            peso = random.uniform(1, 10)
            arista = self.grafo.insertar_arista(u, v, peso)
            repo_aristas.agregar(arista)
            aristas.add((conectado, nuevo))
            conectados.add(nuevo)
        # Agregar aristas adicionales hasta llegar a m_aristas
        posibles = [(i, j) for i in range(n) for j in range(n) if i != j and (i, j) not in aristas and (j, i) not in aristas]
        random.shuffle(posibles)
        for (u_idx, v_idx) in posibles:
            if len(aristas) >= self.m_aristas:
                break
            u, v = vertices[u_idx], vertices[v_idx]
            peso = random.uniform(1, 10)
            arista = self.grafo.insertar_arista(u, v, peso)
            repo_aristas.agregar(arista)
            aristas.add((u_idx, v_idx))
        # --- Asegurar que cada cliente tenga camino desde algún almacenamiento ---
        for cliente in self.clientes:
            vertice_cliente = self.grafo.buscar_vertice_por_elemento(cliente)
            tiene_camino = False
            for almacen in self.almacenamientos:
                vertice_almacen = self.grafo.buscar_vertice_por_elemento(almacen)
                camino, _ = self.grafo.dijkstra_camino_minimo(vertice_almacen, vertice_cliente)
                if camino:
                    tiene_camino = True
                    break
            if not tiene_camino:
                # Agregar arista directa desde un almacenamiento aleatorio
                almacen = random.choice(self.almacenamientos)
                vertice_almacen = self.grafo.buscar_vertice_por_elemento(almacen)
                peso = random.uniform(1, 10)
                arista = self.grafo.insertar_arista(vertice_almacen, vertice_cliente, peso)
                repo_aristas.agregar(arista)

    def _generar_pedidos(self):
        logger = logging.getLogger("Simulacion")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.pedidos = []
        self.hash_pedidos = {}
        self.fabrica_pedidos = FabricaPedidos()  # Reiniciar errores para cada simulación
        prioridades = ['muy bajo', 'bajo', 'medio', 'alto', 'muy alto', 'emergencia']
        if not self.clientes or not self.almacenamientos:
            logger.error("No se pueden crear pedidos: faltan clientes o almacenamientos.")
            raise Exception("No se pueden crear pedidos: faltan clientes o almacenamientos.")
        vertices_clientes = [self.grafo.buscar_vertice_por_elemento(c) for c in self.clientes]
        vertices_almacenamientos = [self.grafo.buscar_vertice_por_elemento(a) for a in self.almacenamientos]
        logger.info(f"vertices_clientes: {vertices_clientes}")
        logger.info(f"vertices_almacenamientos: {vertices_almacenamientos}")
        if not all(vertices_clientes) or not all(vertices_almacenamientos):
            logger.error("Error al obtener vértices válidos para clientes o almacenamientos.")
            raise Exception("Error al obtener vértices válidos para clientes o almacenamientos.")
        from datetime import datetime
        fecha_simulacion = datetime.now()
        repo_pedidos = RepositorioPedidos()
        repo_pedidos.limpiar()
        for i in range(self.n_pedidos):
            vertice_cliente = random.choice(vertices_clientes)
            vertice_almacen = random.choice(vertices_almacenamientos)
            prioridad = random.choice(prioridades)
            logger.info(f"Creando pedido {i} con vertice_cliente: {vertice_cliente}, vertice_cliente.elemento: {getattr(vertice_cliente, 'elemento', lambda: None)() if vertice_cliente else None}, vertice_almacen: {vertice_almacen}, vertice_almacen.elemento: {getattr(vertice_almacen, 'elemento', lambda: None)() if vertice_almacen else None}, prioridad: {prioridad}, fecha: {fecha_simulacion}")
            pedido = self.fabrica_pedidos.crear_pedido(
                id_pedido=i,
                vertice_cliente=vertice_cliente,
                vertice_almacen=vertice_almacen,
                prioridad=prioridad,
                fecha_creacion=fecha_simulacion
            )
            if pedido is not None:
                self.pedidos.append(pedido)
                self.hash_pedidos[pedido.id_pedido] = pedido
                repo_pedidos.agregar(pedido)
                # Asociar el pedido al cliente y al almacenamiento
                if hasattr(vertice_cliente.elemento(), 'agregar_pedido'):
                    logger.info(f"Asociando pedido {pedido.id_pedido} a cliente {vertice_cliente.elemento()}")
                    vertice_cliente.elemento().agregar_pedido(pedido)
                if hasattr(vertice_almacen.elemento(), 'agregar_pedido'):
                    logger.info(f"Asociando pedido {pedido.id_pedido} a almacen {vertice_almacen.elemento()}")
                    vertice_almacen.elemento().agregar_pedido(pedido)
        # Si hay errores, quedan registrados en self.fabrica_pedidos.errores

    def obtener_errores_pedidos(self):
        """
        Devuelve la lista de errores de creación de pedidos registrados por la fábrica.
        """
        return self.fabrica_pedidos.obtener_errores()

    def listar_clientes(self):
        return self.clientes

    def listar_almacenamientos(self):
        return self.almacenamientos

    def listar_recargas(self):
        return self.estaciones_recarga

    def listar_pedidos(self):
        return self.pedidos

    def obtener_aristas(self):
        return list(self.grafo.aristas())

    def obtener_nodos(self):
        return list(self.grafo.vertices())

    def calcular_ruta_pedido(self, id_pedido, algoritmo):
        from Backend.Dominio.Dominio_Ruta import Ruta
        if id_pedido not in self.hash_pedidos:
            raise KeyError(f"Pedido con id {id_pedido} no encontrado")
        pedido = self.hash_pedidos[id_pedido]
        origen = pedido.origen
        destino = pedido.destino
        if pedido.es_enviado():
            raise ValueError("El pedido ya fue enviado")
        # Selección de estrategia
        if algoritmo == 'dijkstra':
            Estrategia = RutaEstrategiaDijkstra()
        elif algoritmo == 'bfs':
            Estrategia = RutaEstrategiaBFS()
        elif algoritmo == 'dfs':
            Estrategia = RutaEstrategiaDFS()
        elif algoritmo == 'floyd_warshall':
            Estrategia = RutaEstrategiaFloydWarshall()
        else:
            raise ValueError("Algoritmo de ruta no soportado")
        camino, costo = Estrategia.calcular_ruta(origen, destino, self.grafo)
        if not camino:
            raise ValueError("No existe una ruta posible entre los nodos seleccionados.")
        ruta = Ruta(origen, destino, camino, costo, algoritmo)
        pedido.asignar_ruta(ruta, costo)
        self.rutas.append(ruta)
        return ruta

    def marcar_pedido_entregado(self, id_pedido):
        pedido = self.obtener_pedido(id_pedido)
        if pedido is not None:
            pedido.marcar_entregado()
            return pedido
        else:
            raise KeyError(f"Pedido con id {id_pedido} no encontrado")

    def rutas_mas_frecuentes(self, top=5):
        # Suponiendo que self.rutas_avl es un AVL que almacena rutas como tuplas y tiene método inorden con frecuencia
        rutas_frecuencia = []
        if hasattr(self.rutas_avl, 'inorden_con_frecuencia'):
            rutas_frecuencia = self.rutas_avl.inorden_con_frecuencia()
        elif hasattr(self.rutas_avl, 'inorden'):
            rutas_frecuencia = self.rutas_avl.inorden()
        rutas_ordenadas = sorted(rutas_frecuencia, key=lambda x: x[1], reverse=True)
        resultado = []
        for camino, frecuencia in rutas_ordenadas[:top]:
            resultado.append(camino)
        return resultado

    def obtener_cliente(self, id):
        for v in self.clientes:
            if v.id_cliente == id:
                return v
        raise KeyError(f"Cliente con id {id} no encontrado")

    def obtener_almacenamiento(self, id):
        for v in self.almacenamientos:
            if v.id_almacenamiento == id:
                return v
        raise KeyError(f"Almacenamiento con id {id} no encontrado")

    def obtener_recarga(self, id):
        for v in self.estaciones_recarga:
            if v.id_recarga == id:
                return v
        raise KeyError(f"Recarga con id {id} no encontrada")

    def obtener_pedido(self, id):
        for p in self.pedidos:
            if p.id_pedido == id:
                return p
        raise KeyError(f"Pedido con id {id} no encontrado")

    def obtener_ruta(self, id):
        for r in self.rutas:
            if hasattr(r, 'id') and r.id == id:
                return r
        raise KeyError(f"Ruta con id {id} no encontrada")

    def obtener_estadisticas(self):
        return {
            'total_clientes': len(self.clientes),
            'total_almacenamientos': len(self.almacenamientos),
            'total_recargas': len(self.estaciones_recarga),
            'total_pedidos': len(self.pedidos),
            'rutas_mas_frecuentes': self.rutas_mas_frecuentes()
        }

    def to_response(self):
        return {
            "ok": True,
            "n_nodos": self.n_nodos,
            "m_aristas": self.m_aristas,
            "n_pedidos": self.n_pedidos
        }

    def calcular_todos_los_caminos_floyd_warshall(self):
        """
        Calcula todos los caminos mínimos entre todos los pares de nodos usando Floyd-Warshall.
        Retorna dos diccionarios: distancias y caminos.
        """
        resultados = self.grafo.floyd_warshall_todos_los_caminos()
        # resultados debe ser una tupla (distancias, caminos)
        distancias, caminos = resultados
        return distancias, caminos

    def calcular_camino_entre_nodos(self, origen_id: int, destino_id: int, algoritmo: str):
        """
        Calcula el camino entre dos nodos usando el algoritmo especificado.
        Retorna un dict serializable con origen, destino, camino, peso_total, algoritmo.
        """
        grafo = self.grafo
        vertices = list(grafo.vertices())
        v_origen = next((v for v in vertices if getattr(v.elemento(), 'id', None) == origen_id or getattr(v.elemento(), 'id_cliente', None) == origen_id or getattr(v.elemento(), 'id_almacenamiento', None) == origen_id or getattr(v.elemento(), 'id_recarga', None) == origen_id), None)
        v_destino = next((v for v in vertices if getattr(v.elemento(), 'id', None) == destino_id or getattr(v.elemento(), 'id_cliente', None) == destino_id or getattr(v.elemento(), 'id_almacenamiento', None) == destino_id or getattr(v.elemento(), 'id_recarga', None) == destino_id), None)
        if v_origen is None or v_destino is None:
            raise ValueError("Nodo origen o destino no encontrado")
        # Selección de estrategia
        if algoritmo == 'dijkstra':
            Estrategia = RutaEstrategiaDijkstra()
        elif algoritmo == 'bfs':
            Estrategia = RutaEstrategiaBFS()
        elif algoritmo == 'dfs':
            Estrategia = RutaEstrategiaDFS()
        elif algoritmo == 'floyd_warshall':
            Estrategia = RutaEstrategiaFloydWarshall()
        else:
            raise ValueError("Algoritmo de ruta no soportado")
        camino, costo = Estrategia.calcular_ruta(v_origen, v_destino, grafo)
        if not camino:
            return None
        camino_ids = [getattr(v.elemento(), 'id', None) or getattr(v.elemento(), 'id_cliente', None) or getattr(v.elemento(), 'id_almacenamiento', None) or getattr(v.elemento(), 'id_recarga', None) for v in camino]
        return {
            'origen': origen_id,
            'destino': destino_id,
            'camino': camino_ids,
            'peso_total': costo,
            'algoritmo': algoritmo
        }

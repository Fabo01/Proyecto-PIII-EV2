from Backend.Infraestructura.Modelos.Modelo_Grafo import Grafo
from Backend.Infraestructura.Modelos.Modelo_Vertice import Vertice
from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.Dominio.Dominio_Almacenamiento import Almacenamiento
from Backend.Dominio.Dominio_Recarga import Recarga
from Backend.Dominio.Dominio_Pedido import Pedido
from Backend.Servicios.EntFabricas.FabricaPedidos import FabricaPedidos
from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
from Backend.Servicios.EntFabricas.FabricaClientes import FabricaClientes
from Backend.Servicios.EntFabricas.FabricaAlmacenamientos import FabricaAlmacenamientos
from Backend.Servicios.EntFabricas.FabricaRecargas import FabricaRecargas
from Backend.Servicios.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Servicios.EntFabricas.FabricaRutas import FabricaRutas
from Backend.Servicios.Observer.SujetoObservable import SujetoObservable
from Backend.Servicios.Observer.ObserverEstadisticas import ObserverEstadisticas
import random
import time
import logging
from Backend.Aplicacion.AlgEstrategias.RutaEstrategiaDijkstra import RutaEstrategiaDijkstra
from Backend.Aplicacion.AlgEstrategias.RutaEstrategiaBFS import RutaEstrategiaBFS
from Backend.Aplicacion.AlgEstrategias.RutaEstrategiaDFS import RutaEstrategiaDFS
from Backend.Aplicacion.AlgEstrategias.RutaEstrategiaFloydWarshall import RutaEstrategiaFloydWarshall
from Backend.Aplicacion.AlgEstrategias.RutaEstrategiaTopologicalSort import RutaEstrategiaTopologicalSort
from Backend.Aplicacion.AlgEstrategias.RutaEstrategiaKruskal import RutaEstrategiaKruskal
from Backend.Infraestructura.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.Infraestructura.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.Infraestructura.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.Infraestructura.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.Infraestructura.Mapeadores.MapeadorRuta import MapeadorRuta

class Simulacion:
    """
    Clase Singleton que representa la simulación logística de drones.
    Utiliza el patrón Singleton para asegurar una única instancia global.
    Expone todos los repositorios como atributos y propiedades de solo lectura.
    """
    _instancia = None

    def __new__(cls, n_vertices=None, m_aristas=None, n_pedidos=None, sujeto_observable=None, estrategia_ruta=None):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Inicialización de repositorios singleton
            cls._instancia._repositorio_clientes = RepositorioClientes()
            cls._instancia._repositorio_almacenamientos = RepositorioAlmacenamientos()
            cls._instancia._repositorio_recargas = RepositorioRecargas()
            cls._instancia._repositorio_vertices = RepositorioVertices()
            cls._instancia._repositorio_aristas = RepositorioAristas()
            cls._instancia._repositorio_pedidos = RepositorioPedidos()
            cls._instancia._repositorio_rutas = RepositorioRutas()
            # ...otros atributos de la simulación...
        return cls._instancia

    @classmethod
    def obtener_instancia(cls):
        if cls._instancia is None:
            raise Exception("La simulación no ha sido inicializada.")
        return cls._instancia

    @classmethod
    def reiniciar_instancia(cls, n_vertices, m_aristas, n_pedidos, sujeto_observable=None, estrategia_ruta=None):
        cls._instancia = None
        return cls(n_vertices, m_aristas, n_pedidos, sujeto_observable, estrategia_ruta)

    def __init__(self, n_vertices, m_aristas, n_pedidos, sujeto_observable=None, estrategia_ruta=None):
        # ...inicialización de la simulación, grafo, estrategias, etc...
        pass

    # Propiedades de solo lectura para los repositorios
    @property
    def repositorio_clientes(self):
        return self._repositorio_clientes

    @property
    def repositorio_almacenamientos(self):
        return self._repositorio_almacenamientos

    @property
    def repositorio_recargas(self):
        return self._repositorio_recargas

    @property
    def repositorio_vertices(self):
        return self._repositorio_vertices

    @property
    def repositorio_aristas(self):
        return self._repositorio_aristas

    @property
    def repositorio_pedidos(self):
        return self._repositorio_pedidos

    @property
    def repositorio_rutas(self):
        return self._repositorio_rutas

    # Métodos para exponer los hashmaps de cada entidad
    def obtener_clientes_hashmap(self):
        return self.repositorio_clientes.obtener_hashmap()

    def obtener_almacenamientos_hashmap(self):
        return self.repositorio_almacenamientos.obtener_hashmap()

    def obtener_recargas_hashmap(self):
        return self.repositorio_recargas.obtener_hashmap()

    def obtener_pedidos_hashmap(self):
        return self.repositorio_pedidos.obtener_hashmap()

    def obtener_vertices_hashmap(self):
        return self.repositorio_vertices.obtener_hashmap()

    def obtener_aristas_hashmap(self):
        return self.repositorio_aristas.obtener_hashmap()

    def obtener_rutas_hashmap(self):
        return self.repositorio_rutas.obtener_hashmap()

    # --- Observer pattern por composición ---
    def agregar_observador(self, observador):
        """Agrega un observador al sujeto observable."""
        self._sujeto_observable.agregar_observador(observador)

    def quitar_observador(self, observador):
        """Quita un observador del sujeto observable."""
        self._sujeto_observable.quitar_observador(observador)

    def notificar_evento(self, evento, datos=None):
        """Notifica a los observadores de un evento."""
        self._sujeto_observable.notificar_observadores(evento, datos)

    def _default_estrategia(self):
        return RutaEstrategiaDijkstra()

    def set_estrategia_ruta(self, nombre_estrategia):
        if nombre_estrategia not in self._registro_estrategias:
            raise ValueError(f"Estrategia de ruta '{nombre_estrategia}' no soportada")
        self._estrategia_ruta = self._registro_estrategias[nombre_estrategia]

    def serializar_estado(self):
        """
        Serializa el estado completo de la simulación usando los mapeadores y DTOs anidados.
        """
        from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado  # import local para evitar circular
        return RespuestaSimulacionEstado(
            clientes=[MapeadorCliente.a_dto(c) for c in self.clientes],
            almacenamientos=[MapeadorAlmacenamiento.a_dto(a) for a in self.almacenamientos],
            recargas=[MapeadorRecarga.a_dto(r) for r in self.estaciones_recarga],
            pedidos=[MapeadorPedido.a_dto(p) for p in self.pedidos],
            rutas=[MapeadorRuta.a_dto(r) for r in self.rutas],
            # ...otros campos según definición...
        )

    def obtener_estadisticas(self):
        # Construir el diccionario de rutas más frecuentes como {str(ruta): frecuencia}
        rutas_dict = {}
        if hasattr(self.rutas_avl, 'inorden_con_frecuencia'):
            rutas_frecuencia = self.rutas_avl.inorden_con_frecuencia()
            for camino, frecuencia in rutas_frecuencia:
                rutas_dict[' -> '.join(str(n) for n in camino)] = frecuencia
        elif hasattr(self.rutas_avl, 'inorden'):
            rutas_frecuencia = self.rutas_avl.inorden()
            for camino, frecuencia in rutas_frecuencia:
                rutas_dict[' -> '.join(str(n) for n in camino)] = frecuencia
        # vertices más visitados (ejemplo: contar ocurrencias en rutas)
        vertices_dict = {}
        for ruta in self.rutas:
            if hasattr(ruta, 'camino'):
                for vertice in ruta.camino:
                    key = str(vertice)
                    vertices_dict[key] = vertices_dict.get(key, 0) + 1
        # Tiempo de respuesta simulado (puede ser calculado real si se requiere)
        import time
        tiempo_respuesta = 0.0  # Aquí puedes calcular el tiempo real si lo deseas
        from Backend.API.DTOs.DTOsRespuesta.RespuestaEstadisticas import RespuestaEstadisticas  # import local para evitar circular
        return RespuestaEstadisticas(
            rutas_mas_frecuentes=rutas_dict,
            vertices_mas_visitados=vertices_dict,
            tiempo_respuesta=tiempo_respuesta
        )

    def _generar_vertices(self):
        n_clientes = max(1, int(self.n_vertices * 0.6))
        n_almacenamientos = max(1, int(self.n_vertices * 0.2))
        n_recargas = self.n_vertices - n_clientes - n_almacenamientos
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
        fabrica_clientes = FabricaClientes()
        fabrica_almacenamientos = FabricaAlmacenamientos()
        fabrica_recargas = FabricaRecargas()
        fabrica_vertices = FabricaVertices()
        for i in range(n_clientes):
            cliente = fabrica_clientes.crear(i, f"Cliente_{i}")
            self.clientes.append(cliente)
            repo_clientes.agregar(cliente)
            v = fabrica_vertices.crear(cliente)
            repo_vertices.agregar(v, cliente.id_cliente)
            self.grafo.insertar_vertice(cliente)
        for i in range(n_almacenamientos):
            almacen = fabrica_almacenamientos.crear(i + n_clientes, f"Almacen_{i}")
            self.almacenamientos.append(almacen)
            repo_almacenamientos.agregar(almacen)
            v = fabrica_vertices.crear(almacen)
            repo_vertices.agregar(v, almacen.id_almacenamiento)
            self.grafo.insertar_vertice(almacen)
        for i in range(n_recargas):
            recarga = fabrica_recargas.crear(i + n_clientes + n_almacenamientos, f"Recarga_{i}")
            self.estaciones_recarga.append(recarga)
            repo_recargas.agregar(recarga)
            v = fabrica_vertices.crear(recarga)
            repo_vertices.agregar(v, recarga.id_recarga)
            self.grafo.insertar_vertice(recarga)

    def _generar_aristas(self):
        """
        Genera las aristas del grafo, asegurando conectividad y evitando duplicidad.
        Utiliza la estrategia de rutas para verificar conectividad, nunca métodos del grafo.
        """
        repo_aristas = RepositorioAristas()
        repo_aristas.limpiar()
        vertices = list(self.grafo.vertices())
        n = len(vertices)
        if n < 2:
            return
        aristas = set()
        conectados = set([0])
        # Conectar todos los vertices asegurando conectividad mínima
        while len(conectados) < n:
            conectado = random.choice(list(conectados))
            nuevo = random.choice([i for i in range(n) if i not in conectados])
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
        estrategia = self._estrategia_ruta or self._default_estrategia()
        for cliente in self.clientes:
            vertice_cliente = self.grafo.buscar_vertice_por_elemento(cliente)
            tiene_camino = False
            for almacen in self.almacenamientos:
                vertice_almacen = self.grafo.buscar_vertice_por_elemento(almacen)
                try:
                    camino, _ = estrategia.calcular_ruta(vertice_almacen, vertice_cliente, self.grafo)
                    if camino:
                        tiene_camino = True
                        break
                except Exception:
                    continue
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
        # Obtener siempre los vértices únicos del grafo
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
            # Refuerza unicidad: siempre usa referencias únicas de vértices
            logger.info(f"Creando pedido {i} con vertice_cliente: {vertice_cliente}, vertice_cliente.elemento: {getattr(vertice_cliente, 'elemento', lambda: None)() if vertice_cliente else None}, vertice_almacen: {vertice_almacen}, vertice_almacen.elemento: {getattr(vertice_almacen, 'elemento', lambda: None)() if vertice_almacen else None}, prioridad: {prioridad}, fecha: {fecha_simulacion}")
            pedido = self.fabrica_pedidos.crear(
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

    def registrar_error_pedido(self, id_pedido, motivo, datos=None):
        """
        Registra un error relacionado con un pedido incompleto o inválido.
        Args:
            id_pedido (int): ID del pedido.
            motivo (str): Descripción del error.
            datos (dict, opcional): Datos adicionales del pedido o contexto.
        """
        error = {
            'id_pedido': id_pedido,
            'error': motivo,
            'datos': datos
        }
        self._errores_pedidos.append(error)

    def obtener_errores_pedidos(self):
        """
        Retorna la lista de errores de pedidos registrados en la simulación.
        Returns:
            list: Lista de errores de pedidos.
        """
        return self._errores_pedidos

    def listar_clientes(self):
        """
        Devuelve la lista de clientes como DTOs completos.
        """
        return [MapeadorCliente.a_dto(c) for c in self.clientes]

    def listar_almacenamientos(self):
        """
        Devuelve la lista de almacenamientos como DTOs completos.
        """
        return [MapeadorAlmacenamiento.a_dto(a) for a in self.almacenamientos]

    def listar_recargas(self):
        """
        Devuelve la lista de recargas como DTOs completos.
        """
        return [MapeadorRecarga.a_dto(r) for r in self.estaciones_recarga]

    def listar_pedidos(self):
        """
        Devuelve la lista de pedidos como DTOs completos.
        """
        return [MapeadorPedido.a_dto(p) for p in self.pedidos]

    def obtener_cliente(self, id):
        for v in self.clientes:
            if v.id_cliente == id:
                return MapeadorCliente.a_dto(v)
        raise KeyError(f"Cliente con id {id} no encontrado")

    def obtener_almacenamiento(self, id):
        for v in self.almacenamientos:
            if v.id_almacenamiento == id:
                return MapeadorAlmacenamiento.a_dto(v)
        raise KeyError(f"Almacenamiento con id {id} no encontrado")

    def obtener_recarga(self, id):
        for v in self.estaciones_recarga:
            if v.id_recarga == id:
                return MapeadorRecarga.a_dto(v)
        raise KeyError(f"Recarga con id {id} no encontrada")

    def obtener_pedido(self, id):
        for p in self.pedidos:
            if p.id_pedido == id:
                return MapeadorPedido.a_dto(p)
        raise KeyError(f"Pedido con id {id} no encontrado")

    def obtener_ruta(self, id):
        for r in self.rutas:
            if hasattr(r, 'id') and r.id == id:
                return MapeadorRuta.a_dto(r)
        raise KeyError(f"Ruta con id {id} no encontrada")

    def calcular_ruta_pedido(self, id_pedido, algoritmo=None):
        from Backend.Dominio.Dominio_Ruta import Ruta
        from Backend.Servicios.EntFabricas.FabricaRutas import FabricaRutas
        import time
        logger = logging.getLogger("SimulacionDominio")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[Simulacion.calcular_ruta_pedido] Calculando ruta para pedido {id_pedido} usando algoritmo {algoritmo or self._estrategia_ruta}")
        if id_pedido not in self.hash_pedidos:
            logger.error(f"Pedido con id {id_pedido} no encontrado")
            raise KeyError(f"Pedido con id {id_pedido} no encontrado")
        pedido = self.hash_pedidos[id_pedido]
        origen = pedido.origen
        destino = pedido.destino
        if pedido.es_enviado():
            logger.warning(f"El pedido {id_pedido} ya fue enviado")
            raise ValueError("El pedido ya fue enviado")
        estrategia = self._estrategia_ruta
        if algoritmo:
            if algoritmo in self._registro_estrategias:
                estrategia = self._registro_estrategias[algoritmo]
            else:
                logger.error(f"Algoritmo de ruta no soportado: {algoritmo}")
                raise ValueError("Algoritmo de ruta no soportado")
        t0 = time.time()
        camino, costo = estrategia.calcular_ruta(origen, destino, self.grafo)
        t1 = time.time()
        tiempo_calculo = t1 - t0
        logger.info(f"[Simulacion.calcular_ruta_pedido] Ruta calculada: camino={camino}, costo={costo}, tiempo_calculo={tiempo_calculo}")
        if not camino:
            logger.error("No existe una ruta posible entre los vertices seleccionados.")
            raise ValueError("No existe una ruta posible entre los vertices seleccionados.")
        fabrica_rutas = FabricaRutas()
        ruta = fabrica_rutas.crear(origen, destino, camino, costo, algoritmo or estrategia.__class__.__name__, tiempo_calculo)
        pedido.asignar_ruta(ruta, costo)
        self.rutas.append(ruta)
        logger.info(f"[Simulacion.calcular_ruta_pedido] Ruta asignada a pedido {id_pedido}: {ruta}")
        self.notificar_evento("ruta_calculada", ruta)
        logger.info(f"[Simulacion.calcular_ruta_pedido] Evento 'ruta_calculada' notificado para ruta: {ruta}")
        return MapeadorRuta.a_dto(ruta)

    def marcar_pedido_entregado(self, id_pedido):
        pedido = self.obtener_pedido(id_pedido)
        pedido.marcar_entregado()
        self.notificar_evento("pedido_entregado", pedido)
        return pedido

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
            "n_vertices": self.n_vertices,
            "m_aristas": self.m_aristas,
            "n_pedidos": self.n_pedidos
        }

    def calcular_todos_los_caminos_floyd_warshall(self):
        """
        Calcula todos los caminos mínimos entre todos los pares de vertices usando la estrategia Floyd-Warshall.
        Retorna dos diccionarios: distancias y caminos.
        """
        estrategia = self._registro_estrategias.get('floyd_warshall', RutaEstrategiaFloydWarshall())
        vertices = list(self.grafo.vertices())
        n = len(vertices)
        distancias = {}
        caminos = {}
        for i, origen in enumerate(vertices):
            for j, destino in enumerate(vertices):
                if i != j:
                    camino, costo = estrategia.calcular_ruta(origen, destino, self.grafo)
                    if camino:
                        distancias[(origen, destino)] = costo
                        caminos[(origen, destino)] = camino
        return distancias, caminos

    def calcular_camino_entre_vertices(self, origen_id: int, destino_id: int, algoritmo: str = None):
        """
        Calcula el camino entre dos vertices usando la estrategia inyectada o la especificada.
        Retorna un dict serializable con origen, destino, camino, peso_total, algoritmo.
        """
        grafo = self.grafo
        vertices = list(grafo.vertices())
        v_origen = next((v for v in vertices if getattr(v.elemento(), 'id', None) == origen_id or getattr(v.elemento(), 'id_cliente', None) == origen_id or getattr(v.elemento(), 'id_almacenamiento', None) == origen_id or getattr(v.elemento(), 'id_recarga', None) == origen_id), None)
        v_destino = next((v for v in vertices if getattr(v.elemento(), 'id', None) == destino_id or getattr(v.elemento(), 'id_cliente', None) == destino_id or getattr(v.elemento(), 'id_almacenamiento', None) == destino_id or getattr(v.elemento(), 'id_recarga', None) == destino_id), None)
        if v_origen is None or v_destino is None:
            raise ValueError("vertice origen o destino no encontrado")
        estrategia = self._estrategia_ruta
        if algoritmo:
            if algoritmo in self._registro_estrategias:
                estrategia = self._registro_estrategias[algoritmo]
            else:
                raise ValueError("Algoritmo de ruta no soportado")
        camino, costo = estrategia.calcular_ruta(v_origen, v_destino, grafo)
        if not camino:
            return None
        camino_ids = [getattr(v.elemento(), 'id', None) or getattr(v.elemento(), 'id_cliente', None) or getattr(v.elemento(), 'id_almacenamiento', None) or getattr(v.elemento(), 'id_recarga', None) for v in camino]
        return {
            'origen': origen_id,
            'destino': destino_id,
            'camino': camino_ids,
            'peso_total': costo,
            'algoritmo': algoritmo or estrategia.__class__.__name__
        }

    def calcular_arbol_expansion_minima(self):
        """
        Calcula el árbol de expansión mínima usando la estrategia de Kruskal.
        Retorna una lista de aristas y el peso total del árbol.
        """
        estrategia = self._registro_estrategias['kruskal']
        vertices = list(self.grafo.vertices())
        if not vertices or len(vertices) < 2:
            raise ValueError("No hay suficientes vértices en el grafo para calcular el árbol de expansión mínima.")
        # Siempre pasa referencias únicas de vértices
        origen = vertices[0]
        destino = vertices[1]
        mst, peso_total = estrategia.calcular_ruta(origen, destino, self.grafo)
        return mst, peso_total

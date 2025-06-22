from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.Infraestructura.Repositorios.repositorio_recargas import RepositorioRecargas
from Backend.Infraestructura.Repositorios.repositorio_vertices import RepositorioVertices
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
from Backend.Servicios.Observer.SujetoObservable import SujetoObservable
from Backend.Servicios.Observer.ObserverEstadisticas import ObserverEstadisticas
from Backend.Servicios.Observer.ObserverPedidos import ObserverPedidos
from Backend.Infraestructura.TDA.TDA_AVL import AVL
import logging
import random
import traceback

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

    def registrar_observadores_global(self, observers=None):
        """
        Registra todos los observers relevantes en todos los repositorios, TDA y entidades de dominio.
        Permite auditar y trazar todos los eventos importantes de la simulación.
        """
        if observers is None:
            observers = [self._observer_estadisticas, self._observer_pedidos]
        # Repositorios y sus hashmaps
        for repo in [self._repo_clientes, self._repo_almacenamientos, self._repo_recargas, self._repo_vertices, self._repo_aristas, self._repo_pedidos, self._repo_rutas]:
            for obs in observers:
                repo.agregar_observador(obs)
            # HashMap interno
            if hasattr(repo, 'obtener_hashmap'):
                hashmap = repo.obtener_hashmap()
                if hashmap:
                    for obs in observers:
                        hashmap.agregar_observador(obs)
        # TDA AVL
        for obs in observers:
            self._avl_rutas.agregar_observador(obs)
        # Grafo (si existe)
        if hasattr(self._repo_vertices, 'grafo') and self._repo_vertices.grafo:
            for obs in observers:
                self._repo_vertices.grafo.agregar_observador(obs)

    def registrar_observadores_entidad(self, entidad, observers=None):
        """
        Registra los observers en una entidad de dominio (Cliente, Almacenamiento, Recarga, Pedido, Arista, etc).
        """
        if observers is None:
            observers = [self._observer_estadisticas, self._observer_pedidos]
        if hasattr(entidad, 'agregar_observador'):
            for obs in observers:
                entidad.agregar_observador(obs)

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observers registrados en la simulación.
        Cumple con la interfaz IObserver (evento, sujeto, datos).
        """
        for observador in getattr(self, '_observadores', []):
            try:
                observador.actualizar(evento, self, datos)
            except Exception as e:
                import logging
                logging.error(f"Error notificando observer {type(observador).__name__}: {e}")

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
            self._avl_rutas = AVL()
            # Instanciar observers
            self._observer_estadisticas = ObserverEstadisticas(servicio_estadisticas=None)  # Pasa el servicio real
            self._observer_pedidos = ObserverPedidos()  # Instancia real
            self._observadores = [self._observer_estadisticas, self._observer_pedidos]
            # Registrar observers en todos los componentes
            self.registrar_observadores_global(self._observadores)
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
        import random
        from collections import defaultdict, deque
        import logging
        logger = logging.getLogger("Simulacion")
        # Limpiar repositorios
        self._repo_clientes.limpiar()
        self._repo_almacenamientos.limpiar()
        self._repo_recargas.limpiar()
        self._repo_vertices.limpiar()
        self._repo_aristas.limpiar()
        self._repo_pedidos.limpiar()
        self._repo_rutas.limpiar()

        # 1. Crear vertices temporales (sin persistencia)
        almacenes = []
        clientes = []
        recargas = []
        total_almacenes = max(1, int(n_vertices * 0.2))
        total_recargas = max(1, int(n_vertices * 0.2))
        total_clientes = n_vertices - total_almacenes - total_recargas
        id_vertices = 0
        for i in range(total_almacenes):
            nombre = f"Almacen_{i} (Vertice {id_vertices})"
            almacen = self.fabricas['almacenamientos'].crear(id_vertices, nombre)
            almacenes.append(almacen)
            id_vertices += 1
        for i in range(total_recargas):
            nombre = f"Recarga_{i} (Vertice {id_vertices})"
            recarga = self.fabricas['recargas'].crear(id_vertices, nombre)
            recargas.append(recarga)
            id_vertices += 1
        for i in range(total_clientes):
            nombre = f"Cliente_{i} (Vertice {id_vertices})"
            cliente = self.fabricas['clientes'].crear(id_vertices, nombre)
            clientes.append(cliente)
            id_vertices += 1
        logger.info(f"[Depuracion] Almacenes generados: {almacenes}")
        logger.info(f"[Depuracion] Recargas generadas: {recargas}")
        logger.info(f"[Depuracion] Clientes generados: {clientes}")

        # 2. Crear grafo temporal puro Python (sin persistencia)
        vertices_tmp = almacenes + recargas + clientes
        id_map = {v: idx for idx, v in enumerate(vertices_tmp)}
        n = len(vertices_tmp)
        # Generar todas las posibles aristas (sin duplicados, no dirigido)
        posibles_aristas = []
        for i in range(n):
            for j in range(i+1, n):
                peso = random.randint(5, 40)
                posibles_aristas.append((i, j, peso))
        random.shuffle(posibles_aristas)

        # 3. Conectividad mínima: usar Union-Find para crear un árbol generador aleatorio
        parent = list(range(n))
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            pu, pv = find(u), find(v)
            if pu == pv:
                return False
            parent[pu] = pv
            return True
        aristas_utiles = []
        usados = set()
        for (u, v, peso) in posibles_aristas:
            if union(u, v):
                aristas_utiles.append((u, v, peso))
                usados.add((u, v))
                usados.add((v, u))
                if len(aristas_utiles) == n-1:
                    break
        # Guardar copia del árbol generador mínimo (persistencia garantizada)
        arbol_generador = list(aristas_utiles)
        usados_arbol = set(usados)

        # 4. Agregar aristas extra hasta m_aristas, validando segmentación
        extras = [a for a in posibles_aristas if (a[0], a[1]) not in usados_arbol and (a[1], a[0]) not in usados_arbol]
        random.shuffle(extras)
        def camino_segmentado(grafo, origen, destino, recarga_idxs):
            # BFS: cada estado es (nodo, bateria_restante)
            queue = deque()
            visitados = set()
            queue.append((origen, 50))
            while queue:
                actual, bateria = queue.popleft()
                if actual == destino:
                    return True
                for vecino, peso in grafo[actual]:
                    nueva_bateria = bateria - peso
                    es_recarga = vecino in recarga_idxs
                    if es_recarga:
                        nueva_bateria = 50
                    if nueva_bateria < 0:
                        continue
                    estado = (vecino, nueva_bateria)
                    if estado not in visitados:
                        visitados.add(estado)
                        queue.append(estado)
            return False
        # Construir grafo temporal para validación
        grafo_tmp = defaultdict(list)
        for (u, v, peso) in aristas_utiles:
            grafo_tmp[u].append((v, peso))
            grafo_tmp[v].append((u, peso))
        recarga_idxs = set(range(total_almacenes, total_almacenes + total_recargas))
        # Agregar aristas extra solo si no rompen la segmentación
        for (u, v, peso) in extras:
            if len(aristas_utiles) >= m_aristas:
                break
            # Probar agregar la arista
            grafo_tmp[u].append((v, peso))
            grafo_tmp[v].append((u, peso))
            valido = True
            for idx_almacen in range(total_almacenes):
                for idx_cliente in range(total_almacenes + total_recargas, n):
                    if not camino_segmentado(grafo_tmp, idx_almacen, idx_cliente, recarga_idxs):
                        valido = False
                        break
                if not valido:
                    break
            if valido:
                aristas_utiles.append((u, v, peso))
                usados_arbol.add((u, v))
                usados_arbol.add((v, u))
            else:
                # Si no es válido, quitar la arista
                grafo_tmp[u].pop()
                grafo_tmp[v].pop()

        # 5. Validar caminos segmentados entre cada (almacen, cliente) (garantía final)
        for idx_almacen in range(total_almacenes):
            for idx_cliente in range(total_almacenes + total_recargas, n):
                if not camino_segmentado(grafo_tmp, idx_almacen, idx_cliente, recarga_idxs):
                    raise Exception(f"No existe camino segmentado entre almacen {idx_almacen} y cliente {idx_cliente}")

        # 6. Persistir solo los vertices y aristas útiles
        # Persistir vertices
        for idx, v in enumerate(vertices_tmp):
            from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
            vertice = Vertice(v)
            id_elemento = getattr(v, 'id_cliente', None) or getattr(v, 'id_almacenamiento', None) or getattr(v, 'id_recarga', None)
            self._repo_vertices.agregar(vertice, idx)
            # Registrar en su repositorio correspondiente
            if hasattr(v, 'id_cliente'):
                self._repo_clientes.agregar(v)
                # Registrar observers en la entidad
                self.registrar_observadores_entidad(v)
            elif hasattr(v, 'id_almacenamiento'):
                self._repo_almacenamientos.agregar(v)
                self.registrar_observadores_entidad(v)
            elif hasattr(v, 'id_recarga'):
                self._repo_recargas.agregar(v)
                self.registrar_observadores_entidad(v)
        # Persistir aristas
        from Backend.Infraestructura.TDA.TDA_Arista import Arista
        for (u, v, peso) in aristas_utiles:
            vertice_u = self._repo_vertices.obtener(u)
            vertice_v = self._repo_vertices.obtener(v)
            arista = Arista(vertice_u, vertice_v, peso)
            clave = (
                getattr(vertice_u.elemento, 'id_cliente', None) or getattr(vertice_u.elemento, 'id_almacenamiento', None) or getattr(vertice_u.elemento, 'id_recarga', None),
                getattr(vertice_v.elemento, 'id_cliente', None) or getattr(vertice_v.elemento, 'id_almacenamiento', None) or getattr(vertice_v.elemento, 'id_recarga', None)
            )
            self._repo_aristas.agregar(arista, clave)
            # Registrar observers en la arista
            self.registrar_observadores_entidad(arista)
        # Generar pedidos aleatorios
        pedidos_generados = 0
        pedidos = []
        while pedidos_generados < n_pedidos:
            cliente = random.choice(clientes)
            almacen = random.choice(almacenes)
            prioridades = ['Muy Baja', 'Baja', 'Media', 'Alta', 'Muy Alta', 'Emergencia']
            prioridad = random.choice(prioridades)
            pedido = self.fabricas['pedidos'].crear(pedidos_generados, almacen, cliente, prioridad)
            self._repo_pedidos.agregar(pedido)
            self.registrar_observadores_entidad(pedido)
            pedidos.append(pedido)
            pedidos_generados += 1
        logger.info(f"[Depuracion] Pedidos generados: {pedidos}")
        # Notificar observadores
        self.notificar_observadores('simulacion_iniciada', {
            'vertices': self._repo_vertices.todos(),
            'aristas': self._repo_aristas.todos(),
            'clientes': self._repo_clientes.todos(),
            'almacenamientos': self._repo_almacenamientos.todos(),
            'recargas': self._repo_recargas.todos(),
            'pedidos': self._repo_pedidos.todos()
        })
        return True

    def registrar_observadores_entidad(self, entidad, observers=None):
        """
        Registra los observers en una entidad de dominio (Cliente, Almacenamiento, Recarga, Pedido, Arista, etc).
        """
        if observers is None:
            observers = [self._observer_estadisticas, self._observer_pedidos]
        if hasattr(entidad, 'agregar_observador'):
            for obs in observers:
                entidad.agregar_observador(obs)

    def obtener_vertices(self):
        return list(self._repo_vertices.todos())

    def obtener_aristas(self):
        return list(self._repo_aristas.todos())

    def obtener_clientes(self):
        return list(self._repo_clientes.todos())

    def obtener_almacenamientos(self):
        return list(self._repo_almacenamientos.todos())

    def obtener_recargas(self):
        return list(self._repo_recargas.todos())

    def obtener_pedidos(self):
        return list(self._repo_pedidos.todos())

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
        # Obtener todas las rutas y sus frecuencias
        rutas_frecuencias = self._avl_rutas.inorden()
        # Ordenar por frecuencia descendente
        rutas_frecuencias.sort(key=lambda x: x[1], reverse=True)
        # Tomar los top N
        top_rutas = rutas_frecuencias[:top]
        # Formatear para la API (puedes ajustar el formato según lo que espera el frontend)
        return [
            {"camino": ruta, "frecuencia": frecuencia}
            for ruta, frecuencia in top_rutas
        ]

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observers registrados en la simulación.
        Cumple con la interfaz IObserver (evento, sujeto, datos).
        """
        for observador in getattr(self, '_observadores', []):
            try:
                observador.actualizar(evento, self, datos)
            except Exception as e:
                import logging
                logging.error(f"Error notificando observer {type(observador).__name__}: {e}")

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

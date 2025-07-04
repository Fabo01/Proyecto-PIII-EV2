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
from Backend.Infraestructura.TDA.GrafoConstructor import GrafoConstructor
from Backend.Dominio.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
from Backend.Dominio.EntFabricas.FabricaClientes import FabricaClientes
from Backend.Dominio.EntFabricas.FabricaAlmacenamientos import FabricaAlmacenamientos
from Backend.Dominio.EntFabricas.FabricaRecargas import FabricaRecargas
from Backend.Dominio.EntFabricas.FabricaPedidos import FabricaPedidos
from Backend.Dominio.EntFabricas.FabricaRutas import FabricaRutas
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
        return cls._instancia

    def __init__(self, repo_clientes=None, repo_almacenamientos=None, repo_recargas=None, repo_vertices=None, repo_aristas=None, repo_pedidos=None, repo_rutas=None):
        if hasattr(self, '_inicializado') and self._inicializado:
            return
        super().__init__()
        self._repo_clientes = repo_clientes or RepositorioClientes()
        self._repo_almacenamientos = repo_almacenamientos or RepositorioAlmacenamientos()
        self._repo_recargas = repo_recargas or RepositorioRecargas()
        self._repo_vertices = repo_vertices or RepositorioVertices()
        self._repo_aristas = repo_aristas or RepositorioAristas()
        self._repo_pedidos = repo_pedidos or RepositorioPedidos()
        self._repo_rutas = repo_rutas or RepositorioRutas()
        # Observers
        self.observer_estadisticas = ObserverEstadisticas()
        self.observer_pedidos = ObserverPedidos()
        # AVL rutas
        self._avl_rutas = AVL()
        # Registrar observers en todos los repositorios y estructuras clave
        for repo in [self._repo_clientes, self._repo_almacenamientos, self._repo_recargas, self._repo_vertices, self._repo_aristas, self._repo_pedidos, self._repo_rutas]:
            repo.agregar_observador(self.observer_estadisticas)
            repo.agregar_observador(self.observer_pedidos)
        self._avl_rutas.agregar_observador(self.observer_estadisticas)
        self._avl_rutas.agregar_observador(self.observer_pedidos)
        self.agregar_observador(self.observer_estadisticas)
        self.agregar_observador(self.observer_pedidos)
        # Snapshots de grafos (privados)
        self._snapshots = {}
        self._grafo_n1 = None
        self._grafo_m = None
        self._grafo = None
        # Fábricas
        self.fabrica_vertices = FabricaVertices()
        self.fabrica_aristas = FabricaAristas()
        self.fabricante_clientes = FabricaClientes()
        self.fabricante_almacenamientos = FabricaAlmacenamientos()
        self.fabricante_recargas = FabricaRecargas()
        self.fabricante_pedidos = FabricaPedidos()
        self.fabricante_rutas = FabricaRutas()
        # Map of factories
        self.fabricas = {
            'clientes': self.fabricante_clientes,
            'almacenamientos': self.fabricante_almacenamientos,
            'recargas': self.fabricante_recargas,
            'vertices': self.fabrica_vertices,
            'aristas': self.fabrica_aristas,
            'pedidos': self.fabricante_pedidos,
            'rutas': self.fabricante_rutas
        }
        self._inicializado = True

    def registrar_observadores_global(self, observers=None):
        """
        Registra todos los observers relevantes en todos los repositorios, TDA y entidades de dominio.
        Permite auditar y trazar todos los eventos importantes de la simulación.
        """
        if observers is None:
            observers = [self.observer_estadisticas, self.observer_pedidos]
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
            observers = [self.observer_estadisticas, self.observer_pedidos]
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

    @property
    def repo_clientes(self):
        return self._repo_clientes

    @property
    def repo_almacenamientos(self):
        return self._repo_almacenamientos

    @property
    def repo_recargas(self):
        return self._repo_recargas

    @property
    def repo_vertices(self):
        return self._repo_vertices

    @property
    def repo_aristas(self):
        return self._repo_aristas

    @property
    def repo_pedidos(self):
        return self._repo_pedidos

    @property
    def repo_rutas(self):
        return self._repo_rutas

    @property
    def avl_rutas(self):
        return self._avl_rutas

    @property
    def snapshots(self):
        return self._snapshots

    @property
    def grafo_n1(self):
        return self._grafo_n1

    @property
    def grafo_m(self):
        return self._grafo_m

    @property
    def grafo(self):
        return self._grafo

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

    def obtener_clientes_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorCliente import MapeadorCliente
        return MapeadorCliente.lista_a_dto(self.obtener_clientes())

    def obtener_almacenamientos_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
        return MapeadorAlmacenamiento.lista_a_dto(self.obtener_almacenamientos())

    def obtener_recargas_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorRecarga import MapeadorRecarga
        return MapeadorRecarga.lista_a_dto(self.obtener_recargas())

    def obtener_vertices_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice
        return MapeadorVertice.lista_a_dto(self.obtener_vertices())

    def obtener_aristas_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
        return MapeadorArista.lista_a_dto(self.obtener_aristas())

    def obtener_pedidos_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
        return MapeadorPedido.lista_a_dto(self.obtener_pedidos())

    def obtener_rutas_hashmap_serializable(self):
        from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
        return MapeadorRuta.lista_a_dto(self.obtener_rutas())

    def obtener_clientes(self):
        """
        Retorna la lista de clientes registrados en el repositorio.
        """
        return self._repo_clientes.todos()

    def obtener_almacenamientos(self):
        """
        Retorna la lista de almacenamientos registrados en el repositorio.
        """
        return self._repo_almacenamientos.todos()

    def obtener_recargas(self):
        """
        Retorna la lista de recargas registradas en el repositorio.
        """
        return self._repo_recargas.todos()

    def obtener_pedidos(self):
        """
        Retorna la lista de pedidos registrados en el repositorio.
        """
        return self._repo_pedidos.todos()

    def obtener_vertices(self):
        """
        Retorna la lista de vértices registrados en el repositorio.
        """
        return self._repo_vertices.todos()

    def obtener_aristas(self):
        """
        Retorna la lista de aristas registradas en el repositorio.
        """
        return self._repo_aristas.todos()

    def obtener_rutas(self):
        """
        Retorna la lista de rutas registradas en el repositorio.
        """
        return self._repo_rutas.todos()

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int):
        """
        Inicializa la simulación creando entidades de dominio, vértices, aristas y pedidos usando fábricas y repositorios.
        Limpia todos los repositorios y fábricas antes de iniciar.
        Registra logs detallados de cada paso y notifica a los observadores al finalizar.
        """
        import logging
        from Backend.Dominio.EntFabricas.FabricaClientes import FabricaClientes
        from Backend.Dominio.EntFabricas.FabricaAlmacenamientos import FabricaAlmacenamientos
        from Backend.Dominio.EntFabricas.FabricaRecargas import FabricaRecargas
        from Backend.Dominio.EntFabricas.FabricaVertices import FabricaVertices
        from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
        from Backend.Dominio.EntFabricas.FabricaPedidos import FabricaPedidos
        from Backend.Infraestructura.TDA.GrafoConstructor import GrafoConstructor
        from random import randint, sample, shuffle
        from datetime import datetime

        logger = logging.getLogger("Simulacion")
        logger.info(f"Iniciando simulación: n_vertices={n_vertices}, m_aristas={m_aristas}, n_pedidos={n_pedidos}")
        # 1. Limpiar todas las fábricas y repositorios
        FabricaClientes().limpiar()
        FabricaAlmacenamientos().limpiar()
        FabricaRecargas().limpiar()
        FabricaVertices().limpiar()
        FabricaAristas().limpiar()
        FabricaPedidos().limpiar()
        FabricaRutas().limpiar()
        # 2. Crear entidades de dominio
        n_almacenamientos = max(1, n_vertices // 5)
        n_recargas = max(1, n_vertices // 5)
        n_clientes = n_vertices - n_almacenamientos - n_recargas
        logger.info(f"Clientes: {n_clientes}, Almacenamientos: {n_almacenamientos}, Recargas: {n_recargas}")
        ids_g = 1
        ids_c = 1
        clientes = []
        for _ in range(n_clientes):
            clientes.append(FabricaClientes().crear(ids_g, f"Cliente_{ids_c}"))
            ids_c += 1
            ids_g += 1

        ids_a = 1
        almacenamientos = []
        for _ in range(n_almacenamientos):
            almacenamientos.append(FabricaAlmacenamientos().crear(ids_g, f"Almacen_{ids_a}"))
            ids_a += 1
            ids_g += 1

        ids_r = 1
        recargas = []
        for _ in range(n_recargas):
            recargas.append(FabricaRecargas().crear(ids_g, f"Recarga_{ids_r}"))
            ids_r += 1
            ids_g += 1
        # 3. Unificar elementos de dominio en orden: almacenamientos, recargas, clientes
        elementos = almacenamientos + recargas + clientes
        # Validar que no hay None
        for idx, el in enumerate(elementos):
            if el is None:
                logger.error(f"Elemento None detectado en la posición {idx} de elementos de dominio. Abortando inicialización.")
                raise ValueError("No se pudo crear una entidad de dominio válida.")
        # 4. Crear vértices para cada elemento
        vertices = [FabricaVertices().crear(el) for el in elementos]
        logger.info(f"Vértices creados: {len(vertices)}")
        # 5. Generar todas las aristas posibles (combinaciones de 2 vértices, peso aleatorio 1-50)
        from itertools import combinations
        indices = list(range(len(elementos)))  # <--- CORRECCIÓN: Definir indices
        aristas_candidatas = set()
        for u, v in combinations(indices, 2):
            peso = randint(1, 50)
            aristas_candidatas.add((u, v, peso))
        aristas_candidatas = list(aristas_candidatas)
        logger.info(f"Aristas candidatas generadas: {len(aristas_candidatas)}")
        # 6. Construir el grafo usando GrafoConstructor (él filtra y valida segmentación/conectividad)
        grafo_constructor = GrafoConstructor(
            n_vertices=len(elementos),
            m_aristas=m_aristas,
            aristas_candidatas=aristas_candidatas,
            elementos=elementos
        )
        try:
            logger.info(f"[SIMULACION] Iniciando construcción del grafo con GrafoConstructor...")
            grafo_constructor.construir()
            logger.info(f"[SIMULACION] Grafo construido exitosamente")
            
            # Guardar referencias a los grafos y snapshots generados
            self._grafo_n1 = grafo_constructor.grafo_n1
            self._grafo_m = grafo_constructor.grafo_m
            self._grafo = grafo_constructor.grafo_m  # El grafo principal es el completo
            self._snapshots = grafo_constructor.snapshots
            
            logger.info(f"[SIMULACION] Snapshots guardados: {list(self._snapshots.keys())}")
            logger.info(f"[SIMULACION] Grafo n-1: {self._grafo_n1 is not None}")
            logger.info(f"[SIMULACION] Grafo m: {self._grafo_m is not None}")
            
            # Verificar contenido de snapshots
            for tipo, snapshot in self._snapshots.items():
                vertices_count = len(snapshot.get('vertices', [])) if isinstance(snapshot, dict) else 0
                aristas_count = len(snapshot.get('aristas', [])) if isinstance(snapshot, dict) else 0
                logger.info(f"[SIMULACION] Snapshot '{tipo}': {vertices_count} vértices, {aristas_count} aristas")
            
        except Exception as e:
            logger.error(f"[SIMULACION] Error al construir el grafo: {e}")
            import traceback
            logger.error(f"[SIMULACION] Traceback: {traceback.format_exc()}")
            raise ValueError("No se pudo construir un árbol conexo válido bajo segmentación. Pruebe aumentando m_aristas o revise la generación de aristas.")
        # 7. Obtener vértices del grafo final para creación de pedidos
        vertices = list(grafo_constructor.grafo_m.vertices())
        logger.info(f"Vértices en grafo final: {len(vertices)}")
        # 8. Crear pedidos usando solo vértices válidos del grafo
        pedidos = []
        for i in range(n_pedidos):
            vertice_cliente = vertices[n_almacenamientos + n_recargas + (i % n_clientes)]
            vertice_almacen = vertices[i % n_almacenamientos]
            prioridad = random.choice(['Muy baja', 'Baja', 'Media', 'Alta', 'Muy alta', 'Emergencia'])
            pedido = FabricaPedidos().crear(i+1, vertice_cliente, vertice_almacen, prioridad)
            if pedido is not None:
                # Asociar pedido al cliente y al almacenamiento usando repositorios
                self._repo_clientes.asociar_pedido_a_cliente(vertice_cliente.elemento.id_cliente, pedido)
                self._repo_almacenamientos.asociar_pedido_a_almacenamiento(vertice_almacen.elemento.id_almacenamiento, pedido)
                pedidos.append(pedido)
        logger.info(f"Pedidos creados: {len(pedidos)}")
        self.notificar_observadores('simulacion_iniciada', {
            'n_vertices': n_vertices,
            'm_aristas': m_aristas,
            'n_pedidos': n_pedidos
        })
        return True

    def marcar_pedido_entregado(self, id_pedido: int):
        pedido = self.repo_pedidos.obtener(id_pedido)
        pedido.actualizar_status("entregado")
        self.notificar_observadores("entrega_pedido", {"pedido": id_pedido})
        return pedido

    def buscar_pedido(self, id_pedido: int):
        return self.repo_pedidos.obtener(id_pedido)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        """
        Obtiene las rutas más frecuentes del AVL.
        Retorna una lista de diccionarios con camino y frecuencia.
        """
        try:
            # Obtener todas las rutas y sus frecuencias del AVL
            rutas_frecuencias = self._avl_rutas.inorden()
            # Ordenar por frecuencia descendente
            rutas_frecuencias.sort(key=lambda x: x[1], reverse=True)
            # Tomar los top N
            top_rutas = rutas_frecuencias[:top]
            # Formatear para la API
            resultado = []
            for clave_camino, frecuencia in top_rutas:
                # La clave_camino es ya un string con formato "id1->id2->id3"
                vertices_camino = clave_camino.split("->") if "->" in clave_camino else [clave_camino]
                resultado.append({
                    "camino": vertices_camino,
                    "frecuencia": frecuencia
                })
            return resultado
        except Exception as e:
            import logging
            logging.getLogger("Simulacion").warning(f"Error obteniendo rutas más frecuentes: {e}")
            return []

    def reiniciar_todo(self):
        self.repo_vertices.limpiar()
        self.repo_aristas.limpiar()
        self.repo_clientes.limpiar()
        self.repo_almacenamientos.limpiar()
        self.repo_recargas.limpiar()
        self.repo_pedidos.limpiar()
        self.repo_rutas.limpiar()
        self._avl_rutas = AVL()
        # Set estado flag
        self.estado = 'reiniciado'
        self.notificar_observadores("simulacion_reiniciada", {})

    def reiniciar(self):
        """Alias para reiniciar_todo, por compatibilidad con los tests."""
        self.reiniciar_todo()  
        
    def snapshot(self, tipo: str) -> dict:
        """
        Devuelve el snapshot del grafo según el tipo solicitado ('n-1' o 'm_aristas').
        Incluye logs detallados para debugging y múltiples fuentes de snapshots.
        """
        import logging
        logger = logging.getLogger("Simulacion")
        logger.info(f"[SNAPSHOT] Solicitado snapshot tipo: '{tipo}'")
        
        # Verificar snapshots en caché
        if hasattr(self, '_snapshots') and self._snapshots and tipo in self._snapshots:
            snapshot = self._snapshots[tipo]
            logger.info(f"[SNAPSHOT] Encontrado en _snapshots: {len(snapshot.get('vertices', []))} vértices, {len(snapshot.get('aristas', []))} aristas")
            return snapshot
        
        # Verificar grafos directos
        if tipo == 'n-1' and hasattr(self, '_grafo_n1') and self._grafo_n1:
            logger.info(f"[SNAPSHOT] Generando desde _grafo_n1...")
            snapshot = self._grafo_n1.snapshot()
            logger.info(f"[SNAPSHOT] Generado desde _grafo_n1: {len(snapshot.get('vertices', []))} vértices, {len(snapshot.get('aristas', []))} aristas")
            return snapshot
        
        if tipo == 'm_aristas' and hasattr(self, '_grafo_m') and self._grafo_m:
            logger.info(f"[SNAPSHOT] Generando desde _grafo_m...")
            snapshot = self._grafo_m.snapshot()
            logger.info(f"[SNAPSHOT] Generado desde _grafo_m: {len(snapshot.get('vertices', []))} vértices, {len(snapshot.get('aristas', []))} aristas")
            return snapshot
        
        # Verificar grafo principal
        if hasattr(self, '_grafo') and self._grafo:
            logger.info(f"[SNAPSHOT] Generando desde _grafo principal...")
            snapshot = self._grafo.snapshot()
            logger.info(f"[SNAPSHOT] Generado desde _grafo principal: {len(snapshot.get('vertices', []))} vértices, {len(snapshot.get('aristas', []))} aristas")
            return snapshot
        
        # Log estado de debugging
        logger.warning(f"[SNAPSHOT] No se encontró snapshot tipo '{tipo}':")
        logger.warning(f"[SNAPSHOT] _snapshots existe: {hasattr(self, '_snapshots')}")
        logger.warning(f"[SNAPSHOT] _snapshots contenido: {getattr(self, '_snapshots', {})}")
        logger.warning(f"[SNAPSHOT] _grafo_n1 existe: {hasattr(self, '_grafo_n1')}")
        logger.warning(f"[SNAPSHOT] _grafo_m existe: {hasattr(self, '_grafo_m')}")
        logger.warning(f"[SNAPSHOT] _grafo existe: {hasattr(self, '_grafo')}")
        
        return {}
        
    @property
    def repositorios(self):
        return {
            'clientes': self._repo_clientes,
            'almacenamientos': self._repo_almacenamientos,
            'recargas': self._repo_recargas,
            'vertices': self._repo_vertices,
            'aristas': self._repo_aristas,
            'pedidos': self._repo_pedidos,
            'rutas': self._repo_rutas
        }

    def calcular_ruta(self, id_pedido: int, algoritmo: str):
        """
        Calcula una ruta para un pedido usando el algoritmo especificado y la registra en el AVL y en el repositorio único de rutas.
        Garantiza unicidad y persistencia usando la fábrica y el repositorio inyectados en la simulación.
        """
        # Obtener el pedido real desde el repositorio único de pedidos
        pedido = self._repo_pedidos.obtener(id_pedido)
        if pedido is None:
            return None
        grafo = self._grafo or None
        # Usar la única fábrica de rutas inyectada en la simulación
        ruta = self.fabricante_rutas.calcular_ruta(pedido, grafo, algoritmo)
        # Registrar en AVL y asegurar unicidad en el repositorio
        if ruta is not None:
            # La FabricaRutas ya se encarga de insertar en el AVL automáticamente
            # try:
            #     self._avl_rutas.insertar(pedido.id_pedido, ruta)
            # except Exception:
            #     pass
            # Asegurar que la ruta esté en el repositorio único de la simulación
            if hasattr(self, '_repo_rutas'):
                clave = (
                    getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None),
                    getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None),
                    algoritmo
                )
                self._repo_rutas.agregar(ruta, clave)
        return ruta

    def calcular_ruta_todos(self, id_pedido: int):
        """
        Calcula rutas para un pedido usando todos los algoritmos disponibles.
        Garantiza unicidad y persistencia usando la fábrica y el repositorio inyectados en la simulación.
        """
        pedido = self._repo_pedidos.obtener(id_pedido)
        if pedido is None:
            return {}
        grafo = self._grafo or None
        rutas_dict = self.fabricante_rutas.calcular_ruta_todos(pedido, grafo)
        # Registrar cada ruta en el AVL y en el repositorio único
        if rutas_dict:
            for algoritmo, ruta in rutas_dict.items():
                if ruta is not None:
                    # La FabricaRutas ya se encarga de insertar en el AVL automáticamente
                    # try:
                    #     self._avl_rutas.insertar(pedido.id_pedido, ruta)
                    # except Exception:
                    #     pass
                    if hasattr(self, '_repo_rutas'):
                        ori_id = getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None)
                        dst_id = getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None)
                        clave = f"{ori_id}-{dst_id}-{algoritmo}"
                        self._repo_rutas.agregar(ruta, clave)
        return rutas_dict

    def floydwarshall_para_todos_los_pedidos(self):
        """
        Ejecuta Floyd-Warshall global y crea rutas para todos los pedidos.
        Garantiza unicidad y persistencia usando la fábrica y el repositorio inyectados en la simulación.
        """
        pedidos = self._repo_pedidos.listar() if hasattr(self._repo_pedidos, 'listar') else []
        grafo = self._grafo or None
        resultados = {}
        for pedido in pedidos:
            if pedido is None:
                continue
            ruta = self.fabricante_rutas.calcular_ruta(pedido, grafo, 'floydwarshall')
            if ruta is not None:
                # La FabricaRutas ya se encarga de insertar en el AVL automáticamente
                # try:
                #     self._avl_rutas.insertar(pedido.id_pedido, ruta)
                # except Exception:
                #     pass
                if hasattr(self, '_repo_rutas'):
                    ori_id = getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None)
                    dst_id = getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None)
                    clave = f"{ori_id}-{dst_id}-floydwarshall"
                    self._repo_rutas.agregar(ruta, clave)
            resultados[pedido.id_pedido] = ruta
        return resultados

    def entregar_pedido(self, id_pedido: int):
        """
        Marca un pedido como entregado usando la fábrica.
        """
        pedido = self._repo_pedidos.obtener(id_pedido)
        entrega = self.fabricante_rutas.entregar_pedido(pedido)
        return entrega

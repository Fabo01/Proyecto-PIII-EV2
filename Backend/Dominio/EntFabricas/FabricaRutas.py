"""
FabricaRutas: Fábrica centralizada para la creación y validación de rutas.
Garantiza unicidad y registro de errores.
Utiliza FabricaVertices y FabricaAristas para componentes internos.
"""
from Backend.Dominio.Dominio_Ruta import Ruta
from Backend.Dominio.EntFabricas.FabricaVertices import FabricaVertices
from Backend.Dominio.EntFabricas.FabricaAristas import FabricaAristas
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz
from Backend.Dominio.AlgEstrategias import RutaEstrategiaBFS, RutaEstrategiaDijkstra, RutaEstrategiaDFS, RutaEstrategiaFloydWarshall, RutaEstrategiaTopologicalSort
import concurrent.futures
import time
import logging

class FabricaRutas(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        # Singleton con repositorio de rutas
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
        return cls._instancia

    def crear(self, origen, destino, camino, peso_total, algoritmo, tiempo_calculo=None, id_pedido=None):
        """
        Crea una ruta y la almacena en el repositorio, garantizando unicidad y validez.
        Si ya existe una ruta con la misma clave, retorna la instancia existente.
        """
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        from Backend.Dominio.Dominio_Ruta import Ruta
        import logging
        logger = logging.getLogger("FabricaRutas")
        repo = RepositorioRutas()
        # Generar clave única de ruta como string para consistencia en el HashMap
        ori_id = getattr(origen.elemento, 'id_cliente', None) or getattr(origen.elemento, 'id_almacenamiento', None) or getattr(origen.elemento, 'id_recarga', None)
        dst_id = getattr(destino.elemento, 'id_cliente', None) or getattr(destino.elemento, 'id_almacenamiento', None) or getattr(destino.elemento, 'id_recarga', None)
        id_ruta_key = f"{ori_id}-{dst_id}-{algoritmo}"
        logger.info(f"Intentando crear ruta: clave={id_ruta_key}, origen={origen}, destino={destino}, algoritmo={algoritmo}, id_pedido={id_pedido}")
        existente = repo.obtener(id_ruta_key)
        if existente:
            logger.info(f"[FabricaRutas] Ruta ya existente en repositorio: clave={id_ruta_key}, id_pedido={getattr(existente, 'id_pedido', None)}")
            return existente
        # Validar que el camino es una lista de aristas reales y extremos correctos
        if not camino or not isinstance(camino, list) or not all(hasattr(a, 'origen') and hasattr(a, 'destino') for a in camino):
            logger.error(f"[FabricaRutas] Camino inválido para la ruta: {camino}")
            self.errores.append(f"Camino inválido para la ruta: {camino}")
            return None
        if camino[0].origen != origen or camino[-1].destino != destino:
            logger.error(f"[FabricaRutas] Los extremos del camino no coinciden con origen/destino")
            self.errores.append("Los extremos del camino no coinciden con origen/destino")
            return None
        try:
            if id_pedido is None:
                logger.warning(f"[FabricaRutas] id_pedido no proporcionado al crear ruta, se recomienda siempre pasar el id real del pedido.")
            # Asignar id_ruta como clave única definida previamente
            id_ruta = id_ruta_key
            ruta = Ruta(id_ruta_key, id_pedido, origen, destino, camino, peso_total, algoritmo, tiempo_calculo)
            # Registrar ruta en repositorio usando clave string uniforme
            repo.agregar(ruta, id_ruta_key)
            # También insertar en el AVL de la simulación singleton para análisis de frecuencias
            self._actualizar_avl_simulacion(ruta, id_pedido)
            logger.info(f"[FabricaRutas] Ruta creada correctamente y registrada en repositorio singleton: {ruta} (id_pedido={id_pedido})")
            return ruta
        except Exception as e:
            logger.error(f"[FabricaRutas] Error creando ruta: {e}")
            self.errores.append(str(e))
            return None

    def obtener(self, clave):
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        return RepositorioRutas().obtener(clave)

    def todos(self):
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        return RepositorioRutas().todos()

    def limpiar(self):
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        RepositorioRutas().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de rutas.
        """
        return self.errores

    def calcular_ruta(self, pedido, grafo, algoritmo, autonomia=50):
        """
        Calcula y crea una ruta para un pedido usando un algoritmo específico.
        Si ya existe una ruta con el mismo origen, destino y algoritmo, la retorna.
        Siempre trabaja con el objeto real de memoria y actualiza el repositorio para unicidad.
        """
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        import time
        import logging
        logger = logging.getLogger("FabricaRutas")
        # Generar clave única de ruta como string para consistencia
        ori_id = getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None)
        dst_id = getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None)
        id_ruta_key = f"{ori_id}-{dst_id}-{algoritmo}"
        repo = RepositorioRutas()
        existente = repo.obtener(id_ruta_key)
        if existente:
            logger.info(f"[FabricaRutas] Ruta ya existente en repositorio: clave={id_ruta_key}")
            return existente
        # Si no existe, calcular y crear
        inicio = time.time()
        estrategias = {
            'bfs': RutaEstrategiaBFS.RutaEstrategiaBFS,
            'dfs': RutaEstrategiaDFS.RutaEstrategiaDFS,
            'dijkstra': RutaEstrategiaDijkstra.RutaEstrategiaDijkstra,
            'floydwarshall': RutaEstrategiaFloydWarshall.RutaEstrategiaFloydWarshall,
            'topologicalsort': RutaEstrategiaTopologicalSort.RutaEstrategiaTopologicalSort
        }
        Estrategia = estrategias.get(algoritmo.lower())
        if not Estrategia:
            logger.error(f"Algoritmo de ruta no soportado: {algoritmo}")
            self.errores.append(f"Algoritmo de ruta no soportado: {algoritmo}")
            return None
        estrategia = Estrategia()
        camino, peso_total = estrategia.calcular_ruta(pedido.origen, pedido.destino, grafo, autonomia)
        tiempo = time.time() - inicio
        if not camino or peso_total is None or peso_total == float('inf'):
            logger.error(f"No existe una ruta posible entre los vertices seleccionados (clave={id_ruta_key})")
            self.errores.append(f"No existe una ruta posible entre los vertices seleccionados (clave={id_ruta_key})")
            return None
        # Crear la ruta y asociar correctamente el id_pedido
        # Crear y registrar la nueva ruta usando la clave string uniforme
        ruta = self.crear(pedido.origen, pedido.destino, camino, peso_total, algoritmo, tiempo_calculo=tiempo, id_pedido=getattr(pedido, 'id_pedido', None))
        logger.info(f"[FabricaRutas] Ruta calculada y registrada para pedido {getattr(pedido, 'id_pedido', None)}: {ruta}")
        return ruta

    def calcular_ruta_todos(self, pedido, grafo, autonomia=50, max_workers=12):
        """
        Calcula rutas para un pedido con todos los algoritmos disponibles.
        Retorna un dict {algoritmo: Ruta} y reutiliza rutas existentes.
        """
        import time
        import logging
        logger = logging.getLogger("FabricaRutas")
        estrategias_clases = {
            'bfs': RutaEstrategiaBFS.RutaEstrategiaBFS,
            'dfs': RutaEstrategiaDFS.RutaEstrategiaDFS,
            'dijkstra': RutaEstrategiaDijkstra.RutaEstrategiaDijkstra,
            'floydwarshall': RutaEstrategiaFloydWarshall.RutaEstrategiaFloydWarshall,
            'topologicalsort': RutaEstrategiaTopologicalSort.RutaEstrategiaTopologicalSort
        }
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        repo = RepositorioRutas()
        resultados = {}
        tiempos = {}
        for algoritmo, Estrategia in estrategias_clases.items():
            # Clave única de ruta como string consistente con crear()
            ori_id = getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None)
            dst_id = getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None)
            id_ruta_key = f"{ori_id}-{dst_id}-{algoritmo}"
            existente = repo.obtener(id_ruta_key)
            if existente:
                logger.info(f"[FabricaRutas] Ruta ya existente en repositorio: clave={id_ruta_key}")
                resultados[algoritmo] = existente
                tiempos[algoritmo] = 0.0
                continue
            inicio = time.time()
            estrategia = Estrategia()
            camino, peso_total = estrategia.calcular_ruta(pedido.origen, pedido.destino, grafo, autonomia)
            tiempo_alg = time.time() - inicio
            if not camino or peso_total is None or peso_total == float('inf'):
                logger.error(f"No existe una ruta posible entre los vertices seleccionados (clave={id_ruta_key})")
                self.errores.append(f"No existe una ruta posible entre los vertices seleccionados (clave={id_ruta_key})")
                resultados[algoritmo] = None
                tiempos[algoritmo] = tiempo_alg
                continue
            # Crear y registrar la nueva ruta
            ruta = self.crear(pedido.origen, pedido.destino, camino, peso_total, algoritmo, tiempo_alg, id_pedido=getattr(pedido, 'id_pedido', None))
            logger.info(f"[FabricaRutas] Ruta creada y registrada en repositorio singleton: {ruta}")
            resultados[algoritmo] = ruta
            tiempos[algoritmo] = tiempo_alg
        return resultados

    def calcular_rutas_algoritmos(self, pedidos, grafo, autonomia=50, max_workers=12):
        """
        Calcula rutas para todos los pedidos y algoritmos en paralelo, usando chunks por pedido.
        Cada proceso calcula todas las rutas de un pedido (todos los algoritmos).
        Retorna un dict {algoritmo: {id_pedido: ruta}} y un dict de tiempos.
        Siempre guarda cada ruta en el repositorio para unicidad y persistencia.
        """
        import concurrent.futures
        import time
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        logger = logging.getLogger("FabricaRutas")
        estrategias_clases = {
            'bfs': RutaEstrategiaBFS.RutaEstrategiaBFS,
            'dfs': RutaEstrategiaDFS.RutaEstrategiaDFS,
            'dijkstra': RutaEstrategiaDijkstra.RutaEstrategiaDijkstra,
            'floydwarshall': RutaEstrategiaFloydWarshall.RutaEstrategiaFloydWarshall,
            'topologicalsort': RutaEstrategiaTopologicalSort.RutaEstrategiaTopologicalSort
        }
        repo = RepositorioRutas()
        resultados = {alg: {} for alg in estrategias_clases}
        tiempos = {alg: 0 for alg in estrategias_clases}
        def tarea_chunk(pedido):
            """Tarea para calcular rutas de un solo pedido, respetando unicidad por clave string"""
            id_pedido = getattr(pedido, 'id_pedido', None)
            res_pedido = {}
            tiempos_pedido = {}
            for algoritmo, Estrategia in estrategias_clases.items():
                # Clave única de ruta como string consistente con crear()
                ori_id = getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None)
                dst_id = getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None)
                id_ruta_key = f"{ori_id}-{dst_id}-{algoritmo}"
                existente = repo.obtener(id_ruta_key)
                if existente:
                    logger.info(f"[FabricaRutas] Ruta ya existente en repositorio: clave={id_ruta_key}")
                    res_pedido[algoritmo] = existente
                    tiempos_pedido[algoritmo] = 0
                    continue
                inicio = time.time()
                estrategia = Estrategia()
                camino, peso_total = estrategia.calcular_ruta(pedido.origen, pedido.destino, grafo, autonomia)
                tiempo_alg = time.time() - inicio
                if not camino or peso_total is None or peso_total == float('inf'):
                    logger.error(f"No existe una ruta posible entre los vertices seleccionados (clave={id_ruta_key})")
                    res_pedido[algoritmo] = None
                    tiempos_pedido[algoritmo] = tiempo_alg
                    continue
                ruta = self.crear(pedido.origen, pedido.destino, camino, peso_total, algoritmo, tiempo_alg, id_pedido=id_pedido)
                logger.info(f"[FabricaRutas] Ruta creada y registrada en repositorio singleton: {ruta}")
                res_pedido[algoritmo] = ruta
                tiempos_pedido[algoritmo] = tiempo_alg
            return (id_pedido, res_pedido, tiempos_pedido)
        pedidos_filtrados = [p for p in pedidos if getattr(p, 'status', None) == 'pendiente']
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for id_pedido, res_pedido, tiempos_pedido in executor.map(tarea_chunk, pedidos_filtrados):
                for algoritmo, ruta in res_pedido.items():
                    if ruta:
                        resultados[algoritmo][id_pedido] = ruta
                        tiempos[algoritmo] += tiempos_pedido[algoritmo]
        return resultados, tiempos

    def floydwarshall_para_todos_los_pedidos(self, pedidos, grafo, autonomia=50, max_workers=12):
        """
        Calcula rutas óptimas para todos los pedidos usando Floyd-Warshall en paralelo.
        Retorna (rutas: list Ruta, tiempo_total: float).
        Optimiza evitando recalcular rutas existentes y guarda en repositorio.
        """
        from Backend.Dominio.AlgEstrategias.RutaEstrategiaFloydWarshall import RutaEstrategiaFloydWarshall
        from Backend.Infraestructura.Repositorios.repositorio_rutas import RepositorioRutas
        import concurrent.futures
        logger = logging.getLogger("FabricaRutas")
        repo = RepositorioRutas()
        estrategia = RutaEstrategiaFloydWarshall()
        rutas_resultado = []
        def tarea(pedido):
            # Generar clave única de ruta como string para consistencia en el HashMap
            ori_id = getattr(pedido.origen.elemento, 'id_cliente', None) or getattr(pedido.origen.elemento, 'id_almacenamiento', None) or getattr(pedido.origen.elemento, 'id_recarga', None)
            dst_id = getattr(pedido.destino.elemento, 'id_cliente', None) or getattr(pedido.destino.elemento, 'id_almacenamiento', None) or getattr(pedido.destino.elemento, 'id_recarga', None)
            clave = f"{ori_id}-{dst_id}-floydwarshall"
            existente = repo.obtener(clave)
            if existente:
                logger.info(f"[FabricaRutas] Ruta FloydWarshall ya existente en repositorio: clave={clave}")
                return existente
            camino, peso_total = estrategia.calcular_ruta(pedido.origen, pedido.destino, grafo, autonomia)
            if not camino or peso_total is None or peso_total == float('inf'):
                logger.error(f"No existe una ruta FloydWarshall posible entre los vertices seleccionados (clave={clave})")
                return None
            ruta = self.crear(pedido.origen, pedido.destino, camino, peso_total, 'floydwarshall', 0, id_pedido=getattr(pedido, 'id_pedido', None))
            logger.info(f"[FabricaRutas] Ruta FloydWarshall creada y registrada en repositorio singleton: {ruta}")
            return ruta
        inicio = time.time()
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for ruta in executor.map(tarea, [p for p in pedidos if getattr(p, 'status', None) == 'pendiente']):
                if ruta:
                    rutas_resultado.append(ruta)
        tiempo_total = time.time() - inicio
        return rutas_resultado, tiempo_total

    def entregar_pedido(self, pedido):
        """
        Marca un pedido como entregado en el dominio.
        """
        pedido.status = 'entregado'
        pedido.fecha_entrega = __import__('datetime').datetime.now().isoformat()
        return pedido

    def _actualizar_avl_simulacion(self, ruta, id_pedido):
        """
        Actualiza el AVL de la simulación singleton con la nueva ruta.
        Esto asegura que las rutas calculadas se reflejen en el análisis de frecuencias.
        """
        try:
            # Importar Simulacion aquí para evitar dependencias circulares
            from Backend.Dominio.Simulacion_dominio import Simulacion
            simulacion = Simulacion()
            if hasattr(simulacion, '_avl_rutas') and ruta is not None:
                # Usar el camino de la ruta como clave para el AVL y pasar el objeto ruta completo
                clave_camino = self._generar_clave_camino(ruta)
                simulacion._avl_rutas.insertar(clave_camino, ruta=ruta)  # Incrementa frecuencia y almacena ruta
                logging.getLogger("FabricaRutas").info(f"[FabricaRutas] Ruta insertada en AVL de simulación: camino={clave_camino}, id_ruta={ruta.id_ruta}")
        except Exception as e:
            logging.getLogger("FabricaRutas").warning(f"[FabricaRutas] No se pudo actualizar AVL de simulación: {e}")

    def _generar_clave_camino(self, ruta):
        """
        Genera una clave string para el AVL basada en el camino de vértices de la ruta.
        """
        try:
            if not ruta or not hasattr(ruta, 'camino') or not ruta.camino:
                return f"ruta_{ruta.id_ruta}" if hasattr(ruta, 'id_ruta') else "ruta_vacia"
            
            # Extraer IDs de vértices del camino de aristas
            vertices_camino = []
            if ruta.camino:
                # Agregar origen de la primera arista
                primera_arista = ruta.camino[0]
                if hasattr(primera_arista, 'origen') and hasattr(primera_arista.origen, 'elemento'):
                    origen_id = getattr(primera_arista.origen.elemento, 'id_cliente', None) or \
                               getattr(primera_arista.origen.elemento, 'id_almacenamiento', None) or \
                               getattr(primera_arista.origen.elemento, 'id_recarga', None)
                    vertices_camino.append(str(origen_id))
                
                # Agregar destinos de todas las aristas
                for arista in ruta.camino:
                    if hasattr(arista, 'destino') and hasattr(arista.destino, 'elemento'):
                        destino_id = getattr(arista.destino.elemento, 'id_cliente', None) or \
                                    getattr(arista.destino.elemento, 'id_almacenamiento', None) or \
                                    getattr(arista.destino.elemento, 'id_recarga', None)
                        vertices_camino.append(str(destino_id))
            
            return "->".join(vertices_camino) if vertices_camino else f"ruta_{ruta.id_ruta}"
        except Exception as e:
            logging.getLogger("FabricaRutas").warning(f"Error generando clave de camino: {e}")
            return f"ruta_{getattr(ruta, 'id_ruta', 'desconocida')}"

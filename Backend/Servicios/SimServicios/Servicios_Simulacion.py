from Backend.Dominio.Interfaces.IntSim.ISimulacionDominioService import ISimulacionDominioService
from Backend.Dominio.Simulacion_dominio import Simulacion
import time

class SimulacionDominioService(ISimulacionDominioService):
    """
    Servicio de dominio para la simulacion.
    Orquesta la logica de negocio usando la instancia de Simulacion inyectada.
    """
    def __init__(self, simulacion: Simulacion):
        self._sim = simulacion

    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int) -> None:
        self._sim.iniciar_simulacion(n_vertices, m_aristas, n_pedidos)
        return {
        "clientes": self._sim.obtener_clientes(),
        "almacenamientos": self._sim.obtener_almacenamientos(),
        "recargas": self._sim.obtener_recargas(),
        "pedidos": self._sim.obtener_pedidos(),
        "rutas": self._sim.obtener_rutas_mas_frecuentes(),
        "estado": "iniciada",
        "mensaje": None
    }

    def obtener_vertices(self):
        return self._sim.obtener_vertices()

    def obtener_aristas(self):
        return self._sim.obtener_aristas()

    def obtener_clientes(self):
        return self._sim.obtener_clientes()

    def obtener_almacenamientos(self):
        return self._sim.obtener_almacenamientos()

    def obtener_recargas(self):
        return self._sim.obtener_recargas()

    def obtener_pedidos(self):
        return self._sim.obtener_pedidos()

    def obtener_rutas(self):
        return self._sim.obtener_rutas()

    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = None):
        return self._sim.calcular_ruta_pedido(id_pedido, algoritmo)

    def marcar_pedido_entregado(self, id_pedido: int):
        return self._sim.marcar_pedido_entregado(id_pedido)

    def buscar_pedido(self, id_pedido: int):
        return self._sim.buscar_pedido(id_pedido)

    def obtener_cliente(self, id_cliente: int):
        return self._sim.repo_clientes.obtener(id_cliente)

    def obtener_almacenamiento(self, id_almacenamiento: int):
        return self._sim.repo_almacenamientos.obtener(id_almacenamiento)

    def obtener_recarga(self, id_recarga: int):
        return self._sim.repo_recargas.obtener(id_recarga)

    def obtener_pedido(self, id_pedido: int):
        return self._sim.repo_pedidos.obtener(id_pedido)

    def obtener_ruta(self, id_ruta: int):
        return self._sim.repo_rutas.obtener(id_ruta)

    def obtener_rutas_mas_frecuentes(self, top: int = 5):
        return self._sim.obtener_rutas_mas_frecuentes(top)

    def obtener_rutas_hashmap(self):
        return self._sim.obtener_rutas_hashmap()

    def obtener_vertices_hashmap(self):
        return self._sim.obtener_vertices_hashmap()

    def obtener_aristas_hashmap(self):
        return self._sim.obtener_aristas_hashmap()

    def obtener_clientes_hashmap(self):
        return self._sim.obtener_clientes_hashmap()

    def obtener_almacenamientos_hashmap(self):
        return self._sim.obtener_almacenamientos_hashmap()

    def obtener_recargas_hashmap(self):
        return self._sim.obtener_recargas_hashmap()

    def obtener_pedidos_hashmap(self):
        return self._sim.obtener_pedidos_hashmap()

    def obtener_clientes_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_clientes_hashmap_serializable()

    def obtener_clientes_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_clientes_hashmap()

    def obtener_almacenamientos_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_almacenamientos_hashmap_serializable()

    def obtener_almacenamientos_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_almacenamientos_hashmap()

    def obtener_recargas_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_recargas_hashmap_serializable()

    def obtener_recargas_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_recargas_hashmap()

    def obtener_vertices_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_vertices_hashmap_serializable()

    def obtener_vertices_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_vertices_hashmap()

    def obtener_aristas_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_aristas_hashmap_serializable()

    def obtener_aristas_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_aristas_hashmap()

    def obtener_pedidos_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_pedidos_hashmap_serializable()

    def obtener_pedidos_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_pedidos_hashmap()

    def obtener_rutas_hashmap_serializable(self):
        return self.simulacion_aplicacion_service.obtener_rutas_hashmap_serializable()

    def obtener_rutas_hashmap(self):
        return self.simulacion_aplicacion_service.obtener_rutas_hashmap()

    def obtener_estadisticas(self):
        """
        Compila estadísticas generales de la simulación:
        - rutas más frecuentes (AVL)
        - conteo de pedidos por estado y por cliente
        - distribución de vértices por tipo
        - total de vértices, aristas y pedidos
        - tiempo de respuesta de la consulta
        """
        import time
        inicio = time.time()
        # Rutas más frecuentes
        rutas_freq = self.obtener_rutas_mas_frecuentes()
        # Pedidos
        pedidos = self._sim.obtener_pedidos()
        total_pedidos = len(pedidos)
        pedidos_por_estado = {}
        pedidos_por_cliente = {}
        for ped in pedidos:
            estado = getattr(ped, 'status', None) or 'desconocido'
            pedidos_por_estado[estado] = pedidos_por_estado.get(estado, 0) + 1
            cliente = ped.obtener_cliente()
            cid = getattr(cliente, 'id_cliente', 'desconocido')
            pedidos_por_cliente[cid] = pedidos_por_cliente.get(cid, 0) + 1
        # Clientes, Almacenamientos y Recargas
        clientes = self._sim.obtener_clientes()
        almacenamientos = self._sim.obtener_almacenamientos()
        recargas = self._sim.obtener_recargas()
        total_clientes = len(clientes)
        total_almacenamientos = len(almacenamientos)
        total_recargas = len(recargas)
        # Vértices
        vertices = self._sim.obtener_vertices()
        total_vertices = len(vertices)
        vertices_por_tipo = {}
        for v in vertices:
            tipo = getattr(getattr(v, 'elemento', None), 'tipo_elemento', 'desconocido')
            vertices_por_tipo[tipo] = vertices_por_tipo.get(tipo, 0) + 1
        # Aristas
        aristas = self._sim.obtener_aristas()
        total_aristas = len(aristas)
        # Destinos más visitados (por entregas)
        vertices_mas_visitados = {}
        for ped in pedidos:
            if getattr(ped, 'status', None) == 'entregado':
                dest = ped.obtener_destino()
                if dest:
                    vid = getattr(dest, 'id_cliente', getattr(dest, 'id_almacenamiento', getattr(dest, 'id_recarga', None)))
                    if vid is not None:
                        vertices_mas_visitados[str(vid)] = vertices_mas_visitados.get(str(vid), 0) + 1
        fin = time.time()
        tiempo = fin - inicio
        # Estadísticas adicionales
        total_rutas_unicas = len(rutas_freq) if rutas_freq is not None else 0
        promedio_pedidos_por_cliente = round(total_pedidos / total_clientes, 4) if total_clientes > 0 else 0.0
        # Convertir claves numéricas a cadenas para cumplimiento del modelo Pydantic
        vertices_mas_visitados_str = {str(k): v for k, v in vertices_mas_visitados.items()}
        pedidos_por_cliente_str = {str(k): v for k, v in pedidos_por_cliente.items()}
        return {
            'rutas_mas_frecuentes': rutas_freq,
            'vertices_mas_visitados': vertices_mas_visitados_str,
            'pedidos_por_estado': pedidos_por_estado,
            'pedidos_por_cliente': pedidos_por_cliente_str,
            'vertices_por_tipo': vertices_por_tipo,
            'total_clientes': total_clientes,
            'total_almacenamientos': total_almacenamientos,
            'total_recargas': total_recargas,
            'total_vertices': total_vertices,
            'total_aristas': total_aristas,
            'total_pedidos': total_pedidos,
            'tiempo_respuesta': round(tiempo, 4),
            'total_rutas_unicas': total_rutas_unicas,
            'promedio_pedidos_por_cliente': promedio_pedidos_por_cliente
        }

    def set_estrategia_ruta(self, estrategia):
        self._sim.set_estrategia_ruta(estrategia)

    def notificar_evento(self, evento, datos=None):
        self._sim.notificar_observadores(evento, datos)

    def reiniciar_todo(self):
        self._sim.reiniciar_todo()

    # Nuevos métodos para frontend
    def obtener_algoritmos(self) -> list:
        """
        Devuelve la lista de algoritmos de ruta disponibles en el sistema.
        """
        return ['BFS', 'DFS', 'Dijkstra', 'FloydWarshall', 'TopologicalSort']

    def obtener_snapshot(self, tipo: str) -> dict:
        """
        Devuelve el snapshot serializado del grafo según el tipo ('n-1' o 'm_aristas').
        """
        if tipo == 'n-1' and hasattr(self._sim, 'grafo_n1') and self._sim.grafo_n1:
            return self._sim.grafo_n1.snapshot()
        elif tipo == 'm_aristas' and hasattr(self._sim, 'grafo_m') and self._sim.grafo_m:
            return self._sim.grafo_m.snapshot()
        elif hasattr(self._sim, 'snapshots') and tipo in self._sim.snapshots:
            return self._sim.snapshots[tipo]
        return {}

    def calcular_ruta(self, id_pedido: int, algoritmo: str):
        """
        Calcula una ruta para un pedido y algoritmo específico.
        """
        pedido = self._sim.repo_pedidos.obtener(id_pedido)
        if pedido is None:
            raise ValueError(f"No se encontró el pedido con ID {id_pedido}. Verifica que la simulación esté inicializada y que el pedido exista.")
        grafo = self._sim.grafo
        fabrica_rutas = self._sim.fabricante_rutas
        return fabrica_rutas.calcular_ruta(pedido, grafo, algoritmo)

    def calcular_ruta_todos(self, id_pedido: int):
        """
        Calcula rutas para un pedido con todos los algoritmos disponibles.
        """
        pedido = self._sim.repo_pedidos.obtener(id_pedido)
        if pedido is None:
            raise ValueError(f"No se encontró el pedido con ID {id_pedido}. Verifica que la simulación esté inicializada y que el pedido exista.")
        grafo = self._sim.grafo
        fabrica_rutas = self._sim.fabricante_rutas
        return fabrica_rutas.calcular_ruta_todos(pedido, grafo)

    def calcular_rutas_algoritmos(self):
        """
        Calcula rutas para todos los pedidos y algoritmos en paralelo.
        """
        pedidos = self._sim.repo_pedidos.todos()
        grafo = self._sim.grafo
        fabrica_rutas = self._sim.fabricante_rutas
        return fabrica_rutas.calcular_rutas_algoritmos(pedidos, grafo)

    def floydwarshall_para_todos_los_pedidos(self):
        """
        Calcula rutas óptimas para todos los pedidos usando Floyd-Warshall en paralelo.
        """
        pedidos = self._sim.repo_pedidos.todos()
        grafo = self._sim.grafo
        fabrica_rutas = self._sim.fabricante_rutas
        return fabrica_rutas.floydwarshall_para_todos_los_pedidos(pedidos, grafo)

    def entregar_pedido(self, id_pedido: int):
        """
        Marca un pedido como entregado.
        """
        return self._sim.entregar_pedido(id_pedido)

    def actualizar_estado_pedido(self, id_pedido: int, nuevo_estado: str):
        """
        Actualiza el estado de un pedido. Estados válidos: 'pendiente', 'enviado', 'entregado'
        """
        return self._sim.actualizar_estado_pedido(id_pedido, nuevo_estado)

    def calcular_mst_kruskal(self):
        """
        Calcula el Árbol de Expansión Mínima (MST) usando el algoritmo de Kruskal.
        Retorna las aristas del MST y el peso total.
        """
        from Backend.Dominio.AlgEstrategias.RutaEstrategiaKruskal import RutaEstrategiaKruskal
        import logging
        
        logger = logging.getLogger("MST_Kruskal")
        
        try:
            # Obtener el grafo de la simulación
            grafo = self._sim.grafo
            if not grafo or not grafo.vertices() or not grafo.aristas():
                return {
                    "aristas": [],
                    "peso_total": 0,
                    "mensaje": "No hay datos de grafo disponibles"
                }
            
            logger.info(f"Grafo disponible: {len(list(grafo.vertices()))} vértices, {len(list(grafo.aristas()))} aristas")
            
            # Crear una instancia de la estrategia Kruskal
            estrategia_kruskal = RutaEstrategiaKruskal()
            
            # Para MST no necesitamos origen/destino específicos, usamos cualquier vértice
            vertices = list(grafo.vertices())
            primer_vertice = vertices[0] if vertices else None
            
            if not primer_vertice:
                return {
                    "aristas": [],
                    "peso_total": 0,
                    "mensaje": "No hay vértices disponibles"
                }
            
            logger.info(f"Calculando MST desde vértice: {primer_vertice}")
            
            # Calcular MST usando la estrategia Kruskal
            mst_aristas = estrategia_kruskal.calcular_ruta(primer_vertice, primer_vertice, grafo)
            
            logger.info(f"MST calculado: {len(mst_aristas)} aristas")
            
            # Convertir las aristas del MST a formato serializable usando unicidad de datos
            aristas_serializadas = []
            peso_total = 0
            vertices_en_mst = set()
            
            for arista in mst_aristas:
                # Obtener IDs únicos de los vértices usando el elemento asociado
                origen_id = None
                destino_id = None
                
                # Extraer ID del origen
                if hasattr(arista.origen, 'elemento'):
                    elemento_origen = arista.origen.elemento
                    origen_id = getattr(elemento_origen, 'id_cliente', None) or \
                               getattr(elemento_origen, 'id_almacenamiento', None) or \
                               getattr(elemento_origen, 'id_recarga', None)
                
                # Extraer ID del destino
                if hasattr(arista.destino, 'elemento'):
                    elemento_destino = arista.destino.elemento
                    destino_id = getattr(elemento_destino, 'id_cliente', None) or \
                                getattr(elemento_destino, 'id_almacenamiento', None) or \
                                getattr(elemento_destino, 'id_recarga', None)
                
                # Si no se pueden obtener IDs del elemento, usar id_vertice como fallback
                if origen_id is None:
                    origen_id = getattr(arista.origen, 'id_vertice', str(arista.origen))
                
                if destino_id is None:
                    destino_id = getattr(arista.destino, 'id_vertice', str(arista.destino))
                
                logger.info(f"Arista MST: {origen_id} -> {destino_id} (peso: {arista.peso})")
                
                arista_data = {
                    "origen": origen_id,
                    "destino": destino_id,
                    "peso": arista.peso
                }
                aristas_serializadas.append(arista_data)
                peso_total += arista.peso
                vertices_en_mst.add(origen_id)
                vertices_en_mst.add(destino_id)
            
            logger.info(f"MST serializado: {len(aristas_serializadas)} aristas, peso total: {peso_total}")
            logger.info(f"Vértices en MST: {vertices_en_mst}")
            
            return {
                "aristas": aristas_serializadas,
                "peso_total": peso_total,
                "num_aristas": len(aristas_serializadas),
                "vertices_en_mst": list(vertices_en_mst),
                "mensaje": "MST calculado correctamente"
            }
            
        except Exception as e:
            return {
                "aristas": [],
                "peso_total": 0,
                "error": str(e),
                "mensaje": "Error al calcular MST"
            }
"""
Estrategia de ruta usando BFS.
"""
from Backend.Dominio.Interfaces.IntEstr.IRutaEstrategia import IRutaEstrategia
from collections import deque
import logging

class RutaEstrategiaBFS(IRutaEstrategia):
    def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
        logger = logging.getLogger("RutaEstrategiaBFS")
        logger.info(f"[BFS] Preparando para calcular ruta: origen={origen}, destino={destino}, autonomia={autonomia}")
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('inicio_calculo_ruta', {'algoritmo': 'bfs', 'origen': origen, 'destino': destino})
        assert origen in grafo.vertices(), "El vértice de origen no es único o no existe en el grafo."
        assert destino in grafo.vertices(), "El vértice de destino no es único o no existe en el grafo."

        logger.debug(f"[BFS] Estado inicial: queue vacía, visitados vacío")
        queue = deque()
        queue.append((origen, autonomia, [], 0))  # (vertice, energia_restante, camino_aristas, distancia_acumulada)
        
        # Cambiar estrategia: usar diccionario para rastrear la mejor energía por vértice
        # Esto permite exploración más exhaustiva mientras evita ciclos infinitos
        mejor_energia_por_vertice = {}  # vertice -> mejor_energia_vista
        mejor_energia_por_vertice[origen] = autonomia

        encontrado = False
        camino_final = None
        energia_final = None
        distancia_final = None
        max_iteraciones = 2000  # Incrementar límite para exploración más exhaustiva
        max_longitud_camino = len(list(grafo.vertices())) * 2  # Evitar caminos excesivamente largos

        logger.info(f"[BFS] Iniciando búsqueda: origen={origen}, destino={destino}, autonomia={autonomia}")
        logger.info(f"[BFS] Vértices disponibles en grafo: {len(list(grafo.vertices()))}")
        logger.info(f"[BFS] Aristas disponibles en grafo: {len(list(grafo.aristas()))}")

        iteracion = 0
        while queue and iteracion < max_iteraciones:
            iteracion += 1
            if iteracion % 100 == 0:  # log cada 100 iteraciones
                logger.debug(f"[BFS] Iteración {iteracion}: tamaño de la cola = {len(queue)}, vértices explorados = {len(mejor_energia_por_vertice)}")
            
            vertice_actual, energia_actual, camino_aristas, distancia_acumulada = queue.popleft()
            logger.debug(f"[BFS] Visitando: {vertice_actual} | Energia: {energia_actual} | Camino: {len(camino_aristas)} aristas | Distancia: {distancia_acumulada}")
            
            # Evitar caminos excesivamente largos (posibles ciclos)
            if len(camino_aristas) > max_longitud_camino:
                logger.debug(f"[BFS] Camino demasiado largo, descartando: {len(camino_aristas)} > {max_longitud_camino}")
                continue
            
            if vertice_actual == destino:
                encontrado = True
                camino_final = list(camino_aristas)
                energia_final = energia_actual
                distancia_final = distancia_acumulada
                logger.info(f"[BFS] Destino alcanzado: {destino} | Camino: {len(camino_aristas)} aristas | Distancia total: {distancia_final} | Energia restante: {energia_actual}")
                break
            
            # Explorar todas las aristas salientes
            aristas_salientes = list(grafo.aristas_incidentes(vertice_actual, salientes=True))
            logger.debug(f"[BFS] Explorando {len(aristas_salientes)} aristas desde {vertice_actual}")
            
            # Log adicional para debugging profundo
            if logger.isEnabledFor(logging.DEBUG):
                for i, arista in enumerate(aristas_salientes):
                    logger.debug(f"[BFS]   Arista {i+1}: {vertice_actual} -> {arista.destino} (peso: {arista.peso})")
            
            aristas_agregadas_cola = 0
            
            for arista in aristas_salientes:
                v = arista.destino
                peso = arista.peso
                logger.debug(f"[BFS] Evaluando arista: {vertice_actual} -> {v} | Peso: {peso} | Energia actual: {energia_actual}")
                
                # Validar que la arista no exceda la autonomía máxima
                if peso > autonomia:
                    logger.debug(f"[BFS] Arista descartada: peso {peso} > autonomía {autonomia}")
                    continue
                
                # Calcular energía después de tomar esta arista
                energia_siguiente = energia_actual - peso
                if energia_siguiente < 0:
                    logger.debug(f"[BFS] No hay suficiente energia: {energia_actual} - {peso} = {energia_siguiente}")
                    continue
                
                # Verificar si es estación de recarga
                es_recarga = hasattr(v.elemento, 'tipo_elemento') and getattr(v.elemento, 'tipo_elemento', None) == 'recarga'
                if es_recarga:
                    energia_siguiente = autonomia
                    logger.debug(f"[BFS] Llegando a estación de recarga en {v}, energía restaurada a {autonomia}")
                
                # Nueva estrategia: permitir exploración más amplia pero evitar ciclos excesivos
                # Solo descartar si la energía es significativamente menor Y ya hemos visitado muchas veces este vértice
                energy_threshold = 15  # Incrementar tolerancia de energía para permitir más exploración alternativa
                should_explore = True
                
                if v in mejor_energia_por_vertice:
                    energia_diferencia = mejor_energia_por_vertice[v] - energia_siguiente
                    
                    # Estrategia más permisiva: permitir exploración si:
                    # 1. Es una estación de recarga (siempre explorar)
                    # 2. La diferencia de energía es pequeña
                    # 3. El camino es relativamente corto (permite exploración inicial)
                    if es_recarga or energia_diferencia <= energy_threshold or len(camino_aristas) <= 3:
                        logger.debug(f"[BFS] Permitiendo exploración: energía {energia_siguiente} vs mejor {mejor_energia_por_vertice[v]} para {v} (recarga={es_recarga}, diff={energia_diferencia}, camino_len={len(camino_aristas)})")
                        should_explore = True
                    else:
                        logger.debug(f"[BFS] Estado descartado: energía {energia_siguiente} es {energia_diferencia} menor que mejor conocida {mejor_energia_por_vertice[v]} para {v}")
                        should_explore = False
                else:
                    logger.debug(f"[BFS] Primer acceso a vértice {v} con energía {energia_siguiente}")
                
                if not should_explore:
                    continue
                
                # Actualizar la mejor energía solo si es realmente mejor
                if v not in mejor_energia_por_vertice or energia_siguiente > mejor_energia_por_vertice[v]:
                    mejor_energia_por_vertice[v] = energia_siguiente
                
                # Añadir a la cola para exploración
                nuevo_camino = camino_aristas + [arista]
                nueva_distancia = distancia_acumulada + peso
                queue.append((v, energia_siguiente, nuevo_camino, nueva_distancia))
                aristas_agregadas_cola += 1
                logger.debug(f"[BFS] Encolado nuevo estado: {v} con energía {energia_siguiente}, distancia total {nueva_distancia}")
            
            # Log de resumen de esta iteración
            logger.debug(f"[BFS] Resumen iteración {iteracion}: {aristas_agregadas_cola} estados encolados desde {vertice_actual}, cola actual: {len(queue)} elementos")
            
            # Si no se agregó nada a la cola y la cola está vacía, log adicional para debug
            if aristas_agregadas_cola == 0 and len(queue) == 0:
                logger.warning(f"[BFS] ¡ALERTA! No se encolaron nuevos estados desde {vertice_actual} y la cola está vacía")
                logger.warning(f"[BFS] Aristas salientes disponibles: {len(aristas_salientes)}")
                for i, arista in enumerate(aristas_salientes):
                    energia_requerida = energia_actual - arista.peso
                    logger.warning(f"[BFS]   Arista {i+1}: {vertice_actual} -> {arista.destino} (peso: {arista.peso}, energia_requerida: {energia_requerida})")

        # Log final de estadísticas  
        logger.info(f"[BFS] Exploración terminada: {iteracion} iteraciones, {len(mejor_energia_por_vertice)} vértices únicos explorados")
        logger.info(f"[BFS] Razón de terminación: {'destino encontrado' if encontrado else 'cola vacía' if len(queue) == 0 else 'límite de iteraciones'}")
        
        # Debug adicional: verificar conectividad básica del grafo
        if not encontrado:
            logger.info(f"[BFS] Verificando conectividad básica del grafo...")
            vertices_alcanzables_simple = set([origen])
            for _ in range(len(list(grafo.vertices()))):  # máximo número de vértices
                nuevos_vertices = set()
                for v in vertices_alcanzables_simple:
                    for arista in grafo.aristas_incidentes(v, salientes=True):
                        if arista.peso <= autonomia:  # Solo aristas factibles
                            nuevos_vertices.add(arista.destino)
                if not nuevos_vertices - vertices_alcanzables_simple:
                    break  # No hay nuevos vértices alcanzables
                vertices_alcanzables_simple.update(nuevos_vertices)
            
            logger.info(f"[BFS] Análisis de conectividad: {len(vertices_alcanzables_simple)} vértices alcanzables desde {origen}")
            logger.info(f"[BFS] Destino {destino} {'SÍ' if destino in vertices_alcanzables_simple else 'NO'} está en el conjunto alcanzable")
            
            if destino in vertices_alcanzables_simple:
                logger.error(f"[BFS] ¡PROBLEMA! El destino ES alcanzable pero BFS no lo encontró - revisar lógica del algoritmo")

        try:
            if not encontrado:
                logger.warning(f"[BFS] No se encontró ruta entre {origen} y {destino}")
                logger.error(f"[BFS] DEBUG: Vértices explorados: {list(mejor_energia_por_vertice.keys())}")
                logger.error(f"[BFS] DEBUG: Mejor energía por vértice: {mejor_energia_por_vertice}")
                logger.error(f"[BFS] DEBUG: No se pudo alcanzar el destino. Cola final: {len(queue)} elementos restantes")
                
                # Verificar si el destino está realmente conectado al origen
                logger.error(f"[BFS] DEBUG: Verificando conectividad del grafo...")
                todos_vertices = list(grafo.vertices())
                logger.error(f"[BFS] DEBUG: Todos los vértices del grafo: {[str(v) for v in todos_vertices]}")
                
                # Verificar si el destino está en el grafo
                destino_en_grafo = destino in todos_vertices
                logger.error(f"[BFS] DEBUG: ¿Destino {destino} está en el grafo? {destino_en_grafo}")
                
                # Verificar aristas desde el origen
                aristas_desde_origen = list(grafo.aristas_incidentes(origen, salientes=True))
                logger.error(f"[BFS] DEBUG: Aristas desde origen {origen}: {[(str(a.destino), a.peso) for a in aristas_desde_origen]}")
                
                if hasattr(self, 'notificar_observadores'):
                    self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'bfs', 'origen': origen, 'destino': destino, 'error': 'No existe una ruta posible'})
                raise ValueError("No existe una ruta posible entre los vertices seleccionados")
            peso_total = sum(a.peso for a in camino_final)
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('ruta_calculada', {'algoritmo': 'bfs', 'camino': camino_final, 'peso_total': peso_total})
            logger.info(f"Ruta BFS calculada: aristas={len(camino_final)}, peso_total={peso_total}, distancia_final={distancia_final}")
            return camino_final, peso_total
        except Exception as e:
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_calculo_ruta', {'algoritmo': 'bfs', 'origen': origen, 'destino': destino, 'error': str(e)})
            logger.exception(f"[BFS] Excepción durante el cálculo de ruta: {e}")
            raise

    def _insertar_recargas_si_necesario(self, camino, grafo, autonomia, estaciones_recarga):
        if not estaciones_recarga:
            return camino, False
        nuevo_camino = []
        acumulado = 0
        for i in range(len(camino)-1):
            u, v = camino[i], camino[i+1]
            arista = next((a for a in grafo.aristas_incidentes(u, salientes=True) if a.destino == v), None)
            if arista is None:
                raise ValueError("Arista no encontrada en el grafo entre los vértices únicos.")
            peso = arista.peso
            acumulado += peso
            nuevo_camino.append(u)
            if acumulado > autonomia:
                recarga = self._buscar_estacion_recarga(u, estaciones_recarga, grafo)
                if recarga:
                    nuevo_camino.append(recarga)
                    acumulado = 0
        nuevo_camino.append(camino[-1])
        return nuevo_camino, True

    def _buscar_estacion_recarga(self, vertice, estaciones_recarga, grafo):
        for recarga in estaciones_recarga:
            if recarga in grafo.vecinos(vertice):
                return recarga
        return None

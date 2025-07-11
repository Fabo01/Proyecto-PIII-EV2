# Optimización y Rendimiento del Sistema

## Descripción General
Este documento describe las estrategias de optimización implementadas en el sistema de simulación logística de drones, incluyendo optimizaciones de algoritmos, estructuras de datos, memoria y rendimiento general del sistema.

## 🚀 Métricas de Rendimiento Objetivo

### Tiempos de Respuesta
- **Inicialización de simulación**: < 2 segundos (hasta 150 vértices)
- **Cálculo de ruta BFS**: < 500ms (grafo de 150 vértices)
- **Visualización de grafo**: < 1 segundo (150 vértices, 300 aristas)
- **Consulta en HashMap**: O(1) - < 1ms promedio
- **Búsqueda en AVL**: O(log n) - < 10ms para 1000 elementos

### Uso de Memoria
- **Simulación máxima**: < 512MB RAM (150 vértices, 500 pedidos)
- **Cache de rutas**: < 100MB para patrones frecuentes
- **Estructuras TDA**: < 50MB overhead total
- **Frontend visualización**: < 200MB renderizado completo

### Throughput
- **Procesamiento de pedidos**: > 100 pedidos/segundo
- **Cálculos de ruta concurrentes**: > 50 rutas/segundo
- **Actualizaciones de UI**: 30 FPS en visualizaciones

## 🔧 Optimizaciones de Estructuras de Datos

### HashMap Optimizado

#### Implementación Eficiente
```python
# Backend/Infraestructura/TDA/HashMap.py - Versión optimizada

class HashMap:
    def __init__(self, capacidad_inicial=16, factor_carga_max=0.75):
        self.capacidad = capacidad_inicial
        self.factor_carga_max = factor_carga_max
        self.tamaño_actual = 0
        self.buckets = [[] for _ in range(self.capacidad)]
        
        # Optimización: Pre-calcular capacidad de redimensionamiento
        self.umbral_redimension = int(self.capacidad * self.factor_carga_max)
    
    def _hash(self, clave):
        """Hash function optimizada para distribución uniforme"""
        if isinstance(clave, int):
            # Multiplicación por número primo para mejor distribución
            return (clave * 31) % self.capacidad
        elif isinstance(clave, str):
            # Algoritmo de hash DJB2 para strings
            hash_value = 5381
            for char in clave:
                hash_value = ((hash_value << 5) + hash_value) + ord(char)
            return hash_value % self.capacidad
        else:
            # Fallback para otros tipos
            return hash(clave) % self.capacidad
    
    def insertar(self, clave, valor):
        """Inserción optimizada con redimensionamiento inteligente"""
        # Verificar si necesita redimensionamiento ANTES de insertar
        if self.tamaño_actual >= self.umbral_redimension:
            self._redimensionar()
        
        indice = self._hash(clave)
        bucket = self.buckets[indice]
        
        # Búsqueda optimizada en bucket
        for i, (k, v) in enumerate(bucket):
            if k == clave:
                bucket[i] = (clave, valor)  # Actualizar existente
                return
        
        # Insertar nuevo elemento
        bucket.append((clave, valor))
        self.tamaño_actual += 1
    
    def obtener(self, clave):
        """Búsqueda optimizada con early return"""
        indice = self._hash(clave)
        bucket = self.buckets[indice]
        
        # Optimización: búsqueda desde el final (elementos recientes)
        for k, v in reversed(bucket):
            if k == clave:
                return v
        return None
    
    def _redimensionar(self):
        """Redimensionamiento eficiente con rehashing"""
        buckets_anteriores = self.buckets
        self.capacidad *= 2
        self.umbral_redimension = int(self.capacidad * self.factor_carga_max)
        self.buckets = [[] for _ in range(self.capacidad)]
        self.tamaño_actual = 0
        
        # Rehashing de todos los elementos
        for bucket in buckets_anteriores:
            for clave, valor in bucket:
                self.insertar(clave, valor)
```

#### Métricas de Rendimiento HashMap
```python
# Benchmark para validar rendimiento
def benchmark_hashmap():
    import time
    import random
    
    hashmap = HashMap()
    n_elementos = 10000
    
    # Test inserción
    start_time = time.time()
    for i in range(n_elementos):
        hashmap.insertar(f"clave_{i}", f"valor_{i}")
    tiempo_insercion = time.time() - start_time
    
    # Test búsqueda
    claves_busqueda = [f"clave_{random.randint(0, n_elementos-1)}" for _ in range(1000)]
    start_time = time.time()
    for clave in claves_busqueda:
        _ = hashmap.obtener(clave)
    tiempo_busqueda = time.time() - start_time
    
    print(f"Inserción {n_elementos} elementos: {tiempo_insercion:.3f}s")
    print(f"Búsqueda 1000 elementos: {tiempo_busqueda:.3f}s")
    print(f"Factor de carga: {hashmap.tamaño_actual / hashmap.capacidad:.2f}")
```

### AVL Optimizado para Rutas

#### Implementación con Cache
```python
# Backend/Infraestructura/TDA/AVL.py - Versión optimizada

class NodoAVL:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1
        self.frecuencia = 1  # Para rutas repetidas
        
        # Cache de información calculada
        self._factor_balance = 0
        self._cache_valido = False

class AVL:
    def __init__(self):
        self.raiz = None
        self.tamaño_actual = 0
        
        # Cache para búsquedas frecuentes
        self.cache_busquedas = {}
        self.cache_max_size = 100
    
    def insertar(self, clave, valor):
        """Inserción optimizada con incremento de frecuencia"""
        self.raiz = self._insertar_recursivo(self.raiz, clave, valor)
        self._limpiar_cache_si_necesario()
    
    def _insertar_recursivo(self, nodo, clave, valor):
        # Inserción estándar BST
        if not nodo:
            self.tamaño_actual += 1
            return NodoAVL(clave, valor)
        
        if clave < nodo.clave:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, clave, valor)
        elif clave > nodo.clave:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, clave, valor)
        else:
            # Clave existente - incrementar frecuencia
            nodo.frecuencia += 1
            nodo.valor = valor  # Actualizar valor si necesario
            return nodo
        
        # Actualizar altura y balance
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda),
                              self._obtener_altura(nodo.derecha))
        
        # Obtener factor de balance
        balance = self._obtener_balance(nodo)
        
        # Rotaciones para balanceo
        if balance > 1 and clave < nodo.izquierda.clave:
            return self._rotacion_derecha(nodo)
        if balance < -1 and clave > nodo.derecha.clave:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)
        
        return nodo
    
    def buscar_con_cache(self, clave):
        """Búsqueda optimizada con cache LRU"""
        if clave in self.cache_busquedas:
            # Mover al final (más reciente)
            valor = self.cache_busquedas.pop(clave)
            self.cache_busquedas[clave] = valor
            return valor
        
        # Búsqueda normal en árbol
        resultado = self.buscar(clave)
        
        # Agregar al cache
        if len(self.cache_busquedas) >= self.cache_max_size:
            # Eliminar el más antiguo (primer elemento)
            self.cache_busquedas.pop(next(iter(self.cache_busquedas)))
        
        self.cache_busquedas[clave] = resultado
        return resultado
    
    def obtener_rutas_mas_frecuentes(self, limite=10):
        """Obtener rutas ordenadas por frecuencia"""
        rutas_frecuencias = []
        self._recopilar_frecuencias(self.raiz, rutas_frecuencias)
        
        # Ordenar por frecuencia descendente
        rutas_frecuencias.sort(key=lambda x: x[1], reverse=True)
        return rutas_frecuencias[:limite]
    
    def _recopilar_frecuencias(self, nodo, lista):
        """Recopilación eficiente de frecuencias"""
        if nodo:
            lista.append((nodo.clave, nodo.frecuencia))
            self._recopilar_frecuencias(nodo.izquierda, lista)
            self._recopilar_frecuencias(nodo.derecha, lista)
```

## ⚡ Optimizaciones de Algoritmos

### BFS Optimizado para Rutas

#### Implementación con Poda Inteligente
```python
# Backend/Dominio/AlgEstrategias/RutaEstrategiaBFS.py - Optimizado

from collections import deque
import heapq

class RutaEstrategiaBFS:
    def __init__(self):
        self.cache_rutas = {}  # Cache de rutas calculadas
        self.estadisticas = {
            'cache_hits': 0,
            'cache_misses': 0,
            'nodos_explorados': 0,
            'tiempo_calculo': 0
        }
    
    def calcular_ruta(self, origen, destino, grafo, autonomia=50):
        """BFS optimizado con cache y poda inteligente"""
        import time
        start_time = time.time()
        
        # Verificar cache primero
        cache_key = f"{origen.id_vertice}_{destino.id_vertice}_{autonomia}"
        if cache_key in self.cache_rutas:
            self.estadisticas['cache_hits'] += 1
            return self.cache_rutas[cache_key]
        
        self.estadisticas['cache_misses'] += 1
        
        # BFS optimizado
        resultado = self._bfs_optimizado(origen, destino, grafo, autonomia)
        
        # Guardar en cache si la ruta es válida
        if resultado:
            self.cache_rutas[cache_key] = resultado
            
            # Limitar tamaño del cache
            if len(self.cache_rutas) > 1000:
                # Eliminar el 20% más antiguo
                claves_a_eliminar = list(self.cache_rutas.keys())[:200]
                for clave in claves_a_eliminar:
                    del self.cache_rutas[clave]
        
        self.estadisticas['tiempo_calculo'] += time.time() - start_time
        return resultado
    
    def _bfs_optimizado(self, origen, destino, grafo, autonomia):
        """BFS con optimizaciones específicas"""
        # Cola de prioridad para explorar caminos más prometedores primero
        cola = deque([(origen, [origen], 0, autonomia)])  # (vértice, camino, peso, energía)
        visitados = set()
        nodos_explorados = 0
        
        # Heurística: distancia euclidiana aproximada (si hay coordenadas)
        def distancia_estimada(v1, v2):
            # Placeholder - en implementación real usar coordenadas
            return 0
        
        while cola and nodos_explorados < 10000:  # Límite de seguridad
            vertice_actual, camino_actual, peso_actual, energia_actual = cola.popleft()
            nodos_explorados += 1
            
            # Crear estado único para evitar cycles
            estado = (vertice_actual.id_vertice, energia_actual)
            if estado in visitados:
                continue
            visitados.add(estado)
            
            # ¿Llegamos al destino?
            if vertice_actual == destino:
                self.estadisticas['nodos_explorados'] += nodos_explorados
                return {
                    'camino': camino_actual,
                    'peso_total': peso_actual,
                    'energia_restante': energia_actual,
                    'nodos_explorados': nodos_explorados
                }
            
            # Explorar aristas de manera optimizada
            aristas_salientes = grafo.aristas_incidentes(vertice_actual)
            
            # Ordenar aristas por peso (menor primero) para encontrar rutas más eficientes
            aristas_ordenadas = sorted(aristas_salientes, key=lambda a: a.peso)
            
            for arista in aristas_ordenadas:
                vertice_siguiente = arista.destino
                peso_arista = arista.peso
                
                # Poda: si el peso de la arista excede la energía actual, saltar
                if peso_arista > energia_actual:
                    continue
                
                # Poda: evitar bucles simples
                if vertice_siguiente in camino_actual:
                    continue
                
                nuevo_peso = peso_actual + peso_arista
                nueva_energia = energia_actual - peso_arista
                
                # Restaurar energía en estaciones de recarga
                if (hasattr(vertice_siguiente, 'elemento') and 
                    vertice_siguiente.elemento and
                    vertice_siguiente.elemento.tipo_elemento == "recarga"):
                    nueva_energia = autonomia  # Recarga completa
                
                nuevo_camino = camino_actual + [vertice_siguiente]
                
                # Poda: si el camino es muy largo, probablemente no es óptimo
                if len(nuevo_camino) > 20:
                    continue
                
                cola.append((vertice_siguiente, nuevo_camino, nuevo_peso, nueva_energia))
        
        self.estadisticas['nodos_explorados'] += nodos_explorados
        return None  # No se encontró ruta
    
    def limpiar_cache(self):
        """Limpiar cache para liberar memoria"""
        self.cache_rutas.clear()
        self.estadisticas = {
            'cache_hits': 0,
            'cache_misses': 0,
            'nodos_explorados': 0,
            'tiempo_calculo': 0
        }
    
    def obtener_estadisticas(self):
        """Obtener estadísticas de rendimiento"""
        total_consultas = self.estadisticas['cache_hits'] + self.estadisticas['cache_misses']
        if total_consultas > 0:
            hit_rate = self.estadisticas['cache_hits'] / total_consultas
        else:
            hit_rate = 0
            
        return {
            **self.estadisticas,
            'cache_hit_rate': hit_rate,
            'tamaño_cache': len(self.cache_rutas)
        }
```

### Optimización de Generación de Grafos

#### Algoritmo de Generación Conecta Eficiente
```python
# Backend/Dominio/EntFabricas/Fabrica_Grafo.py - Optimizado

import random
from collections import defaultdict, deque

class FabricaGrafoOptimizada:
    def __init__(self):
        self.cache_conectividad = {}
    
    def generar_grafo_conectado_optimizado(self, n_vertices, n_aristas):
        """Generación optimizada de grafo conectado"""
        if n_aristas < n_vertices - 1:
            raise ValueError("Aristas insuficientes para conectividad")
        
        vertices = []
        aristas = []
        
        # 1. Crear vértices eficientemente
        vertices = self._crear_vertices_lote(n_vertices)
        
        # 2. Generar árbol de expansión mínima (garantiza conectividad)
        aristas_mst = self._generar_mst_optimizado(vertices)
        aristas.extend(aristas_mst)
        
        # 3. Agregar aristas adicionales eficientemente
        aristas_adicionales = self._agregar_aristas_adicionales(
            vertices, aristas, n_aristas - len(aristas_mst)
        )
        aristas.extend(aristas_adicionales)
        
        # 4. Verificación final rápida
        if not self._verificar_conectividad_rapida(vertices, aristas):
            # Fallback: algoritmo tradicional
            return self._generar_fallback(n_vertices, n_aristas)
        
        return vertices, aristas
    
    def _crear_vertices_lote(self, n_vertices):
        """Creación de vértices en lote"""
        vertices = []
        
        # Calcular distribución
        n_clientes = int(n_vertices * 0.6)
        n_almacenes = int(n_vertices * 0.2)
        n_recargas = n_vertices - n_clientes - n_almacenes
        
        # Crear en lotes por tipo
        vertices.extend(self._crear_vertices_tipo("cliente", n_clientes))
        vertices.extend(self._crear_vertices_tipo("almacenamiento", n_almacenes))
        vertices.extend(self._crear_vertices_tipo("recarga", n_recargas))
        
        # Shuffle para distribución aleatoria
        random.shuffle(vertices)
        return vertices
    
    def _generar_mst_optimizado(self, vertices):
        """Generar MST usando algoritmo de Kruskal optimizado"""
        n = len(vertices)
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        
        # Generar todas las aristas posibles con pesos aleatorios
        aristas_candidatas = []
        for i in range(n):
            for j in range(i + 1, n):
                peso = random.randint(5, 25)
                aristas_candidatas.append((peso, i, j))
        
        # Ordenar por peso
        aristas_candidatas.sort()
        
        # Construir MST
        aristas_mst = []
        id_arista = 1
        
        for peso, i, j in aristas_candidatas:
            if union(i, j):
                arista = Arista(id_arista, vertices[i], vertices[j], peso)
                aristas_mst.append(arista)
                id_arista += 1
                if len(aristas_mst) == n - 1:
                    break
        
        return aristas_mst
    
    def _agregar_aristas_adicionales(self, vertices, aristas_existentes, n_adicionales):
        """Agregar aristas adicionales evitando duplicados"""
        aristas_existentes_set = set()
        for arista in aristas_existentes:
            par = (min(arista.origen.id_vertice, arista.destino.id_vertice),
                   max(arista.origen.id_vertice, arista.destino.id_vertice))
            aristas_existentes_set.add(par)
        
        aristas_adicionales = []
        intentos = 0
        max_intentos = n_adicionales * 10
        id_arista = len(aristas_existentes) + 1
        
        while len(aristas_adicionales) < n_adicionales and intentos < max_intentos:
            i, j = random.sample(range(len(vertices)), 2)
            par = (min(i, j), max(i, j))
            
            if par not in aristas_existentes_set:
                peso = random.randint(5, 25)
                arista = Arista(id_arista, vertices[i], vertices[j], peso)
                aristas_adicionales.append(arista)
                aristas_existentes_set.add(par)
                id_arista += 1
            
            intentos += 1
        
        return aristas_adicionales
    
    def _verificar_conectividad_rapida(self, vertices, aristas):
        """Verificación rápida de conectividad usando BFS"""
        if not vertices:
            return True
        
        # Construir lista de adyacencia
        adj = defaultdict(list)
        for arista in aristas:
            adj[arista.origen.id_vertice].append(arista.destino.id_vertice)
            adj[arista.destino.id_vertice].append(arista.origen.id_vertice)
        
        # BFS desde el primer vértice
        visitados = set()
        cola = deque([vertices[0].id_vertice])
        visitados.add(vertices[0].id_vertice)
        
        while cola:
            actual = cola.popleft()
            for vecino in adj[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        
        return len(visitados) == len(vertices)
```

## 💾 Optimizaciones de Memoria

### Gestión Eficiente de Repositorios

#### Pool de Objetos para Entidades
```python
# Backend/Infraestructura/Repositorios/pool_objetos.py

class PoolObjetos:
    """Pool de objetos reutilizables para reducir garbage collection"""
    
    def __init__(self):
        self.pools = {
            'Vertice': [],
            'Arista': [],
            'Ruta': [],
            'EstadoBFS': []
        }
        self.max_size_por_pool = 1000
    
    def obtener_objeto(self, tipo_clase, *args, **kwargs):
        """Obtener objeto del pool o crear nuevo"""
        pool = self.pools.get(tipo_clase, [])
        
        if pool:
            obj = pool.pop()
            # Reinicializar objeto
            if hasattr(obj, 'reinicializar'):
                obj.reinicializar(*args, **kwargs)
            return obj
        else:
            # Crear nuevo objeto
            if tipo_clase == 'Vertice':
                return Vertice(*args, **kwargs)
            elif tipo_clase == 'Arista':
                return Arista(*args, **kwargs)
            # ... otros tipos
    
    def devolver_objeto(self, obj, tipo_clase):
        """Devolver objeto al pool para reutilización"""
        pool = self.pools.get(tipo_clase, [])
        
        if len(pool) < self.max_size_por_pool:
            # Limpiar objeto antes de devolverlo
            if hasattr(obj, 'limpiar'):
                obj.limpiar()
            pool.append(obj)
    
    def limpiar_pools(self):
        """Limpiar todos los pools para liberar memoria"""
        for pool in self.pools.values():
            pool.clear()
```

### Lazy Loading para Visualizaciones

#### Carga Diferida de Datos Gráficos
```python
# frontendv2/servicios/optimizacion.py

class OptimizadorVisualizacion:
    """Optimizaciones para renderizado de grafos grandes"""
    
    def __init__(self):
        self.cache_layouts = {}
        self.umbral_simplificacion = 100  # Vértices
    
    def obtener_datos_grafo_optimizados(self, vertices, aristas, nivel_detalle='auto'):
        """Obtener datos optimizados según el tamaño del grafo"""
        n_vertices = len(vertices)
        
        if nivel_detalle == 'auto':
            if n_vertices <= 50:
                nivel_detalle = 'completo'
            elif n_vertices <= 100:
                nivel_detalle = 'medio'
            else:
                nivel_detalle = 'simplificado'
        
        if nivel_detalle == 'simplificado':
            return self._simplificar_grafo(vertices, aristas)
        elif nivel_detalle == 'medio':
            return self._optimizar_medio(vertices, aristas)
        else:
            return self._datos_completos(vertices, aristas)
    
    def _simplificar_grafo(self, vertices, aristas):
        """Simplificar grafo para renderizado rápido"""
        # Agrupar vértices cercanos
        vertices_agrupados = self._agrupar_vertices_por_tipo(vertices)
        
        # Reducir aristas redundantes
        aristas_principales = self._filtrar_aristas_principales(aristas)
        
        return {
            'vertices': vertices_agrupados,
            'aristas': aristas_principales,
            'simplificado': True,
            'factor_reduccion': len(vertices) / len(vertices_agrupados)
        }
    
    def _cache_layout_grafo(self, grafo_id, layout_data):
        """Cache de layouts calculados para reutilización"""
        if len(self.cache_layouts) > 10:
            # Eliminar el más antiguo
            oldest_key = next(iter(self.cache_layouts))
            del self.cache_layouts[oldest_key]
        
        self.cache_layouts[grafo_id] = layout_data
    
    def obtener_layout_cached(self, grafo_id):
        """Obtener layout desde cache si existe"""
        return self.cache_layouts.get(grafo_id)
```

## 📊 Monitoreo de Rendimiento

### Sistema de Métricas en Tiempo Real

#### Collector de Métricas
```python
# Backend/Servicios/SimServicios/metricas_rendimiento.py

import time
import threading
from collections import defaultdict, deque
from functools import wraps

class CollectorMetricas:
    """Recopilador de métricas de rendimiento del sistema"""
    
    def __init__(self):
        self.metricas = defaultdict(deque)
        self.contadores = defaultdict(int)
        self.tiempos_respuesta = defaultdict(list)
        self.max_historial = 1000
        self.lock = threading.Lock()
        
        # Métricas específicas del sistema
        self.inicializar_metricas_sistema()
    
    def inicializar_metricas_sistema(self):
        """Inicializar métricas específicas del dominio"""
        self.metricas_personalizadas = {
            'rutas_calculadas_total': 0,
            'cache_hits_rutas': 0,
            'cache_misses_rutas': 0,
            'vertices_visitados_promedio': 0,
            'tiempo_bfs_promedio': 0,
            'memoria_hashmap_mb': 0,
            'memoria_avl_mb': 0,
            'pedidos_procesados_total': 0,
            'errores_conectividad': 0
        }
    
    def cronometrar(self, nombre_metrica):
        """Decorator para cronometrar funciones"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                resultado = func(*args, **kwargs)
                tiempo_transcurrido = time.time() - start_time
                
                self.registrar_tiempo_respuesta(nombre_metrica, tiempo_transcurrido)
                return resultado
            return wrapper
        return decorator
    
    def registrar_tiempo_respuesta(self, operacion, tiempo):
        """Registrar tiempo de respuesta de operación"""
        with self.lock:
            self.tiempos_respuesta[operacion].append(tiempo)
            if len(self.tiempos_respuesta[operacion]) > self.max_historial:
                self.tiempos_respuesta[operacion].pop(0)
    
    def incrementar_contador(self, nombre_contador, cantidad=1):
        """Incrementar contador de eventos"""
        with self.lock:
            self.contadores[nombre_contador] += cantidad
    
    def registrar_metrica(self, nombre, valor):
        """Registrar valor de métrica"""
        with self.lock:
            self.metricas[nombre].append((time.time(), valor))
            if len(self.metricas[nombre]) > self.max_historial:
                self.metricas[nombre].popleft()
    
    def obtener_estadisticas_rendimiento(self):
        """Obtener resumen de estadísticas de rendimiento"""
        with self.lock:
            estadisticas = {}
            
            # Tiempos de respuesta promedio
            for operacion, tiempos in self.tiempos_respuesta.items():
                if tiempos:
                    estadisticas[f"{operacion}_promedio"] = sum(tiempos) / len(tiempos)
                    estadisticas[f"{operacion}_maximo"] = max(tiempos)
                    estadisticas[f"{operacion}_minimo"] = min(tiempos)
            
            # Contadores actuales
            estadisticas.update(self.contadores)
            
            # Métricas personalizadas
            estadisticas.update(self.metricas_personalizadas)
            
            return estadisticas
    
    def obtener_metricas_tiempo_real(self, ventana_segundos=60):
        """Obtener métricas de los últimos N segundos"""
        tiempo_limite = time.time() - ventana_segundos
        metricas_recientes = {}
        
        with self.lock:
            for nombre, valores in self.metricas.items():
                valores_recientes = [(t, v) for t, v in valores if t >= tiempo_limite]
                if valores_recientes:
                    metricas_recientes[nombre] = {
                        'promedio': sum(v for _, v in valores_recientes) / len(valores_recientes),
                        'ultimo': valores_recientes[-1][1],
                        'tendencia': self._calcular_tendencia(valores_recientes)
                    }
        
        return metricas_recientes
    
    def _calcular_tendencia(self, valores):
        """Calcular tendencia simple (creciente/decreciente/estable)"""
        if len(valores) < 2:
            return 'estable'
        
        primera_mitad = valores[:len(valores)//2]
        segunda_mitad = valores[len(valores)//2:]
        
        promedio_primera = sum(v for _, v in primera_mitad) / len(primera_mitad)
        promedio_segunda = sum(v for _, v in segunda_mitad) / len(segunda_mitad)
        
        diferencia_porcentual = ((promedio_segunda - promedio_primera) / promedio_primera) * 100
        
        if diferencia_porcentual > 10:
            return 'creciente'
        elif diferencia_porcentual < -10:
            return 'decreciente'
        else:
            return 'estable'

# Instancia global del collector
collector_metricas = CollectorMetricas()
```

### Dashboard de Rendimiento
```python
# frontendv2/ui/vista_rendimiento.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from frontendv2.servicios.api import cliente_api

def mostrar_dashboard_rendimiento():
    """Dashboard de métricas de rendimiento en tiempo real"""
    st.title("📊 Dashboard de Rendimiento del Sistema")
    
    # Obtener métricas del backend
    metricas = cliente_api.obtener_metricas_rendimiento()
    
    if not metricas:
        st.warning("No hay métricas disponibles")
        return
    
    # Layout en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Rutas Calculadas",
            metricas.get('rutas_calculadas_total', 0),
            delta=f"+{metricas.get('rutas_ultima_hora', 0)} (última hora)"
        )
    
    with col2:
        cache_hit_rate = metricas.get('cache_hit_rate', 0) * 100
        st.metric(
            "Cache Hit Rate",
            f"{cache_hit_rate:.1f}%",
            delta=f"{'🟢' if cache_hit_rate > 80 else '🟡' if cache_hit_rate > 60 else '🔴'}"
        )
    
    with col3:
        tiempo_bfs = metricas.get('calcular_ruta_bfs_promedio', 0) * 1000
        st.metric(
            "Tiempo BFS Promedio",
            f"{tiempo_bfs:.1f}ms",
            delta=f"{'🟢' if tiempo_bfs < 100 else '🟡' if tiempo_bfs < 500 else '🔴'}"
        )
    
    # Gráficos de rendimiento
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de tiempos de respuesta
        if 'tiempos_respuesta_historico' in metricas:
            fig_tiempos = go.Figure()
            for operacion, tiempos in metricas['tiempos_respuesta_historico'].items():
                fig_tiempos.add_trace(go.Scatter(
                    y=tiempos,
                    name=operacion,
                    mode='lines'
                ))
            
            fig_tiempos.update_layout(
                title="Tiempos de Respuesta por Operación",
                xaxis_title="Tiempo",
                yaxis_title="Milisegundos"
            )
            st.plotly_chart(fig_tiempos, use_container_width=True)
    
    with col2:
        # Gráfico de uso de memoria
        if 'uso_memoria' in metricas:
            fig_memoria = px.pie(
                values=[
                    metricas.get('memoria_hashmap_mb', 0),
                    metricas.get('memoria_avl_mb', 0),
                    metricas.get('memoria_cache_mb', 0)
                ],
                names=['HashMap', 'AVL', 'Cache'],
                title="Distribución de Uso de Memoria"
            )
            st.plotly_chart(fig_memoria, use_container_width=True)
    
    # Tabla de métricas detalladas
    st.subheader("Métricas Detalladas")
    
    metricas_tabla = [
        {"Métrica": "Vértices promedio explorados (BFS)", "Valor": metricas.get('vertices_visitados_promedio', 0)},
        {"Métrica": "Pedidos procesados total", "Valor": metricas.get('pedidos_procesados_total', 0)},
        {"Métrica": "Errores de conectividad", "Valor": metricas.get('errores_conectividad', 0)},
        {"Métrica": "Tamaño cache rutas", "Valor": metricas.get('tamaño_cache_rutas', 0)},
        {"Métrica": "Elementos en HashMap", "Valor": metricas.get('elementos_hashmap_total', 0)},
        {"Métrica": "Altura promedio AVL", "Valor": metricas.get('altura_promedio_avl', 0)}
    ]
    
    st.table(metricas_tabla)
    
    # Botón para limpiar métricas
    if st.button("🗑️ Limpiar Métricas"):
        cliente_api.limpiar_metricas_rendimiento()
        st.success("Métricas limpiadas exitosamente")
        st.experimental_rerun()
```

## 🎯 Recomendaciones de Optimización Avanzada

### 1. Paralelización de Cálculos
```python
# Para simulaciones grandes, implementar cálculo paralelo de rutas
import concurrent.futures
import multiprocessing

class CalculadorRutasParalelo:
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or multiprocessing.cpu_count()
    
    def calcular_rutas_lote(self, pedidos, grafo, algoritmo):
        """Calcular múltiples rutas en paralelo"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._calcular_ruta_single, pedido, grafo, algoritmo): pedido
                for pedido in pedidos
            }
            
            resultados = {}
            for future in concurrent.futures.as_completed(futures):
                pedido = futures[future]
                try:
                    resultado = future.result()
                    resultados[pedido.id_pedido] = resultado
                except Exception as e:
                    logger.error(f"Error calculando ruta para pedido {pedido.id_pedido}: {e}")
            
            return resultados
```

### 2. Compresión de Datos de Visualización
```python
# Para grafos muy grandes, comprimir datos antes de enviar al frontend
import json
import gzip

def comprimir_datos_grafo(vertices, aristas):
    """Comprimir datos de grafo para transferencia eficiente"""
    datos = {
        'vertices': [{'id': v.id_vertice, 'tipo': v.elemento.tipo_elemento} for v in vertices],
        'aristas': [{'id': a.id_arista, 'origen': a.origen.id_vertice, 'destino': a.destino.id_vertice, 'peso': a.peso} for a in aristas]
    }
    
    json_str = json.dumps(datos)
    compressed = gzip.compress(json_str.encode('utf-8'))
    
    return {
        'datos_comprimidos': compressed,
        'tamaño_original': len(json_str),
        'tamaño_comprimido': len(compressed),
        'ratio_compresion': len(compressed) / len(json_str)
    }
```

### 3. Índices Espaciales para Grafos Grandes
```python
# Implementar índices espaciales para optimizar búsquedas de proximidad
class IndiceEspacial:
    def __init__(self, ancho_cuadricula=10):
        self.cuadrilla = defaultdict(list)
        self.ancho_cuadricula = ancho_cuadricula
    
    def indexar_vertice(self, vertice, x, y):
        """Indexar vértice en cuadrícula espacial"""
        cuadricula_x = x // self.ancho_cuadricula
        cuadricula_y = y // self.ancho_cuadricula
        clave_cuadricula = (cuadricula_x, cuadricula_y)
        
        self.cuadrilla[clave_cuadricula].append(vertice)
    
    def buscar_vertices_cercanos(self, x, y, radio=1):
        """Buscar vértices en cuadrículas cercanas"""
        vertices_cercanos = []
        cuadricula_x = x // self.ancho_cuadricula
        cuadricula_y = y // self.ancho_cuadricula
        
        for dx in range(-radio, radio + 1):
            for dy in range(-radio, radio + 1):
                clave = (cuadricula_x + dx, cuadricula_y + dy)
                vertices_cercanos.extend(self.cuadrilla.get(clave, []))
        
        return vertices_cercanos
```

## 📈 Plan de Optimización Continua

### Fase 1: Optimizaciones Básicas (Implementadas)
- ✅ HashMap optimizado con factor de carga
- ✅ AVL con cache de búsquedas frecuentes
- ✅ BFS con poda inteligente
- ✅ Pool de objetos para reducir GC

### Fase 2: Optimizaciones Intermedias (En Progreso)
- 🔄 Paralelización de cálculos de rutas
- 🔄 Compresión de datos de visualización
- 🔄 Cache distribuido para múltiples sesiones
- 🔄 Índices espaciales para grafos grandes

### Fase 3: Optimizaciones Avanzadas (Planificadas)
- 📋 Algoritmos aproximados para grafos masivos
- 📋 Machine learning para predicción de rutas
- 📋 Persistencia optimizada en base de datos
- 📋 CDN para assets de visualización

### Métricas de Éxito
- **Tiempo de inicialización**: Reducir 50% (objetivo: < 1s para 150 vértices)
- **Memoria total**: Reducir 30% (objetivo: < 350MB para simulación máxima)
- **Throughput**: Aumentar 200% (objetivo: > 200 rutas/segundo)
- **Latencia UI**: Reducir 60% (objetivo: < 500ms para cualquier operación)

Este sistema de optimización garantiza que el sistema de simulación logística mantenga un rendimiento óptimo incluso con las cargas de trabajo más exigentes, proporcionando una experiencia fluida tanto para operadores como para análisis en tiempo real.

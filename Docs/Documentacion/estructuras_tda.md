# Documentación de Estructuras de Datos TDA

## Descripción General
Las Estructuras de Datos TDA (Tipos de Datos Abstractos) implementadas en el sistema proporcionan funcionalidades especializadas y optimizadas para las operaciones críticas del sistema logístico de drones. Estas estructuras están diseñadas específicamente para satisfacer los requisitos de rendimiento y funcionalidad del dominio del problema.

## Ubicación en la Arquitectura
- **Capa de Infraestructura**: `Backend/Infraestructura/TDA/`
- **Patrón**: Implementaciones especializadas de estructuras de datos
- **Responsabilidad**: Operaciones optimizadas de almacenamiento, búsqueda y gestión de datos

## 1. Árbol AVL para Gestión de Rutas

### Propósito
Mantiene un registro balanceado y ordenado de las rutas más frecuentemente utilizadas en el sistema, permitiendo análisis eficiente de patrones de uso y optimización de rutas.

### Estructura
```python
class NodoAVL:
    def __init__(self, clave_ruta: str, datos_ruta: dict):
        self.clave: str = clave_ruta           # Secuencia de vértices como string
        self.datos: dict = datos_ruta          # Información de la ruta y frecuencia
        self.altura: int = 1                   # Altura del nodo para balanceado
        self.izquierdo: Optional[NodoAVL] = None
        self.derecho: Optional[NodoAVL] = None
        self.frecuencia: int = 1               # Contador de uso de la ruta

class AVLRutas:
    def __init__(self):
        self.raiz: Optional[NodoAVL] = None
        self.total_rutas: int = 0
        self.cache_frecuentes: List[Tuple[str, int]] = []
```

### Operaciones Principales
```python
def insertar_ruta(self, secuencia_vertices: List[str], datos_ruta: dict) -> bool:
    """
    Inserta una nueva ruta o incrementa frecuencia si ya existe
    Complejidad: O(log n)
    """
    clave_ruta = " -> ".join(secuencia_vertices)
    self.raiz = self._insertar_recursivo(self.raiz, clave_ruta, datos_ruta)
    self.total_rutas += 1
    self._invalidar_cache()
    return True

def buscar_ruta(self, secuencia_vertices: List[str]) -> Optional[dict]:
    """
    Busca información de una ruta específica
    Complejidad: O(log n)
    """
    clave_ruta = " -> ".join(secuencia_vertices)
    nodo = self._buscar_recursivo(self.raiz, clave_ruta)
    return nodo.datos if nodo else None

def obtener_rutas_mas_frecuentes(self, limite: int = 10) -> List[Tuple[str, int]]:
    """
    Retorna las rutas más utilizadas
    Complejidad: O(n) con cache O(1)
    """
    if not self.cache_frecuentes:
        self._construir_cache_frecuencias()
    return self.cache_frecuentes[:limite]

def obtener_estadisticas_ruta(self, secuencia_vertices: List[str]) -> dict:
    """
    Retorna estadísticas detalladas de una ruta
    """
    datos = self.buscar_ruta(secuencia_vertices)
    if not datos:
        return {}
    
    return {
        'frecuencia_uso': datos['frecuencia'],
        'costo_promedio': datos['costo_total'],
        'tiempo_promedio': datos.get('tiempo_promedio', 0),
        'recargas_necesarias': datos.get('recargas_utilizadas', []),
        'eficiencia_energetica': datos.get('eficiencia', 0.0)
    }
```

### Algoritmos de Balanceado
```python
def _balancear(self, nodo: NodoAVL) -> NodoAVL:
    """
    Realiza rotaciones necesarias para mantener balance AVL
    """
    # Actualizar altura
    nodo.altura = 1 + max(self._obtener_altura(nodo.izquierdo),
                         self._obtener_altura(nodo.derecho))
    
    # Calcular factor de balance
    balance = self._obtener_balance(nodo)
    
    # Rotación derecha (caso izquierda-izquierda)
    if balance > 1 and self._obtener_balance(nodo.izquierdo) >= 0:
        return self._rotar_derecha(nodo)
    
    # Rotación izquierda (caso derecha-derecha)
    if balance < -1 and self._obtener_balance(nodo.derecho) <= 0:
        return self._rotar_izquierda(nodo)
    
    # Rotación izquierda-derecha
    if balance > 1 and self._obtener_balance(nodo.izquierdo) < 0:
        nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
        return self._rotar_derecha(nodo)
    
    # Rotación derecha-izquierda
    if balance < -1 and self._obtener_balance(nodo.derecho) > 0:
        nodo.derecho = self._rotar_derecha(nodo.derecho)
        return self._rotar_izquierda(nodo)
    
    return nodo
```

### Casos de Uso Específicos
```python
# Registro de ruta utilizada
def registrar_uso_ruta(self, ruta: Ruta, tiempo_ejecucion: float):
    """
    Registra el uso de una ruta con métricas de rendimiento
    """
    datos_ruta = {
        'costo_total': ruta.obtener_costo_total(),
        'tiempo_ejecucion': tiempo_ejecucion,
        'recargas_utilizadas': ruta.obtener_estaciones_recarga(),
        'eficiencia': ruta.calcular_eficiencia_energetica(),
        'timestamp': datetime.now()
    }
    
    self.insertar_ruta(ruta.obtener_secuencia_vertices(), datos_ruta)

# Análisis de patrones
def analizar_patrones_uso(self) -> dict:
    """
    Analiza patrones en el uso de rutas
    """
    rutas_frecuentes = self.obtener_rutas_mas_frecuentes(20)
    
    # Análisis de origen-destino más comunes
    origenes_frecuentes = {}
    destinos_frecuentes = {}
    
    for ruta_str, frecuencia in rutas_frecuentes:
        vertices = ruta_str.split(" -> ")
        origen, destino = vertices[0], vertices[-1]
        
        origenes_frecuentes[origen] = origenes_frecuentes.get(origen, 0) + frecuencia
        destinos_frecuentes[destino] = destinos_frecuentes.get(destino, 0) + frecuencia
    
    return {
        'rutas_mas_utilizadas': rutas_frecuentes[:10],
        'origenes_populares': sorted(origenes_frecuentes.items(), key=lambda x: x[1], reverse=True)[:5],
        'destinos_populares': sorted(destinos_frecuentes.items(), key=lambda x: x[1], reverse=True)[:5],
        'total_rutas_unicas': self.total_rutas,
        'eficiencia_promedio': self._calcular_eficiencia_promedio()
    }
```

## 2. HashMap para Acceso Rápido a Entidades

### Propósito
Proporciona acceso O(1) a entidades del sistema (clientes, pedidos, vértices) mediante claves únicas, optimizando las operaciones de búsqueda y gestión.

### Estructura
```python
class EntradaHash:
    def __init__(self, clave: str, valor: Any):
        self.clave: str = clave
        self.valor: Any = valor
        self.siguiente: Optional[EntradaHash] = None

class HashMapOptimizado:
    def __init__(self, capacidad_inicial: int = 16):
        self.capacidad: int = capacidad_inicial
        self.tamaño: int = 0
        self.buckets: List[Optional[EntradaHash]] = [None] * self.capacidad
        self.factor_carga_maximo: float = 0.75
        self.total_operaciones: int = 0
        self.colisiones: int = 0
```

### Función Hash Optimizada
```python
def _hash(self, clave: str) -> int:
    """
    Función hash optimizada para strings usando algoritmo djb2
    """
    hash_value = 5381
    for char in clave:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % self.capacidad

def _hash_secundario(self, clave: str) -> int:
    """
    Función hash secundaria para doble hashing
    """
    hash_value = 0
    for char in clave:
        hash_value = hash_value * 31 + ord(char)
    return 7 - (hash_value % 7)  # Número primo diferente
```

### Operaciones Principales
```python
def insertar(self, clave: str, valor: Any) -> bool:
    """
    Inserta o actualiza una entrada en el HashMap
    Complejidad: O(1) promedio, O(n) peor caso
    """
    if self.tamaño >= self.capacidad * self.factor_carga_maximo:
        self._redimensionar()
    
    indice = self._hash(clave)
    entrada_actual = self.buckets[indice]
    
    # Verificar si la clave ya existe
    while entrada_actual:
        if entrada_actual.clave == clave:
            entrada_actual.valor = valor  # Actualizar valor existente
            return True
        entrada_actual = entrada_actual.siguiente
    
    # Insertar nueva entrada
    nueva_entrada = EntradaHash(clave, valor)
    if self.buckets[indice] is not None:
        self.colisiones += 1
    nueva_entrada.siguiente = self.buckets[indice]
    self.buckets[indice] = nueva_entrada
    self.tamaño += 1
    self.total_operaciones += 1
    
    return True

def obtener(self, clave: str) -> Optional[Any]:
    """
    Obtiene valor asociado a una clave
    Complejidad: O(1) promedio
    """
    indice = self._hash(clave)
    entrada_actual = self.buckets[indice]
    
    while entrada_actual:
        if entrada_actual.clave == clave:
            self.total_operaciones += 1
            return entrada_actual.valor
        entrada_actual = entrada_actual.siguiente
    
    return None

def eliminar(self, clave: str) -> bool:
    """
    Elimina entrada del HashMap
    Complejidad: O(1) promedio
    """
    indice = self._hash(clave)
    entrada_actual = self.buckets[indice]
    entrada_anterior = None
    
    while entrada_actual:
        if entrada_actual.clave == clave:
            if entrada_anterior:
                entrada_anterior.siguiente = entrada_actual.siguiente
            else:
                self.buckets[indice] = entrada_actual.siguiente
            self.tamaño -= 1
            self.total_operaciones += 1
            return True
        
        entrada_anterior = entrada_actual
        entrada_actual = entrada_actual.siguiente
    
    return False
```

### Gestión Dinámica de Memoria
```python
def _redimensionar(self):
    """
    Redimensiona el HashMap cuando el factor de carga es alto
    """
    buckets_antiguos = self.buckets
    capacidad_antigua = self.capacidad
    
    # Duplicar capacidad
    self.capacidad *= 2
    self.buckets = [None] * self.capacidad
    tamaño_anterior = self.tamaño
    self.tamaño = 0
    
    # Reinsertar todas las entradas
    for bucket in buckets_antiguos:
        entrada_actual = bucket
        while entrada_actual:
            self.insertar(entrada_actual.clave, entrada_actual.valor)
            entrada_actual = entrada_actual.siguiente
    
    # Ajustar contador (insertar incrementa el tamaño)
    self.tamaño = tamaño_anterior

def obtener_estadisticas(self) -> dict:
    """
    Retorna estadísticas de rendimiento del HashMap
    """
    buckets_ocupados = sum(1 for bucket in self.buckets if bucket is not None)
    factor_carga_actual = self.tamaño / self.capacidad
    
    return {
        'capacidad': self.capacidad,
        'elementos': self.tamaño,
        'factor_carga': factor_carga_actual,
        'buckets_ocupados': buckets_ocupados,
        'colisiones_total': self.colisiones,
        'operaciones_total': self.total_operaciones,
        'eficiencia': (self.total_operaciones - self.colisiones) / max(self.total_operaciones, 1)
    }
```

### Especializaciones por Tipo de Entidad
```python
class HashMapClientes(HashMapOptimizado):
    """HashMap especializado para gestión de clientes"""
    
    def insertar_cliente(self, cliente: Cliente) -> bool:
        return self.insertar(cliente.id_cliente, cliente)
    
    def obtener_cliente(self, id_cliente: str) -> Optional[Cliente]:
        return self.obtener(id_cliente)
    
    def listar_clientes_activos(self) -> List[Cliente]:
        """Retorna solo clientes activos"""
        clientes_activos = []
        for bucket in self.buckets:
            entrada = bucket
            while entrada:
                if entrada.valor.activo:
                    clientes_activos.append(entrada.valor)
                entrada = entrada.siguiente
        return clientes_activos

class HashMapPedidos(HashMapOptimizado):
    """HashMap especializado para gestión de pedidos"""
    
    def insertar_pedido(self, pedido: Pedido) -> bool:
        return self.insertar(pedido.id_pedido, pedido)
    
    def obtener_pedido(self, id_pedido: str) -> Optional[Pedido]:
        return self.obtener(id_pedido)
    
    def obtener_pedidos_por_cliente(self, id_cliente: str) -> List[Pedido]:
        """Retorna todos los pedidos de un cliente específico"""
        pedidos_cliente = []
        for bucket in self.buckets:
            entrada = bucket
            while entrada:
                if entrada.valor.cliente.id_cliente == id_cliente:
                    pedidos_cliente.append(entrada.valor)
                entrada = entrada.siguiente
        return pedidos_cliente
    
    def obtener_pedidos_por_estado(self, estado: EstadoPedido) -> List[Pedido]:
        """Retorna pedidos filtrados por estado"""
        pedidos_estado = []
        for bucket in self.buckets:
            entrada = bucket
            while entrada:
                if entrada.valor.estado == estado:
                    pedidos_estado.append(entrada.valor)
                entrada = entrada.siguiente
        return pedidos_estado
```

## 3. Grafo Optimizado para Red de Transporte

### Propósito
Estructura especializada para representar la red de transporte con operaciones optimizadas para cálculo de rutas y análisis de conectividad.

### Estructura Híbrida
```python
class GrafoOptimizado:
    def __init__(self):
        self.vertices: HashMapOptimizado = HashMapOptimizado()  # ID -> Vértice
        self.matriz_adyacencia: Dict[str, Dict[str, float]] = {}  # Pesos de aristas
        self.lista_adyacencia: Dict[str, List[str]] = {}          # Vecinos por vértice
        self.aristas_por_peso: List[Tuple[str, str, float]] = []  # Ordenadas por peso
        self.componentes_conexas: List[Set[str]] = []             # Cache de componentes
        self.mst_cache: Optional[List[Tuple[str, str, float]]] = None  # MST cacheado
```

### Operaciones Optimizadas
```python
def agregar_vertice_optimizado(self, vertice: Vertice) -> bool:
    """
    Agrega vértice con optimizaciones específicas
    """
    if not self.vertices.insertar(vertice.id_vertice, vertice):
        return False
    
    # Inicializar estructuras auxiliares
    self.lista_adyacencia[vertice.id_vertice] = []
    self.matriz_adyacencia[vertice.id_vertice] = {}
    
    # Invalidar caches
    self._invalidar_caches()
    return True

def agregar_arista_bidireccional(self, id_origen: str, id_destino: str, peso: float) -> bool:
    """
    Agrega arista bidireccional con optimizaciones
    """
    if id_origen not in self.vertices or id_destino not in self.vertices:
        return False
    
    # Actualizar matriz de adyacencia
    self.matriz_adyacencia[id_origen][id_destino] = peso
    self.matriz_adyacencia[id_destino][id_origen] = peso
    
    # Actualizar lista de adyacencia
    if id_destino not in self.lista_adyacencia[id_origen]:
        self.lista_adyacencia[id_origen].append(id_destino)
    if id_origen not in self.lista_adyacencia[id_destino]:
        self.lista_adyacencia[id_destino].append(id_origen)
    
    # Mantener aristas ordenadas por peso
    self.aristas_por_peso.append((id_origen, id_destino, peso))
    self.aristas_por_peso.sort(key=lambda x: x[2])
    
    self._invalidar_caches()
    return True

def obtener_peso_arista(self, origen: str, destino: str) -> Optional[float]:
    """
    Acceso O(1) al peso de una arista
    """
    return self.matriz_adyacencia.get(origen, {}).get(destino)

def obtener_vecinos_rapido(self, id_vertice: str) -> List[str]:
    """
    Acceso O(1) a vecinos de un vértice
    """
    return self.lista_adyacencia.get(id_vertice, [])
```

### Algoritmos Especializados
```python
def calcular_mst_optimizado(self) -> List[Tuple[str, str, float]]:
    """
    Calcula MST con optimizaciones y cache
    """
    if self.mst_cache is not None:
        return self.mst_cache
    
    # Union-Find optimizado
    padre = {v: v for v in self.vertices.obtener_claves()}
    rango = {v: 0 for v in self.vertices.obtener_claves()}
    
    def encontrar_con_compresion(x):
        if padre[x] != x:
            padre[x] = encontrar_con_compresion(padre[x])  # Compresión de camino
        return padre[x]
    
    def unir_por_rango(x, y):
        px, py = encontrar_con_compresion(x), encontrar_con_compresion(y)
        if px == py:
            return False
        
        # Unir por rango para mantener árbol balanceado
        if rango[px] < rango[py]:
            px, py = py, px
        padre[py] = px
        if rango[px] == rango[py]:
            rango[px] += 1
        return True
    
    mst = []
    for origen, destino, peso in self.aristas_por_peso:
        if unir_por_rango(origen, destino):
            mst.append((origen, destino, peso))
            if len(mst) == len(self.vertices) - 1:
                break
    
    self.mst_cache = mst
    return mst

def busqueda_bfs_optimizada(self, origen: str, destino: str, 
                           autonomia: float = 50.0) -> Optional[dict]:
    """
    BFS optimizado con heurísticas específicas del dominio
    """
    if origen == destino:
        return {'camino': [origen], 'costo': 0, 'recargas': []}
    
    # Heurística: verificar distancia Manhattan como cota inferior
    if not self._es_alcanzable_heuristica(origen, destino, autonomia):
        return None
    
    cola = deque([{
        'vertice': origen,
        'camino': [origen],
        'energia': autonomia,
        'costo_total': 0,
        'recargas': []
    }])
    
    visitados = {}  # (vertice, energia_aproximada) -> mejor_costo
    mejor_solucion = None
    
    while cola:
        estado = cola.popleft()
        vertice_actual = estado['vertice']
        energia_actual = estado['energia']
        
        # Clave de estado para poda
        clave_estado = (vertice_actual, int(energia_actual / 5) * 5)  # Discretizar energía
        
        if clave_estado in visitados and visitados[clave_estado] <= estado['costo_total']:
            continue
        visitados[clave_estado] = estado['costo_total']
        
        # ¿Llegamos al destino?
        if vertice_actual == destino:
            if mejor_solucion is None or estado['costo_total'] < mejor_solucion['costo_total']:
                mejor_solucion = estado
            continue
        
        # Explorar vecinos
        for vecino in self.obtener_vecinos_rapido(vertice_actual):
            peso_arista = self.obtener_peso_arista(vertice_actual, vecino)
            
            if energia_actual >= peso_arista:
                nueva_energia = energia_actual - peso_arista
                nuevo_estado = {
                    'vertice': vecino,
                    'camino': estado['camino'] + [vecino],
                    'energia': nueva_energia,
                    'costo_total': estado['costo_total'] + peso_arista,
                    'recargas': estado['recargas'].copy()
                }
                
                # Si es estación de recarga, restaurar energía
                vertice_obj = self.vertices.obtener(vecino)
                if vertice_obj and vertice_obj.tipo == TipoVertice.RECARGA:
                    nuevo_estado['energia'] = autonomia
                    nuevo_estado['recargas'].append(vecino)
                
                cola.append(nuevo_estado)
    
    return mejor_solucion
```

## Integración y Rendimiento

### 1. Métricas de Rendimiento
```python
class MonitorTDA:
    def __init__(self):
        self.metricas_avl = {}
        self.metricas_hashmap = {}
        self.metricas_grafo = {}
    
    def medir_operacion_avl(self, operacion: str, tiempo: float):
        """Registra métricas de operaciones AVL"""
        if operacion not in self.metricas_avl:
            self.metricas_avl[operacion] = []
        self.metricas_avl[operacion].append(tiempo)
    
    def obtener_reporte_rendimiento(self) -> dict:
        """Genera reporte completo de rendimiento"""
        return {
            'avl': {
                'insercion_promedio': statistics.mean(self.metricas_avl.get('insercion', [0])),
                'busqueda_promedio': statistics.mean(self.metricas_avl.get('busqueda', [0])),
                'altura_promedio': self._calcular_altura_promedio_avl()
            },
            'hashmap': {
                'factor_carga': self._obtener_factor_carga_hashmap(),
                'colisiones_porcentaje': self._calcular_porcentaje_colisiones(),
                'tiempo_acceso_promedio': statistics.mean(self.metricas_hashmap.get('acceso', [0]))
            },
            'grafo': {
                'densidad': self._calcular_densidad_grafo(),
                'conectividad': self._verificar_conectividad(),
                'tiempo_bfs_promedio': statistics.mean(self.metricas_grafo.get('bfs', [0]))
            }
        }
```

### 2. Optimizaciones Específicas del Dominio
```python
class OptimizacionesDominio:
    """Optimizaciones específicas para el sistema logístico"""
    
    def optimizar_para_rutas_frecuentes(self, avl_rutas: AVLRutas, hashmap_pedidos: HashMapPedidos):
        """
        Optimiza estructuras basándose en patrones de uso
        """
        rutas_frecuentes = avl_rutas.obtener_rutas_mas_frecuentes(50)
        
        # Precalcular rutas frecuentes
        cache_rutas = {}
        for ruta_str, frecuencia in rutas_frecuentes:
            vertices = ruta_str.split(" -> ")
            if len(vertices) >= 2:
                origen, destino = vertices[0], vertices[-1]
                cache_rutas[(origen, destino)] = {
                    'ruta_optima': vertices,
                    'frecuencia': frecuencia,
                    'precalculada': True
                }
        
        return cache_rutas
    
    def redimensionar_estructuras_dinamicamente(self, metricas: dict):
        """
        Ajusta tamaños de estructuras basándose en uso real
        """
        if metricas['hashmap']['factor_carga'] > 0.8:
            # Expandir HashMap si está muy cargado
            return {'accion': 'expandir_hashmap', 'factor': 2}
        
        if metricas['avl']['altura_promedio'] > 15:
            # Considerar rebalanceado si el árbol está muy alto
            return {'accion': 'rebalancear_avl'}
        
        return {'accion': 'ninguna'}
```

## Testing y Validación

### 1. Pruebas de Correctitud
```python
def test_avl_mantiene_propiedades():
    """Verifica que el AVL mantiene sus propiedades invariantes"""
    avl = AVLRutas()
    
    # Insertar múltiples rutas
    rutas_test = [
        ["A", "B", "C"],
        ["A", "D", "C"],
        ["B", "E", "F"],
        ["A", "B", "C"],  # Duplicada
    ]
    
    for ruta in rutas_test:
        avl.insertar_ruta(ruta, {'costo': 10})
    
    # Verificar balance
    assert avl._verificar_balance_completo()
    
    # Verificar frecuencias
    datos_abc = avl.buscar_ruta(["A", "B", "C"])
    assert datos_abc['frecuencia'] == 2

def test_hashmap_rendimiento():
    """Verifica que HashMap mantiene rendimiento O(1)"""
    hashmap = HashMapClientes()
    
    # Insertar muchos clientes
    inicio = time.time()
    for i in range(10000):
        cliente = Cliente(f"CLI{i:05d}", f"Cliente {i}", f"email{i}@test.com", "123456789")
        hashmap.insertar_cliente(cliente)
    tiempo_insercion = time.time() - inicio
    
    # Verificar acceso rápido
    inicio = time.time()
    for i in range(1000):
        cliente = hashmap.obtener_cliente(f"CLI{i:05d}")
        assert cliente is not None
    tiempo_acceso = time.time() - inicio
    
    # El tiempo de acceso debe ser muy pequeño
    assert tiempo_acceso < 0.1  # 100ms para 1000 accesos
```

### 2. Pruebas de Integración
```python
def test_integracion_completa_tda():
    """Prueba integración entre todas las estructuras TDA"""
    # Inicializar estructuras
    avl_rutas = AVLRutas()
    hashmap_clientes = HashMapClientes()
    hashmap_pedidos = HashMapPedidos()
    grafo = GrafoOptimizado()
    
    # Crear datos de prueba
    crear_datos_integracion(grafo, hashmap_clientes, hashmap_pedidos)
    
    # Simular flujo completo
    for i in range(100):
        # Obtener pedido
        pedido = hashmap_pedidos.obtener_pedido(f"PED{i:03d}")
        
        # Calcular ruta
        resultado_ruta = grafo.busqueda_bfs_optimizada(
            pedido.almacenamiento_origen.id_almacenamiento,
            pedido.cliente.id_cliente
        )
        
        # Registrar en AVL
        if resultado_ruta:
            avl_rutas.insertar_ruta(resultado_ruta['camino'], {
                'costo': resultado_ruta['costo'],
                'recargas': resultado_ruta['recargas']
            })
    
    # Verificar consistencia
    assert avl_rutas.total_rutas > 0
    assert len(avl_rutas.obtener_rutas_mas_frecuentes()) > 0
    
    estadisticas = {
        'avl': avl_rutas.obtener_estadisticas(),
        'hashmap_clientes': hashmap_clientes.obtener_estadisticas(),
        'hashmap_pedidos': hashmap_pedidos.obtener_estadisticas()
    }
    
    # Verificar métricas razonables
    assert estadisticas['hashmap_clientes']['eficiencia'] > 0.8
    assert estadisticas['hashmap_pedidos']['factor_carga'] < 0.9
```

Las estructuras TDA implementadas proporcionan la base de rendimiento crítica para el sistema, garantizando operaciones eficientes y escalables para todos los componentes del sistema logístico de drones.

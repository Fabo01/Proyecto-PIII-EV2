# Documentación del Componente Grafo

## Descripción General
El componente `Grafo` es la estructura de datos fundamental que modela la red de transporte de drones. Representa la topología física de la red logística, incluyendo todos los puntos de interés (clientes, almacenes, estaciones de recarga) y las conexiones entre ellos. Es la base sobre la cual se calculan todas las rutas de entrega.

## Ubicación en la Arquitectura
- **Capa de Infraestructura**: `Backend/Infraestructura/TDA/grafo.py`
- **Patrón**: Estructura de datos especializada
- **Responsabilidad**: Representación y manipulación de la red de transporte

## Estructura del Grafo

### Componentes Principales
```python
class Grafo:
    def __init__(self):
        self._vertices: Dict[str, Vertice] = {}      # HashMap de vértices por ID
        self._aristas: List[Arista] = []             # Lista de todas las aristas
        self._matriz_adyacencia: Dict[str, Dict[str, Arista]] = {}  # Matriz de adyacencia
        self._es_dirigido: bool = False              # Tipo de grafo (no dirigido)
        self._conectado: bool = True                 # Garantía de conectividad
```

### Tipos de Vértices
```python
class TipoVertice(Enum):
    CLIENTE = "cliente"           # 60% - Destinos de entrega
    ALMACENAMIENTO = "almacenamiento"  # 20% - Orígenes de entrega
    RECARGA = "recarga"          # 20% - Estaciones de recarga energética
```

### Propiedades del Grafo
- **No Dirigido**: Las conexiones son bidireccionales
- **Conectado**: Garantiza camino entre cualquier par de vértices
- **Ponderado**: Cada arista tiene peso (costo energético)
- **Dinámico**: Permite modificaciones durante la simulación

## Funcionalidades Principales

### 1. Gestión de Vértices
```python
def agregar_vertice(self, vertice: Vertice) -> bool:
    """Agrega un nuevo vértice al grafo"""
    
def quitar_vertice(self, id_vertice: str) -> bool:
    """Remueve vértice y todas sus aristas"""
    
def obtener_vertice(self, id_vertice: str) -> Optional[Vertice]:
    """Busca vértice por ID"""
    
def listar_vertices_por_tipo(self, tipo: TipoVertice) -> List[Vertice]:
    """Filtra vértices por tipo específico"""
    
def cantidad_vertices(self) -> int:
    """Retorna total de vértices en el grafo"""
```

### 2. Gestión de Aristas
```python
def agregar_arista(self, origen: str, destino: str, peso: float) -> bool:
    """Crea conexión entre dos vértices"""
    
def quitar_arista(self, origen: str, destino: str) -> bool:
    """Elimina conexión específica"""
    
def obtener_arista(self, origen: str, destino: str) -> Optional[Arista]:
    """Busca arista específica"""
    
def obtener_vecinos(self, id_vertice: str) -> List[str]:
    """Retorna IDs de vértices adyacentes"""
    
def cantidad_aristas(self) -> int:
    """Retorna total de aristas en el grafo"""
```

### 3. Consultas Topológicas
```python
def existe_camino(self, origen: str, destino: str) -> bool:
    """Verifica conectividad entre dos vértices"""
    
def es_conectado(self) -> bool:
    """Verifica si el grafo es completamente conectado"""
    
def obtener_componentes_conexas(self) -> List[List[str]]:
    """Identifica componentes conexas del grafo"""
    
def calcular_grado(self, id_vertice: str) -> int:
    """Calcula grado de un vértice"""
```

### 4. Algoritmos de Búsqueda
```python
def busqueda_bfs(self, origen: str, destino: str, 
                autonomia_maxima: float = 50.0) -> Optional[List[str]]:
    """Búsqueda en anchura considerando autonomía"""
    
def busqueda_dfs(self, origen: str, destino: str) -> Optional[List[str]]:
    """Búsqueda en profundidad"""
    
def dijkstra(self, origen: str, destino: str) -> Optional[Tuple[List[str], float]]:
    """Algoritmo de Dijkstra para ruta mínima"""
```

## Algoritmos Implementados

### 1. BFS Modificado con Autonomía
```python
def busqueda_bfs_con_autonomia(self, origen: str, destino: str, 
                              autonomia_maxima: float = 50.0) -> Optional[List[str]]:
    """
    BFS que considera limitaciones energéticas del dron.
    Si la energía se agota, busca estaciones de recarga.
    """
    if origen == destino:
        return [origen]
    
    cola = deque([(origen, [origen], autonomia_maxima)])
    visitados = set()
    
    while cola:
        vertice_actual, camino, energia_restante = cola.popleft()
        
        if vertice_actual in visitados:
            continue
        visitados.add(vertice_actual)
        
        for vecino in self.obtener_vecinos(vertice_actual):
            arista = self.obtener_arista(vertice_actual, vecino)
            costo_movimiento = arista.peso
            
            # Verificar si llegamos al destino
            if vecino == destino and energia_restante >= costo_movimiento:
                return camino + [vecino]
            
            # Calcular energía después del movimiento
            nueva_energia = energia_restante - costo_movimiento
            
            # Si la energía es suficiente, continuar
            if nueva_energia >= 0:
                nuevo_camino = camino + [vecino]
                
                # Si es estación de recarga, restaurar energía
                vertice_vecino = self.obtener_vertice(vecino)
                if vertice_vecino.tipo == TipoVertice.RECARGA:
                    nueva_energia = autonomia_maxima
                
                cola.append((vecino, nuevo_camino, nueva_energia))
    
    return None  # No se encontró camino viable
```

### 2. Verificación de Conectividad
```python
def verificar_conectividad_completa(self) -> bool:
    """
    Verifica que el grafo sea completamente conectado
    usando DFS desde un vértice arbitrario.
    """
    if not self._vertices:
        return True
    
    # Comenzar DFS desde primer vértice
    inicio = next(iter(self._vertices.keys()))
    visitados = set()
    stack = [inicio]
    
    while stack:
        vertice = stack.pop()
        if vertice not in visitados:
            visitados.add(vertice)
            for vecino in self.obtener_vecinos(vertice):
                if vecino not in visitados:
                    stack.append(vecino)
    
    # Verificar si se visitaron todos los vértices
    return len(visitados) == len(self._vertices)
```

### 3. Generación de MST (Minimum Spanning Tree)
```python
def calcular_mst_kruskal(self) -> List[Arista]:
    """
    Calcula el Árbol de Expansión Mínima usando algoritmo de Kruskal.
    Útil para optimización de la red y análisis de conectividad.
    """
    # Ordenar aristas por peso
    aristas_ordenadas = sorted(self._aristas, key=lambda a: a.peso)
    
    # Estructuras para Union-Find
    padre = {v: v for v in self._vertices.keys()}
    rango = {v: 0 for v in self._vertices.keys()}
    
    def encontrar(x):
        if padre[x] != x:
            padre[x] = encontrar(padre[x])
        return padre[x]
    
    def unir(x, y):
        px, py = encontrar(x), encontrar(y)
        if px == py:
            return False
        if rango[px] < rango[py]:
            px, py = py, px
        padre[py] = px
        if rango[px] == rango[py]:
            rango[px] += 1
        return True
    
    mst = []
    for arista in aristas_ordenadas:
        if unir(arista.origen, arista.destino):
            mst.append(arista)
            if len(mst) == len(self._vertices) - 1:
                break
    
    return mst
```

## Generación Automática del Grafo

### Algoritmo de Generación Conecta
```python
def generar_grafo_conectado(num_vertices: int, num_aristas: int, 
                          porcentajes: Dict[TipoVertice, float]) -> Grafo:
    """
    Genera un grafo aleatorio garantizando conectividad.
    
    Pasos:
    1. Crear vértices con tipos según porcentajes
    2. Generar árbol de expansión para garantizar conectividad
    3. Agregar aristas adicionales aleatoriamente
    4. Verificar conectividad final
    """
    grafo = Grafo()
    
    # 1. Crear vértices
    tipos_vertices = []
    for tipo, porcentaje in porcentajes.items():
        cantidad = int(num_vertices * porcentaje)
        tipos_vertices.extend([tipo] * cantidad)
    
    # Ajustar para totalizar exactamente num_vertices
    while len(tipos_vertices) < num_vertices:
        tipos_vertices.append(TipoVertice.CLIENTE)
    
    for i in range(num_vertices):
        id_vertice = f"V{i:03d}"
        tipo = tipos_vertices[i]
        
        # Crear elemento específico según tipo
        if tipo == TipoVertice.CLIENTE:
            elemento = Cliente(id_vertice, f"Cliente {i}", f"cliente{i}@email.com", "123456789")
        elif tipo == TipoVertice.ALMACENAMIENTO:
            elemento = Almacenamiento(id_vertice, f"Almacén {i}", 1000.0, True)
        else:  # RECARGA
            elemento = Recarga(id_vertice, f"Recarga {i}", 100.0, True)
        
        vertice = Vertice(id_vertice, tipo, elemento)
        grafo.agregar_vertice(vertice)
    
    # 2. Generar árbol de expansión (garantiza conectividad)
    vertices_ids = list(grafo._vertices.keys())
    for i in range(1, len(vertices_ids)):
        origen = vertices_ids[random.randint(0, i-1)]
        destino = vertices_ids[i]
        peso = random.uniform(1.0, 15.0)
        grafo.agregar_arista(origen, destino, peso)
    
    # 3. Agregar aristas adicionales
    aristas_adicionales = num_aristas - (num_vertices - 1)
    intentos = 0
    max_intentos = aristas_adicionales * 10
    
    while grafo.cantidad_aristas() < num_aristas and intentos < max_intentos:
        origen = random.choice(vertices_ids)
        destino = random.choice(vertices_ids)
        
        if origen != destino and not grafo.obtener_arista(origen, destino):
            peso = random.uniform(1.0, 15.0)
            grafo.agregar_arista(origen, destino, peso)
        
        intentos += 1
    
    return grafo
```

## Optimizaciones de Rendimiento

### 1. Matriz de Adyacencia Optimizada
```python
def _actualizar_matriz_adyacencia(self, origen: str, destino: str, arista: Arista):
    """Mantiene matriz de adyacencia para acceso O(1)"""
    if origen not in self._matriz_adyacencia:
        self._matriz_adyacencia[origen] = {}
    if destino not in self._matriz_adyacencia:
        self._matriz_adyacencia[destino] = {}
    
    self._matriz_adyacencia[origen][destino] = arista
    self._matriz_adyacencia[destino][origen] = arista  # Grafo no dirigido
```

### 2. Cache de Cálculos Frecuentes
```python
class GrafoConCache(Grafo):
    def __init__(self):
        super().__init__()
        self._cache_caminos: Dict[Tuple[str, str], Optional[List[str]]] = {}
        self._cache_distancias: Dict[Tuple[str, str], float] = {}
    
    def busqueda_bfs_cached(self, origen: str, destino: str) -> Optional[List[str]]:
        """BFS con cache para rutas frecuentes"""
        clave = (origen, destino)
        if clave in self._cache_caminos:
            return self._cache_caminos[clave]
        
        resultado = self.busqueda_bfs(origen, destino)
        self._cache_caminos[clave] = resultado
        return resultado
```

## Integración con Otros Componentes

### 1. Con Vértices y Aristas
- **Composición**: Grafo contiene y gestiona vértices y aristas
- **Encapsulación**: Acceso controlado a elementos internos
- **Validación**: Integridad referencial garantizada

### 2. Con Algoritmos de Ruta
- **Proveedor**: Suministra estructura para cálculos
- **Abstracción**: Interfaz uniforme para diferentes algoritmos
- **Flexibilidad**: Soporte para múltiples estrategias

### 3. Con Simulación
- **Base**: Fundamento de toda la simulación
- **Estado**: Mantiene estado actual de la red
- **Evolución**: Permite cambios dinámicos durante simulación

## Validaciones y Restricciones

### 1. Validaciones Topológicas
- **Conectividad**: Verificación continua de conectividad
- **Ciclos**: Detección y manejo de ciclos
- **Aislamiento**: Prevención de vértices aislados

### 2. Restricciones de Negocio
- **Tipos de Vértice**: Distribución según porcentajes requeridos
- **Capacidad**: Límites máximos de vértices y aristas
- **Pesos**: Validación de rangos de pesos en aristas

### 3. Invariantes del Sistema
- **Consistencia**: Estado siempre válido
- **Integridad**: Referencias correctas entre componentes
- **Escalabilidad**: Rendimiento mantenido con crecimiento

## Casos de Uso Principales

### 1. Inicialización de Red
```python
# Generar red inicial
grafo = generar_grafo_conectado(
    num_vertices=15,
    num_aristas=20,
    porcentajes={
        TipoVertice.CLIENTE: 0.6,
        TipoVertice.ALMACENAMIENTO: 0.2,
        TipoVertice.RECARGA: 0.2
    }
)

# Verificar conectividad
assert grafo.es_conectado()
```

### 2. Cálculo de Rutas
```python
# Buscar ruta con autonomía limitada
almacenes = grafo.listar_vertices_por_tipo(TipoVertice.ALMACENAMIENTO)
clientes = grafo.listar_vertices_por_tipo(TipoVertice.CLIENTE)

ruta = grafo.busqueda_bfs_con_autonomia(
    origen=almacenes[0].id_vertice,
    destino=clientes[0].id_vertice,
    autonomia_maxima=50.0
)
```

### 3. Análisis de Red
```python
# Calcular MST para optimización
mst = grafo.calcular_mst_kruskal()
costo_total_mst = sum(arista.peso for arista in mst)

# Analizar centralidad de vértices
for vertice_id in grafo._vertices:
    grado = grafo.calcular_grado(vertice_id)
    print(f"Vértice {vertice_id}: grado {grado}")
```

## Métricas y Estadísticas

### 1. Métricas Topológicas
- **Densidad**: `2 * num_aristas / (num_vertices * (num_vertices - 1))`
- **Grado promedio**: `2 * num_aristas / num_vertices`
- **Diámetro**: Distancia máxima entre cualquier par de vértices
- **Radio**: Distancia mínima desde el centro

### 2. Métricas de Rendimiento
- **Tiempo de búsqueda**: Medición de algoritmos de ruta
- **Memoria utilizada**: Tamaño de estructuras internas
- **Cache hit rate**: Efectividad del cache de rutas

### 3. Métricas de Negocio
- **Cobertura**: Porcentaje de clientes accesibles
- **Eficiencia energética**: Rutas que requieren recarga
- **Balanceamiento**: Distribución de carga entre almacenes

## Testing y Validación

### Pruebas Unitarias
```python
def test_agregar_vertice():
    grafo = Grafo()
    vertice = crear_vertice_cliente("V001")
    
    assert grafo.agregar_vertice(vertice) == True
    assert grafo.cantidad_vertices() == 1
    assert grafo.obtener_vertice("V001") == vertice

def test_conectividad():
    grafo = generar_grafo_conectado(10, 15, PORCENTAJES_ESTANDAR)
    
    assert grafo.es_conectado() == True
    
    # Verificar camino entre todos los pares
    vertices = list(grafo._vertices.keys())
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            assert grafo.existe_camino(vertices[i], vertices[j]) == True
```

### Pruebas de Rendimiento
```python
def test_rendimiento_busqueda():
    grafo = generar_grafo_conectado(100, 200, PORCENTAJES_ESTANDAR)
    
    inicio = time.time()
    for _ in range(1000):
        origen = random.choice(list(grafo._vertices.keys()))
        destino = random.choice(list(grafo._vertices.keys()))
        grafo.busqueda_bfs(origen, destino)
    
    tiempo_total = time.time() - inicio
    assert tiempo_total < 5.0  # Debe completarse en menos de 5 segundos
```

Este componente es el corazón estructural del sistema, proporcionando la base sobre la cual se construyen todas las funcionalidades de routing y simulación del sistema logístico de drones.

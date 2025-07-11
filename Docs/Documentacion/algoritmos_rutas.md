# Algoritmos de Cálculo de Rutas

## Descripción General
El sistema implementa múltiples algoritmos para el cálculo de rutas óptimas entre almacenamientos y clientes, considerando la autonomía limitada de los drones y la necesidad de estaciones de recarga.

## 🔍 Algoritmos Implementados

### 1. BFS (Breadth-First Search)
**Archivo**: `Backend/Dominio/AlgEstrategias/RutaEstrategiaBFS.py`

#### Características
- **Objetivo**: Encontrar la ruta con menor número de saltos
- **Complejidad**: O(V + E) donde V = vértices, E = aristas
- **Garantiza**: La ruta con menor número de vértices intermedios

#### Implementación Específica
```python
def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
    queue = deque()
    queue.append((origen, autonomia, [], 0))  # (vertice, energia, camino, distancia)
    
    mejor_energia_por_vertice = {}
    mejor_energia_por_vertice[origen] = autonomia
    
    while queue:
        vertice_actual, energia_actual, camino_aristas, distancia = queue.popleft()
        
        if vertice_actual == destino:
            return camino_aristas, sum(a.peso for a in camino_aristas)
```

#### Estrategias de Optimización
1. **Control de Energía**: Rastrea la mejor energía alcanzada en cada vértice
2. **Tolerancia Energética**: Permite exploración alternativa con threshold de 15 unidades
3. **Gestión de Recarga**: Restaura energía automáticamente en estaciones de recarga
4. **Prevención de Ciclos**: Limita la longitud máxima del camino

### 2. DFS (Depth-First Search)
**Archivo**: `Backend/Dominio/AlgEstrategias/RutaEstrategiaDFS.py`

#### Características
- **Objetivo**: Exploración profunda, encuentra cualquier ruta válida
- **Complejidad**: O(V + E)
- **Ventaja**: Menor uso de memoria

#### Implementación
```python
def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
    stack = [(origen, autonomia)]
    prev = dict()  # Estado -> (predecesor, energia_previa, arista)
    visitados = dict()  # vertice -> energia_maxima_alcanzada
    
    while stack:
        vertice_actual, energia_actual = stack.pop()
        if vertice_actual == destino:
            # Reconstruir camino
            return self._reconstruir_camino(prev, destino, energia_actual)
```

### 3. Dijkstra
**Archivo**: `Backend/Dominio/AlgEstrategias/RutaEstrategiaDijkstra.py`

#### Características
- **Objetivo**: Ruta de menor costo total
- **Complejidad**: O((V + E) log V)
- **Garantiza**: La ruta óptima en términos de peso total

#### Implementación
```python
def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
    import heapq
    pq = [(0, origen, autonomia, [])]  # (costo, vertice, energia, camino)
    visitados = {}
    
    while pq:
        costo_actual, vertice_actual, energia_actual, camino = heapq.heappop(pq)
        
        if vertice_actual == destino:
            return camino, costo_actual
```

### 4. Floyd-Warshall
**Archivo**: `Backend/Dominio/AlgEstrategias/RutaEstrategiaFloydWarshall.py`

#### Características
- **Objetivo**: Todas las rutas mínimas entre todos los pares de vértices
- **Complejidad**: O(V³)
- **Uso**: Precálculo para consultas rápidas múltiples

### 5. Topological Sort
**Archivo**: `Backend/Dominio/AlgEstrategias/RutaEstrategiaTopologicalSort.py`

#### Características
- **Objetivo**: Ordenamiento topológico para DAG
- **Aplicación**: Rutas con dependencias secuenciales

### 6. Kruskal (MST)
**Archivo**: `Backend/Dominio/AlgEstrategias/RutaEstrategiaKruskal.py`

#### Características
- **Objetivo**: Árbol de expansión mínima
- **Uso**: Optimización de infraestructura de red

## 🔋 Gestión de Autonomía

### Modelo de Energía
```python
energia_inicial = 50  # Autonomía máxima del dron
energia_actual = energia_inicial - peso_arista

# En estación de recarga
if es_estacion_recarga(vertice):
    energia_actual = energia_inicial  # Recarga completa
```

### Validaciones
1. **Peso de Arista**: `peso <= autonomia_maxima`
2. **Energía Suficiente**: `energia_actual >= peso_arista`
3. **Recarga Obligatoria**: Si no hay energía suficiente para continuar

## 🎯 Selección de Algoritmo

### Criterios de Selección
| Algoritmo | Mejor Para | Ventajas | Desventajas |
|-----------|------------|----------|-------------|
| BFS | Rutas cortas | Menor número de saltos | No considera pesos |
| DFS | Exploración rápida | Bajo uso de memoria | No garantiza óptimo |
| Dijkstra | Costo mínimo | Ruta óptima | Mayor complejidad |
| Floyd-Warshall | Múltiples consultas | Precálculo completo | Alto costo inicial |

### Parámetros de Configuración
```python
# Configuración por defecto
AUTONOMIA_DEFAULT = 50
MAX_ITERACIONES = 2000
TOLERANCE_ENERGIA = 15
MAX_LONGITUD_CAMINO = num_vertices * 2
```

## 🏗️ Arquitectura de Estrategias

### Patrón Strategy
```python
class IRutaEstrategia:
    def calcular_ruta(self, origen, destino, grafo, autonomia, estaciones_recarga):
        pass

class FabricaRutas:
    def __init__(self):
        self.estrategias = {
            'bfs': RutaEstrategiaBFS(),
            'dfs': RutaEstrategiaDFS(),
            'dijkstra': RutaEstrategiaDijkstra(),
            # ...
        }
    
    def calcular_ruta(self, pedido, grafo, algoritmo):
        estrategia = self.estrategias[algoritmo]
        return estrategia.calcular_ruta(origen, destino, grafo)
```

## 📊 Métricas y Logging

### Información Registrada
1. **Tiempo de cálculo**
2. **Número de iteraciones**
3. **Vértices explorados**
4. **Energía final**
5. **Longitud del camino**

### Ejemplo de Log
```
[BFS] Preparando para calcular ruta: origen=Almacen_1, destino=Cliente_6, autonomia=50
[BFS] Iniciando búsqueda: 15 vértices, 20 aristas disponibles
[BFS] Exploración terminada: 45 iteraciones, 12 vértices explorados
[BFS] Destino alcanzado: camino=8 aristas, peso_total=47, energia_restante=28
```

## 🚀 Optimizaciones Futuras

### Mejoras Propuestas
1. **A* Search**: Heurística para búsqueda dirigida
2. **Algoritmos Genéticos**: Para optimización multi-objetivo
3. **Machine Learning**: Predicción de patrones de tráfico
4. **Paralelización**: Cálculo simultáneo de múltiples rutas

### Consideraciones de Rendimiento
- **Caching**: Almacenar rutas calculadas frecuentemente
- **Precálculo**: Floyd-Warshall para grafos estáticos
- **Índices Espaciales**: Para búsqueda geográfica eficiente

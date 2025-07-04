# Plan de Refactorización: Integración Total de Rutas

Este documento describe el plan **atomizado y detallado** para implementar completamente la funcionalidad de cálculo de rutas en todas las capas del sistema, **sin crear archivos nuevos**, solo refactorizando los existentes. El plan asegura modularidad, cohesión y alineación con los patrones existentes según `Requisitos.md`.

---

## Funcionalidades Objetivo

### 1. Calcular Ruta Individual
- **Input**: `id_pedido` + `algoritmo` específico  
- **Output**: Objeto `Ruta` con aristas, peso total, tiempo de cálculo
- **Constraint**: NO marca el pedido como entregado

### 2. Calcular Todas las Rutas para un Pedido
- **Input**: `id_pedido` + `algoritmo="todos"`
- **Output**: Diccionario `{algoritmo: Ruta}` para comparación
- **Constraint**: NO marca el pedido como entregado

### 3. Calcular Todos los Algoritmos para Todos los Pedidos
- **Input**: Sin parámetros específicos
- **Output**: Matriz completa de rutas `{id_pedido: {algoritmo: Ruta}}`

### 4. Calcular Floyd-Warshall Global
- **Input**: Algoritmo específico "floyd_warshall"
- **Output**: Matriz de distancias pre-calculada para toda la red

### 5. Entregar Pedido (Separado)
- **Input**: `id_pedido` + `ruta_seleccionada` (opcional)
- **Output**: Cambio de estado a "entregado"
- **Constraint**: Acción independiente del cálculo de ruta

---

## Arquitectura y Patrones Identificados

### Entidades Core
- **Vértices**: Cliente, Almacenamiento, Recarga (únicos en repositorio O(1))
- **Aristas**: Conexiones con peso, referencias a vértices extremos
- **Grafo**: Estructura centralizada con HashMap O(1) para acceso
- **Autonomía**: 50 unidades, reseteo en recargas
- **Pedidos**: Estado independiente del cálculo de ruta

### Flujo de Datos
```
Frontend → API → Aplicación → Servicio → Dominio → Estrategias
                ↓
RepositorioRutas (O(1)) → HashMap → Respuesta DTO → Frontend
```

---

## Plan de Refactorización Detallado

## FASE 1: Dominio de Rutas

### 1.1. Refactorizar `Dominio_Ruta.py`
**Objetivo**: Crear clase Ruta robusta que integre con el sistema existente

**Atributos de la clase Ruta:**
```python
class Ruta:
    def __init__(self, id_ruta, id_pedido, origen, destino, aristas_ids, peso_total, algoritmo, tiempo_calculo):
        self._id_ruta = id_ruta                    # UUID único
        self._id_pedido = id_pedido                # Referencia al pedido
        self._origen = origen                      # Vértice origen
        self._destino = destino                    # Vértice destino  
        self._aristas_ids = aristas_ids            # Lista de IDs de aristas recorridas
        self._peso_total = peso_total              # Peso sin contar resets de recarga
        self._algoritmo = algoritmo                # Estrategia utilizada
        self._tiempo_calculo = tiempo_calculo      # Tiempo en segundos
        self._fecha_creacion = datetime.now()
        self._observadores = []                    # Patrón Observer
```

**Métodos requeridos:**
- Getters/Setters con validación
- `obtener_camino_vertices()`: Reconstruir camino completo desde aristas
- `es_valida_para_autonomia(autonomia)`: Verificar si la ruta respeta la autonomía
- `agregar_observador()`, `notificar_observadores()`: Patrón Observer
- `__eq__`, `__hash__`: Para comparaciones y almacenamiento en HashMap

### 1.2. Refactorizar Estrategias en `Dominio/AlgEstrategias/`
**Cambios necesarios en cada estrategia:**

**IRutaEstrategia.py** (Interfaz):
```python
@abstractmethod
def calcular_ruta(self, origen_id, destino_id, grafo, autonomia=50, estaciones_recarga=None):
    """
    Retorna tupla: (lista_aristas_ids, peso_total)
    """
    pass
```

**Por cada estrategia específica** (`RutaEstrategiaDijkstra.py`, `RutaEstrategiaBFS.py`, etc.):
- **Input estandarizado**: `origen_id`, `destino_id`, `grafo`, `autonomia=50`
- **Output estandarizado**: `(aristas_ids: List[int], peso_total: float)`
- **Lógica de recarga**: Insertar estaciones de recarga cuando peso acumulado > autonomía
- **Manejo de errores**: Retornar `([], float('inf'))` si no hay ruta válida

### 1.3. Crear Enum de Estrategias
**En nuevo archivo o dentro de interfaces:**
```python
from enum import Enum

class TipoEstrategia(Enum):
    DIJKSTRA = "dijkstra"
    BFS = "bfs"
    DFS = "dfs"
    FLOYD_WARSHALL = "floyd_warshall"
    KRUSKAL = "kruskal"
    TOPOLOGICAL_SORT = "topological_sort"
    TODOS = "todos"
```

---

## FASE 2: Infraestructura

### 2.1. Crear `repositorio_rutas.py`
**Estructura del repositorio:**
```python
class RepositorioRutas(IRepositorio):
    def __init__(self):
        self._rutas = HashMap()  # Clave: id_ruta, Valor: Ruta
        self._indice_por_pedido = HashMap()  # Clave: id_pedido, Valor: List[id_ruta]
        self._indice_por_algoritmo = HashMap()  # Clave: algoritmo, Valor: List[id_ruta]
        
    def obtener_por_pedido(self, id_pedido):
        """Retorna todas las rutas de un pedido específico"""
        
    def obtener_por_algoritmo(self, algoritmo):
        """Retorna todas las rutas calculadas con un algoritmo"""
        
    def existe_ruta(self, id_pedido, algoritmo):
        """Verifica si ya existe una ruta para pedido+algoritmo"""
```

### 2.2. Integrar en Simulación Singleton
**Refactorizar `Simulacion_dominio.py`:**
- Agregar `self._repositorio_rutas = RepositorioRutas()`
- Método `obtener_repositorio_rutas()` para acceso global
- Integrar limpieza en `limpiar_simulacion()`

---

## FASE 3: Fábrica y Servicios

### 3.1. Refactorizar `FabricaRutas.py`
**Responsabilidades:**
```python
class FabricaRutas(FabricaInterfaz):
    def crear_ruta(self, id_pedido, origen, destino, algoritmo, grafo, autonomia=50):
        """
        1. Obtener estrategia según algoritmo
        2. Ejecutar cálculo y medir tiempo
        3. Crear objeto Ruta con resultados
        4. Registrar en repositorio
        5. Retornar Ruta creada
        """
        
    def crear_rutas_multiples(self, id_pedido, origen, destino, grafo, autonomia=50):
        """
        1. Iterar sobre todas las estrategias disponibles
        2. Crear ruta para cada una
        3. Retornar diccionario {algoritmo: Ruta}
        """
        
    def crear_floyd_warshall_global(self, grafo):
        """
        1. Ejecutar Floyd-Warshall para toda la red
        2. Crear matriz de rutas pre-calculadas
        3. Registrar en repositorio con clave especial
        """
```

### 3.2. Refactorizar Servicios de Aplicación
**En `Aplicacion_Simulacion.py`:**
```python
def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str):
    """
    1. Validar que pedido existe
    2. Extraer origen/destino del pedido
    3. Delegar a FabricaRutas
    4. NO cambiar estado del pedido
    5. Retornar Ruta creada
    """

def calcular_rutas_todos_algoritmos(self, id_pedido: int):
    """
    1. Validar pedido
    2. Delegar a FabricaRutas.crear_rutas_multiples
    3. Retornar diccionario de rutas
    """

def entregar_pedido(self, id_pedido: int, ruta_id: str = None):
    """
    1. Cambiar estado del pedido a "entregado"
    2. Registrar fecha de entrega
    3. Notificar observadores
    4. Acción independiente del cálculo de ruta
    """
```

---

## FASE 4: DTOs y Mapeadores

### 4.1. Refactorizar DTOs en `DTOsRespuesta/`
**RespuestaRuta.py:**
```python
class RespuestaRuta(BaseModel):
    id_ruta: str
    id_pedido: int
    origen: int  # ID del vértice origen
    destino: int  # ID del vértice destino
    aristas_ids: List[int]  # IDs de aristas recorridas
    peso_total: float
    algoritmo: str
    tiempo_calculo: float
    fecha_creacion: str
    
class RespuestaMultiplesRutas(BaseModel):
    id_pedido: int
    resultados: Dict[str, RespuestaRuta]  # {algoritmo: RespuestaRuta}
    tiempo_total: float
    
class RespuestaCalculoMasivo(BaseModel):
    total_pedidos: int
    rutas_calculadas: int
    errores: List[str]
    tiempo_total: float
    resultados: Dict[int, Dict[str, RespuestaRuta]]  # {id_pedido: {algoritmo: RespuestaRuta}}
```

### 4.2. Crear Mapeadores
**MapeadorRuta.py:**
```python
class MapeadorRuta(IMapeadorDominioDTO):
    @staticmethod
    def a_dto(ruta: Ruta) -> RespuestaRuta:
        """Convertir Ruta de dominio a RespuestaRuta DTO"""
        
    @staticmethod  
    def rutas_multiples_a_dto(rutas_dict: Dict[str, Ruta], id_pedido: int) -> RespuestaMultiplesRutas:
        """Convertir diccionario de rutas a DTO de múltiples rutas"""
```

---

## FASE 5: API y Endpoints

### 5.1. Refactorizar `rutas_enrutador.py`
**Endpoints específicos:**
```python
@router.post("/calcular/{id_pedido}/{algoritmo}")
def calcular_ruta_individual(id_pedido: int, algoritmo: str):
    """Calcular ruta para un pedido con algoritmo específico"""

@router.post("/calcular/{id_pedido}/todos") 
def calcular_todas_rutas_pedido(id_pedido: int):
    """Calcular rutas con todos los algoritmos para un pedido"""

@router.post("/calcular/masivo/todos")
def calcular_masivo_todos_pedidos():
    """Calcular todos los algoritmos para todos los pedidos pendientes"""

@router.post("/calcular/floyd-warshall/global")
def calcular_floyd_warshall_global():
    """Pre-calcular matriz Floyd-Warshall para toda la red"""

@router.get("/pedido/{id_pedido}")
def obtener_rutas_pedido(id_pedido: int):
    """Obtener todas las rutas calculadas para un pedido"""

@router.get("/algoritmo/{algoritmo}")  
def obtener_rutas_algoritmo(algoritmo: str):
    """Obtener todas las rutas calculadas con un algoritmo específico"""

@router.post("/entregar/{id_pedido}")
def entregar_pedido_endpoint(id_pedido: int, ruta_id: str = None):
    """Marcar pedido como entregado (acción separada del cálculo)"""
```

---

## FASE 6: Frontend

### 6.1. Refactorizar `vista_red.py`
**Agregar controles de cálculo de rutas:**
```python
# Después de selección de pedido
st.subheader("Calcular Ruta")

algoritmo_seleccionado = st.radio(
    "Algoritmo a utilizar:",
    options=["dijkstra", "bfs", "dfs", "floyd_warshall", "kruskal", "topological_sort", "todos"],
    horizontal=True
)

col1, col2 = st.columns(2)
with col1:
    if st.button("Calcular Ruta", disabled=not pedido_id):
        # Llamar endpoint de cálculo individual
        
with col2:
    if st.button("Entregar Pedido", disabled=not pedido_id):
        # Llamar endpoint de entrega (separado)
```

### 6.2. Agregar Vista de Análisis de Rutas
**En `vista_rutas.py`:**
```python
def mostrar_analisis_rutas():
    st.subheader("Análisis Comparativo de Algoritmos")
    
    # Selector de pedido para análisis
    pedido_analisis = st.selectbox("Pedido a analizar:", opciones_pedidos)
    
    if st.button("Comparar Todos los Algoritmos"):
        # Llamar endpoint de cálculo múltiple
        # Mostrar tabla comparativa con tiempos y pesos
        
    st.subheader("Cálculo Masivo")
    if st.button("Calcular Rutas para Todos los Pedidos"):
        # Llamar endpoint de cálculo masivo
        # Mostrar progress bar y resultados
```

---

## FASE 7: Integración y Testing

### 7.1. Validaciones de Integridad
- **Unicidad**: Evitar duplicados ruta+pedido+algoritmo
- **Consistencia**: Verificar que aristas_ids corresponden a aristas válidas
- **Autonomía**: Validar que rutas respetan límites de autonomía
- **Estado de Pedidos**: Asegurar separación entre cálculo y entrega

### 7.2. Testing Incremental
**Por cada fase completada:**
1. Test unitario de la capa refactorizada
2. Test de integración con capas anteriores
3. Test de endpoints con Postman/pytest
4. Test de UI con datos de prueba

### 7.3. Monitoreo y Logging
- **Performance**: Medir tiempos de cálculo por algoritmo
- **Errores**: Registrar fallos en cálculo de rutas
- **Uso**: Estadísticas de algoritmos más utilizados
- **Integridad**: Auditar creación/modificación de rutas

---

## Cronograma de Implementación

### Día 1: Dominio (Fases 1-2)
- Refactorizar `Dominio_Ruta.py`
- Actualizar todas las estrategias en `AlgEstrategias/`  
- Crear `repositorio_rutas.py`
- Integrar en simulación singleton

### Día 2: Servicios y Lógica (Fase 3)
- Refactorizar `FabricaRutas.py`
- Actualizar servicios de aplicación
- Testing unitario de lógica de dominio

### Día 3: API (Fases 4-5) 
- Crear/refactorizar DTOs de rutas
- Implementar mapeadores
- Desarrollar endpoints completos
- Testing de API con Postman

### Día 4: Frontend (Fase 6)
- Refactorizar `vista_red.py` con controles de ruta
- Mejorar `vista_rutas.py` con análisis comparativo
- Integrar llamadas a nuevos endpoints
- Testing de UI end-to-end

### Día 5: Integración (Fase 7)
- Testing integral de todas las capas
- Validaciones de consistencia
- Optimización de performance
- Documentación final

---

## Consideraciones Técnicas

### Manejo de Autonomía
- **Límite**: 50 unidades por tramo
- **Reset**: En estaciones de recarga (vertices tipo "recarga")
- **Validación**: Insertar recargas automáticamente si es necesario
- **Peso**: No contar el peso de los resets en el peso total

### Optimización de Performance
- **Cache**: Resultados de Floyd-Warshall pre-calculados
- **Índices**: HashMap O(1) por pedido y por algoritmo
- **Lazy Loading**: Calcular rutas solo cuando se requieren
- **Batch Processing**: Cálculo masivo optimizado

### Escalabilidad
- **Estrategias**: Fácil agregar nuevos algoritmos implementando IRutaEstrategia
- **Persistencia**: Repositorio preparado para BD futura
- **Distribución**: Patrón Observer permite procesamiento asíncrono
- **Monitoring**: Métricas integradas para análisis de performance

Este plan asegura una implementación robusta, modular y completamente integrada del sistema de rutas, manteniendo la separación de responsabilidades y siguiendo los patrones arquitectónicos establecidos.

**Kruskal:**
- Calcular árbol de expansión mínima (MST)
- Retornar lista de aristas del MST, no camino específico

**Topological Sort:**
- Solo válido para grafos dirigidos acíclicos
- Retornar orden topológico filtrado por camino origen→destino

**Interfaz común actualizada:**
```python
def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
    # Implementación específica
    # Retorna: (camino: List[Vertice], aristas_recorridas: List[Arista])
```

### 2.2. Clase `Ruta` (`Dominio/Dominio_Ruta.py`)
**Nuevos atributos:**
- `aristas_ids: List[int]` - IDs de aristas recorridas en orden
- `tiempo_calculo: float` - Tiempo en segundos del cálculo
- `autonomia_usada: float` - Autonomía total consumida
- `recargas_necesarias: int` - Número de recargas insertadas

**Métodos actualizados:**
- `serializar()`: Incluir nuevos campos
- `es_valida()`: Validar autonomía y conectividad de aristas
- `calcular_peso_total()`: Sumar pesos de aristas sin contar resets de recarga

### 2.3. Fábrica de Rutas (`Dominio/EntFabricas/FabricaRutas.py`)
**Métodos principales:**

```python
def calcular_ruta_unica(self, origen, destino, algoritmo, grafo, autonomia=50):
    """Calcula ruta con algoritmo específico"""

def calcular_todas_las_rutas(self, origen, destino, grafo, autonomia=50):
    """Calcula rutas con todos los algoritmos disponibles"""
    
def crear_ruta(self, origen, destino, camino, algoritmo, tiempo_calculo):
    """Crea instancia Ruta a partir de camino calculado"""

def calcular_todo_con_tiempos(self, origen, destino, grafo, autonomia=50):
    """Calcula todas las rutas y mide tiempos de todos los algoritmos"""
```

**Lógica de medición de tiempo:**
- `time.perf_counter()` antes y después de cada cálculo
- Para "todos": dict `{algoritmo: tiempo}`, tiempo_total = suma ,

---

## 3. Infraestructura y Repositorio

### 3.1. RepositorioRutas (`Infraestructura/Repositorios/repositorio_rutas.py`)
**Completar implementación:**

```python
class RepositorioRutas(IRepositorio):
    def _clave_ruta(self, origen_id, destino_id, algoritmo):
        return f"{origen_id}-{destino_id}-{algoritmo}"
    
    def obtener_por_pedido(self, id_pedido):
        """Obtiene todas las rutas calculadas para un pedido"""
    
    def obtener_por_algoritmo(self, algoritmo):
        """Obtiene todas las rutas calculadas con un algoritmo específico"""
    
    def todos_serializados(self):
        """Retorna todas las rutas en formato DTO usando MapeadorRuta"""
```

**Claves de HashMap:**
- Formato: `"{origen_id}-{destino_id}-{algoritmo}"`
- Garantiza unicidad por combinación origen-destino-algoritmo
- Permite múltiples rutas para el mismo par origen-destino con diferentes algoritmos

### 3.2. HashMap de Aristas Existente
**Aprovechar HashMap O(1) existente:**
- Usar `repositorio_aristas.obtener_por_vertices(origen, destino)` para encontrar arista específica
- Extraer `arista.id` para llenar `aristas_ids` en la ruta
- Usar `arista.peso` para cálculo de peso total y validación de autonomía

---

## 4. DTOs y Mapeadores

### 4.1. DTOs de Salida Actualizados

**RespuestaRuta.py:**
```python
class RespuestaRuta(BaseModel):
    id_pedido: int
    origen: RespuestaVertice
    destino: RespuestaVertice
    aristas_ids: List[int]  # IDs de aristas recorridas en orden
    camino_vertices: List[RespuestaVertice]  # Vértices del camino
    peso_total: float
    algoritmo: str
    tiempo_calculo: float
    autonomia_usada: float
    recargas_necesarias: int

class RespuestaMultiplesRutas(BaseModel):
    id_pedido: int
    origen: RespuestaVertice
    destino: RespuestaVertice
    resultados: Dict[str, RespuestaRuta]
    tiempo_total: float
    algoritmo_mas_rapido: str
    algoritmo_peso_minimo: str
```

### 4.2. MapeadorRuta Actualizado (`Backend/API/Mapeadores/MapeadorRuta.py`)

```python
@staticmethod
def a_dto(ruta: Ruta, id_pedido: int) -> RespuestaRuta:
    """Mapea Ruta de dominio a DTO, incluyendo aristas_ids"""

@staticmethod
def multiples_a_dto(ruta_multiple: RutaMultiple) -> RespuestaMultiplesRutas:
    """Mapea RutaMultiple a DTO con análisis comparativo"""

@staticmethod
def extraer_aristas_ids(camino: List[Vertice], grafo) -> List[int]:
    """Extrae IDs de aristas del camino usando HashMap O(1)"""
```

---

## 5. Servicios y Aplicación

### 5.1. Caso de Uso (`Aplicacion/SimAplicacion/Aplicacion_Simulacion.py`)

**Nuevos métodos:**
```python
def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str = "bfs") -> Union[Ruta, RutaMultiple]:
    """
    Orquesta el cálculo de ruta para un pedido específico
    1. Validar que el pedido existe y está pendiente
    2. Extraer origen y destino del pedido
    3. Obtener grafo y estaciones de recarga de la simulación
    4. Delegar a FabricaRutas para cálculo
    5. Registrar en RepositorioRutas
    6. Retornar resultado
    """

def obtener_rutas_pedido(self, id_pedido: int) -> List[Ruta]:
    """Obtiene todas las rutas calculadas para un pedido"""

def analizar_rutas_frecuentes(self) -> Dict[str, int]:
    """Analiza frecuencia de uso de rutas para AVL"""
```

### 5.2. Servicio de Simulación (`Servicios/SimServicios/Servicios_Simulacion.py`)

**Integración con simulación:**
```python
def calcular_ruta_con_contexto(self, id_pedido: int, algoritmo: str):
    """
    Wrapper que incluye contexto de simulación activa
    - Verificar simulación activa
    - Obtener instancia singleton de simulación
    - Delegar a caso de uso
    - Manejar errores y logging
    """
```

---

## 6. API y Endpoints

### 6.1. Router de Rutas (`Backend/API/rutas_enrutador.py`)

**Endpoints principales:**
```python
@router.post("/rutas/{id_pedido}")
def calcular_ruta(id_pedido: int, algoritmo: str =):
    """Calcula ruta para pedido con algoritmo específico o todos"""

@router.get("/rutas/{id_pedido}")
def obtener_rutas_pedido(id_pedido: int):
    """Obtiene todas las rutas calculadas para un pedido"""

@router.get("/rutas")
def listar_todas_las_rutas():
    """Lista todas las rutas en el sistema con filtros opcionales"""

@router.get("/rutas/analisis/frecuencias")
def analizar_frecuencias():
    """Análisis de rutas más frecuentes para AVL"""
    
```

**Manejo de errores:**
- 404: Pedido no existe
- 400: Algoritmo inválido
- 409: Ruta ya calculada con ese algoritmo
- 422: Validación de datos de entrada

### 6.2. Integración con Endpoints Existentes
- Actualizar `/simulacion/info` para incluir estadísticas de rutas
- Modificar `/pedidos/{id}` para mostrar rutas asociadas

---

## 7. Frontend Streamlit

### 7.1. Vista de Red (`frontendv2/ui/vista_red.py`)

**Nuevos componentes:**
```python
# Después del selectbox de pedidos
algoritmo_seleccionado = st.radio(
    "Algoritmo de cálculo",
    ["bfs", "dfs", "dijkstra", "floydwarshall", "kruskal", "topologicalsort", "todos"],
    index=0
)

if st.button("Calcular Ruta", key="calcular_ruta"):
    # Llamar a API para calcular ruta
    # Mostrar resultados en expander
    # Actualizar visualización del grafo con ruta destacada
```

**Visualización de rutas:**
- Destacar camino calculado en el grafo con color diferente
- Mostrar métricas: peso total, tiempo de cálculo, recargas necesarias
- Para "todos": tabla comparativa de algoritmos

### 7.2. Nueva Vista de Análisis de Rutas (`frontendv2/ui/vista_rutas.py`)

**Funcionalidades:**
- Tabla de todas las rutas calculadas
- Filtros por algoritmo, pedido, peso
- Gráficos comparativos de rendimiento
- Análisis de frecuencias para alimentar AVL

### 7.3. Cache y Gestión de Estado (`frontendv2/servicios/cache.py`)

```python
@st.cache_data(ttl=10, show_spinner=False)
def cachear_rutas():
    return obtener_rutas_dto()

def inicializar_snapshot_datos():
    # ...código existente...
    datos['rutas'] = cachear_rutas()
    # Agregar rutas al snapshot global
```

### 7.4. API Frontend (`frontendv2/servicios/api.py`)

```python
def calcular_ruta_pedido(id_pedido: int, algoritmo: str = "bfs"):
    """POST /rutas/{id_pedido}"""

def obtener_rutas_pedido(id_pedido: int):
    """GET /rutas/{id_pedido}"""

def obtener_rutas_dto():
    """GET /rutas"""
```

---

## 8. Integración con AVL y Análisis de Frecuencias

### 8.1. AVL de Rutas Frecuentes
**Modificar AVL existente para rutas:**
- Clave: `"origen_id-destino_id"` (sin algoritmo)
- Valor: contador de frecuencia de uso
- Incrementar contador cada vez que se calcula/usa una ruta

### 8.2. Observer Pattern para Frecuencias
```python
class ObservadorFrecuenciaRutas:
    def actualizar(self, evento, ruta, datos):
        if evento == 'ruta_calculada':
            # Incrementar frecuencia en AVL
            # Registrar en auditoria
```

---

## 9. Testing y Validación

### 9.1. Tests Unitarios
**Por cada estrategia:**
- Grafo de prueba con 5 vértices, 6 aristas
- Verificar camino esperado para cada algoritmo
- Validar manejo de autonomía y recargas
- Verificar medición de tiempo

**Para repositorio:**
- Unicidad de claves
- Operaciones CRUD O(1)
- Serialización correcta

### 9.2. Tests de Integración
**Flujo completo:**
1. Crear simulación con pedidos
2. Calcular ruta con API
3. Verificar persistencia en repositorio
4. Consultar desde frontend
5. Validar datos en cache

### 9.3. Tests BDD
```gherkin
Scenario: Calcular ruta con algoritmo específico
  Given una simulación activa con pedidos
  When calculo ruta para pedido 1 con algoritmo "dijkstra"
  Then debo obtener una ruta válida
  And la ruta debe estar registrada en el repositorio
  And el tiempo de cálculo debe ser mayor que 0

Scenario: Calcular todas las rutas
  Given un pedido con origen y destino válidos
  When calculo ruta con algoritmo "todos"
  Then debo obtener rutas para cada algoritmo disponible
  And cada ruta debe tener su tiempo de cálculo individual
```

---

## 10. Plan de Implementación por Fases

### Fase 1: Fundamentos (Días 1-2)
1. Completar DTOs de entrada y salida
2. Actualizar clase `Ruta` con nuevos atributos
3. Refactorizar estrategias para interfaz común
4. Completar `RepositorioRutas`

### Fase 2: Lógica de Negocio (Días 3-4)
1. Implementar `FabricaRutas` con medición de tiempo
2. Crear casos de uso en `Aplicacion_Simulacion`
3. Actualizar `MapeadorRuta`
4. Implementar `RutaMultiple`

### Fase 3: API y Endpoints (Día 5)
1. Completar `rutas_enrutador.py`
2. Integrar con servicios existentes
3. Manejo de errores y validaciones
4. Tests de endpoints

### Fase 4: Frontend (Días 6-7)
1. Actualizar `vista_red.py` con selector de algoritmos
2. Implementar visualización de rutas en grafo
3. Crear `vista_rutas.py` para análisis
4. Integrar con cache y snapshot

### Fase 5: Integración y Testing (Días 8-10)
1. Tests unitarios e integración
2. Tests BDD completos
3. Integración con AVL de frecuencias
4. Observer pattern para auditoría
5. Optimizaciones y refactorización final

---

## 11. Consideraciones Técnicas

### 11.1. Rendimiento
- HashMap O(1) para acceso a aristas y rutas
- Cache de 10 segundos en frontend para reducir llamadas API
- Medición precisa de tiempo con `time.perf_counter()`
- Lazy loading de rutas en frontend

### 11.2. Escalabilidad
- Patrón Strategy fácilmente extensible para nuevos algoritmos
- Repositorio único garantiza gestión centralizada
- DTOs permiten versionado de API
- Observer pattern para extensiones futuras

### 11.3. Mantenibilidad
- Separación clara de responsabilidades por capa
- Interfaces bien definidas entre componentes
- Logging y auditoría en todas las operaciones
- Documentación completa de APIs

### 11.4. Robustez
- Validación de datos en cada capa
- Manejo de errores específicos y descriptivos
- Fallbacks para algoritmos que fallen
- Validación de conectividad de grafo antes de calcular

3.1. **RepositorioRutas** (`Infraestructura/Repositorios/repositorio_rutas.py`):
   - Añadir métodos: `obtener_por_pedido(id_pedido)`, `todos_por_algoritmo(alg)`.
   - Serialización: exponer método `todos_serializados()` usando `MapeadorRuta`.

## 4. Mapeadores y DTOs de Respuesta

4.1. **DTOs** (`Backend/API/DTOs/DTOsRespuesta/RespuestaRuta.py`):
   - Completar clase `RespuestaMultiplesRutas` con campos: id_pedido, resultados: Dict[str, RespuestaRuta] o List[RespuestaRuta].
4.2. **MapeadorRuta** (`Backend/API/Mapeadores/MapeadorRuta.py`):
   - Ajustar `a_dto` para llenar `aristas` con IDs.
   - Añadir `a_multiples(ruta_multiple)` para mapear cada algoritmo.

## 5. Servicio de Aplicación y Casos de Uso

5.1. **Caso de Uso** (`Aplicacion/SimAplicacion/Aplicacion_Simulacion.py`):
   - Agregar método `calcular_ruta_pedido(id_pedido, algoritmo)` que:
     - Valida existencia de pedido y grafo.
     - Llama a `FabricaRutas.crear(...)` o `crear_todas(...)`.
     - Actualiza estado del pedido en memoria: asigna ruta, peso_total.
5.2. **Servicios** (`Servicios/SimServicios/Servicios_Simulacion.py`):
   - Invocar el caso de uso desde capa API.

## 6. Endpoints de Rutas

6.1. **Router** (`Backend/API/rutas_enrutador.py`):
   - POST `/rutas/{id_pedido}` con query `?algoritmo=<alg>` que devuelve `RespuestaRuta`.
   - POST `/rutas/{id_pedido}/todos` que devuelve `RespuestaMultiplesRutas`.
   - GET `/rutas` que lista todas las rutas existentes (frecuencias opcionales).
6.2. Asegurar manejo correcto de errores (404 pedido no existe, 400 algoritmo inválido).

## 7. Frontend Streamlit

7.1. **Vista de Rutas** (`frontendv2/ui/vista_red.py`):
   - Bajo select de `pedido`, agregar `st.radio` con opciones de algoritmos + "Todos".
   - Al presionar "Calcular Ruta":
     - Llamar al endpoint correspondiente.
     - Mostrar JSON resultante y renderizar camino sobre grafo con `networkx`.
7.2. **Snapshot de Datos** (`frontendv2/servicios/cache.py`):
   - Incluir funciones para cachear rutas (`cachear_rutas()`).
   - Actualizar `inicializar_snapshot_datos()` para traer rutas iniciales.
7.3. **Botón Global**: en `menu.py`, reutilizar `boton_actualizar_datos()` para limpiar snapshot y recargar rutas.

## 8. Pruebas y BDD

8.1. **Tests Unitarios**:
   - Para cada estrategia: rutas esperadas en grafos de prueba.
   - Para `FabricaRutas`: unicidad y manejo "todos".
   - Para servicio de aplicación: validaciones y actualizaciones de estado.
8.2. **Tests Integrales / BDD**:
   - Escenario "Calcular ruta única" y "Calcular todas rutas".
   - Escenario de recarga automática cuando excede autonomía.

## 9. Documentación y Ejemplos

9.1. Actualizar `Docs/serializacion.md` con ejemplos de salida de `RespuestaRuta` y `RespuestaMultiplesRutas`.
9.2. Incluir diagramas de secuencia en `Docs/diagramas/` para flujo de `Calcular Ruta`.

## 10. Despliegue y Validación Final

10.1. Ejecutar la aplicación completa, verificar pestañas de Streamlit y endpoints de FastAPI.
10.2. Revisar perfiles de rendimiento: medir tiempos de cálculo y caché.
10.3. Entregar PR con revisión de código y documentación adjunta.

---

*Fin del plan de refactorización de rutas.*

# Documentación del Componente Pedido

## Descripción General
El componente `Pedido` representa una solicitud de entrega en el sistema logístico de drones. Es la entidad central que coordina la información entre clientes, rutas, almacenes y el proceso de entrega. Cada pedido encapsula toda la información necesaria para ejecutar una entrega desde el origen hasta el destino.

## Ubicación en la Arquitectura
- **Capa de Dominio**: `Backend/Dominio/Dominio_Pedido.py`
- **Patrón**: Entidad agregada rica con lógica de negocio
- **Responsabilidad**: Gestión del ciclo de vida de entregas y coordinación entre componentes

## Estructura de la Clase

### Atributos Principales
```python
class Pedido:
    def __init__(self, id_pedido: str, cliente: Cliente, almacenamiento_origen: Almacenamiento,
                 descripcion: str, peso: float, prioridad: PrioridadPedido):
        self._id_pedido: str                    # Identificador único del pedido
        self._cliente: Cliente                  # Cliente que solicita el pedido
        self._almacenamiento_origen: Almacenamiento  # Almacén de origen
        self._descripcion: str                  # Descripción del contenido
        self._peso: float                       # Peso del paquete (kg)
        self._prioridad: PrioridadPedido       # Prioridad de entrega
        self._estado: EstadoPedido             # Estado actual del pedido
        self._fecha_creacion: datetime         # Fecha de creación
        self._fecha_entrega: Optional[datetime] # Fecha de entrega (si completado)
        self._ruta_asignada: Optional[Ruta]    # Ruta calculada para la entrega
        self._costo_total: Optional[float]     # Costo total de la entrega
        self._observaciones: str               # Notas adicionales
```

### Enumeraciones Asociadas
```python
class EstadoPedido(Enum):
    PENDIENTE = "pendiente"      # Pedido creado, esperando procesamiento
    EN_RUTA = "en_ruta"         # Ruta calculada, en proceso de entrega
    ENTREGADO = "entregado"     # Entrega completada exitosamente
    CANCELADO = "cancelado"     # Pedido cancelado
    FALLIDO = "fallido"         # Entrega fallida

class PrioridadPedido(Enum):
    BAJA = 1        # Entrega estándar
    MEDIA = 2       # Entrega prioritaria
    ALTA = 3        # Entrega urgente
    CRITICA = 4     # Entrega crítica (médica, emergencia)
```

## Funcionalidades Principales

### 1. Gestión del Ciclo de Vida
```python
def iniciar_procesamiento(self) -> bool:
    """Cambia estado a EN_RUTA cuando se asigna ruta"""
    
def completar_entrega(self, fecha_entrega: datetime = None) -> bool:
    """Marca el pedido como entregado"""
    
def cancelar_pedido(self, motivo: str) -> bool:
    """Cancela el pedido con motivo"""
    
def marcar_como_fallido(self, motivo: str) -> bool:
    """Marca entrega como fallida"""
```

### 2. Gestión de Rutas
```python
def asignar_ruta(self, ruta: Ruta) -> bool:
    """Asocia una ruta calculada al pedido"""
    
def obtener_ruta(self) -> Optional[Ruta]:
    """Retorna la ruta asignada"""
    
def calcular_costo_estimado(self) -> float:
    """Calcula costo basado en ruta y peso"""
    
def tiene_ruta_asignada(self) -> bool:
    """Verifica si tiene ruta calculada"""
```

### 3. Consultas y Validaciones
```python
def es_entregable(self) -> bool:
    """Verifica si el pedido puede ser entregado"""
    
def requiere_atencion_prioritaria(self) -> bool:
    """Verifica si necesita procesamiento urgente"""
    
def tiempo_desde_creacion(self) -> timedelta:
    """Calcula tiempo transcurrido desde creación"""
    
def obtener_destino(self) -> str:
    """Retorna ID del vértice destino (cliente)"""
```

### 4. Gestión de Información
```python
def actualizar_descripcion(self, nueva_descripcion: str) -> bool:
    """Actualiza descripción del pedido"""
    
def agregar_observacion(self, observacion: str) -> None:
    """Agrega nota adicional al pedido"""
    
def obtener_resumen(self) -> dict:
    """Retorna resumen completo del pedido"""
```

## Reglas de Negocio

### 1. Estados y Transiciones
- **PENDIENTE → EN_RUTA**: Cuando se asigna ruta válida
- **EN_RUTA → ENTREGADO**: Cuando se completa entrega exitosa
- **EN_RUTA → FALLIDO**: Cuando falla la entrega
- **PENDIENTE/EN_RUTA → CANCELADO**: Por solicitud del cliente o sistema
- **No reversibles**: Estados finales (ENTREGADO, CANCELADO, FALLIDO)

### 2. Validaciones de Negocio
- **Peso**: Debe ser positivo y no superar límite del dron
- **Prioridad**: Afecta orden de procesamiento
- **Cliente**: Debe estar activo para crear pedidos
- **Almacén**: Debe existir y estar operativo

### 3. Restricciones Temporales
- **Tiempo máximo**: Pedidos pendientes no pueden superar límite
- **Prioridad crítica**: Procesamiento inmediato
- **Horarios**: Consideración de ventanas de entrega

### 4. Costos
- **Base**: Costo fijo por entrega
- **Distancia**: Costo por unidad de distancia
- **Peso**: Costo adicional por peso
- **Prioridad**: Multiplicador según prioridad

## Relaciones con Otros Componentes

### 1. Con Cliente
- **Relación**: Muchos a uno (N:1)
- **Tipo**: Asociación fuerte (pedido pertenece a cliente)
- **Navegabilidad**: Bidireccional

### 2. Con Almacenamiento
- **Relación**: Muchos a uno (N:1)
- **Tipo**: Asociación (origen de la entrega)
- **Validación**: Almacén debe estar operativo

### 3. Con Ruta
- **Relación**: Uno a uno (1:1)
- **Tipo**: Composición (ruta específica para el pedido)
- **Lifecycle**: Ruta se calcula cuando pedido está listo

### 4. Con Vértices
- **Origen**: Vértice de almacenamiento
- **Destino**: Vértice de cliente
- **Recarga**: Vértices intermedios si es necesario

## Integración con TDA

### HashMap de Pedidos
```python
# Acceso O(1) por ID
repositorio_pedidos.obtener_pedido(id_pedido)

# Búsqueda eficiente
pedidos_cliente = repositorio_pedidos.obtener_por_cliente(cliente_id)
```

### AVL de Rutas
```python
# Registro de ruta para estadísticas
avl_rutas.insertar(ruta.obtener_secuencia(), pedido)

# Consulta de rutas frecuentes
rutas_frecuentes = avl_rutas.obtener_mas_utilizadas()
```

### Grafo de Red
```python
# Validación de conectividad
if grafo.existe_camino(origen, destino):
    ruta = calcular_ruta(origen, destino)
    pedido.asignar_ruta(ruta)
```

## Casos de Uso Principales

### 1. Creación de Pedido
```
1. Cliente solicita entrega
2. Sistema valida datos (cliente activo, almacén disponible)
3. Se crea instancia de Pedido con estado PENDIENTE
4. Se registra en repositorio
5. Se notifica a observadores
6. Se programa para cálculo de ruta
```

### 2. Procesamiento de Pedido
```
1. Sistema selecciona pedido PENDIENTE
2. Calcula ruta óptima considerando autonomía
3. Asigna ruta al pedido
4. Cambia estado a EN_RUTA
5. Inicia simulación de entrega
6. Actualiza estadísticas
```

### 3. Completar Entrega
```
1. Dron llega al destino
2. Sistema verifica entrega exitosa
3. Marca pedido como ENTREGADO
4. Registra fecha de entrega
5. Calcula costo final
6. Actualiza estadísticas de cliente y rutas
7. Notifica al cliente
```

## Eventos y Observadores

### Eventos Generados
- `PedidoCreado`: Al crear nuevo pedido
- `RutaAsignada`: Al calcular y asignar ruta
- `EstadoCambiado`: Al cambiar estado del pedido
- `EntregaCompletada`: Al finalizar entrega exitosa
- `PedidoCancelado`: Al cancelar pedido

### Observadores Típicos
- **Auditoría**: Registra cambios para trazabilidad
- **Estadísticas**: Actualiza métricas de entregas
- **Notificaciones**: Informa al cliente sobre cambios
- **Dashboard**: Actualiza visualización en tiempo real

## Algoritmos de Cálculo

### Cálculo de Costo
```python
def calcular_costo_total(self) -> float:
    """
    Costo = CostoBase + (Distancia * CostoPorKm) + 
            (Peso * CostoPorKg) + (Prioridad * Multiplicador)
    """
    if not self._ruta_asignada:
        return 0.0
    
    costo_base = 1000  # CLP
    costo_distancia = self._ruta_asignada.obtener_costo_total() * 50
    costo_peso = self._peso * 100
    multiplicador_prioridad = {
        PrioridadPedido.BAJA: 1.0,
        PrioridadPedido.MEDIA: 1.2,
        PrioridadPedido.ALTA: 1.5,
        PrioridadPedido.CRITICA: 2.0
    }
    
    costo_total = costo_base + costo_distancia + costo_peso
    return costo_total * multiplicador_prioridad[self._prioridad]
```

### Validación de Entregabilidad
```python
def es_entregable(self) -> bool:
    """Verifica si el pedido puede ser procesado"""
    if self._estado != EstadoPedido.PENDIENTE:
        return False
    
    if not self._cliente.activo:
        return False
    
    if not self._almacenamiento_origen.operativo:
        return False
    
    # Verificar conectividad en el grafo
    grafo = obtener_grafo_red()
    return grafo.existe_camino(
        self._almacenamiento_origen.id_almacenamiento,
        self._cliente.id_cliente
    )
```

## Consideraciones de Rendimiento

### 1. Gestión Eficiente
- **Acceso**: O(1) por ID mediante HashMap
- **Búsquedas**: Indexación por cliente, estado, fecha
- **Memoria**: Referencias directas a objetos relacionados

### 2. Cálculos Optimizados
- **Costo**: Calculado on-demand y cacheado
- **Rutas**: Reutilización de rutas frecuentes
- **Validaciones**: Evaluación lazy de condiciones

### 3. Escalabilidad
- **Volumen**: Soporte para miles de pedidos simultáneos
- **Concurrencia**: Preparado para procesamiento paralelo
- **Distribución**: Estructura compatible con sistemas distribuidos

## Ejemplos de Uso

### Creación Completa
```python
# Crear pedido
pedido = Pedido(
    id_pedido="PED001",
    cliente=cliente_juan,
    almacenamiento_origen=almacen_central,
    descripcion="Documentos urgentes",
    peso=0.5,
    prioridad=PrioridadPedido.ALTA
)

# Procesar pedido
if pedido.es_entregable():
    ruta = calcular_ruta_optima(pedido)
    pedido.asignar_ruta(ruta)
    pedido.iniciar_procesamiento()
```

### Consultas Comunes
```python
# Verificar estado
if pedido.estado == EstadoPedido.EN_RUTA:
    print(f"Pedido {pedido.id_pedido} en proceso de entrega")

# Calcular tiempo
tiempo = pedido.tiempo_desde_creacion()
if tiempo.days > 1:
    print("Pedido requiere atención prioritaria")

# Obtener información completa
resumen = pedido.obtener_resumen()
```

## Validaciones y Errores

### Excepciones Específicas
- `PedidoInvalidoError`: Datos de pedido inválidos
- `EstadoInvalidoError`: Transición de estado no permitida
- `RutaNoAsignadaError`: Operación requiere ruta asignada
- `ClienteInactivoError`: Cliente no puede recibir pedidos
- `AlmacenNoOperativoError`: Almacén no disponible

### Validaciones de Integridad
- **Consistencia**: Estado coherente con ruta y fechas
- **Referencias**: Cliente y almacén deben existir
- **Temporales**: Fechas lógicas y secuenciales
- **Negocio**: Reglas específicas del dominio

## Testing y Calidad

### Pruebas Unitarias
- Creación y validación de pedidos
- Transiciones de estado
- Cálculos de costo
- Gestión de rutas

### Pruebas de Integración
- Flujo completo de entrega
- Integración con repositorios
- Eventos y observadores

### Casos de Prueba BDD
```gherkin
Escenario: Crear pedido válido
  Dado un cliente activo "Juan Pérez"
  Y un almacén operativo "Almacén Central"
  Cuando se crea un pedido con descripción "Documentos"
  Entonces el pedido debe estar en estado "PENDIENTE"
  Y debe estar asociado al cliente correcto
```

Este componente es crucial para el sistema ya que representa la unidad de trabajo principal y coordina todas las operaciones de entrega del sistema logístico.

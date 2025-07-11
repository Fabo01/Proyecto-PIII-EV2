# Documentación del Componente Cliente

## Descripción General
El componente `Cliente` representa una entidad fundamental del sistema que actúa como punto de destino para las entregas de drones. Los clientes mantienen información personal, ubicación en la red y una gestión completa de sus pedidos asociados.

## Ubicación en la Arquitectura
- **Capa de Dominio**: `Backend/Dominio/Dominio_Cliente.py`
- **Patrón**: Entidad de dominio rica con lógica de negocio
- **Responsabilidad**: Gestión de datos del cliente y coordinación de pedidos

## Estructura de la Clase

### Atributos Principales
```python
class Cliente:
    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        self._id_cliente: str           # Identificador único del cliente
        self._nombre: str               # Nombre completo del cliente
        self._email: str                # Correo electrónico para notificaciones
        self._telefono: str             # Teléfono de contacto
        self._pedidos: List[Pedido]     # Lista de pedidos asociados al cliente
        self._fecha_registro: datetime  # Fecha de registro en el sistema
        self._activo: bool             # Estado del cliente en el sistema
```

### Propiedades de Solo Lectura
- `id_cliente`: Identificador inmutable del cliente
- `nombre`: Nombre del cliente
- `email`: Correo electrónico
- `telefono`: Teléfono de contacto
- `fecha_registro`: Fecha de registro
- `activo`: Estado de actividad

### Propiedades de Gestión
- `pedidos`: Lista de pedidos del cliente (solo lectura)
- `total_pedidos`: Contador de pedidos asociados

## Funcionalidades Principales

### 1. Gestión de Pedidos
```python
def agregar_pedido(self, pedido: Pedido) -> bool:
    """Asocia un nuevo pedido al cliente"""
    
def quitar_pedido(self, id_pedido: str) -> bool:
    """Remueve un pedido específico del cliente"""
    
def obtener_pedido(self, id_pedido: str) -> Optional[Pedido]:
    """Busca un pedido específico por ID"""
    
def listar_pedidos_por_estado(self, estado: EstadoPedido) -> List[Pedido]:
    """Filtra pedidos por estado específico"""
```

### 2. Consultas y Estadísticas
```python
def tiene_pedidos_pendientes(self) -> bool:
    """Verifica si el cliente tiene pedidos sin completar"""
    
def calcular_total_gastado(self) -> float:
    """Calcula el total gastado en pedidos completados"""
    
def obtener_pedido_mas_reciente(self) -> Optional[Pedido]:
    """Retorna el pedido más recientemente creado"""
```

### 3. Gestión de Estado
```python
def activar(self) -> None:
    """Activa el cliente en el sistema"""
    
def desactivar(self) -> None:
    """Desactiva el cliente (no elimina datos)"""
    
def actualizar_informacion(self, nombre: str = None, email: str = None, 
                          telefono: str = None) -> bool:
    """Actualiza información personal del cliente"""
```

## Reglas de Negocio

### 1. Unicidad
- Cada cliente tiene un ID único e inmutable
- No pueden existir dos clientes con el mismo ID
- El email debe ser único en el sistema (validado a nivel de servicio)

### 2. Gestión de Pedidos
- Un cliente puede tener múltiples pedidos
- Los pedidos se mantienen históricamente (no se eliminan)
- Solo se pueden agregar pedidos válidos (con ID y estado definido)

### 3. Estados de Cliente
- **Activo**: Puede recibir nuevos pedidos
- **Inactivo**: No puede recibir nuevos pedidos, mantiene historial

### 4. Validaciones
- El nombre no puede estar vacío
- El email debe tener formato válido
- El teléfono debe tener formato válido
- Los pedidos asociados deben pertenecer al cliente

## Relaciones con Otros Componentes

### 1. Con Pedido
- **Relación**: Uno a muchos (1:N)
- **Tipo**: Composición (el cliente gestiona sus pedidos)
- **Navegabilidad**: Bidireccional

### 2. Con Vértice
- **Relación**: Uno a uno (1:1) cuando actúa como destino
- **Tipo**: Asociación (el cliente puede estar asociado a un vértice de la red)
- **Uso**: El cliente es el destino de entregas en vértices tipo "Cliente"

### 3. Con Repositorio de Clientes
- **Relación**: Gestionado por
- **Tipo**: Repositorio maneja persistencia y consultas
- **Acceso**: O(1) mediante HashMap

## Casos de Uso Principales

### 1. Registro de Cliente
```
1. Sistema valida datos del cliente
2. Se crea instancia de Cliente
3. Se registra en repositorio con HashMap
4. Se asocia a vértice de la red (si corresponde)
```

### 2. Creación de Pedido
```
1. Cliente recibe solicitud de pedido
2. Se valida que el cliente esté activo
3. Se crea pedido asociado al cliente
4. Se agrega a la lista de pedidos del cliente
5. Se notifica a observadores del sistema
```

### 3. Consulta de Historial
```
1. Sistema solicita pedidos del cliente
2. Cliente filtra por criterios (estado, fecha, etc.)
3. Retorna lista de pedidos coincidentes
4. Frontend muestra historial organizado
```

## Integración con TDA

### HashMap de Clientes
- **Acceso**: O(1) por ID de cliente
- **Gestión**: Repositorio mantiene instancias únicas
- **Búsqueda**: Eficiente para operaciones frecuentes

### AVL de Rutas
- **Conexión**: Los pedidos del cliente se registran en rutas
- **Frecuencia**: Clientes frecuentes generan rutas recurrentes
- **Optimización**: Sistema aprende patrones de entrega

## Eventos y Observadores

### Eventos Generados
- `ClienteCreado`: Al registrar nuevo cliente
- `ClienteActualizado`: Al modificar información
- `ClienteDesactivado`: Al cambiar estado
- `PedidoAgregado`: Al asociar nuevo pedido

### Observadores Típicos
- **Auditoría**: Registra cambios para trazabilidad
- **Estadísticas**: Actualiza métricas de clientes
- **Notificaciones**: Envía confirmaciones al cliente

## Consideraciones de Rendimiento

### 1. Gestión de Memoria
- Lista de pedidos se mantiene en memoria
- Para clientes con muchos pedidos, considerar paginación
- Referencias directas evitan búsquedas costosas

### 2. Consultas Optimizadas
- Búsqueda de pedidos por estado: O(n) en lista
- Acceso a cliente por ID: O(1) en HashMap
- Estadísticas calculadas on-demand

### 3. Escalabilidad
- Soporte para miles de clientes
- Estructura preparada para persistencia futura
- Separación clara facilita distribución

## Ejemplos de Uso

### Creación de Cliente
```python
cliente = Cliente(
    id_cliente="CLI001",
    nombre="Juan Pérez",
    email="juan.perez@email.com",
    telefono="+56912345678"
)
```

### Gestión de Pedidos
```python
# Agregar pedido
pedido = Pedido(id_pedido="PED001", cliente=cliente, ...)
cliente.agregar_pedido(pedido)

# Consultar pedidos pendientes
pendientes = cliente.listar_pedidos_por_estado(EstadoPedido.PENDIENTE)

# Verificar actividad
if cliente.tiene_pedidos_pendientes():
    print(f"Cliente {cliente.nombre} tiene pedidos pendientes")
```

### Estadísticas
```python
# Total gastado
total = cliente.calcular_total_gastado()

# Pedido más reciente
ultimo = cliente.obtener_pedido_mas_reciente()

# Cantidad de pedidos
cantidad = cliente.total_pedidos
```

## Validaciones y Errores

### Validaciones de Entrada
- **ID**: No vacío, formato válido
- **Nombre**: No vacío, longitud mínima/máxima
- **Email**: Formato válido, único en sistema
- **Teléfono**: Formato válido para el país

### Manejo de Errores
- `ClienteInvalidoError`: Datos de cliente inválidos
- `PedidoNoEncontradoError`: Pedido no existe en cliente
- `ClienteInactivoError`: Operación en cliente inactivo
- `EmailDuplicadoError`: Email ya registrado

## Testing y Calidad

### Pruebas Unitarias
- Creación y validación de clientes
- Gestión de pedidos (agregar, quitar, buscar)
- Cálculos de estadísticas
- Manejo de estados

### Pruebas de Integración
- Integración con repositorio
- Eventos y observadores
- Validaciones de negocio

### Métricas de Calidad
- Cobertura de código > 90%
- Complejidad ciclomática baja
- Documentación completa

Este componente es fundamental para el sistema ya que representa la entidad central del negocio y mantiene la integridad de los datos relacionados con los clientes y sus pedidos.

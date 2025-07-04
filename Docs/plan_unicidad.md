# Plan de Refactorización Integral: Unicidad, Hashmaps y TDA

## Contexto y Problemática

El sistema actual presenta errores de serialización (`PydanticSerializationError`) porque los repositorios guardan objetos reales con relaciones complejas (como `Pedido` con objetos `Cliente`, `Vertice`, etc.), pero cuando estos objetos se exponen a través de la API, Pydantic no puede serializarlos directamente. Siempre prioriza refactorizar los archivos existentes antes de crear archivos nuevos.

La solución requiere una refactorización completa que implemente tres capas claramente separadas:
1. **Repositorios**: Almacenan objetos reales con relaciones reales para garantizar unicidad y acceso O(1)
2. **Mapeadores**: Convierten objetos de dominio a diccionarios planos serializables
3. **DTOs**: Reciben solo datos planos (diccionarios) listos para consumir en la API

## Arquitectura Objetivo

```
[Dominio] → [Repositorios con HashMap] → [Mapeadores] → [DTOs] → [API]
    ↓              ↓                        ↓           ↓        ↓
Objetos reales  Unicidad O(1) con      Dicts planos   Pydantic  JSON
    ↓              objetos reales
```

## Entidades del Sistema (7 objetos principales)

1. **Cliente** (`Dominio_Cliente.py`)
2. **Pedido** (`Dominio_Pedido.py`) 
3. **Almacenamiento** (`Dominio_Almacenamiento.py`)
4. **Recarga** (`Dominio_Recarga.py`)
5. **Vertice** (`TDA_Vertice.py`)
6. **Arista** (`TDA_Arista.py`)
7. **Ruta** (`Dominio_Ruta.py`)

---

## FASE 1: AUDITORÍA Y ANÁLISIS DEL ESTADO ACTUAL

### Paso 1.1: Inventario de Repositorios Existentes
- [ ] Revisar `Backend/Infraestructura/Repositorios/`
- [ ] Listar todos los repositorios implementados:
  - `repositorio_clientes.py`
  - `repositorio_pedidos.py`
  - `repositorio_almacenamientos.py`
  - `repositorio_recargas.py`
  - `repositorio_vertices.py`
  - `repositorio_aristas.py`
  - `repositorio_rutas.py`
- [ ] Verificar que todos implementen `IntRepos/IRepositorio`, si es necesario refactorizar la interfaz, hazlo.
- [ ] Documentar métodos implementados vs. faltantes
- [ ] Verificar que todos los repositorios usen `TDA_Hash_map` para unicidad y acceso O(1)
- [ ] Verificar que todos los repositorios mantengan referencias de los objetos reales y sus atributos, no solo IDs.
- [ ] Verificar que todos los repositorios asocien correctamente las relaciones entre objetos, manteniendo referencias del objeto real y sus atributos, no solo IDs.

### Paso 1.2: Inventario de Mapeadores Existentes
- [ ] Revisar `Backend/API/Mapeadores/`
- [ ] Listar todos los mapeadores implementados:
  - `MapeadorCliente.py`
  - `MapeadorPedido.py`
  - `MapeadorAlmacenamiento.py`
  - `MapeadorRecarga.py`
  - `MapeadorVertice.py`
  - `MapeadorArista.py`
  - `MapeadorRuta.py`
  - `MapeadorSimulacion.py`
  - `MapeadorSnapshot.py`
- [ ] Verificar que todos implementen `IntMapeadores/IMapeador`, refactorizar si es necesario.
- [ ] Documentar métodos implementados vs. faltantes
- [ ] Verificar que todos los mapeadores implementen `a_dto()` y `a_hashmap()` de manera correcta, evitando ciclos y referencias profundas.
- [ ] Verificar las implementaciones de `a_dto()` y `a_hashmap()` retornen datos planos y objetos reales respectivamente.
- [ ] Verificar que todos los mapeadores manejen correctamente las relaciones entre objetos, manteniendo referencias del objeto real y sus atributos, no solo IDs para los hashmaps y referencias a los datos planos para los dtos.

### Paso 1.3: Inventario de DTOs Existentes
- [ ] Revisar `Backend/API/DTOs/DTOsRespuesta/`
- [ ] Listar todos los DTOs implementados:
  - `RespuestaCliente.py`
  - `RespuestaPedido.py`
  - `RespuestaAlmacenamiento.py`
  - `RespuestaRecarga.py`
  - `RespuestaVertice.py`
  - `RespuestaArista.py`
  - `RespuestaRuta.py`
  - `RespuestaHashMap.py`
- [ ] Verificar que todos campos de relaciones sean `Optional[Dict[str, Any]]`
- [ ] Verifica todos los archivos Respuesta* y considera refactorizar si es necesario.
- [ ] Verificar que todos los DTOs implementen `BaseModel` de Pydantic, considera refactorizar si es necesario.
- [ ] Verificar que los DTOs referencien datos planos y que no tengan referencias circulares

---

---

## FASE 2: REFACTORIZACIÓN DE REPOSITORIOS

### Paso 2.1: RepositorioClientes
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_clientes.py`

- [ ] **Verificar unicidad**: Método `agregar()` debe verificar si `cliente.id_cliente` ya existe
- [ ] **HashMap interno**: Asegurar que usa `TDA_Hash_map` correctamente
- [ ] **Método obtener_hashmap()**: Debe retornar `Dict[int, Cliente]` con objetos reales
- [ ] **Logging**: Agregar logging detallado en operaciones CRUD
- [ ] **Observadores**: Notificar en todas las operaciones
- [ ] **Verificar relaciones**: Cliente debe mantener lista de pedidos como objetos reales

### Paso 2.2: RepositorioPedidos (Ya parcialmente refactorizado)
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_pedidos.py`

- [ ] **Verificar método obtener_hashmap()**: Debe retornar `Dict[int, Pedido]` con objetos reales
- [ ] **Verificar método obtener_hashmap_serializable()**: Debe usar `MapeadorPedido.a_hashmap()`
- [ ] **Relaciones**: Pedido debe mantener referencias reales a Cliente, Vertice origen, Vertice destino
- [ ] **Logging detallado**: Ya implementado, verificar funcionamiento
- [ ] **IRepositorioSerializable**: Ya implementado, verificar métodos

### Paso 2.3: RepositorioAlmacenamientos
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_almacenamientos.py`

- [ ] **Agregar método obtener_hashmap_serializable()**: Usar `MapeadorAlmacenamiento.a_hashmap()`
- [ ] **Implementar IRepositorioSerializable**: Extender interfaz
- [ ] **Verificar unicidad**: Por `almacenamiento.id_almacenamiento`
- [ ] **Logging**: Agregar logging detallado
- [ ] **Relaciones**: Almacenamiento puede tener pedidos asociados

### Paso 2.4: RepositorioRecargas
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_recargas.py`

- [ ] **Agregar método obtener_hashmap_serializable()**: Usar `MapeadorRecarga.a_hashmap()`
- [ ] **Implementar IRepositorioSerializable**: Extender interfaz
- [ ] **Verificar unicidad**: Por `recarga.id_recarga`
- [ ] **Logging**: Agregar logging detallado

### Paso 2.5: RepositorioVertices
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_vertices.py`

- [ ] **Agregar método obtener_hashmap_serializable()**: Usar `MapeadorVertice.a_hashmap()`
- [ ] **Verificar clave**: Usa `id_elemento` como clave, debe ser consistente
- [ ] **Relaciones**: Vertice debe mantener referencia real al elemento (`Cliente`, `Almacenamiento`, `Recarga`)
- [ ] **Logging**: Agregar logging detallado

### Paso 2.6: RepositorioAristas
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_aristas.py`

- [ ] **Refactorizar método a_hashmap_serializable()**: Usar `MapeadorArista.a_hashmap()`
- [ ] **Verificar clave**: Debe ser consistente (ej: `"origen_id-destino_id"`)
- [ ] **Relaciones**: Arista debe mantener referencias reales a Vertice origen y destino
- [ ] **Logging**: Ya implementado, verificar funcionamiento

### Paso 2.7: RepositorioRutas
**Archivo**: `Backend/Infraestructura/Repositorios/repositorio_rutas.py`

- [ ] **Agregar método obtener_hashmap_serializable()**: Usar `MapeadorRuta.a_hashmap()`
- [ ] **Implementar IRepositorioSerializable**: Extender interfaz
- [ ] **Verificar unicidad**: Por `ruta.id_ruta` o clave compuesta
- [ ] **Relaciones**: Ruta debe mantener lista de vertices/aristas reales
- [ ] **Logging**: Agregar logging detallado

---

## FASE 3: REFACTORIZACIÓN DE MAPEADORES

### Paso 3.1: MapeadorCliente
**Archivo**: `Backend/API/Mapeadores/MapeadorCliente.py`

- [ ] **Método a_dto()**: 
  - Recibe objeto `Cliente` del dominio
  - Convierte pedidos asociados usando `MapeadorPedido.a_hashmap()` (NO `a_dto()` para evitar ciclos)
  - Retorna `RespuestaCliente` con campos planos
- [ ] **Método a_hashmap()**:
  - Convierte Cliente a dict plano: `{'id_cliente', 'nombre', 'tipo_elemento', 'pedidos': [list_of_dicts]}`
  - No debe hacer llamadas recursivas profundas
- [ ] **Manejo de relaciones**: Lista de pedidos como lista de dicts, no objetos Pedido

### Paso 3.2: MapeadorPedido (Ya parcialmente refactorizado)
**Archivo**: `Backend/API/Mapeadores/MapeadorPedido.py`

- [ ] **Método a_dto()**: Ya implementado, verificar que funcione
- [ ] **Método a_hashmap()**: Ya implementado, verificar que:
  - Cliente se serializa como dict plano
  - Origen (Vertice) se serializa como dict plano
  - Destino (Vertice) se serializa como dict plano
  - Ruta se serializa como dict plano (si existe)
- [ ] **Sin ciclos**: No debe llamar recursivamente a mapeadores que retornen DTOs

### Paso 3.3: MapeadorAlmacenamiento
**Archivo**: `Backend/API/Mapeadores/MapeadorAlmacenamiento.py`

- [ ] **Revisar método a_dto()**: Debe manejar pedidos asociados sin ciclos
- [ ] **Revisar método a_hashmap()**: Ya implementado, verificar funcionamiento
- [ ] **Relaciones**: Pedidos asociados como lista de IDs o dicts planos

### Paso 3.4: MapeadorRecarga
**Archivo**: `Backend/API/Mapeadores/MapeadorRecarga.py`

- [ ] **Revisar método a_dto()**: Verificar campos necesarios
- [ ] **Revisar método a_hashmap()**: Ya implementado, verificar funcionamiento
- [ ] **Sin relaciones complejas**: Recarga es entidad simple

### Paso 3.5: MapeadorVertice
**Archivo**: `Backend/API/Mapeadores/MapeadorVertice.py`

- [ ] **Revisar método a_dto()**: Debe serializar el elemento asociado (Cliente/Almacenamiento/Recarga)
- [ ] **Método a_hashmap()**:
  - Serializar elemento asociado como dict plano
  - Incluir tipo de elemento
  - No exponer estructura interna del Vertice
- [ ] **Manejo de tipos**: Detectar tipo de elemento correctamente

### Paso 3.6: MapeadorArista
**Archivo**: `Backend/API/Mapeadores/MapeadorArista.py`

- [ ] **Crear si no existe** o **revisar método a_dto()**: 
  - Debe serializar origen y destino como dicts planos
  - Incluir peso y otros atributos
- [ ] **Método a_hashmap()**:
  - Serializar vertices origen/destino sin recursión profunda
  - Peso como valor numérico
- [ ] **Evitar ciclos**: Vertices como dicts simples con IDs

### Paso 3.7: MapeadorRuta
**Archivo**: `Backend/API/Mapeadores/MapeadorRuta.py`

- [ ] **Revisar método a_dto()**: Ya implementado, verificar funcionamiento
- [ ] **Método a_hashmap()**:
  - Lista de vertices como dicts planos
  - Lista de aristas como dicts planos
  - Sin recursión profunda en relaciones
- [ ] **Estructura**: Ruta debe ser serializable como lista ordenada

---

## FASE 4: REFACTORIZACIÓN DE DTOs

### Paso 4.1: RespuestaCliente
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaCliente.py`

- [ ] **Verificar campos**:
  ```python
  id_cliente: int
  nombre: str
  tipo_elemento: str
  pedidos: Optional[List[Dict[str, Any]]] = None  # Lista de dicts, NO objetos
  ```
- [ ] **Asegurar que todos los campos de relaciones sean Dict o List[Dict]**

### Paso 4.2: RespuestaPedido (Ya refactorizado)
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaPedido.py`

- [ ] **Verificar campos**: Ya correcto, todos como `Optional[Dict[str, Any]]`
- [ ] **Validar funcionamiento**: Debe recibir dicts planos del mapeador

### Paso 4.3: RespuestaAlmacenamiento
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaAlmacenamiento.py`

- [ ] **Verificar campos de relaciones**:
  ```python
  pedidos: Optional[List[Dict[str, Any]]] = None  # Si tiene pedidos asociados
  ```

### Paso 4.4: RespuestaRecarga
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaRecarga.py`

- [ ] **Verificar campos**: Entidad simple, no debería tener relaciones complejas

### Paso 4.5: RespuestaVertice
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaVertice.py`

- [ ] **Verificar campos**:
  ```python
  elemento: Optional[Dict[str, Any]] = None  # Cliente/Almacenamiento/Recarga serializado
  tipo_elemento: str
  ```

### Paso 4.6: RespuestaArista
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaArista.py`

- [ ] **Verificar campos**:
  ```python
  origen: Optional[Dict[str, Any]] = None  # Vertice origen serializado
  destino: Optional[Dict[str, Any]] = None  # Vertice destino serializado
  peso: float
  ```

### Paso 4.7: RespuestaRuta
**Archivo**: `Backend/API/DTOs/DTOsRespuesta/RespuestaRuta.py`

- [ ] **Verificar campos**:
  ```python
  vertices: Optional[List[Dict[str, Any]]] = None
  aristas: Optional[List[Dict[str, Any]]] = None
  ```

---

## FASE 5: INTEGRACIÓN EN ENDPOINTS

### Paso 5.1: Refactorizar Endpoints de Clientes
**Archivo**: `Backend/API/clientes_enrutador.py`

- [ ] **Endpoint GET /clientes/**: 
  ```python
  clientes = service.obtener_clientes()  # Objetos reales
  return [MapeadorCliente.a_dto(c) for c in clientes]  # DTOs
  ```
- [ ] **Endpoint GET /clientes/hashmap**: 
  ```python
  return {"hashmap": service.obtener_clientes_hashmap_serializable()}  # Dict plano
  ```
- [ ] **Endpoint GET /clientes/{id}**: 
  ```python
  cliente = service.obtener_cliente(id)  # Objeto real
  return MapeadorCliente.a_dto(cliente)  # DTO
  ```

### Paso 5.2: Refactorizar Endpoints de Pedidos
**Archivo**: `Backend/API/pedidos_enrutador.py`

- [ ] **Verificar que ya usa repositorio serializable** ✓ (Ya implementado)
- [ ] **Verificar que usa MapeadorPedido.a_dto()** ✓ (Ya implementado)

### Paso 5.3: Refactorizar Endpoints de Almacenamientos
**Archivo**: `Backend/API/almacenamientos_enrutador.py`

- [ ] **Verificar patrón consistente**: Repositorio → Mapeador → DTO
- [ ] **Endpoint /hashmap**: Debe usar método serializable del repositorio

### Paso 5.4: Refactorizar Endpoints de Recargas
**Archivos**: `Backend/API/recargas_enrutador.py` o en `simulacion_endpoints_enrutador.py`

- [ ] **Aplicar patrón consistente**: Repositorio → Mapeador → DTO

### Paso 5.5: Refactorizar Endpoints de Vertices
**Archivo**: `Backend/API/vertices_enrutador.py`

- [ ] **Verificar serialización de elementos**: Usar `MapeadorVertice.a_hashmap()`

### Paso 5.6: Refactorizar Endpoints de Aristas
**Archivo**: `Backend/API/aristas_enrutador.py`

- [ ] **Verificar que usa MapeadorArista** (revisar si existe)
- [ ] **Eliminar lógica de serialización manual**: Ya implementado parcialmente

### Paso 5.7: Refactorizar Endpoints de Rutas
**Archivos**: `Backend/API/rutas_enrutador.py` o en `simulacion_endpoints_enrutador.py`

- [ ] **Aplicar patrón consistente**: Repositorio → Mapeador → DTO

---

## FASE 6: INTEGRACIÓN CON SERVICIOS DE APLICACIÓN

### Paso 6.1: Simulacion_dominio.py
**Archivo**: `Backend/Dominio/Simulacion_dominio.py`

- [ ] **Propiedad hashmaps**: Debe retornar objetos reales de repositorios
- [ ] **Métodos obtener_*_hashmap()**: Delegar a repositorios, objetos reales
- [ ] **Métodos obtener_*_hashmap_serializable()**: Nuevos métodos que usen mapeadores

### Paso 6.2: Aplicacion_Simulacion.py
**Archivo**: `Backend/Aplicacion/SimAplicacion/Aplicacion_Simulacion.py`

- [ ] **Implementar métodos *_hashmap_serializable()**: Delegar a simulacion_dominio
- [ ] **Mantener métodos que retornan objetos reales**: Para uso interno
- [ ] **Separar claramente**: Métodos para dominio vs. métodos para API

### Paso 6.3: Servicios_Simulacion.py
**Archivo**: `Backend/Servicios/SimServicios/Servicios_Simulacion.py`
- [ ] **Implementar métodos *_hashmap_serializable()**: Delegar a Aplicacion_Simulacion
- [ ] **Mantener métodos que retornan objetos reales**: Para uso interno
- [ ] **Separar claramente**: Métodos para dominio vs. métodos para API


---

## FASE 8: TESTS Y VALIDACIÓN

### Paso 8.1: Tests de Repositorios
- [ ] **Test unicidad**: Agregar mismo objeto dos veces, verificar que retorna existente
- [ ] **Test HashMap**: Verificar acceso O(1)
- [ ] **Test serialización**: Verificar que `obtener_hashmap_serializable()` funciona
- [ ] **Test relaciones**: Verificar que objetos mantienen referencias reales

### Paso 8.2: Tests de Mapeadores
- [ ] **Test a_dto()**: Objeto dominio → DTO válido
- [ ] **Test a_hashmap()**: Objeto dominio → Dict plano serializable
- [ ] **Test sin ciclos**: Verificar que no hay recursión infinita
- [ ] **Test JSON**: Verificar que dict resultante es serializable a JSON

### Paso 8.3: Tests de DTOs
- [ ] **Test Pydantic**: Verificar que DTOs se crean correctamente con dicts planos
- [ ] **Test serialización**: DTO → JSON sin errores
- [ ] **Test validación**: Campos obligatorios y opcionales

### Paso 8.4: Tests de Integración
- [ ] **Test endpoint completo**: Request → Dominio → Repositorio → Mapeador → DTO → JSON
- [ ] **Test hashmap endpoint**: Verificar que retorna dict serializable
- [ ] **Test relaciones**: Verificar que relaciones se mantienen correctamente

---

## FASE 9: DOCUMENTACIÓN Y LIMPIEZA

### Paso 9.1: Documentación Técnica
- [ ] **Actualizar README**: Explicar nueva arquitectura
- [ ] **Documentar patrones**: Repositorio → Mapeador → DTO
- [ ] **Documentar interfaces**: IRepositorio, IMapeadorDominioDTO
- [ ] **Ejemplos de uso**: Código ejemplo para cada patrón

### Paso 9.2: Limpieza de Código Legacy
- [ ] **Eliminar serialización manual**: En endpoints que la tengan
- [ ] **Unificar logging**: Patrón consistente en todos los módulos
- [ ] **Revisar imports**: Eliminar imports no utilizados
- [ ] **Verificar convenciones**: snake_case, español, sin acentos

---

## CRITERIOS DE ÉXITO

### ✅ Funcionalidad
- [ ] Todos los endpoints retornan JSON válido sin errores de serialización
- [ ] Hashmaps contienen objetos reales para uso interno
- [ ] Hashmaps serializables contienen dicts planos para API
- [ ] Relaciones entre objetos se mantienen correctamente

### ✅ Rendimiento
- [ ] Acceso O(1) a entidades mediante HashMap
- [ ] Sin duplicación de objetos (unicidad garantizada)
- [ ] Serialización eficiente sin recursión excesiva

### ✅ Mantenibilidad
- [ ] Separación clara de responsabilidades
- [ ] Interfaces bien definidas
- [ ] Código modular y escalable
- [ ] Logging detallado para debugging

### ✅ Compatibilidad
- [ ] Convenciones en español mantenidas
- [ ] Sin acentos en nombres de variables/funciones
- [ ] Compatibilidad con arquitectura hexagonal
- [ ] Tests pasan completamente

---

## ORDEN DE EJECUCIÓN RECOMENDADO

1. **FASES 1-2**: Auditoría e interfaces (fundación)
2. **FASE 3**: Repositorios (capa de datos)
3. **FASE 4**: Mapeadores (capa de transformación)
4. **FASE 5**: DTOs (capa de presentación)
5. **FASES 6-7**: Integración (endpoints y servicios)
6. **FASES 8-9**: Tests y documentación

Cada fase debe completarse antes de continuar con la siguiente para evitar errores en cascada.

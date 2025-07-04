# Plan de Refactorización: Unicidad, Repositorios, Mapeadores y DTOs

## Objetivo General
Implementar un patrón arquitectónico cohesivo que garantice:
1. **Unicidad de objetos** mediante HashMap en repositorios con acceso O(1)
2. **Relaciones reales** entre objetos de dominio (no IDs sueltos)
3. **Mapeo seguro** de objetos complejos a DTOs serializables
4. **Separación clara** entre capas de dominio, infraestructura y API
5. **Escalabilidad** y mantenimiento del sistema

## Problemática Actual
- Error de serialización de Pydantic: objetos complejos (`Pedido`, `Vertice`) no pueden ser serializados directamente
- Los repositorios devuelven objetos reales con relaciones, pero la API requiere datos planos
- Falta de patrón consistente para convertir objetos de dominio a DTOs
- Inconsistencias en el manejo de relaciones entre entidades

---

## FASE 1: Refactorización de Interfaces Base

### 1.1 Actualizar IMapeadorDominioDTO
**Archivo:** `Backend/Dominio/Interfaces/IntMapeadores/IMapeadorDominioDTO.py`
**Descripción:** Ampliar la interfaz base para incluir todos los métodos estándar de mapeo.

**Cambios requeridos:**
```python
@staticmethod
@abstractmethod
def a_dto(objeto_dominio, **kwargs):
    """Convierte objeto de dominio a DTO de respuesta"""
    pass

@staticmethod
@abstractmethod  
def a_hashmap(objeto_dominio):
    """Convierte objeto de dominio a dict plano serializable"""
    pass

@staticmethod
@abstractmethod
def lista_a_hashmap(lista_objetos):
    """Convierte lista de objetos de dominio a lista de dicts planos"""
    pass
```

### 1.2 Crear Interface IRepositorioSerializable
**Archivo:** `Backend/Dominio/Interfaces/IntRepos/IRepositorioSerializable.py` (nuevo)
**Descripción:** Extender IRepositorio para incluir métodos de serialización consistentes.

**Métodos requeridos:**
- `obtener_todos_serializables()` → dict plano para API
- `obtener_por_tipo(tipo_elemento)` → objetos filtrados por tipo
- `serializar_relaciones()` → mapeo de relaciones para frontend

---

## FASE 2: Refactorización de Repositorios

### 2.1 RepositorioPedidos
**Archivo:** `Backend/Infraestructura/Repositorios/repositorio_pedidos.py`

**Cambios específicos:**
1. **Mantener `obtener_hashmap()`** devolviendo objetos reales (como está)
2. **Agregar método `obtener_hashmap_serializable()`** que use mapeador
3. **Implementar `obtener_por_cliente(id_cliente)`** para consultas específicas
4. **Agregar validación de relaciones** en `agregar()`

**Código de referencia:**
```python
def obtener_hashmap_serializable(self):
    """Retorna hashmap serializado usando MapeadorPedido"""
    from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
    pedidos_dict = {}
    for id_pedido, pedido in self._pedidos.items():
        pedidos_dict[id_pedido] = MapeadorPedido.a_hashmap(pedido)
    return pedidos_dict

def obtener_por_cliente(self, id_cliente):
    """Obtiene todos los pedidos asociados a un cliente específico"""
    pedidos_cliente = []
    for pedido in self._pedidos.valores():
        if hasattr(pedido, 'cliente') and hasattr(pedido.cliente, 'id_cliente'):
            if pedido.cliente.id_cliente == id_cliente:
                pedidos_cliente.append(pedido)
    return pedidos_cliente
```

1.2. **Todos los repositorios deben implementar la interfaz `IRepositorio`** (`agregar`, `obtener`, `eliminar`, `todos`, `limpiar`, `obtener_hashmap`).

1.3. **Utilizar internamente `TDA_Hash_map`** para almacenar instancias, garantizando unicidad y acceso O(1) por ID real.

1.4. **Unicidad estricta**: Antes de agregar una entidad, verificar si ya existe por ID. Si existe, retornar la instancia existente; si no, agregar la nueva. Si se intenta agregar un duplicado, retornar la instancia original y notificar.

1.5. **Notificar a observadores** en cada operación relevante (alta, baja, modificación, limpieza) para trazabilidad y auditoría. Permitir la suscripción de observadores externos.

---

## 2. Relaciones Reales y Gestión de Asociaciones

2.1. **Al agregar un Pedido al repositorio**, asociar el objeto real de Cliente y Almacenamiento (no solo IDs). El Pedido debe contener referencias a los objetos reales.

2.2. **En Cliente y Almacenamiento**, mantener listas de objetos Pedido reales asociados (no solo IDs). Al agregar/eliminar un Pedido, actualizar la lista correspondiente.

2.3. **Asegurar que al consultar un Cliente o Almacenamiento**, se pueda acceder a sus pedidos como objetos completos (no solo IDs).

2.4. **En Recarga, Ruta, Arista y Vertice**, mantener referencias a los objetos reales relacionados según corresponda (por ejemplo, una Arista referencia los objetos Vertice reales).

2.5. **Evitar referencias circulares** en la lógica de dominio: los pedidos conocen a su cliente y origen, pero la gestión de pedidos está separada de Cliente y Almacenamiento.

---

## 3. Mapeadores: De Objeto Real a DTO Plano

3.1. **Cada entidad debe tener un mapeador dedicado** en `Backend/API/Mapeadores/`, implementando la interfaz `IMapeador`.

3.2. **El método `a_dto` debe convertir el objeto real a un DTO plano** (sin objetos anidados, solo IDs o listas de IDs para relaciones). Ejemplo: ClienteDTO, PedidoDTO, AlmacenamientoDTO, etc.

3.3. **Evitar recursividad y ciclos**: nunca incluir objetos anidados que puedan generar referencias circulares. Usar solo IDs o listas de IDs para relaciones.

3.4. **Permitir flags en los mapeadores** para incluir detalles adicionales solo si es estrictamente necesario y seguro.

3.5. **Mapear listas de objetos a listas de DTOs planos** usando métodos utilitarios en cada mapeador.

---

## 4. DTOs: Estructura Plana y Sin Recursividad

4.1. **Todos los DTOs deben ser planos**: solo atributos primitivos y listas de IDs. No incluir objetos anidados.

4.2. **Para relaciones, usar solo IDs o listas de IDs** (ejemplo: ClienteDTO tiene `ids_pedidos`, PedidoDTO tiene `id_cliente`, etc).

4.3. **DTOs deben estar en `Backend/API/DTOs/`** y ser utilizados exclusivamente para la comunicación con la API.

---

## 5. Serialización y Entrega a la API

5.1. **En los servicios de dominio**, obtener los objetos reales desde los repositorios.

5.2. **Mapear los objetos reales a DTOs planos** usando los mapeadores correspondientes.

5.3. **Entregar los DTOs serializados a la API** para su consumo por el frontend, asegurando que los datos sean planos y sin recursividad.

5.4. **Asegurar que toda la trazabilidad y relaciones reales se mantengan en memoria**, pero solo se expongan datos planos a la API.

---

## 6. Auditoría, Observabilidad y Trazabilidad

6.1. **Notificar a observadores** en cada operación relevante de los repositorios y entidades para auditoría y trazabilidad.

6.2. **Registrar logs de operaciones clave** (alta, baja, modificación, asociaciones) en los repositorios y entidades.

6.3. **Permitir la suscripción de observadores externos** (auditoría, visualización, etc.) a los repositorios y entidades.

---

## 7. Validación, Pruebas y Escalabilidad

7.1. **Implementar tests unitarios y de integración** para cada repositorio, mapeador y DTO, verificando unicidad, relaciones y mapeo correcto.

7.2. **Validar que no existan duplicados** en los repositorios y que las relaciones sean siempre a objetos reales.

7.3. **Asegurar que el sistema escale correctamente** hasta el máximo de entidades definido en los requisitos.

---

## 8. Convenciones y Buenas Prácticas

8.1. **Seguir las convenciones de código en español**: snake_case para variables y funciones, PascalCase para clases, sin acentos.

8.2. **Documentar todas las clases y funciones principales** con docstrings en español.

8.3. **Mantener la modularidad y separación de responsabilidades** en todos los módulos.

8.4. **Alinear todos los nombres, estructuras y validaciones** con lo especificado en `Docs/Requisitos.md` y la documentación técnica.

---

Este plan debe ser seguido rigurosamente para garantizar unicidad, trazabilidad, relaciones reales y entrega de datos planos a la API, cumpliendo con los requisitos y la arquitectura del sistema Correos Chile.

---

## FASE 2: Refactorización de Repositorios (continuación)

### 2.2 RepositorioClientes
**Archivo:** `Backend/Infraestructura/Repositorios/repositorio_clientes.py`

**Cambios específicos:**
1. **Validar unicidad** de clientes por `id_cliente`
2. **Gestionar relaciones con pedidos** correctamente
3. **Implementar método `agregar_pedido_a_cliente(id_cliente, pedido)`**
4. **Serialización** usando MapeadorCliente

### 2.3 RepositorioVertices  
**Archivo:** `Backend/Infraestructura/Repositorios/repositorio_vertices.py`

**Cambios específicos:**
1. **Garantizar unicidad por ID del elemento** (id_cliente, id_almacen, id_recarga)
2. **Validar tipo de elemento** antes de agregar
3. **Implementar filtros por tipo:** `obtener_por_tipo('cliente')`
4. **Serialización** que preserve información del elemento

### 2.4 Aplicar patrón similar a todos los repositorios
- RepositorioAlmacenamientos
- RepositorioRecargas  
- RepositorioRutas
- RepositorioAristas

---

## FASE 3: Refactorización de Mapeadores

### 3.1 MapeadorPedido
**Archivo:** `Backend/API/Mapeadores/MapeadorPedido.py`

**Refactorización requerida:**
1. **Reemplazar lógica de `pedido_a_dict`** del archivo creado anteriormente
2. **Implementar manejo robusto de relaciones**
3. **Evitar referencias circulares** con flags (`incluir_cliente`, `incluir_almacenamiento`)
4. **Logging detallado** de errores de mapeo

**Código de referencia:**
```python
@staticmethod
def a_hashmap(pedido):
    """Serializa pedido a dict plano con todas las relaciones como dicts"""
    try:
        cliente_dict = None
        if hasattr(pedido, 'cliente') and pedido.cliente:
            cliente_dict = {
                'id_cliente': getattr(pedido.cliente, 'id_cliente', None),
                'nombre': getattr(pedido.cliente, 'nombre', None),
                'tipo_elemento': getattr(pedido.cliente, 'tipo_elemento', None)
            }
        
        origen_dict = None
        if hasattr(pedido, 'origen') and pedido.origen:
            elemento = getattr(pedido.origen, 'elemento', None)
            if elemento:
                origen_dict = {
                    'id': getattr(elemento, 'id_almacenamiento', getattr(elemento, 'id_cliente', None)),
                    'nombre': getattr(elemento, 'nombre', None),
                    'tipo_elemento': getattr(elemento, 'tipo_elemento', None)
                }
        
        # Similar para destino, ruta...
        
        return {
            'id_pedido': getattr(pedido, 'id_pedido', None),
            'cliente': cliente_dict,
            'origen': origen_dict,
            'destino': destino_dict,
            'prioridad': getattr(pedido, 'prioridad', None),
            'status': getattr(pedido, 'status', None),
            'ruta': ruta_dict,
            'peso_total': getattr(pedido, 'peso_total', None),
            'fecha_creacion': str(getattr(pedido, 'fecha_creacion', '')),
            'fecha_entrega': str(getattr(pedido, 'fecha_entrega', '')) if getattr(pedido, 'fecha_entrega', None) else None
        }
    except Exception as e:
        MapeadorPedido.logger.error(f"Error serializando pedido: {e}")
        return {'id_pedido': getattr(pedido, 'id_pedido', None), 'error': str(e)}
```

### 3.2 MapeadorCliente
**Archivo:** `Backend/API/Mapeadores/MapeadorCliente.py`

**Refactorización requerida:**
1. **Gestionar lista de pedidos** como objetos completos
2. **Evitar recursión infinita** en `a_dto` con flag `incluir_pedidos`
3. **Implementar `a_hashmap`** que serialice pedidos como dicts simples

### 3.3 MapeadorVertice
**Archivo:** `Backend/API/Mapeadores/MapeadorVertice.py`

**Refactorización requerida:**
1. **Detectar tipo de elemento** automáticamente
2. **Extraer atributos reales** del elemento asociado
3. **Manejar casos edge:** elemento nulo, tipos desconocidos

### 3.4 Aplicar patrón consistente a todos los mapeadores
- MapeadorAlmacenamiento  
- MapeadorRecarga
- MapeadorRuta
- MapeadorArista

---

## FASE 4: Refactorización de DTOs de Respuesta

### 4.1 Validar estructura de RespuestaPedido
**Archivo:** `Backend/API/DTOs/DTOsRespuesta/RespuestaPedido.py`

**Estado actual:** ✅ Correcto (ya recibe Dict[str, Any] para relaciones)

**Verificaciones:**
- ✅ `cliente: Optional[Dict[str, Any]] = None`
- ✅ `origen: Optional[Dict[str, Any]] = None`  
- ✅ `destino: Optional[Dict[str, Any]] = None`
- ✅ `ruta: Optional[Dict[str, Any]] = None`

### 4.2 Actualizar otros DTOs de respuesta
**Archivos:** `Backend/API/DTOs/DTOsRespuesta/`

**Verificaciones requeridas:**
- `RespuestaCliente`: `pedidos: Optional[List[Dict[str, Any]]] = None`
- `RespuestaAlmacenamiento`: `pedidos: Optional[List[Dict[str, Any]]] = None`
- `RespuestaRuta`: campos de vertices como `Dict[str, Any]`

---

## FASE 5: Integración en Endpoints/Enrutadores

### 5.1 Patrón de uso en endpoints
**Ubicación:** `Backend/API/` (todos los enrutadores)

**Patrón estándar a implementar:**
```python
# ❌ MAL - Devolver objetos de dominio directamente
def obtener_pedidos():
    repo = RepositorioPedidos()
    pedidos = repo.todos()  # Objetos Pedido reales
    return pedidos  # ❌ Error de serialización

# ✅ BIEN - Usar mapeador antes de devolver
def obtener_pedidos():
    repo = RepositorioPedidos()
    pedidos = repo.todos()  # Objetos Pedido reales
    pedidos_dto = [MapeadorPedido.a_dto(p) for p in pedidos]
    return {"pedidos": pedidos_dto}

# ✅ ALTERNATIVA - Usar hashmap serializable directo
def obtener_pedidos_hashmap():
    repo = RepositorioPedidos()
    return {"pedidos": repo.obtener_hashmap_serializable()}
```

### 5.2 Actualizar endpoints específicos
**Archivos a modificar:**
- `pedidos_enrutador.py`
- `clientes_enrutador.py`
- `almacenamientos_enrutador.py`
- `vertices_enrutador.py`
- `rutas_enrutador.py`
- `simulacion_endpoints_enrutador.py`

**Cada endpoint debe:**
1. Obtener objetos reales del repositorio
2. Aplicar mapeador correspondiente  
3. Devolver DTOs serializables
4. Manejar errores de mapeo con try/catch

---

## FASE 6: Validación y Testing

### 6.1 Tests de repositorios
**Ubicación:** `Tests/`

**Verificaciones requeridas:**
1. **Unicidad:** Insertar mismo objeto dos veces debe devolver instancia existente
2. **Relaciones:** Pedido debe mantener referencias a objetos reales (Cliente, Vertice)
3. **Serialización:** `obtener_hashmap_serializable()` debe devolver dict válido

### 6.2 Tests de mapeadores  
**Verificaciones requeridas:**
1. **Mapeo a DTO:** Objeto real → DTO válido de Pydantic
2. **Mapeo a hashmap:** Objeto real → dict serializable JSON
3. **Manejo de nulos:** Relaciones nulas no deben causar errores
4. **Evitar recursión:** Flags deben prevenir referencias circulares

### 6.3 Tests de integración API
**Verificaciones requeridas:**
1. **Endpoints:** Respuestas deben ser JSON válido
2. **Consistencia:** Mismos datos en diferentes formatos
3. **Performance:** Acceso O(1) en consultas por ID

---

## FASE 7: Documentación y Limpieza

### 7.1 Actualizar documentación técnica
**Archivos a actualizar:**
- `Docs/relaciones.md`
- `Docs/negocio.md`  
- Docstrings en clases principales

### 7.2 Remover código obsoleto
**Archivos a revisar:**
- `mapeador_pedido.py` (archivo temporal creado)
- Métodos deprecados en repositorios
- DTOs no utilizados

### 7.3 Configurar logging consistente
**Configuración requerida:**
- Logger específico por mapeador
- Auditoria de operaciones en repositorios
- Tracking de errores de serialización

---

## Cronograma de Implementación

### Día 1: Interfaces y Repositorios Base
- [ ] 1.1 Actualizar IMapeadorDominioDTO  
- [ ] 1.2 Crear IRepositorioSerializable
- [ ] 2.1 Refactorizar RepositorioPedidos

### Día 2: Repositorios Restantes
- [ ] 2.2 Refactorizar RepositorioClientes
- [ ] 2.3 Refactorizar RepositorioVertices  
- [ ] 2.4 Aplicar patrón a otros repositorios

### Día 3: Mapeadores Críticos
- [ ] 3.1 Refactorizar MapeadorPedido
- [ ] 3.2 Refactorizar MapeadorCliente
- [ ] 3.3 Refactorizar MapeadorVertice

### Día 4: Mapeadores Restantes y DTOs
- [ ] 3.4 Refactorizar otros mapeadores
- [ ] 4.1-4.2 Validar y actualizar DTOs

### Día 5: Integración y Testing
- [ ] 5.1-5.2 Actualizar endpoints
- [ ] 6.1-6.3 Tests y validación
- [ ] 7.1-7.3 Documentación y limpieza

---

## Checklist de Verificación Final

### ✅ Repositorios
- [ ] Todos los repositorios garantizan unicidad con HashMap
- [ ] Método `obtener_hashmap()` devuelve objetos reales  
- [ ] Método `obtener_hashmap_serializable()` usa mapeadores
- [ ] Relaciones entre objetos son referencias reales (no IDs)

### ✅ Mapeadores  
- [ ] Todos implementan `IMapeadorDominioDTO`
- [ ] Método `a_dto()` produce DTOs válidos de Pydantic
- [ ] Método `a_hashmap()` produce dicts serializables JSON
- [ ] Flags previenen referencias circulares

### ✅ DTOs
- [ ] Campos de relaciones son `Dict[str, Any]` o `List[Dict[str, Any]]`
- [ ] No contienen objetos de dominio directamente
- [ ] Todas las forward references resueltas

### ✅ API
- [ ] Endpoints usan mapeadores antes de devolver datos
- [ ] Respuestas son JSON válido sin errores de serialización
- [ ] Manejo de errores implementado en cada endpoint

### ✅ Testing
- [ ] Tests de unicidad en repositorios pasan
- [ ] Tests de mapeo sin errores de serialización  
- [ ] Tests de integración API funcionan correctamente

---

## Beneficios Esperados

1. **Eliminación total** de errores de serialización Pydantic
2. **Unicidad garantizada** de objetos en toda la aplicación
3. **Relaciones coherentes** entre entidades de dominio
4. **API robusta** con datos serializables consistentes  
5. **Escalabilidad** para nuevas entidades y relaciones
6. **Mantenimiento simplificado** con patrones consistentes
7. **Performance óptima** con acceso O(1) en repositorios

Esta refactorización establece una base sólida y escalable para el sistema de simulación logística de drones, siguiendo principios SOLID y buenas prácticas de arquitectura limpia.

````markdown
# Plan de Refactorización Atomizado para Correos Chile

Este documento describe, de manera extremadamente detallada y atomizada, los pasos necesarios para refactorizar la arquitectura de Repositorios, Fábricas, Mapeadores y DTOs en el sistema de simulación de Correos Chile. Incorpora las siguientes aclaraciones:

- **Creación de objetos**: Todas las entidades se crean mediante las fábricas definidas en `simulacion_dominio.py`.
- **Almacenamiento de referencias**: Los `TDA_Hash_map` internos de los repositorios guardan referencias a los objetos reales, incluyendo asociaciones.
- **Estructura del grafo**: El grafo persiste objetos únicos de `Vertice` y `Arista`. Cada `Arista` almacena referencias a instancias de `Vertice`. Cada `Vertice` contiene un atributo `_elemento` que es un objeto de dominio real (`Cliente`, `Almacenamiento` o `Recarga`), con su propio ID (`id_cliente`, `id_almacenamiento`, `id_recarga`) y un atributo común `tipo_elemento`.

## 1. Preparación y Estructura de Carpetas

1.1. Crear la carpeta `Backend/Infraestructura/Repositorios/` si no existe.

1.2. Crear la carpeta `Backend/API/Mapeadores/` si no existe.

1.3. Crear la carpeta `Backend/API/DTOs/` si no existe.

1.4. Verificar que exista `simulacion_dominio.py` en `Backend/Dominio/`.

## 2. Repositorios: Unicidad, HashMap y Observadores

> **Objetivo**: Garantizar unicidad, acceso O(1) y trazabilidad mediante notificación a observadores.

2.1. **Definir la interfaz `IRepositorio<T>`** en `Backend/Infraestructura/Repositorios/IRepositorio.py`:
- Métodos: `agregar(obj: T) -> T`, `obtener_por_id(id_obj: Any) -> T | None`, `eliminar(id_obj: Any) -> bool`, `todos() -> List[T]`, `limpiar() -> None`, `obtener_hashmap() -> HashMap`.

2.2. **Implementar `TDA_Hash_map`**:
- Estructura que interne guarda `{id: objeto}`.
- Métodos internos: `contains(id)`, `get(id)`, `set(id, obj)`, `remove(id)`, `clear()`.

2.3. **Crear repositorios para cada entidad** en `Backend/Infraestructura/Repositorios/`:
- `RepositorioClientes`, `RepositorioPedidos`, `RepositorioAlmacenamientos`, `RepositorioRecargas`, `RepositorioRutas`, `RepositorioVertices`, `RepositorioAristas`.
- Cada clase implementa `IRepositorio<T>`.

2.4. **Implementar método `agregar(obj)`** en cada repositorio:
- Paso 1: obtener `id_real` de `obj` (`obj.id_cliente`, `obj.id_pedido`, etc.).
- Paso 2: si `hash_map.contains(id_real)`: devolver instancia existente y registrar notificación de duplicado.
- Paso 3: si no existe: `hash_map.set(id_real, obj)`, notificar alta y devolver `obj`.

2.5. **Implementar método `obtener_por_id(id)`**:
- Devolver `hash_map.get(id)` o `None`.

2.6. **Implementar `eliminar(id)`**:
- Si existe: `hash_map.remove(id)`, notificar baja, devolver `True`.
- Si no existe: devolver `False`.

2.7. **Implementar `todos()`**:
- Devolver lista de valores de `hash_map`.

2.8. **Implementar `limpiar()`**:
- Llamar `hash_map.clear()`, notificar limpieza.

2.9. **Observadores**:
- Definir interfaz `IObservadorRepositorio` con métodos `on_alta(obj)`, `on_baja(obj)`, `on_modificacion(obj)`, `on_limpieza()`.
- En cada repositorio, mantener lista de `observadores`.
- En cada operación, invocar el método correspondiente en todos los observadores suscritos.
- Crear el mecanismo de suscripción: `suscribir(observador: IObservadorRepositorio)`.

2.10. **IMPORTANTE** los repositorios deben de guardar referencias a los objetos reales, no solo IDs. Esto es crucial para mantener las relaciones y asociaciones en memoria.

## 3. Fábricas en `simulacion_dominio.py`

> **Objetivo**: Centralizar la creación de objetos y asegurar que se pasen por los repositorios.

3.1. **Ubicar o crear `simulacion_dominio.py`** en `Backend/Dominio/`.

3.2. **Definir clase `FabricaDominio`** con métodos estáticos para cada entidad:
- `crear_cliente(datos: dict) -> Cliente`
- `crear_pedido(datos: dict) -> Pedido`
- `crear_almacenamiento(datos: dict) -> Almacenamiento`
- `crear_recarga(datos: dict) -> Recarga`
- `crear_ruta(datos: dict) -> Ruta`
- `crear_vertice(elemento: Union[Cliente, Almacenamiento, Recarga]) -> Vertice`
- `crear_arista(origen: Vertice, destino: Vertice, peso: float) -> Arista`

3.3. **En cada método de fábrica**:
- Paso 1: Instanciar el objeto de dominio puro.
- Paso 2: Llamar al repositorio correspondiente: `RepositorioX.agregar(obj)`.
- Paso 3: Retornar la instancia única retornada por el repositorio.

## 4. Relaciones y Asignación de Referencias Reales

> **Objetivo**: Mantener relaciones en memoria con objetos reales.

4.1. **Pedidos y Cliente/Almacenamiento**:
- Al crear un `Pedido`, la fábrica debe:
  - Localizar `Cliente` real con `RepositorioCliente.obtener_por_id(id_cliente)`.
  - Localizar `Almacenamiento` real con `RepositorioAlmacenamiento.obtener_por_id(id_almacenamiento)`.
  - Asignar `pedido._cliente = instancia_cliente` y `pedido._origen = instancia_almacenamiento`.
  - Agregar `pedido` a listas internas: `instancia_cliente.pedidos.append(pedido)`, `instancia_almacenamiento.pedidos.append(pedido)`.

4.2. **Vértices y Áreas**:
- Al crear un `Vertice`, fábrica envía el objeto real (`Cliente`, `Almacenamiento` o `Recarga`) al constructor de `Vertice`, almacenándolo en `vertice._elemento`.

4.3. **Aristas**:
- Al crear una `Arista`, fábrica localiza los `Vertice` reales mediante sus repositorios.
- Asocia `arista._origen = vertice_origen`, `arista._destino = vertice_destino`.
- En cada `Vertice`, mantener lista `vertice.adyacentes.append(arista)`.

4.4. **Rutas**:
- Al crear una `Ruta`, fábrica recibe una lista de IDs de vértices.
- Localizar cada `Vertice` real y asignar lista de objetos a la ruta.

4.5. **Evitar referencias circulares profundas**:
- No agregar listas inversas en entidades no necesarias.
- Mantener las asociaciones solo en un lado cuando posible.

4.6. **Estructura del grafo**:
- El grafo se construye y persiste con objetos únicos de `Vertice` y `Arista`.
- Las aristas almacenan referencias a objetos `Vertice`.
- Cada `Vertice` almacena el objeto de dominio real.
- Los repositorios aseguran unicidad y acceso O(1).
- La simulación y el resto del sistema operan siempre sobre los objetos reales.

4.7. **Asociaciones**
- Todos los hashmaps de los repositorios deben de almacenar los objetos reales, no solo IDs.
- Los hashmaps deben de almacenar las relaciones reales, no solo IDs, para que las entidades puedan acceder a sus relaciones completas.
- Las relaciones entre objetos en los hashmaps debe estar correctamente definidas para evitar ciclos y referencias circulares.


## 5. Mapeadores: Objeto Real → DTO Plano

> **Objetivo**: Crear representaciones planas para la API.

5.1. **Definir interfaz `IMapeador<T, U>`** en `Backend/API/Mapeadores/IMapeador.py`:
- Métodos: `a_dto(obj: T) -> U` y opcional `de_dto(dto: U) -> T`.

5.2. **Crear mapeador por entidad** en `Backend/API/Mapeadores/`:
- `MapeadorCliente`, `MapeadorPedido`, `MapeadorAlmacenamiento`, `MapeadorRecarga`, `MapeadorRuta`, `MapeadorVertice`, `MapeadorArista`.

5.3. **Implementar `a_dto`**:
- Extraer atributos primitivos.
- Para relaciones, incluir solo IDs o listas de IDs.
- Ejemplo:
  ```python
  class ClienteDTO:
      id_cliente: str
      nombre: str
      ids_pedidos: List[str]
````

5.4. **Bandera de profundidad**:

- Permitir incluir detalles (por ejemplo, pedidos completos) bajo flag `detalles: bool = False`.

5.5. **Evitar ciclos**:

- Nunca llamar recursivamente a otros mapeadores que retornen objetos anidados.

## 6. DTOs: Estructura y Ubicación

> **Objetivo**: Definir clases planas para intercambio de datos.

6.1. **Crear directorio **``.

6.2. **Definir DTOs**:

- `ClienteDTO`, `PedidoDTO`, `AlmacenamientoDTO`, `RecargaDTO`, `RutaDTO`, `VerticeDTO`, `AristaDTO`.
- Cada DTO contiene solo atributos primitivos y listas de IDs.

6.3. **Ejemplo de DTO**:

```python
@dataclass
class PedidoDTO:
    id_pedido: str
    id_cliente: str
    id_almacenamiento: str
    peso: float
    estado: str
```

## 7. Servicios y Serialización a la API

> **Objetivo**: Orquestar el flujo: repositorio → dominio → DTO → respuesta HTTP.

7.1. **En servicios de dominio** (`Backend/API/Servicios/`), inyectar repositorios y mapeadores.

7.2. **Método ejemplo**: `obtener_cliente_con_pedidos(id_cliente: str) -> ClienteDTO`:

- Obtener `Cliente` real con `RepositorioCliente.obtener_por_id`.
- Llamar `MapeadorCliente.a_dto(cliente, detalles=True)`.
- Retornar DTO.

7.3. **En controladores/API** (`FastAPI`):

- Definir rutas: `GET /clientes/{id}` que llama al servicio.
- Responder con JSON serializando el DTO.

## 8. Pruebas Unitarias e Integración

8.1. **Configurar **`` en la raíz del proyecto.

8.2. **Tests de Repositorios**:

- `test_repositorio_cliente.py`: agregar, duplicado, eliminar, todos.
- Similar para cada entidad.

8.3. **Tests de Fábricas**:

- Verificar que `FabricaDominio.crear_*` llama al repositorio y retorna instancia única.

8.4. **Tests de Relaciones**:

- Crear pedido y comprobar listas de `Cliente.pedidos` y `Almacenamiento.pedidos` actualizadas.

8.5. **Tests de Mapeadores**:

- Convertir objetos reales a DTOs planos con y sin flag de detalles.

8.6. **Tests de Servicios**:

- Llamar servicios de API y comparar JSON resultante.

## 9. Convenciones, Documentación y Buenas Prácticas

9.1. **Nombres en español**: snake\_case para variables/funciones, PascalCase para clases, sin acentos.

9.2. **Docstrings en español** en todas las clases y métodos públicos.

9.3. **Separación de responsabilidades**:

- Repositorios: acceso a datos.
- Fábricas: creación de objetos.
- Mapeadores: conversión a DTO.
- Servicios: orquestación.

9.4. **Logs y Observabilidad**:

- Utilizar `logging` para informar eventos de repositorio y fábrica.
- Configurar formato de logs con timestamp y nivel.

---

*Este plan atomizado garantiza unicidad, referencias reales, mapeo plano y respuesta preparada para la API, cumpliendo los requisitos de la simulación de Correos Chile.*

```
```

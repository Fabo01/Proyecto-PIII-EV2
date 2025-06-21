# Plan de Implementacion de Logica de Negocio y Observadores (Refactorizado)

Este documento describe a detalle cada paso necesario para implementar completamente la logica de negocio y el patron observer de forma atomizada. El objetivo es crear un sistema modular, escalable y robusto que cumpla principios SOLID y Clean Architecture, asegurando la integracion coherente de todas las capas y entidades del proyecto.

---

## 0. Preparacion y referencias
1. **Lectura de `Docs/Requisitos.md`:** Considerar este archivo como la fuente de verdad para requisitos y reglas de negocio.
2. **Revision de implementaciones previas:** Revisar `Docs/estrategias.md`, `Docs/mejoras.md`, `Docs/parche.md` y `Docs/relaciones.md` para tener mas contexto.
3. **Configuracion de entorno Python y dependencias:** Instalar paquetes necesarios (p. ej. pytest, networkx, streamlit, etc.).
4. **Adherencia a SOLID y Clean Architecture:** Mantener una separacion clara de capas (Dominio, Aplicacion, Infraestructura, etc.).
5. **Iteracion por cada entidad:** Cada entidad del dominio debe tener sus metodos y validaciones clave implementados.
6. **Asegurar unicidad de entidades:** Garantizar que cada instancia de entidad (Cliente, Almacenamiento, Recarga, Pedido, etc.) sea unica y no duplicada.
7. **Manejo exclusivo de HashMap para unicidad:** Todos los vertices se referencian en la estructura HashMap, que garantiza la unicidad y evita atributos de posicion relativa dentro del propio vertice; solo se usa el HashMap como referencia principal de posiciones y unicidad, para todas las entidades.
8. **Manejo de vertices en el dominio:** No deben contener atributos de origen ni dominio, ni atributos de posicion relativa; unicamente `_elemento`,.
9. **Manejo de aristas con restriccion de peso:** El `_peso` de la Arista no puede ser mayor a 50 dentro de ningun recorrido.
10. **Atributo `tipo_elemento` en entidades:** Asegurar que cada entidad (Cliente, Almacenamiento, Recarga) define su tipo (`'cliente'`, `'almacenamiento'`, `'recarga'`).
11. **Atributos de Pedido y Ruta:** Verificar consistencia de campos obligatorios (p. ej. `id_pedido`, `origen`, `destino`, etc.).
12. **Documentacion y docstrings en espanol:** Sin acentos y describiendo proposito y uso de cada metodo y clase.

---

## 1. Capa de Dominio: Entidades Principales

### 1.1. Cliente (Dominio_Cliente.py)
- **Atributos:**
  - `id_cliente`
  - `nombre`
  - `tipo_elemento = 'cliente'`
  - `_pedidos = []` (lista interna de pedidos asociados)
- **Metodos:**
  1. `__init__`: Inicializa todos los atributos y crea la lista de pedidos.
  2. `agregar_pedido(pedido)`: Valida unicidad del pedido y lo asocia al cliente.
  3. `eliminar_pedido(pedido)`: Elimina el pedido si existe en la lista interna.
  4. `limpiar_pedidos()`: Vacia la lista de pedidos por completo.
  5. `obtener_pedidos() -> List[Pedido]`: Retorna la lista completa de pedidos asociados.
  6. `total_pedidos() -> int`: Retorna la cantidad de pedidos que tiene el cliente.
- **Documentacion:** Incluir docstrings en espanol (sin acentos) que expliquen proposito y uso de cada metodo.

### 1.2. Almacenamiento (Dominio_Almacenamiento.py)
- **Atributos:**
  - `id_almacenamiento`
  - `nombre`
  - `tipo_elemento = 'almacenamiento'`
  - `_pedidos = []`
- **Metodos:**
  1. `__init__(...)`: Inicializa atributos y la estructura interna para pedidos.
  2. `agregar_pedido(pedido)`: Valida unicidad y asocia el pedido.
  3. `obtener_pedidos() -> List[Pedido]`: Retorna la lista de pedidos.
  4. `total_pedidos() -> int`: Devuelve el numero de pedidos almacenados.
  5. `limpiar_pedidos()`: Vacia la lista interna de pedidos.
- **Documentacion:** Mismos lineamientos que la entidad Cliente.

### 1.3. Recarga (Dominio_Recarga.py)
- **Atributos:**
  - `id_recarga`
  - `nombre`
  - `tipo_elemento = 'recarga'`
- **Metodos:**
  1. `__init__`: Inicializa atributos y valida unicidad.
  2. `__str__`: Retorno legible para debugging o logs.
- **Validacion:** Verificar que `id_recarga` sea unico y que la instancia se cree correctamente.

### 1.4. Pedido (Dominio_Pedido.py)
- **Atributos:**
  - `id_pedido`
  - `cliente_v` (vertice asociado al cliente)
  - `origen_v` (vertice de origen)
  - `destino_v` (vertice de destino)
  - `prioridad`
  - `status`
  - `ruta`
  - `fecha_creacion`
- **Metodos:**
  1. `asignar_ruta(camino: List[int], peso_total: float)`: Asocia la ruta con el pedido.
  2. `actualizar_status(nuevo_status: str)`: Gestiona transicion entre estados (p. ej. pendiente, en_ruta, entregado).
- **Validacion:** 
  - Chequear la unicidad de `id_pedido`.
  - Validar que `origen_v` y `destino_v` como vertices sean correctos.
  - Verificar consistencia de fecha de creacion.

### 1.5. Ruta (Dominio_Ruta.py)
- **Atributos:**
  - `origen`
  - `destino`
  - `camino`
  - `peso_total`
  - `algoritmo`
  - `tiempo_calculo`
- **Metodos:**
  1. `es_valida() -> bool`: Retorna `True` si el camino conecta origen y destino coerentemente.
  2. `__str__`: Representacion legible del objeto Ruta.
- **Validacion:** Asegurar no duplicar rutas y que los vertices referenciados esten en repositorios validos.

---

## 2. Estructuras de Datos y Unicidad

### 2.1. Vertice (TDA_Vertice.py)
- **Atributos:**
  - `_elemento`: Referencia a una entidad del dominio (`Cliente`, `Almacenamiento` o `Recarga`).
- **Metodos:**
  1. Acceso y asignacion de `_elemento`.
  2. Comparacion segun la identidad del elemento (p. ej. `id_cliente`).
  3. Validar unicidad por id y tipo.
- **Regla:** No contiene logica de negocio, referencias de dominio ni atributos de posicion relativa.

### 2.2. Arista (TDA_Arista.py)
- **Atributos:**
  - `_origen` (Vertice)
  - `_destino` (Vertice)
  - `_peso` (float)
- **Metodos:**
  1. Acceso a extremos (vertice origen y destino).
  2. Validacion de `_peso`: no debe exceder 50 segun la logica de negocio.
  3. Comparacion para asegurar unicidad.
- **Regla:** No contener logica extra, solo representar la relacion entre vertices.

### 2.3. HashMap (TDA_Hash_map.py)
- **Proposito:** Acceso O(1) a entidades y a sus relaciones, centralizando y garantizando unicidad.  
  - Se usa de forma **exclusiva** para mantener las referencias del grafo, asegurando la integridad y eliminando la necesidad de posiciones relativas en los vertices.
- **Metodos potenciales:**
  1. `insertar(clave, valor)`
  2. `obtener(clave) -> valor`
  3. `existe(clave) -> bool`
  4. `eliminar(clave)`
  5. `limpiar()`
- **Regla:** Adaptar su implementacion a todas las entidades del dominio.

---

## 3. Fabricas y Repositorios

### 3.1. Fabricas (Dominio/EntFabricas/)
- **Objetivo:** Crear y validar instancias de entidades, asegurando unicidad y consistencia segun la logica de negocio.  
- **Ejemplos:**  
  - `FabricaClientes`, `FabricaAlmacenamientos`, `FabricaRecargas`, `FabricaPedidos`, `FabricaRutas`, `FabricaVertices`, `FabricaAristas`.
- **Metodos:**
  1. `crear(...)`: Genera una nueva instancia validando parametros.
  2. `obtener(...)`: Devuelve una instancia existente, buscandola en un HashMap o similar.
  3. `todos()`: Retorna un listado de todas las instancias.
  4. `limpiar()`: Limpia instancias para rehacer las pruebas o simulaciones.
  5. `obtener_errores()`: Retorna errores de creacion o validacion si los hay.

### 3.2. Repositorios (Infraestructura/Repositorios/)
- **Objetivo:** Proveer acceso a entidades (altas, bajas, cambios y consultas), almacenandolas en un HashMap u otra estructura.
- **Ejemplos:**
  - `RepositorioClientes`, `RepositorioAlmacenamientos`, `RepositorioRecargas`, `RepositorioPedidos`, `RepositorioRutas`, `RepositorioVertices`, `RepositorioAristas`.
- **Metodos:**
  1. `agregar(entidad)`: Almacena la entidad internamente.
  2. `obtener(identificador)`: Retorna la entidad buscada.
  3. `eliminar(identificador)`: Elimina la entidad por su identificador.
  4. `todos()`: Lista de todas las entidades.
  5. `limpiar()`: Reinicia la estructura interna.
  6. `obtener_hashmap()`: Devuelve la instancia del HashMap para uso externo.

---

## 4. Servicio de Simulacion (Dominio)

### 4.1. Interfaces (Dominio/Interfaces/IntSim/ISimulacionDominioService.py)
- **Metodos abstractos:**
  1. `iniciar_simulacion(n_vertices, m_aristas, n_pedidos)`
  2. `obtener_vertices()`
  3. `obtener_aristas()`
  4. `obtener_pedidos()`
  5. `obtener_rutas()`
  6. `obtener_recargas()`
  7. `obtener_estadisticas()`
  8. `listar_clientes()`
  9. `listar_almacenamientos()`
  10. `listar_recargas()`
- **Regla:** Debe proveer los metodos base para inicializar y consultar los datos de la simulacion.

### 4.2. Implementacion de Simulacion (Dominio/Simulacion_dominio.py)
- **Clase: `Simulacion` (Singleton)**
  - **Atributos**:
    - `_repo_vertices`
    - `_repo_aristas`
    - `_repo_clientes`
    - `_repo_almacenamientos`
    - `_repo_recargas`
    - `_repo_pedidos`
    - `_repo_rutas`
    - `_estrategia`
  - **Metodos**:
    1. `iniciar_simulacion`: Limpia repositorios, genera el grafo (vertices y aristas), crea pedidos y asocia entidades. Devuelve configuracion inicial.
    2. Elegir y asignar estrategia: Permite cambiar la logica de calculo de rutas en tiempo de ejecucion.
    3. Metodos de consulta (`obtener_*_hashmap()` y `obtener_*()`): Retornan la informacion solicitada desde repositorios.
    4. **Buena practica**: Toda la logica de negocio (creacion, busqueda, etc.) se delega a los repos o fabricas.
  - **Regla:** Mantener la instancia unica (Singleton) para coordinar la simulacion.

---

## 5. Estrategias de Rutas y Logica de Recarga

### 5.1. Estrategias (Dominio/AlgEstrategias/)
- **Implementaciones a realizar**: BFS, DFS, Topological Sort, Dijkstra, Floyd-Warshall, Kruskal.
- **Metodo clave**:
  - `calcular_ruta(origen, destino, grafo, autonomia=50, estaciones_recarga=None)`: Retorna la ruta deseada, considerando la autonomia y la necesidad de estaciones de recarga, considera si es necesario guardar un hashmap del grafo.
    * `_insertar_recargas_si_necesario`: Metodo interno para manejar casos en que la ruta exceda la autonomia.
- **Regla**: Cada estrategia debe ser capaz de manejar la logica de autonomia y recarga, asegurando que las rutas calculadas son viables para el drone, segun los requisitos especificados en "Requisitos.md".
- **Validacion**: Cada estrategia debe ser capaz de manejar la estructura de ruta y sus atributos, deben de usar objetos `Vertice` únicos y no IDs o diccionarios sueltos, utilizando los metodos de vecinos/aristas y el hashmap, sin crear vertices fuera de los repositorio.
- **Auditoria**: Implementar un mecanismo de auditoria para registrar las rutas calculadas, incluyendo el tiempo de calculo y si se requirieron recargas, para analisis posterior.
### 5.2. Inyeccion de Estrategia
- **Metodo**: `set_estrategia(self, estrategia: IRutaEstrategia)`
- **Objetivo**: Inyectar estrategicamente la logica de calculo de rutas en la simulacion. Permite alternar algoritmos de forma dinamica.
- **Uso**: Invocar este metodo en la instancia de `Simulacion` para cambiar la estrategia de calculo de rutas en tiempo de ejecucion.
- **Regla**: Cada estrategia debe cumplir con la interfaz definida y ser capaz de calcular rutas considerando la autonomia y las estaciones de recarga.

---

## 6. Observadores y Eventos

### 6.1. Interfaces (Dominio/Interfaces/IntObs/)
- **ISujeto**: Metodos para `agregar(observador)`, `quitar(observador)`, `notificar(evento, datos=None)`, `get_observadores()`, .
- **IObserver**: Metodo `actualizar(evento, datos=None)` para reaccionar a eventos.

### 6.2. Implementacion total a través de todas las capas, 
- **Eventos relevantes**:
  - Creacion de pedido
  - Entrega de pedido
  - Calculo de ruta
  - Cambio de estrategia
  - Actualizacion de estado de pedido
  -etc...
- **Notificacion**: Los metodos o servicios relevantes invocan `notificar` cada vez que ocurre un evento significativo.
- Ten en cuenta que los observadores deben ser capaces de reaccionar a los eventos sin introducir logica de negocio compleja, manteniendo la separacion de responsabilidades.
- **Ejemplo de implementacion**:
  - `PedidoObserver`: Observa eventos de pedidos y registra cambios en un log o base de datos.
  - `RutaObserver`: Observa eventos de rutas y actualiza estadisticas de uso.   etc..

  - Los observadores deben estar presentes de manera transversal, en cada capa, para asegurar que todos los eventos relevantes son capturados y procesados adecuadamente.

  - **Objetivo**: Proporcionar visibilidad y trazabilidad de eventos clave en el sistema, permitiendo a los desarrolladores y administradores monitorear el comportamiento del sistema en tiempo real.
- **Regla**: Cada entidad relevante debe implementar la interfaz `ISujeto` y notificar a los observadores registrados cuando ocurran eventos significativos.
- Lo importante es que al notar un evento, se notifique a todos los observadores registrados, permitiendo que cada uno reaccione de manera independiente y sin acoplamiento directo con la entidad que genera el evento. Esto permite auditorias de la totalidad del sistema y sus eventos sin implementar logs en el codigo de negocio, manteniendo la logica de negocio separada de la logica de auditoria y eventos.

---

## 7. Mapeadores y DTOs Y refactorizacion de Endpoints

### 7.1. Mapeadores (Dominio/Interfaces/IntMapeadores/)
- **Proposito**: Convertir objetos de dominio en DTOs u objetos de transferencia, evitando ciclos de importacion.
- **Regla**: Mantener ligereza y evitar exponer logica de negocio. Ejemplo:
  - `IMapeadorDominioDTO`
  - `PedidoMapeador` (convierte `Pedido` a un DTO con atributos serializables)
- **Beneficio**: Facilitar integraciones y reducir acoplamiento entre la capa de dominio y otras capas.
### 7.2. Refactorizacion de Endpoints
- **Objetivo**: Asegurar que todos los endpoints usan objetos `Vertice` únicos y no IDs o diccionarios sueltos, utilizando los metodos de vecinos/aristas y el hashmap, sin crear vertices fuera de los repositorio.
-  Refactoriza la carpeta de API/ para que todos los enrutadores sueltos esten en una carpeta /API/Endpoints/ y que cada endpoint use los mapeadores y fabricas para crear los objetos necesarios y reales, teniendo unicidad utilizando el hashmap.
- **Regla**: Cada endpoint debe validar la unicidad de los vertices antes de calcular rutas, asegurando que no se usen IDs sueltos.
- La estructura de endpoints debe de ser modular, escalable y coherente, siguiendo los principios de diseño limpio y SOLID, teniendo una cohesion total con el sistema.
- **Ejemplo de endpoint refactorizado**:
  - `calcular_ruta`: Asegurarse de que recibe objetos `Vertice` únicos, valida la autonomia y usa la estrategia correcta para calcular la ruta.

---

## 8. Validacion, Pruebas y Documentacion

### 8.0. Validacion
- **Unicidad**: Asegurar que todas las entidades (Clientes, Almacenamientos, Recargas, Pedidos) son unicas y no se duplican.
- **Integridad de datos**: Validar que las relaciones entre entidades (p. ej. pedidos asociados a clientes) se mantienen correctamente.
- **Consistencia de atributos**: Verificar que los atributos requeridos (p. ej. `id_pedido`, `origen`, `destino`) se cumplen en todas las entidades.
- **Autonomia y recarga**: Validar que las rutas calculadas cumplen con la autonomia del drone y que se insertan estaciones de recarga cuando es necesario.
- ****: Asegurar que los endpoints y las estrategias de ruta usan objetos `Vertice` únicos y no IDs o diccionarios sueltos, utilizando los metodos de vecinos/aristas y el hashmap, sin crear vertices fuera de los repositorio.
- ****: Siempre se deben de utilizar la totalidad de repositorios, fabricas, estrategias, etc, para asegurar que la logica de negocio se aplica correctamente y que cada componente cumple su responsabilidad unicamente.
- **Auditoria de rutas**: Implementar un mecanismo para registrar las rutas calculadas, incluyendo el tiempo de calculo y si se requirieron recargas, para analisis posterior.

### 8.1. Pruebas
1. **BDD**: Verificar escenarios de negocio y comportamiento global (unicidad, relaciones, integridad de datos).  
2. **Unitarias**: Probar cada metodo y clase, validando:
   - Unicidad de entidades
   - Correcta creacion y eliminacion en repositorios
   - Calculo de rutas considerando autonomia y puntos de recarga
   - Separacion de responsabilidades (SOLID)

### 8.2. Documentacion
- **Docstrings en espanol** para metodos y clases clave.
- **Sin acentos** en nombres de variables y clases, manteniendo consistencia.
- **Apoyarse en**: 
  - `Docs/Requisitos.md` como fuente principal.
  - `Docs/Documentacion/` para mas detalles tecnicos.
- **Objetivo**: Tener guias de uso claras para futuros desarrolladores y mantener la coherencia con la arquitectura propuesta.

---

## Conclusion

Este documento refactorizado detalla un plan integral y atomizado para desarrollar la logica de negocio y la implementacion de observadores. Siguiendo los principios aqui descritos, se logra una arquitectura modular, escalable y alineada con los principios SOLID y Clean Architecture. El uso de fabricas, repositorios, entidades de dominio y un sistema de observadores asegura que cada componente cumpla con su responsabilidad unicamente, permitiendo una evolucion ordenada y robusta de todo el proyecto.
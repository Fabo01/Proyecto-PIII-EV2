# Plan de implementación para la corrección de estrategias y endpoints de rutas

## 1. Garantizar unicidad de vértices y aristas en todas las estrategias

### 1.1. Refactorización de acceso a vértices
- Todas las estrategias (`RutaEstrategiaDijkstra`, `RutaEstrategiaBFS`, `RutaEstrategiaDFS`, `RutaEstrategiaKruskal`, `RutaEstrategiaFloydWarshall`, etc.) deben recibir y operar únicamente con objetos `Vertice` únicos, obtenidos siempre desde el grafo o el repositorio centralizado, o utilizando el hashmap.
- Antes de cualquier cálculo de ruta, los endpoints deben buscar los vértices de origen y destino usando el grafo (`grafo.buscar_vertice_por_elemento` o `grafo._repositorio_vertices.obtener(id)`), nunca crear nuevos objetos ni usar diccionarios/IDs sueltos con el hashmap.
- Todas las comparaciones y recorridos en los algoritmos deben hacerse por referencia de objeto (`is` o `==` sobre el objeto `Vertice`), nunca por ID o por atributos.
- Validar que los métodos de los TDA y modelos (`__hash__`, `__eq__`) estén correctamente implementados para garantizar unicidad y uso en estructuras hash.

### 1.2. Refactorización de estrategias
- Revisar cada clase de estrategia para asegurar que:
  - Solo recorra y compare objetos `Vertice` únicos.
  - No acepte ni retorne IDs, diccionarios ni copias.
  - Use el grafo y sus métodos para obtener vecinos y aristas.
- Añadir pruebas unitarias para verificar que no existen duplicados de vértices/aristas y que los caminos calculados son correctos.
- Las estrategias deben ser capaces de manejar la estructura de ruta y sus atributos, deben de usar objetos `Vertice` únicos y no IDs o diccionarios sueltos, utilizando los metodos de vecinos/aristas y el hashmap, sin crear vertices fuera de los repositorio.
## 1.3. Validación de autonomía y recarga
- En cada estrategia, si la distancia entre origen y destino excede la autonomía del drone, esta autonomia es el peso acumulado de las aristas recorridas, y este nunca puede superar 50, luego de eso se debe buscar y forzar la inclusión de estaciones de recarga en la ruta para asegurar una total autonomia del drone.
- Implementar lógica para dividir la ruta en tramos que no excedan la autonomía, insertando vertices de recarga donde sea necesario.
- Registrar en el resultado si la ruta cumple autonomía o cuántas recargas fueron necesarias.
- Las estrategias deben ser capaces de manejar la lógica de autonomía y recarga, asegurando que las rutas calculadas son viables para el drone, segun los requisitos especificados en "Requisitos.md".
- Si el algoritmo, por definicion, no puede calcular rutas con autonomía (de 50 de peso en este caso), debe ser documentado y validado en los endpoints, para que no se use incorrectamente.
- Ten en cuenta seguir SOLID y los principios de diseño limpio, asegurando que cada estrategia sea cohesiva y cumpla una única responsabilidad.
- Implementa una clase base abstracta para delegar los metodos abstractos para las estrategias de ruta que defina los métodos comunes y la lógica de validación de autonomía, de esta forma se puede reutilizar código y asegurar consistencia en todas las estrategias, una solución modular, escalable y coherente.
- Implementar un mecanismo de auditoría para registrar las rutas calculadas, incluyendo el tiempo de cálculo y si se requirieron recargas, para análisis posterior.

## 2. Refactorización de endpoints en /rutas

### 2.1. Refactorización de acceso a vértices
- Antes de llamar a cualquier estrategia, buscar los vértices únicos usando el grafo/repositorio.
- Validar que los vértices existen y son únicos, lanzar error si no.
- Llamar a la estrategia pasando los objetos `Vertice` únicos y el grafo.

### 2.2. Endpoints requeridos

#### 2.2.1. Endpoint: Calcular ruta para un pedido con cualquier estrategia
- **Ruta:** `/rutas/calcular`
- **Método:** `GET`
- **Parámetros:** `id_pedido`, `algoritmo`
- **Proceso:**
  1. Buscar el pedido y sus vértices únicos.
  2. Validar autonomía: si la ruta calculada excede la autonomía, incluir vertices de recarga automáticamente.
  3. Llamar a la estrategia correspondiente.
  4. Retornar la ruta, el tiempo y si cumple autonomía, aunque siempre debe cumplirla, o documentar si algun algoritmo, por definicion no puede usar la restriccion de autonomia (peso acumulado de las aristas recorridas, como maximo 50).

#### 2.2.2. Endpoint: Calcula todos los pedidos con las mejores rutas usando Floyd-Warshall
- **Ruta:** `/rutas/floydwarshall_pedidos`
- **Método:** `GET`
- **Proceso:**
  1. Para cada pedido, buscar vértices únicos.
  2. Calcular la mejor ruta usando Floyd-Warshall considerando autonomía y estaciones de recarga para todos los pedidos.
  3. Registrar y retornar los resultados para cada pedido.

#### 2.2.3. Endpoint: Calcular para cada pedido todas sus rutas posibles con todos los algoritmos
- **Ruta:** `/rutas/pedido_todos_algoritmos`
- **Método:** `GET`
- **Proceso:**
  1. Para cada pedido, buscar vértices únicos.
  2. Para cada pedido, poder calcular todos los algoritmos de ruta y el tiempo de cálculo.
  3. Validar autonomía y registrar si requiere recarga.
  4. Registrar los resultados antes de cambiar el estado del pedido a completado, calcular el tiempo de todas las rutas antes de cambiar el estado del pedido a completado.
  5. Retornar un resumen con los tiempos y rutas para cada pedido y algoritmo.


## 4. Integración y pruebas
- Validar con pruebas automatizadas que no existen duplicados de vértices/aristas y que los caminos calculados son correctos y cumplen autonomía.
- Auditar el uso de hash map y unicidad en todos los puntos críticos del sistema.
- Documentar en los endpoints y estrategias el uso de referencias únicas y la lógica de autonomía.

## 5. Checklist de cumplimiento
- [ ] Todas las estrategias usan solo objetos `Vertice` únicos.
- [ ] Los endpoints de rutas validan unicidad antes de calcular.
- [ ] Se valida autonomía y se insertan recargas si es necesario.
- [ ] Se registran y retornan los resultados de rutas y tiempos para cada pedido y algoritmo.
- [ ] Se documenta y prueba la integración total del sistema.
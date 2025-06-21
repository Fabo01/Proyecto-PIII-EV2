# Plan Central de Refactorización Integral

Este documento describe un plan paso a paso, atomizado y detallado, para refactorizar completamente la capa de Simulación de dominio, el Servicio de Simulación y la Aplicación de Simulación. El objetivo es lograr una arquitectura modular, escalable, robusta y coherente con los principios SOLID y los lineamientos de `Requisitos.md`.

---

## 1. Refactorización de la Capa de Dominio: `Simulacion_dominio.py`

### 1.1 Extraer y eliminar colecciones internas
- **Tarea 1.1.1**: Identificar y eliminar todas las listas internas en la clase `Simulacion` que almacenan entidades (clientes, pedidos, rutas, vértices, aristas).
  - _Código legacy a eliminar_: cualquier atributo tipo `self._clientes = []`, `self._pedidos = []`, `self._rutas = []`, etc.
- **Tarea 1.1.2**: Declarar atributos privados para inyección de repositorios (ej.: `_repo_clientes`, `_repo_pedidos`, `_repo_vertices`, `_repo_aristas`, `_repo_rutas`).
  - Inicializarlos en el constructor o método estático de inicialización.
- **Tarea 1.1.3**: Exponer propiedades de solo lectura para cada repositorio:
  ```python
  @property
  def repo_clientes(self):
      return self._repo_clientes
  ```
  - Repetir para pedidos, vértices, aristas, rutas, etc....

### 1.2 Delegar lógica a Servicios y Aplicación
- **Tarea 1.2.1**: Revisar métodos de negocio en `Simulacion` (generación de pedidos, cálculo de rutas, control de entregas) y refactorizar y eliminar cualquier flujo de control que invoque directamente DTOs o mapeadores.
  - _Código legacy a eliminar_: llamadas a `Mapeador...`, construcción de respuestas DTO, logica de Servicios o Aplicacion en `Simulacion`, yendo a su debida capa para refactorizarse.
- **Tarea 1.2.2**: Dejar en dominio solo métodos puros de negocio que operen con entidades y repositorios:
  - `generar_pedido()`,  etc...: crear instancia de `Pedido` via repositorio de pedidos.
  - `calcular_ruta()`, etc...: delegar en estrategia inyectada, solo armar parámetros.
  - `marcar_entregado(id_pedido)`, etc...: actualizar estado en repositorio.
  - `[metodo] _x()`, etc...: y así para cada metodo existente, asegurando una integracion robusta y total en el sistema.

### 1.3 Aplicar Singleton con DI de repositorios
- **Tarea 1.3.1**: Mantener método estático `obtener_instancia()` que reciba en su primera llamada los repositorios como parámetros.
- **Tarea 1.3.2**: Hacer que la instancia única almacene las referencias a los repositorios inyectados.
- **Tarea 1.3.3**: Eliminar cualquier instancia directa de `Simulacion` en el código legacy, reemplazándola por `Simulacion.obtener_instancia()`.

---

## 2. Refactorización del Servicio de Dominio: `Servicios_Simulacion.py`

### 2.1 Inyección de la instancia de Simulación
- **Tarea 2.1.1**: Cambiar el constructor para recibir la instancia de `Simulacion` por parámetro (DI) y nombrar `SimulacionDominioService` a `SimDominioServicio`.
  ```python
  class SimDominioServicio:
      def __init__(self, simulacion: Simulacion):
          self._sim = simulacion
  ```
- **Tarea 2.1.2**: Eliminar cualquier instancia directa de `Simulacion` dentro del servicio, asegurando que se use siempre la inyectada.
- **Tarea 2.1.3**: Asegurar que todos los métodos del servicio usen `self._sim` para acceder a repositorios y entidades.

### 2.2 Uso de repositorios expuestos
- **Tarea 2.2.1**: Modificar cada método para usar `self._sim.repo_*` en vez de accesos directos o `RepositorioXYZ()`.
- **Tarea 2.2.2**: Eliminar cualquier creación de entidades dentro del servicio.
  - _Código legacy a eliminar_: `Cliente(...)`, `Pedido(...)` o `Vertice(...)` instanciados en el servicio.

### 2.3 Exposición de métodos claros
- **Tarea 2.3.1**: Definir métodos públicos:
  - `obtener_vertices_hashmap()` → llama a `self._sim.repo_vertices.obtener_hashmap()`.
  - `obtener_pedidos_hashmap()` → `self._sim.repo_pedidos.obtener_hashmap()`.
  - `obtener_rutas_hashmap()`, `obtener_aristas_hashmap()`, etc.
    - `obtener_clientes_hashmap()` → `self._sim.repo_clientes.obtener_hashmap()`.
  - `obtener_{funcion}()` → `self._sim.repo_[entidad]{funcion}` y así para cada método existente, asegurando una integracion total del sistema a través de todas las capas.
- **Tarea 2.3.2**: Eliminar cualquier lógica de mapeo o conversión de DTO dentro de este servicio.

---

## 3. Refactorización de la Capa de Aplicación: `Aplicacion_Simulacion.py`

### 3.1 Inyección del Servicio de Dominio
- **Tarea 3.1.1**: Cambiar la clase `SimulacionAplicacionService` a `SimAplicacionServicio`, además `SimAplicacionServicio` debe recibir mediante un Patrón Constructor (Builder) la instancia de `SimDominioServicio` o una inyección normal, hay que definir cual es mas robusta y alineada.
- **Tarea 3.1.2**: Eliminar uso directo de `Simulacion` o repositorios, todo debe delegarse a través de las inyecciones y métodos.
- **Tarea 3.1.3**: Asegurar que todos los métodos de la aplicación usen `self._servicio` para acceder a los métodos del servicio de dominio.
- **Tarea 3.1.4**: Eliminar cualquier lógica de negocio compleja, asegurando que la aplicación solo actúe como un intermediario entre la API y el servicio de dominio.
- **Tarea 3.1.5**: Eliminar cualquier lógica de mapeo o conversión de DTO dentro de esta capa.
- **Tarea 3.1.6**: Asegurar que la aplicación no tenga dependencias directas a DTOs, sino que use los métodos del servicio para obtener datos.
- **Tarea 3.1.7**: Eliminar cualquier instancia directa de `SimulacionAplicacionService` en el código legacy, reemplazándola por `SimAplicacionServicio.obtener_instancia()`.
- **Tarea 3.1.8**: Asegurar que todos los métodos de `SimAplicacionServicio` sean estáticos, para evitar instanciaciones innecesarias.



### 3.2 Exposición de endpoints y métodos de conveniencia
- **Tarea 3.2.1**: Para cada acción de la API (listar vértices, obtener pedidos), implementar métodos que llamen unívocamente a un método del servicio.
  - Ej.: `def listar_vertices()` → `self._dominio_servicio.obtener_vertices()`.
    - Ej.: `def obtener_pedidos()` → `self._dominio_servicio.obtener_pedidos()`.
    - Ej.: `def [] ()` → `self._servicio.obtener_rutas()`.
- **Tarea 3.2.2**: Eliminar cualquier lógica de validación compleja o mapeo en la capa de aplicación.
- **Tarea 3.2.3**: Asegurar que todos los métodos de la aplicación devuelvan datos en un formato adecuado para la API, sin lógica de negocio.


---

## 4. Limpieza de lógica de Mapeo y DTOs
- **Tarea 4.1**: Eliminar todo uso de `Mapeador*` dentro de `Simulacion_dominio.py` y `Servicios_Simulacion.py` y `Aplicacion_Simulacion.py`.
- **Tarea 4.2**: Mantener mapeadores solo en la capa API (Diferenciar entre DTOs y Mapeadores).

---
---

## 5. Resumen de Eliminaciones Legacy
- Listas internas en `Simulacion`.
- Instanciaciones directas de entidades en servicios y aplicación.
- Lógica de mapeo en dominio y servicio.
- Dependencias directas a DTOs en dominio.
- Cualquier `import` de `Mapeador*` fuera de la capa API.

---

## 6. Refactorización Integral por Capas

Para garantizar un sistema cohesivo, robusto y alineado entre las capas Dominio, Servicio, Aplicación, Infraestructura y API, se plantea el siguiente plan detallado.

#### 6.1 Dominio (Backend/Dominio)
- Tarea 6.1.1: Eliminar todas las colecciones internas (`listas`, `diccionarios`) de entidades.  
  - Código legado a eliminar: atributos como `_clientes`, `_almacenamientos`, `_pedidos`, `_rutas` en `Simulacion_dominio.py` y métodos de gestión interna en clases de dominio.
- Tarea 6.1.2: Mantener únicamente inyección de repositorios en `Simulacion` (Singleton).  
  - Validar que `__new__` y `__init__` solo configuren repositorios.
- Tarea 6.1.3: Refactorizar clases de dominio (`Dominio_Cliente.py`, `Dominio_Almacenamiento.py`, `Dominio_Pedido.py`, `Dominio_Ruta.py`, `Dominio_Recarga.py`) para eliminar manejo interno de listas de pedidos y delegar al repositorio.

#### 6.2 Infraestructura (Backend/Infraestructura)
- Tarea 6.2.1: Verificar que cada repositorio (`RepositorioClientes`, `RepositorioAlmacenamientos`, `RepositorioRecargas`, `RepositorioVertices`, `RepositorioAristas`, `RepositorioPedidos`, `RepositorioRutas`) implemente solo los métodos de la interfaz: `agregar`, `obtener`, `eliminar`, `todos`, `limpiar`, `obtener_hashmap`.
  - Eliminar inicializaciones o lógica de negocio adicional.
- Tarea 6.2.2: Asegurar que internamente usan `HashMap` y que `todos()` devuelva una lista de entidades, `obtener_hashmap()` un diccionario `ID → entidad`.

#### 6.3 Servicio de Dominio (Backend/Servicios/SimServicios)
- Tarea 6.3.1: Inyectar `Simulacion` en el constructor de `SimulacionDominioService`.
- Tarea 6.3.2: Refactorizar cada método para delegar a repositorios de `Simulacion`.  
  - Ej.: `obtener_vertices()` → `self._sim.repo_vertices.todos()`.
- Tarea 6.3.3: Añadir métodos de conveniencia: `obtener_vertices_hashmap()`, `obtener_rutas_hashmap()`, `obtener_clientes_hashmap()`, etc.
- Código legado a eliminar: lógica de creación directa de entidades y acceso a atributos internos de `Simulacion`.

#### 6.4 Aplicación (Backend/Aplicacion/SimAplicacion)
- Tarea 6.4.1: Inyectar `SimulacionDominioService` en el constructor.
- Tarea 6.4.2: Refactorizar cada método para llamar únicamente a un método de servicio de dominio.
  - Ej.: `obtener_pedidos()` → `self._serv.obtener_pedidos()`.
- Tarea 6.4.3: Eliminar cualquier validación o mapeo interno.

#### 6.5 API (Backend/API)
- Tarea 6.5.1: Crear proveedor único en `Backend/API/proveedores.py` que instancie repositorios, dominio, servicio y aplicación.
- Tarea 6.5.2: Refactorizar `get_simulacion_service()` en cada módulo API para usar el proveedor.
- Tarea 6.5.3: En cada endpoint, usar solo métodos de la capa aplicación; eliminar uso directo de repositorios y mapeadores en controladores.
  - Ej.: en `listar_aristas()`: `return service.obtener_aristas()`.
- Tarea 6.5.4: Mantener mapeadores solo para conversión DTO → dominio en la capa API.
- Código legado a eliminar: imports de `Mapeador*` fuera de controladores y lógica de mapeo en servicios o dominio.

---

Este plan atomiza cada responsabilidad y detalla el código legacy a eliminar, asegurando un sistema modular, escalable y alineado con los requisitos centrales del proyecto.

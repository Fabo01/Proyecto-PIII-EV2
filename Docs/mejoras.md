s# Plan de Mejoras y Auditoría Integral para la Simulación de Drones – Correos Chile

Este documento unifica el plan de auditoría de instanciación única con el plan de mejora general del sistema, alineado con los requisitos de `Requisitos.md` y buenas prácticas SOLID.

## 1. Introducción

- Mantener la consistencia de instanciación y referencias únicas para Vértices, Aristas, Pedidos, Rutas y Grafo.
- Aplicar patrones de diseño (Singleton, Factory, Repository, Estrategia, Observer, Dependency Injection, Builder, Mapper).
- Refactorizar la arquitectura para escalabilidad, modularidad y facilidad de pruebas.
- Garantizar cumplimiento de estándares de código en español, snake_case y PascalCase.

## 2. Objetivos

1. Auditar e implementar instanciación única de objetos centrales.
2. Centralizar la creación y gestión de entidades en repositorios y fábricas.
3. Desacoplar algoritmos de ruta mediante Estrategia.
4. Introducir inyección de dependencias en servicios y bootstrap.
5. Separar mapeo dominio→DTO en mapeadores dedicados.
6. Publicar eventos relevantes (Observer) para UI y estadísticas en tiempo real.

## 3. Resumen de Auditoría (Plan existente)

### 3.1 TDA e Infraestructura
- Revisar y asegurar que `Modelo_Vertice.py`, `Modelo_Arista.py` y `TDA` (AVL, HashMap) gestionen correctamente `__hash__`, `__eq__` y no generen clones accidentalmente.
- Verificar que `Grafo` inserte y busque siempre las mismas instancias de vértices.

### 3.2 Objeto Grafo y Simulación
- Confirmar que `Simulacion` es Singleton y reinicializa grafo una sola vez.
- Auditar métodos `_generar_vertices`, `_generar_aristas` para evitar instanciaciones duplicadas.

### 3.3 Entidades del Dominio
- Validar la coherencia de `Cliente`, `Almacenamiento`, `Recarga`, `Pedido` y `Ruta`.
- Revisar la separación de responsabilidades: clientes gestionan solo sus pedidos; pedidos no crean clientes ni vértices.

### 3.4 Fábricas y Servicios
- Auditar `FabricaPedidos`: lista de errores, validaciones y logging.
- Verificar servicios de Dominio y Aplicación para inyección de instancias y evitar `new` dispersos.

### 3.5 API, DTOs y Frontend
- Revisar DTOs (`Dtos1`, `Dtos2`), extraer lógica de mapeo a mapeadores.
- Asegurar que el dashboard use datos consistentes y tablas de errores de fábrica.

## 4. Plan de Mejora Detallado

### 4.1 Infraestructura de Repositorios
#### 4.1.1 Crear estructura de carpetas y archivos
- [ ] `Infraestructura/Repositorios/` (directorio raíz)
- [ ] Archivos: `RepositorioGrafo.py`, `RepositorioPedido.py`, `RepositorioCliente.py`, `RepositorioAlmacenamiento.py`, `RepositorioRecarga.py`

**Código legacy a revisar/modificar/eliminar:**
- Uso directo de `TDA_Hash_map.HashMap` o `TDA_AVL.AVL` en `Simulacion_dominio.py`
- Manipulación de listas internas (`self.clientes`, `self.pedidos`, etc.) sin pasar por repositorios
- `hash_pedidos` en `Simulacion_dominio.py`

#### 4.1.2 Definir interfaces y contratos (IRepositorio*)
- [ ] `Infraestructura/Repositorios/Interfaces` (directorio raíz)
- [ ] `IRepositorioGrafo`: métodos CRUD para vértices y aristas
- [ ] `IRepositorioPedido`: métodos para creación, búsqueda, actualización y eliminación de pedidos
- [ ] `IRepositorioCliente`, `IRepositorioAlmacenamiento`, `IRepositorioRecarga` con operaciones específicas de dominio

**Código legacy a revisar/modificar/eliminar:**
- Acceso directo a estructuras internas en `Simulacion_dominio.py` y servicios

#### 4.1.3 Implementación de clases de repositorio
- [ ] `RepositorioGrafo`: delegar a TDA interno (HashMap y AVL)
- [ ] `RepositorioPedido`: usar `FabricaPedidos` y `TDA_HashMap` para almacenamiento en memoria
- [ ] `RepositorioCliente`, `RepositorioAlmacenamiento`, `RepositorioRecarga`: CRUD y validaciones de existencia

**Código legacy a revisar/modificar/eliminar:**
- Acceso directo a listas y TDAs en dominio y servicios

#### 4.1.4 Refactorización de TDA y Grafo
- [ ] Ajustar `Modelo_Grafo.py` para que reciba instancia de `RepositorioGrafo` en constructor
- [ ] Marcar `HashMap` y `AVL` como internos (no públicos) y accesibles solo vía repositorios

**Código legacy a revisar/modificar/eliminar:**
- Uso directo de `HashMap` y `AVL` fuera de repositorios

#### 4.1.5 Pruebas unitarias para repositorios
- [ ] Crear tests unitarios en `Tests/unitarios/` para cada repositorio: CRUD, condiciones de error y casos límite

---

### 4.2 Singletons Controlados
- [ ] Convertir `Simulacion` en Singleton puro:
  1. Constructor privado
  2. Método estático `instance()`
  3. Método `reiniciar()` para limpiar estado
  4. Tests de comportamiento singleton y reinicio
- [ ] Convertir `Grafo` en Singleton similar
- [ ] Actualizar bootstrap (`main.py` o `bootstrap.py`) para usar `instance()` en lugar de `new`

**Código legacy a revisar/modificar/eliminar:**
- Llamadas `new Grafo()` en el init de `Simulacion`
- Reinicializaciones directas en `reiniciar_instancia`
- Instanciaciones directas de `SimulacionDominioService()` y `Simulacion()` dentro de servicios

---

### 4.3 Patrón Estrategia para Algoritmos de Ruta
#### 4.3.1 Definir interfaz `IRutaEstrategia`
- [ ] Método `calcular(origen, destino, max_peso, forzar_recarga)`
#### 4.3.2 Implementaciones concretas
- [ ] `DijkstraEstrategia`
- [ ] `FloydWarshallEstrategia`
- [ ] `BFSEstrategia`
- [ ] La totalidad de las estrategias debe ser inyectada en `Simulacion` y endpoints API siguiendo el mismo patrón
- [ ] Tests comparativos de rutas entre estrategias
#### 4.3.3 Registro y fábrica de estrategias
- [ ] `RutaEstrategiaFabrica` que mapea claves a instancias de estrategia
- [ ] Configuración en `SimulacionConstructor` o bootstrap

**Código legacy a revisar/modificar/eliminar:**
- Código monolítico de `dijkstra_camino_minimo`, `bfs_camino`, `dfs_camino`, `topological_sort_camino` en `Simulacion_dominio.py`
- Validación de origen/destino y lógica de recorrido embebida

---

### 4.4 Extensión de Fábricas de Entidades
#### 4.4.1 Nuevas fábricas básicas
- [ ] `FabricaVertice`, `FabricaArista`, `FabricaCliente`, `FabricaAlmacenamiento`, `FabricaRecarga`
- [ ] Cada fábrica debe:
  - Validar datos de entrada
  - Crear instancias únicas de entidades
  - Manejar errores y logging centralizado
  - Reemplazar lógicas legacy en `Dominio_Pedido.py` y `Simulacion_dominio.py` y en todas las capas del sistema. Así cada fábrica debe ser responsable de la creación y validación de sus entidades, siendo estas únicas en la aplicación y evitando duplicaciones.
- [ ] Validaciones de datos y reglas de dominio centralizadas, enfatizando una correcta implementacion a través de todas las capas para todas las fábricas, reemplazando las lógicas legacy por las nuevas en todas las capas.
#### 4.4.2 Integración de fabricas en todas las capas
- [ ] Ajustar `Simulacion` para usar `FabricaPedidos`, `FabricaRuta`, `FabricaCliente`, `FabricaAlmacenamiento`, `FabricaRecarga`
- [ ] Ajustar `SimulacionDominioService` para usar `FabricaPedidos`, `FabricaRuta`, `FabricaCliente`, `FabricaAlmacenamiento`, `FabricaRecarga`
- [ ] Ajustar `SimulacionAplicacionService` para usar `FabricaPedidos`, `FabricaRuta`, `FabricaCliente`, `FabricaAlmacenamiento`, `FabricaRecarga`
- [ ] Ajustar `FabricaPedidos` para usar `FabricaCliente`, `FabricaAlmacenamiento`, `FabricaRecarga` y `FabricaRuta`
- [ ] Ajustar `FabricaRuta` para usar `FabricaVertice` y `FabricaArista`
- [ ] Ajustar todas las funcionalidades de creación de pedidos, rutas y demás entidades para que utilicen las fábricas correspondientes a través de todas las capas en la totalidad del sistema. 
- [ ] Manejo centralizado de errores y logging unificado en todas las fábricas.
#### 4.4.3 Pruebas BDD para cada fábrica
- [ ] Escenarios de creación válida e inválida de cada entidad y validaciones de dominio para cada fábrica.

**Código legacy a revisar/modificar/eliminar:**
- Validaciones duplicadas dentro de `Pedido.__init__` en `Dominio_Pedido.py`
- Creación directa de vértices y aristas en `Simulacion_dominio.py`

---

### 4.5 Inyección de Dependencias
- [ ] Crear módulo `bootstrap.py`
- [ ] Inyectar repositorios, fábricas y logger en:
  - `SimulacionDominioService`
  - `SimulacionAplicacionService`
  - `Simulacion`
  - `SimulacionConstructor`
  - `ObservadorEstadisticas` etc...
    - cualquiera que sea el servicio que maneje la lógica de negocio y aplicación, o archivo necesario para la inyección de dependencias en todas las capas. Inyecta por dependencia todas las dependencias necesarias para cada servicio, fábrica, repositorio y demás componentes del sistema. todo lo que pueda inyectarse por dependencia debe ser inyectado, y todo lo que no pueda inyectarse por dependencia debe ser refactorizado para poder inyectarse por dependencia.
- [ ] Usar `inject` para inyectar dependencias en servicios y mapeadores
- [ ] Añadir tipos de constructor y validaciones de DI
- [ ] Tests que usan mocks para simular repositorios y fábricas

**Código legacy a revisar/modificar/eliminar:**
- Instanciaciones directas de servicios y dependencias en servicios y dominio 

---

### 4.6 Mapeadores de Dominio a DTO
- [ ] Directorio `API/Mapeadores/`
- [ ] Clases estáticas: `PedidoMapper`, `RutaMapper`, `ClienteMapper`, `AlmacenamientoMapper`, `RecargaMapper`
- [ ] Mover lógica de conversión de `Dtos1`/`Dtos2` a mapeadores de forma modular
- [ ] Tests de mapeo bidireccional dominio↔DTO

**Código legacy a revisar/modificar/eliminar:**
- Argumentos primitivos pasados a `Simulacion.new` e `init` directamente

### 4.7 Auditoria de Código Legacy e integración de Nuevas Funcionalidades
- [ ] Revisar y eliminar código legacy en todo el sistema y capas que no cumpla con los nuevos patrones y funcionalidades desarrolladas en ese archivo.
- [ ] Revisar cada seccion de código legacy y determinar si es necesario modificar, eliminar o refactorizar para cumplir con los nuevos patrones de diseño y arquitectura.
- [ ] Priorizar siempre la implementación de las nuevas funcionalidades y patrones de diseño, implementaciones para conectar capas, y verificar que las nuevas implementaciones desarrolladas reemplacen completamente al código legacy en todas las capas, asegurando actualizacion, modularidad, patrones y arquitectura, solid y buenas practicas.

**Código legacy a revisar/modificar/eliminar:**
- Funciones utilitarias `pedido_a_dto`, `ruta_a_dto`, etc. en `Dtos1.py`

---

### 4.8 Patrón Observer
#### 4.8.1 Definición de eventos
- [ ] Clases de evento: `PedidoCreado`, `RutaCalculada`, `PedidoEntregado`, `EstadisticaActualizada`
- [ ] Definir atributos relevantes para cada evento (ej. `pedido_id`, `ruta_id`, `estadisticas`)
- [ ] Crear directorio `Eventos/` en `Backend/Infraestructura/`
- [ ] Implementar `__str__` para cada evento para facilitar logging y debugging
- [ ] Definir interfaz `IObserver` con método `actualizar(evento)`
- [ ] Crear clase base `Observable` con métodos `registrar_observador`, `eliminar_observador`, `notificar_observadores`
- [ ] Implementar `Observable` en `Simulacion` y `SimulacionDominioService`
- [ ] Integrar eventos en lógica de negocio:
  - `PedidoCreado` al crear un pedido
  - `RutaCalculada` al calcular una ruta
  - `PedidoEntregado` al completar un pedido
  - `EstadisticaActualizada` al actualizar estadísticas
- [ ] Registrar observadores en `Simulacion` y `SimulacionDominioService` para recibir eventos relevantes
- [ ] Implementar `Observer` en UI y módulo de estadísticas para recibir eventos y actualizar visualizaciones en tiempo real
- [ ] Crear tests unitarios para eventos y Observer
- [ ] Crear logica de estadísticas que se actualice en tiempo real a través de eventos para mostar unformación relevante en el dashboard y en la API.
#### 4.8.2 Implementación de `Observer`
- [ ] Suscripción: método `subscribirse(tipo_evento, manejador)`
- [ ] Desuscripción: método `desuscribirse(tipo_evento, manejador)`
- [ ] Notificación: método `notificar(evento)`
- [ ] Registro de observadores: método `registrar_observador(tipo_evento, observador)`
- [ ] Eliminación de observadores: método `eliminar_observador(tipo_evento, observador)`
- [ ] Implementar `Observer` en `Simulacion` y `SimulacionDominioService`
- [ ] Crear manejadores específicos para cada tipo de evento (ej. `PedidoCreadoManejador`, `RutaCalculadaManejador`, etc.)
- [ ] Publicación: método `publicar(instancia_evento)`
- [ ] Integrar eventos en lógica de negocio:
  - `PedidoCreado` al crear un pedido
  - `RutaCalculada` al calcular una ruta
  - `PedidoEntregado` al completar un pedido
  - `EstadisticaActualizada` al actualizar estadísticas
- [ ] Registrar observadores en `Simulacion` y `SimulacionDominioService` para recibir eventos relevantes
- [ ] Implementar `Observer` en UI y módulo de estadísticas para recibir eventos y actualizar visualizaciones en tiempo real
- [ ] Crear tests unitarios para eventos y Observer
- [ ] Crear lógica de estadísticas que se actualice en tiempo real a través de eventos para mostrar información relevante en el dashboard y en la API
- [ ] Integrar suscriptores en UI y módulo de estadísticas
- [ ] Tests de flujo de eventos

**Código legacy a revisar/modificar/eliminar:**
- Callbacks ad-hoc o prints dispersos en `Pedido`, `Simulacion`, `Servicios_Simulacion`

---



---

### 4.9 Refactorización de UI y Tests
- [ ] Actualizar `frontend/dashboard_v2.py` para usar repositorios y Observer, mapeadores y todo lo implementado en las mejoras hechas en este archivo
- [ ] Actualizar `main.py` y todos los routers para usar todos los nuevos patrones de diseño, inyección de dependencias, Observer, mapeadores y todo lo implementado en las mejoras hechas en este archivo, considera crear un `bootstrap.py` y elige la mejor forma de inyectar las dependencias en todos los routers y servicios.
- [ ] Actualizar `Tests/integracion`, `Tests/unitarios`, `Tests/rendimiento` y `Tests/e2e2` para incluir pruebas unitarias, de integracion, de rendimiento y e2e, de todas las nuevas funcionalidades, patrones de diseño, inyección de dependencias, Observer, mapeadores, repositorios, fabricas, eventos, Estrategias de algoritmos para las rutas y todo lo implementado en las mejoras hechas en este archivo.
- [ ] Actualiza el sistema para una total implementacion y utilizacion de los nuevos patrones de diseño, inyección de dependencias, Observer, mapeadores, repositorios, fabricas, eventos, Estrategias de algoritmos para las rutas y todo lo implementado en este archivo. Ten en cuenta implementar todas las mejoras y eliminar codigo legacy e inutilizable en todas las capas del sistema, asegurando que todo el sistema se adapte a los nuevos patrones de diseño y arquitectura.
- [ ] Verifica la necesidad de crear SimulacionConstructor utilizando el singleton de Simulacion, evalúa si hay que utilizar y crear una nueva clase SimulacionConstructor para inyectar las dependencias y crear instancias de `Simulacion` y `Grafo` de forma controlada y refactoriza de ser necesario.
- [ ] Verifica y haz una auditoria de Simulacion_dominio para saber si cumple con la arquitectura y patrones de diseño implementados, si no cumple, refactoriza para que cumpla con los nuevos patrones de diseño, inyección de dependencias, Observer, mapeadores, repositorios, fabricas, eventos, Estrategias de algoritmos para las rutas y todo lo implementado en este archivo, revisa además servicio_dominio y aplicacion_dominio.


**Código legacy a revisar/modificar/eliminar:**
- Cachés redundantes que repiten el mismo `@st.cache_data` en dashboard
- Acceso directo a datos sin pasar por servicios/mapeadores
- Tests en `Tests/` (unitarios, integración y e2e) que validan instanciación única, CRUD de repositorios, mapeos, estrategias y Observer

---

## 5. Arquitectura y Estructura de Archivos (Mermaid)

```mermaid
flowchart TD
    A[Docs]
    B[Backend]
    C[frontend]
    D[Tests]

    subgraph Backend
        B1[Dominio]
        B2[Infraestructura]
        B3[Aplicacion]
        B4[API]
        B5[Servicios]
        B6[Interfaces]
    end

    subgraph Infraestructura
        B2a[Modelos]
        B2b[TDA]
        B2c[Repositorios]
    end

    subgraph Repositorios
        B2c1[Interfaces]
        B2c2[RepositorioGrafo.py]
        B2c3[RepositorioPedido.py]
        B2c4[RepositorioCliente.py]
        B2c5[RepositorioAlmacenamiento.py]
        B2c6[RepositorioRecarga.py]
    end

    subgraph API
        B4a[DTOs]
        B4b[Mapeadores]
        B4c[main.py]
        B4d[simulacion_endpoints.py]
        B4e[rutas.py]
        B4f[clientes.py]
        B4g[almacenamientos.py]
        B4h[recargas.py]
        B4i[pedidos.py]
        B4j[estadisticas.py]
    end

    subgraph frontend
        C1[dashboard_v2.py]
        C2[dashboard.py]
    end

    subgraph Tests
        D1[unitarios]
        D2[integracion]
        D3[e2e]
    end

    A --> B
    B --> B1
    B --> B2
    B --> B3
    B --> B4
    B --> B5
    B --> B6
    B2 --> B2a
    B2 --> B2b
    B2 --> B2c
    B2c --> B2c1
    B2c --> B2c2
    B2c --> B2c3
    B2c --> B2c4
    B2c --> B2c5
    B2c --> B2c6
    B4 --> B4a
    B4 --> B4b
    B4 --> B4c
    B4 --> B4d
    B4 --> B4e
    B4 --> B4f
    B4 --> B4g
    B4 --> B4h
    B4 --> B4i
    B4 --> B4j
    C --> C1
    C --> C2
    D --> D1
    D --> D2
    D --> D3
```

---

Con este plan fusionado de auditoría y mejoras, se asegura una arquitectura robusta, escalable y alineada con los requisitos de `Requisitos.md` y mejores prácticas de diseño. Siempre ten en cuenta que la implementación debe seguir los principios SOLID y mantener una alta cohesión y bajo acoplamiento entre componentes inyectando dependencias adecuadamente en todo el sistema.

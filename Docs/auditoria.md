# Auditoría y Plan de Refactorización de Instanciación Única

Este documento describe de manera detallada y atomizada el plan de auditoría y refactorización para garantizar que todos los objetos centrales (Vértices, Aristas, Pedidos, Rutas y Grafo) se instancien una única vez y sean referenciados de forma consistente en todo el sistema.

## Objetivo
- Asegurar una única instancia por cada elemento del sistema.
- Evitar duplicidades, copias o instanciaciones erróneas.
- Garantizar el uso consistente de los TDA e Infraestructura como fuente de verdad.
- Aplicar patrones de diseño (Singleton, Factory, Dependency Injection) donde corresponda.
- Documentar pasos atómicos y detallados para su implementación.

## Alcance
Se revisarán las siguientes capas:
1. **TDA e Infraestructura** (Modelos de Grafo, Vértice, Arista, Map).
2. **Dominio** (Cliente, Almacenamiento, Recarga, Pedido, Ruta, Simulación).
3. **Fábrica de Pedidos** (FabricaPedidos).
4. **Servicios de Dominio y Aplicación**.
5. **DTOs y API**.
6. **Frontend** (Streamlit dashboard).
7. **Pruebas (Tests unitarios, integración, e2e)**.

---

## Paso 1: Auditoría de TDA e Infraestructura
1.1. Revisar `Modelo_Vertice.py` y `Modelo_Arista.py`:
   - Verificar que `__hash__`, `__eq__` y atributos sean consistentes para evitar instancias duplicadas en colecciones.
   - Confirmar que no se creen clones de vértices o aristas en métodos de grafo.
1.2. Revisar `Modelo_Grafo.py`:
   - Asegurar que al insertar o buscar vértices, siempre se devuelva la misma instancia.
   - Validar que los métodos `buscar_vertice_por_elemento` y `insertar_vertice` no dupliquen instancias.
   - Garantizar que las colecciones internas (`_adyacentes`, `_entrantes`) almacenen referencias únicas.
1.3. Inspeccionar `TDA-Map.py` y su adaptación en `Infraestructura/TDA`:
   - Verificar que el mapa (`HashMap`) contenga referencias a objetos únicos.
   - Validar operaciones de inserción y eliminación para no re-instantiar claves/valores.

## Paso 2: Auditoría de Objeto Grafo
2.1. Patrón Singleton para la clase `Simulacion.grafo`:
   - Confirmar que la simulación crea solo una instancia de grafo.
   - Revisar `reiniciar_instancia` y el constructor para reinicializar grafo correctamente.
2.2. Colección de Vértices y Aristas:
   - Comprobar que al generar nodos/aristas se invoca únicamente métodos de `Grafo`.
   - Revisar `_generar_nodos` y `_generar_aristas` para evitar nuevas instancias de vértices con elementos duplicados.

## Paso 3: Auditoría de Entidades del Dominio
3.1. **Clientes, Almacenamientos y Recargas**:
   - Verificar que cada entidad se crea una sola vez durante la simulación.
   - Confirmar que la relación entre vértice y entidad use siempre el mismo objeto.
3.2. **Pedidos**:
   - Revisar `FabricaPedidos` y `Pedido.__init__`:
     - Confirmar que la fábrica devuelva la misma instancia de `Pedido` para un `id_pedido` dado si ya existe.
     - Aplicar patrón _Multiton_ o _Registry_ si es necesario.
3.3. **Rutas**:
   - Asegurar que la creación de objetos `Ruta` se realice vía fábrica o método único.
   - Verificar que la asignación de `ruta` en un pedido guarde la misma instancia.

## Paso 4: Integración de Fábrica y Singleton
4.1. **Implementar un registro global** para instancias de `Pedido`, `Ruta` y `Cliente` en `FabricaPedidos` y servicios de dominio.
4.2. **Patrón Dependency Injection**:
   - Inyectar servicios de grafo y fábrica en las capas de aplicación y API.
4.3. Asegurar que `Simulacion.obtener_instancia()` se use en todas las capas y no se creen nuevas simulaciones.

## Paso 5: Refactorización de Servicios
5.1. **Servidores de Dominio** (`Servicios_Simulacion`):
   - Verificar que recuperen las instancias de Simulación y no creen nuevas colecciones.
   - Depurar cualquier re-instanciación accidental de listas o mapas.
5.2. **Servicios de Aplicación** (`SimulacionAplicacionService`):
   - Asegurar que todas las llamadas utilicen instancias inyectadas.
   - Aplicar principios SOLID: Single Responsibility, Open/Closed.

## Paso 6: DTOs y Serialización
6.1. **Mapeo de objetos a DTOs**:
   - Validar que se extraigan referencias de los objetos originales (id, atributos) sin duplicar instancias.
   - Revisar funciones `*_a_dto` para no crear nuevos objetos de dominio.
6.2. **Consistencia de datos**:
   - Confirmar que fechas, rutas y estados correspondan a las instancias reales.

## Paso 7: Frontend
7.1. **Cache y estado**:
   - Asegurar que las funciones `@st.cache_data` referencien IDs y no instancias serializadas.
7.2. **Visualización de Grafo y Árbol AVL**:
   - Verificar que utilicen referencias consistentes a nodos y rutas.
7.3. **Interacción con API**:
   - Comprobar que no se generen nuevas instancias al renderizar tablas o gráficas.

## Paso 8: Pruebas y Validación
8.1. **Tests unitarios**:
   - Crear pruebas que aseguren que, tras múltiples consultas, `is` (mismo objeto) sea True.
8.2. **Tests de integración y E2E**:
   - Verificar consistencia de instanciación al recorrer endpoints.
8.3. **Cobertura de auditoría**:
   - Agregar pruebas que registren y validen errores en `FabricaPedidos.errores`.

## Paso 9: Documentación y Guía de Implementación
9.1. Agregar comentarios en cada módulo explicando el patrón de instanciación única.
9.2. Ordenar y numerar pasos en este documento para guiar la implementación.
9.3. Enlazar a `Docs/Requisitos.md` y `Docs/pedidosverdad.md` como referencias.

---

**¡Con este plan detallado podrá realizarse la auditoría y refactorización garantizando la única instanciación y referencia consistente de todos los objetos centrales!**

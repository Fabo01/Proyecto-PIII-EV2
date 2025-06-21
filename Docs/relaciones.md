# Plan de Relaciones y Solución de Serialización Detallada

## Objetivo
Crear una estrategia clara y atomizada para definir y mapear las relaciones entre Clientes, Almacenamientos y Pedidos en toda la capa de respuesta y mapeadores, evitando importaciones circulares y garantizando coherencia con la arquitectura y patrones SOLID.

---

### Paso 1: Identificar Relaciones y Dependencias
1. Cliente ↔ Pedido
   - Un Cliente contiene **varios** Pedidos.
   - Un Pedido referencia un **único** Cliente.
2. Almacenamiento ↔ Pedido
   - Un Almacenamiento contiene **varios** Pedidos.
   - Un Pedido referencia un **único** Almacenamiento.
3. Recarga y Ruta
   - Recarga es un vértice independiente (no bidireccional con Pedido, similar a Almacenamiento o Cliente).
   - Ruta contiene orígenes y destinos como vértices (Cliente, Almacenamiento o Recarga).

### Paso 2: Diseñar DTOs sin Ciclos
1. En cada DTO de respuesta, usar **anotaciones de cadena** (string forward refs) para referenciar otros DTOs.
2. Evitar `TYPE_CHECKING` como única forma de romper el ciclo: registrar forward refs explícitamente en cada archivo con:
   ```python
   DTOClase.update_forward_refs(
       Pedidos=RespuestaPedido,
       Cliente=RespuestaCliente,
       Almacenamiento=RespuestaAlmacenamiento,
       Ruta=RespuestaRuta
   )
   ```

### Paso 3: Refactorizar Mapeadores para DTOs Anidados
3.1. Crear interfaz `IMapeador` en `Infraestructura/Mapeadores/IMapeador.py` con método `a_dto(entidad)->DTO`.
3.2. Cada mapeador (`MapeadorCliente`, `MapeadorAlmacenamiento`, `MapeadorRecarga`, `MapeadorPedido`, `MapeadorRuta`, etc...):
    - Implementar `IMapeador`.
    - Asegurar que `a_dto` reciba flags de inclusión (p.ej. `incluir_pedidos`, `incluir_cliente`) para romper recursividad.
    - Utilizar forward refs en DTOs y `update_forward_refs()` tras su definición.
3.3. Validar la transformación inversa si existe (DTO -> dominio) o aislarla en otro mapper.

## Paso 4: Actualizar Dominio y Servicios
4.1. **Dominio** (`Simulacion_dominio.py` y entidades):
    - Quitar dependencias directas a DTOs.
    - Exponer colecciones de vértices y pedidos como objetos de dominio.
    - Asegurar métodos para obtener `vertice.elemento()`.

4.2. **Servicios de dominio** (`Servicios/SimServicios/Servicios_Simulacion.py`):
    - Inyectar estrategia de ruta y mapeadores.
    - En cada método de respuesta (`obtener_clientes`, `obtener_pedidos`, etc.), usar mapeadores para devolver DTOs completos.
    - Manejar errores y casos extremos (sin datos, rutas nulas).

## Paso 5: Actualizar Endpoints y Controladores
5.1. En cada endpoint de `Backend/API/*.py`:
    - Eliminar serialización manual.
    - Llamar al servicio de dominio para obtener DTOs.
    - Devolver instancias de DTO anidados (no IDs simples).
5.2. Añadir Pydantic `Config(from_attributes=True)` en DTOs donde se lean atributos de dominio.
5.3. Ajustar validaciones y ejemplos de esquema en OpenAPI.

## Paso 6: Verificación y Puesta a Punto
6.1. **Pruebas Unitarias y de Integración**:
    - Ajustar tests de DTOs (`test_mapeador_*`) para validar objetos complejos.
    - Validar modelos Pydantic con forward refs y `update_forward_refs()`.
6.2. **Pruebas de API**:
    - Ejecutar `pytest Tests/Test_Mapeadores` y `Tests/Test_Dominio`.
    - Probar endpoints con `curl` o Swagger UI.
6.3. Documentar cualquier cambio adicional en `serializacion.md` y `auditorias.md`.
6.4. Revisar circularidades residuales y corregir importaciones en módulos afectados.

---

> Con este plan atomizado, podremos romper ciclos de importación, mantener alta cohesión y bajo acoplamiento, y asegurar la correcta serialización de objetos completos y válidos.
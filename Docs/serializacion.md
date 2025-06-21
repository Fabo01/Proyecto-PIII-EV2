# Plan de Refactorización para Serialización de Objetos Completos

## Objetivo
Refactorizar el sistema para que los datos transferidos entre capas y expuestos por la API sean objetos completos (DTOs anidados), no solo IDs. Esto permitirá una mayor robustez, escalabilidad y alineación con los lineamientos de `Requisitos.md` y `auditorias.md`.

---

## 1. Modificación de DTOs de Respuesta
- **Ubicación:** `Backend/API/DTOs/DTOsRespuesta/`
- **Acción:**
  - Cambiar los campos que actualmente son `List[int]` o `int` por listas u objetos de los DTOs correspondientes.
  - Ejemplo: En `RespuestaCliente`, cambiar `pedidos: List[int]` por `pedidos: List[RespuestaPedido]`.
  - En `RespuestaPedido`, los campos `id_cliente`, `id_almacenamiento`, `origen`, `destino` deben ser objetos DTO, no enteros. Las posiciones y referencias a otros vértices, aristas u objetos deben hacerse correctamente para mantenerse la referencia de los objetos.
- **Archivos a modificar:**
  - `RespuestaCliente.py`, `RespuestaPedido.py`, `RespuestaAlmacenamiento.py`, etc.., es necesario recorrer todos los archivos en `Backend/API/DTOs/DTOsRespuesta/` y modificarlos correctamente.
  - Eliminar/ajustar los campos legacy que solo usan IDs.

## 2. Refactorización de Mapeadores
- **Ubicación:** `Backend/Infraestructura/Mapeadores/`
- **Acción:**
  - Actualizar los métodos de mapeo para que utilicen los mapeadores de los objetos anidados.
  - Ejemplo: `MapeadorCliente.a_dto` debe mapear cada pedido usando `MapeadorPedido.a_dto`.
  - Evitar referencias circulares (ej: un pedido incluye cliente, que incluye pedidos, etc.).
  - Asegurarse de que los mapeadores devuelvan objetos completos, no solo IDs en las posiciones y referencias a otros vertices y objetos, para mantener las referencias unicas.
- **Archivos a modificar:**
  - `MapeadorCliente.py`, `MapeadorPedido.py`, `MapeadorAlmacenamiento.py`, etc.., es necesario recorrer todos los archivos en `Backend/Infraestructura/Mapeadores/` y modificarlos correctamente.
  - Eliminar lógica legacy que solo serializa IDs.

## 3. Actualización de Dominio y Endpoints
- **Ubicación:** `Backend/Dominio/`, `Backend/API/`
- **Acción:**
  - Adaptar el dominio para trabajar con los nuevos DTOs anidados.
  - Asegurarse de que los endpoints utilicen los nuevos DTOs en sus respuestas
  - Asegurarse de que los endpoints y Dominio devuelvan objetos completos, no solo IDs en las posiciones y referencias a otros vertices y objetos, para mantener las referencias unicas.
- **Archivos a modificar:**
  - `clientes.py`, `pedidos.py`, `almacenamientos.py`, `simulacion_endpoints.py`, etc es necesario recorrer todos los archivos en `Backend/API/` y modificarlos correctamente.
  - `Simulacion_Dominio`, `Dominio_Cliente`, `Dominio_Pedido`, etc., es necesario recorrer todos los archivos en `Backend/Dominio/` y modificarlos correctamente.

  ## 4. Actualización de Servicios y Aplicacion
- **Ubicación:** `Backend/Aplicacion/`, `Backend/Servicios/`
- **Acción:**
  - Adaptar los servicios y endpoints para trabajar con los nuevos DTOs anidados, manteniendo las referencias de posiciones y objetos creados.
  - Asegurarse de que los endpoints devuelvan la estructura completa y correcta, manteniendo las referencias únicas de posiciones y objetos creados.
- **Archivos a modificar:**
  - `Aplicacion_Simulacion.py`, etc es necesario recorrer todos los archivos en `Backend/Aplicacion/` y modificarlos correctamente
  - `Servicios_Simulacion`, etc es necesario recorrer todos los archivos en `Backend/Servicios/` y modificarlos correctamente.
  - Eliminar/ajustar lógica legacy de serialización plana.

## 5. Actualización de Dominio y Endpoints
- **Ubicación:** `Backend/Dominio/`, `Backend/API/`
- **Acción:**
  - Adaptar el dominio para trabajar con los nuevos DTOs anidados.
  - Asegurarse de que los endpoints utilicen los nuevos DTOs en sus respuestas
  - Asegurarse de que los endpoints y Dominio devuelvan objetos completos, no solo IDs en las posiciones y referencias a otros vertices y objetos, para mantener las referencias unicas.
- **Archivos a modificar:**
  - `clientes.py`, `pedidos.py`, `almacenamientos.py`, `simulacion_endpoints.py`, etc es necesario recorrer todos los archivos en `Backend/API/` y modificarlos correctamente.
  - `Simulacion_Dominio`, `Dominio_Cliente`, `Dominio_Pedido`, etc., es necesario recorrer todos los archivos en `Backend/Dominio/` y modificarlos correctamente.

## 6. Documentación y Auditoría
- **Ubicación:** `Docs/`
- **Acción:**
  - Documentar el nuevo flujo de serialización y los cambios realizados.
  - Actualizar los checklists de auditoría para reflejar la nueva estructura.
- **Archivos a modificar/agregar:**
  - `serializacion.md` (este archivo), `auditorias.md`, `Requisitos.md` (si aplica).

---

## Referencias a Código Legacy a Eliminar o Modificar
- Todos los campos en DTOs y mapeadores que solo usan IDs para relaciones deben ser eliminados o refactorizados.
- Ejemplo: `pedidos: List[int]` → `pedidos: List[RespuestaPedido]`.
- Métodos de mapeo que devuelven solo IDs deben ser reemplazados por métodos que devuelvan objetos completos.

---

## Consideraciones de Diseño
- Mantener la modularidad y separación de responsabilidades.
- Evitar referencias circulares profundas en la serialización.
- Seguir las convenciones de código en español y la arquitectura definida.

---

## Checklist de Integración
- [ ] DTOs modificados para objetos completos.
- [ ] Mapeadores refactorizados para serialización anidada.
- [ ] Endpoints y servicios adaptados.
- [ ] Tests actualizados.
- [ ] Documentación y auditoría revisadas.

---

Este plan debe ser seguido de forma iterativa y auditada según los lineamientos de `auditorias.md` y `Requisitos.md`.

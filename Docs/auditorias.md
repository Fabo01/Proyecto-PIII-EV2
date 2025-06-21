# Plan de Auditoría Integral para Simulación Drones - Correos Chile

**Objetivo:**
Describir de manera atomizada los pasos y criterios de auditoría para garantizar cohesión, coherencia y cumplimiento de los lineamientos de `Requisitos.md` en todas las capas de la arquitectura.

---

## 1. Capa de Infraestructura

1.1. TDA (Estructuras de Datos)
- TDA_Hash_map.py:
  - Verificar implementación de métodos `insertar`, `buscar`, `eliminar`.
  - Confirmar unicidad de referencias y acceso O(1).
  - Comprobar nombres en snake_case y docstrings en español.
- TDA_AVL.py:
  - Auditar métodos `insertar`, `_insertar`, rotaciones y balanceo.
  - Validar manejo de frecuencias de rutas y validez de vertices.

1.2. Modelos
- Modelo_Vertice.py:
  - Revisar que almacene solo `_elemento` y no contenga lógica de dominio.
  - Confirmar métodos de acceso y nomenclatura.
- Modelo_Arista.py:
  - Verificar definición de `__slots__` y atributos `_origen`, `_destino`, `_peso`.
- Modelo_Grafo.py:
  - Auditar unicidad de instanciación de vertices y aristas.
  - Confirmar uso de repositorios y fábricas.

1.3. Repositorios
- repositorio_vertices.py, repositorio_aristas.py, repositorio_clientes.py, repositorio_pedidos.py, repositorio_almacenamientos.py, repositorio_recargas.py:
  - Confirmar implementación de IRepositorioX (agregar, obtener, eliminar, todos, limpiar).
  - Verificar uso de HashMap y consistencia de claves.

1.4. Mapeadores
- MapeadorCliente.py, MapeadorAlmacenamiento.py, MapeadorRecarga.py, MapeadorPedido.py, MapeadorRuta.py:
  - Validar métodos `a_dto` y correspondencia con DTOs de respuesta.
  - Comprobar inyección de dependencias y patrones Mapper.

---

## 2. Capa de Dominio

2.1. Entidades de negocio
- Dominio_Cliente.py, Dominio_Almacenamiento.py, Dominio_Pedido.py, Dominio_Recarga.py, Dominio_Ruta.py:
  - Revisar constructores (`__init__`) y firmas de métodos coincidentes con uso en fábrica y repositorio.
  - Comprobar separación lógica: clientes gestionan pedidos, vértices gestionan posición.
  - Validar docstrings en español y sin acentos.

2.2. Simulación
- Simulacion_dominio.py:
  - Confirmar patrón Singleton y acceso a grafo, clientes y pedidos.
  - Auditar inyección de estrategia y lógica de orquestación.

---

## 3. Capa de Servicios

3.1. Fábricas de Entidades
- FabricaVertices, FabricaAristas, FabricaClientes, FabricaPedidos, FabricaRecargas:
  - Revisar métodos de creación y aseguramiento de unicidad.
  - Verificar uso de repositorios para instanciación única.

3.2. Servicios de Dominio
- Servicios_Simulacion.py y cualquier ISimulacionDominioService:
  - Auditar contratos de interfaz y su cumplimiento.
  - Confirmar desacoplamiento de lógica de simulación y API.

---

## 4. Capa de Aplicación

4.1. Servicios de Aplicación
- Aplicacion_Simulacion.py e ISimulacionAplicacionService:
  - Verificar métodos expuestos a la API.
  - Comprobar transformaciones entre dominio y DTOs.
  - Validar manejo de errores y excepciones.

---

## 5. Capa de API

5.1. Endpoints y routers
- archivos en Backend/API: clientes.py, pedidos.py, rutas.py, rutas_algoritmos.py, recargas.py, almacenamientos.py, estadisticas.py, simulacion_endpoints.py, main.py:
  - Auditar rutas, verbos HTTP y modelos de request/response.
  - Confirmar response_model y validaciones Pydantic.
  - Verificar coherencia con BaseModel y RespuestaX.

5.2. DTOs
- DTOs/BaseX.py y DTOsRespuesta/RespuestaX.py:
  - Validar alineación de campos con entidades de dominio.
  - Confirmar tipos correctos y uso de Optional donde aplica.

---

## 6. Capa de Frontend

- dashboard_v2.py:
  - Comprobar llamadas API desacopladas (`api_get`, `api_post`) y cache.
  - Validar nombres en snake_case, docstrings, y visualización con matplotlib y networkx.
  - Auditar manejo de errores y UX.

---

## 7. Patrones y Principios SOLID

- Verificar implementación de:
  - Singleton (Simulación, repositorios).
  - Factory (Fábricas de entidades).
  - Repository (Repositorios centralizados).
  - Strategy (Estrategias de rutas).
  - Observer (notificaciones en simulación si aplica).
  - Dependency Injection (inyección de servicios).
- Confirmar adherencia a principios SOLID en cada capa.

---

## 8. Pruebas y Calidad

- Repositorio Tests/:
  - Unitarios, integración, E2E y performance tests.
  - Auditar cobertura para cada módulo y capa.

---

## 9. Documentación y Mantenimiento

- Revisar `Docs/Requisitos.md`, `Docs/mejoras.md` y restante en `Docs/Documentacion/`:
  - Confirmar que el código implementa los requisitos.
  - Verificar consistencia de versiones y comentarios.

---

## 10. Objetivo final de la auditoría

El objetivo principal de esta auditoría es conectar todas las capas de la arquitectura en su totalidad, asegurando coherencia y cohesión entre ellas y garantizando que la integración de Infraestructura, Dominio, Servicios, Aplicación, API y Frontend cumpla con los lineamientos de `Requisitos.md`.

---

**Proceso iterativo:** aplicar checklist en revisiones de código, pull requests y pruebas automatizadas para garantizar que cada punto sea auditado y corregido si es necesario.
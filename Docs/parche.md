# Análisis y posibles soluciones al problema de pedidos no listados correctamente

## Descripción del problema
- La fábrica de pedidos (`FabricaPedidos`) crea y valida pedidos correctamente, registrando errores si algún dato es inválido.
- El log muestra que los pedidos se crean y asocian correctamente a clientes y almacenamientos.
- Sin embargo, al consultar `/pedidos/`, la lista de pedidos aparece vacía o con datos incompletos, y la tabla de errores también está vacía.
- Los errores se verifican correctamente, solo que se deja pasar en la fabrica las instancias de pedidos incompletos, con valores none, no está mal, pero deben de añadirse a la tabla de errores.

## Posibles causas
1. **Pedidos no agregados a la lista principal**: Aunque la fábrica retorna un pedido válido, puede que no se agregue correctamente a la lista `self.pedidos` de la simulación.
2. **Referencia incorrecta de vértices**: Si los vértices de origen/destino se pierden o se reasignan, los métodos de obtención pueden fallar y devolver `None`, .
3. **Problemas de serialización o mapeo**: El mapeador puede estar esperando atributos que no existen o que han sido sobrescritos.
4. **Repositorios singleton no reseteados**: Si los repositorios no se limpian correctamente entre simulaciones, pueden quedar referencias cruzadas o inconsistentes.
5. **Errores de sincronización entre DTO y modelo**: Si el DTO espera datos que no se han actualizado en el modelo, el mapeo puede fallar silenciosamente.

## Acciones recomendadas
- Verificar que cada pedido creado y retornado por la fábrica se agregue a `self.pedidos` y a los repositorios.
- Asegurar que los métodos `obtener_origen` y `obtener_destino` de `Pedido` siempre devuelvan objetos válidos.
- Añadir logs y validaciones en el mapeador para detectar si algún campo clave es `None` antes de mapear.
- Limpiar todos los repositorios singleton antes de iniciar una nueva simulación.
- Si un pedido no puede mapearse correctamente, debe registrarse como error en la tabla de errores de pedidos.
- Documentar y testear con datos mínimos para asegurar que la cadena de creación → mapeo → API → frontend es robusta.

## Próximos pasos
1. Refactorizar la función de generación y listado de pedidos para filtrar y registrar cualquier pedido incompleto.
2. Añadir logs detallados en el mapeador y en la API para identificar en qué punto se pierden los datos.
3. Validar la limpieza de repositorios y el ciclo de vida de los objetos entre simulaciones.
4. Probar la API con casos límite y revisar la tabla de errores tras cada simulación.

---

Este análisis debe ser revisado y actualizado tras aplicar los parches y observar el comportamiento en la siguiente simulación.

### Contexto General

Estás trabajando en un proyecto de simulación de drones que conecta:

- **Almacenes**
- **Clientes**
- **Puntos de recarga**

Utilizamos un TDA Grafo obligatorio para modelar la red, y guardamos en memoria y persistencia solo las entidades y aristas que forman un grafo válido desde el inicio.

### Nuevo Requisito de Peso y Segmentación

Para cada par *(almacén, cliente)* debe existir un camino en el grafo compuesto por uno o más **segmentos**, donde cada segmento corresponde a una subsecuencia de vértices que va de:

- almacén → punto de recarga
- recarga → recarga
- recarga → cliente
- **o** cliente → cliente (p. ej. almacén1→cliente1→cliente2→...→clienteObjetivo)

**Regla:** en ningún segmento la suma de los pesos de aristas recorridas debe exceder **50**. Entre un almacén y un cliente puede haber múltiples segmentos, cuya suma total de pesos **sí** puede superar 50, siempre que cada segmento individual resetee el contador en un punto de recarga.

- Si un recorrido directo entre almacén y cliente excede 50, se debe incluir al menos un vértice de recarga en el recorrido para reiniciar el conteo.
- Si un recorrido pasa por varios clientes antes de llegar al objetivo, cada tramo entre reinicios no supera 50.
- Los segmentos pueden encadenarse indefinidamente, pero ninguno debe exceder el límite.

### Gestión de Aristas y Conectividad Mínima

- Durante la **generación inicial** del grafo, se calculan todas las posibles aristas candidatas.
- Las aristas que no permiten formar **ningún** camino válido entre **algún** par almacén‑cliente deben ser **eliminadas** de repositorios y hashmaps.
- **Importante:** Las aristas descartadas **no deben** restar del contador de `m_aristas` que representa la meta de aristas a incluir en el grafo.
- Una vez filtradas, `m_aristas` debe reflejar el número exacto de aristas válidas que se agregarán, manteniendo:
  - **n–1** aristas para el árbol mínimo segmentado.
  - **m** aristas totales para el grafo completo.
- **Problema actual:** el algoritmo de construcción consume el presupuesto de `m_aristas` incluso al intentar y descartar aristas inválidas, lo que puede agotar las iteraciones antes de completar el árbol mínimo y lanzar error de conectividad.

### Puntos Clave para la Refactorización

1. **Generación Inicial del Grafo**
   - Diseñar un algoritmo que genere el grafo **completo y válido** desde el inicio, asegurando rutas segmentadas ≤50.
   - Elegir entre:
     - Grafo virtual que valida y ajusta antes de persistir.
     - Grafo real que agrega y elimina entidades en tiempo de creación.
2. **Validación y Segmentación**
   - Al insertar cada arista, verificar su contribución a posibles segmentos.
   - Garantizar rutas viables mediante puntos de recarga.
3. **Mantenimiento de **``** y Conectividad**
   - Ajustar la lógica de conteo para **no decrementar** el presupuesto de aristas al descartar inválidas.
   - Separar el concepto de "intentos" de inserción de aristas del conteo de `m_aristas` efectivo.
   - Después de filtrar, usar `m_aristas` para:
     - Construir un árbol mínimo segmentado (n–1 aristas).
     - Completar el grafo con aristas adicionales hasta `m_aristas`.
4. **Gestión de Intentos vs. Inserciones**
   - Implementar un mecanismo de reintentos ilimitado para descartar y volver a intentar aristas hasta encontrar válidas, sin consumir el presupuesto real.
   - Asegurar que las aristas descartadas por lógica no reduzcan el contador de `m_aristas`.
5. **Persistencia y Limpieza**
   - Almacenar únicamente entidades y aristas que formen parte de algún camino válido.
   - Eliminar permanentemente las que no se usan.
6. **Implementación en **``
   1. Generar todas las aristas candidatas.
   2. Filtrar las inválidas según las reglas de segmentos.
   3. Ajustar `m_aristas` al recuento de aristas filtradas.
   4. Construir el árbol mínimo segmentado con n–1 aristas usando solo ingresos válidos.
   5. Reintentar generación de aristas adicionales hasta alcanzar `m_aristas` válidas.
   6. Verificar conectividad completa para cada almacén‑cliente.

### Requisitos.md

Mantente alineado con el contenido de `Requisitos.md` del proyecto.

```text
Eres un ingeniero de software con experiencia en TDA Grafo, conectividad de red y principios SOLID. Refactoriza el método `iniciar_simulacion` de la clase `Simulacion` en `simulacion_dominio` para que:

1. Para cada par (almacén, cliente) exista un camino válido segmentado, donde ningún segmento supere 50 en suma de pesos.
2. Cada segmento corresponde a tramos entre almacén, clientes o recargas que reinician el contador.
3. Las aristas descartadas por no cumplir autonomía **no resten** del presupuesto `m_aristas`.
4. `m_aristas` refleje exactamente el número de aristas válidas tras el filtrado.
5. Separar el conteo de intentos de inserción de aristas del presupuesto real, permitiendo reintentos ilimitados.
6. Construir primero un árbol mínimo segmentado con n–1 aristas y luego agregar hasta `m_aristas` válidas.
7. El grafo se construya **completo y correcto** desde el inicio, sin limpiezas posteriores necesarias.
8. Se use obligatoriamente el TDA Grafo.
9. Se sigan los detalles de `Requisitos.md`.

Pasos sugeridos:
1. Inspeccionar estructuras de datos y repositorios actuales.
2. Diseñar algoritmo de generación y filtrado de aristas segmentadas.
3. Implementar validaciones por segmento al insertar aristas.
4. Refactorizar `iniciar_simulacion` para:
   - Generar y filtrar aristas.
   - Ajustar `m_aristas` sin descontar inválidas.
   - Implementar reintentos ilimitados de inserción.
   - Verificar conectividad n–1 y m.
5. Añadir pruebas unitarias que cubran casos de rechazo y reintentos de aristas.

Entrega el prompt en Markdown listo para incorporar en tu tablero de tareas.
```


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
- Si un recorrido pasa por varios clientes antes de llegar al objetivo, cada tramo entre reinicios (puntos de recarga) no supera 50.
- Los segmentos pueden encadenarse indefinidamente, pero ninguno debe exceder el límite.

### Gestión de Aristas y Conectividad Mínima

- Durante la **generación inicial** del grafo, se calculan todas las posibles aristas. Las aristas que no permiten formar **ningún** camino válido entre **algún** par almacén‑cliente deben ser **eliminadas** de repositorios y hashmaps.
- Evitar que aristas inútiles permanezcan en memoria o persistencia.
- **Problema detectado:** al iniciar la simulación con `m_aristas` (número objetivo de aristas), las aristas eliminadas ya no cuentan, reduciendo el total real y pudiendo bajar por debajo de **n–1**, comprometiendo la conectividad mínima.

### Puntos Clave para la Refactorización

1. **Generación Inicial del Grafo**
   - Diseñar un algoritmo que genere el grafo **completo y válido** desde el inicio y asegure conectividad con segmentos ≤50.
   - Elegir entre:
     - Grafo virtual que valide y ajuste antes de persistir.
     - Grafo real que agrega y borra aristas/vértices válidos en tiempo de creación.
2. **Validación y Segmentación**
   - Al insertar cada arista, verificar su contribución a posibles segmentos.
   - Garantizar rutas viables (posibles segmentaciones con recarga).
3. **Mantenimiento de **``** y Conectividad Mínima**
   - Ajustar la lógica de conteo para incluir solo aristas válidas en `m_aristas`.
   - Asegurar que tras eliminar aristas inútiles, el grafo mantenga al menos **n–1** aristas útiles.
4. **Persistencia y Limpieza**
   - Almacenar exclusivamente entidades y aristas que formen parte de algún camino válido.
   - Eliminar permanentemente las aristas y vértices no usados.
5. \*\*Implementación en \*\*``
   - Refactorizar para que la **construcción inicial** del grafo:
     1. Calcule todas las aristas candidatas.
     2. Filtre las inválidas según reglas de segmentos.
     3. Ajuste el conteo de `m_aristas` al total de válidas.
     4. Asegure conectividad (n–1 aristas, rutas para cada almacén-cliente).
     5. No requiera limpiezas posteriores para cumplir requisitos.

### Requisitos.md

Mantente alineado con el contenido de `Requisitos.md` del proyecto.

---

### Prompt Final

```text
Eres un ingeniero de software con experiencia en TDA Grafo, conectividad de red y principios SOLID. Refactoriza el método `iniciar_simulacion` de la clase `Simulacion` en `simulacion_dominio` para que:

1. Para cada par (almacén, cliente) exista un camino válido segmentado, donde ningún segmento supere 50 en suma de pesos.
2. Cada segmento corresponde a tramos entre almacén, clientes o entre recargas que reinician el contador.
3. Las aristas que no contribuyen a **ningún** camino válido sean eliminadas desde la generación inicial.
4. `m_aristas` refleje el número de aristas válidas tras el filtrado, garantizando al menos **n–1** para conectividad mínima.
5. El grafo se construya **completo y correcto** desde el inicio, sin modificaciones parciales.
6. Se use obligatoriamente el TDA Grafo.
7. Se sigan los detalles de `Requisitos.md`.

Pasos sugeridos:
1. Inspeccionar estructuras de datos y repositorios actuales.
2. Diseñar algoritmo de generación y filtro de aristas segmentadas.
3. Implementar validaciones por segmento al insertar aristas.
4. Refactorizar `iniciar_simulacion` para:
   - Generar y filtrar aristas.
   - Ajustar `m_aristas`.
   - Verificar conectividad n–1.
5. Añadir pruebas unitarias que cubran casos extremos de segmentación.

```


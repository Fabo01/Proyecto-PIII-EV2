la arista almacena referencias a objetos Vertice, y cada Vertice contiene como atributo _elemento un objeto de tipo Cliente, Almacenamiento o Recarga, cada uno con su propio atributo de ID (id_cliente, id_almacenamiento, id_recarga) y un atributo común tipo_elemento.

El grafo se construye y persiste con objetos únicos de vértices y aristas.
Las aristas almacenan referencias a objetos Vertice.
Cada Vertice almacena el objeto de dominio real.
Los repositorios aseguran unicidad y acceso O(1).
La simulación y el resto del sistema operan siempre sobre los objetos reales.
Los endpoints y serializadores exponen los datos usando los IDs reales.




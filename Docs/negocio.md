# Plan de Implementación de Lógica de Negocio y Observadores

Este documento define de forma atomizada los pasos necesarios para implementar completamente la lógica de negocio y el patrón observer, garantizando un sistema modular, escalable y coherente de acuerdo a los lineamientos de `Requisitos.md`.

---

## 0. Preparación y referencias
1. Leer y comprender `Docs/Requisitos.md` como fuente de verdad.
2. Revisar las implementaciones previas en `Docs/estrategias.md`, `Docs/mejoras.md`, `Docs/parche.md` y `Docs/relaciones.md` para contexto.
3. Configurar entorno Python y dependencias necesarias.
4. Asegurar que el proyecto sigue los principios SOLID y Clean Architecture.
5. Es importante iterar por cada entidad e iterar por todos los métodos totalmente necesarios e implementarlos en la lógica de negocio y dominio, asegurando que cada método necesario esté implementado y documentado correctamente, siguiendo los lineamientos de `Requisitos.md`.
6. Ten en cuenta que cada entidad cuenta con unicidad en el sistema, por lo que cada entidad debe ser única y no duplicada,asegurando referenciar correctamente cada entidad creada y sus relaciones, evitando ciclos de importación y referencias circulares. 
7. Respecto a lo anterior, ten en cuenta que cada vertice, a nivel de dominio, no cuenta con atributos de origen ni dominio, estas referencias se deben manejar con el hashmap para mapear los vertices y aristas en el grafo. 
8. Cada vertice contiene un atributo `_elemento` que referencia a la entidad de dominio, como `Cliente`, `Almacenamiento`, `Recarga`, etc. No debe contener atributos de origen ni dominio, ya que no contiene estos atributos.
9. Cada Arista contiene un atributo `_peso` que representa el peso de la arista, el cual segun logica de negocia critica nunca puede ser mas de 50 en ningun recorrido, sí tiene atributos de origen y destino, estos son los vertices que conecta en cada extremo de la arista, los cuales son objetos `Vertice` que contienen el atributo `_elemento` que referencia a la entidad de dominio, como `Cliente`, `Almacenamiento`, `Recarga`, etc., formando así las posiciones relativas, quedando guardado en `self.origen` y `self.destino` y pudiendo documentar y acceder a esas posiciones a través de los métodos `get_origen()` y `get_destino()`, los cuales retornan el objeto `Vertice` correspondiente, que contiene el atributo `_elemento` que referencia a la entidad de dominio, como `Cliente`, `Almacenamiento`, `Recarga`, etc. Además el hashmap O1 permite acceder a los vertices y aristas de forma eficiente, asegurando que cada entidad es única y no duplicada en el sistema, aprovechando las ventajas de las estructuras de datos hash para un acceso rápido y eficiente a las entidades y sus relaciones.
10. Cada Cliente, Almacenamiento y Recarga contiene un atributo `tipo_elemento` que indica su tipo, por ejemplo, `tipo_elemento = 'cliente'`, `tipo_elemento = 'almacenamiento'`, `tipo_elemento = 'recarga'`, etc., para poder identificar el tipo de entidad en el sistema.
11. Cada Pedido contiene atributos como `id_pedido`, `cliente_v`, `origen_v`, `destino_v`, `prioridad`, `fecha_creacion`, los cuales son necesarios para la lógica de negocio y dominio, asegurando que cada pedido es único y no duplicado en el sistema, los atributos `cliente_v`, `origen_v` y `destino_v` son referencias a los vértices correspondientes en el grafo y a sus posiciones relativas en el grafo y en el hashmap. Cada pedido llama a un Vertice Cliente y Almacen que contienen el mismo pedido, y se comienzan a autoreferenciar.
12. Cada Ruta contiene atributos como `origen`, `destino`, `camino`, `peso_total`, `algoritmo`, `tiempo_calculo`, los cuales son necesarios para la lógica de negocio y dominio, asegurando que cada ruta es única y no duplicada en el sistema, los atributos `origen` y `destino` son referencias a los vértices correspondientes en el grafo y a sus posiciones relativas en el grafo y en el hashmap. 


refactoriza el documento "negocio.md" teniendo en cuenta todo este contexto.

Además ten en cuenta que lo prioriotario es atomizar al máximo las implementaciones y sus pasos para poder desarrollar sus explicaciones al maximo. Estos pasos deben de crear un sistema integral, modular y escalar, que sigue patrones y arquitecruas junto a solid, siempre buscando un sistema robusto, coherente y que conecta de manera integral cohesivamente 

1. Capa de Dominio: Entidades Principales
1.1. Cliente (Dominio_Cliente.py)
Atributos: id_cliente, nombre, tipo_elemento = 'cliente', _pedidos = [].
Métodos:
__init__: Inicializa atributos y lista interna de pedidos.
agregar_pedido(pedido): Valida unicidad y asocia pedido.
eliminar_pedido(pedido): Remueve pedido si existe.
limpiar_pedidos(): Vacía la lista de pedidos.
obtener_pedidos() -> List[Pedido]: Retorna lista de pedidos asociados.
total_pedidos(): Retorna cantidad de pedidos asociados.
Documentación: Docstrings en español, sin acentos, explicando propósito y uso.
1.2. Almacenamiento (Dominio_Almacenamiento.py)
Atributos: id_almacenamiento, nombre, tipo_elemento = 'almacenamiento', _pedidos = [].
Métodos:
agregar_pedido(pedido), obtener_pedidos(), total_pedidos(), limpiar_pedidos().
Documentación: Igual que Cliente.
1.3. Recarga (Dominio_Recarga.py)
Atributos: id_recarga, nombre, tipo_elemento = 'recarga'.
Métodos: Constructor y representación legible.
Validación: Verificar unicidad y correcta inicialización.
1.4. Pedido (Dominio_Pedido.py)
Atributos: id_pedido, cliente_v, origen_v, destino_v, prioridad, status, ruta, fecha_creacion.
Métodos:
asignar_ruta(camino: List[int], peso_total: float): Asocia ruta al pedido.
actualizar_status(nuevo_status: str): Gestiona transición de estados (pendiente, en_ruta, entregado).
Validación: Unicidad, referencias a vértices válidos, fechas válidas.
1.5. Ruta (Dominio_Ruta.py)
Atributos: origen, destino, camino, peso_total, algoritmo, tiempo_calculo.
Métodos:
es_valida() -> bool: Verifica que el camino conecta origen y destino.
__str__: Representación legible.
Validación: Unicidad, referencias a vértices válidos.
2. Estructuras de Datos y Unicidad
2.1. Vertice (TDA_Vertice.py)
Atributos: _elemento (referencia a Cliente, Almacenamiento o Recarga).
Métodos: Acceso a elemento, comparación, unicidad por id, tipo.
Regla: No contiene lógica de negocio ni referencias de dominio.
2.2. Arista (TDA_Arista.py)
Atributos: _origen, _destino (objetos Vertice), _peso.
Métodos: Acceso a extremos, validación de peso, unicidad.
Regla: Peso máximo por recorrido: 50.
2.3. HashMap (TDA_Hash_map.py)
Propósito: Acceso O(1) a entidades y relaciones, garantizando unicidad y eficiencia.
3. Fábricas y Repositorios
3.1. Fábricas (Dominio/EntFabricas/)
FabricaClientes, FabricaAlmacenamientos, FabricaRecargas, FabricaPedidos, FabricaRutas, FabricaVertices, FabricaAristas.
Responsabilidad: Crear, validar y garantizar unicidad de instancias.
Métodos: crear, obtener, todos, limpiar, obtener_errores.
3.2. Repositorios (Infraestructura/Repositorios/)
RepositorioClientes, RepositorioAlmacenamientos, RepositorioRecargas, RepositorioPedidos, RepositorioRutas, RepositorioVertices, RepositorioAristas.
Responsabilidad: Acceso centralizado, inserción, obtención, eliminación, limpieza y acceso por HashMap.
Métodos: agregar, obtener, eliminar, todos, limpiar, obtener_hashmap.
4. Servicio de Simulación (Dominio)
4.1. Interfaces (Dominio/Interfaces/IntSim/ISimulacionDominioService.py)
Métodos abstractos:
iniciar_simulacion(n_vertices, m_aristas, n_pedidos)
obtener_vertices(), obtener_aristas(), obtener_pedidos(), obtener_rutas(), obtener_recargas(), obtener_estadisticas()
listar_clientes(), listar_almacenamientos(), listar_recargas(), etc.
4.2. Implementación de Simulación (Dominio/Simulacion_dominio.py)
Clase Singleton: Simulacion
Atributos: _repo_vertices, _repo_aristas, _repo_clientes, _repo_almacenamientos, _repo_recargas, _repo_pedidos, _repo_rutas, _estrategia.
Métodos:
iniciar_simulacion: Limpia repositorios, genera grafo, crea vértices y aristas, crea pedidos, asocia entidades, retorna configuración inicial.
Métodos de consulta: obtener_*_hashmap(), obtener_*().
Lógica de negocio: Delegar siempre en repositorios y fábricas.
5. Estrategias de Rutas y Lógica de Recarga
5.1. Estrategias (Dominio/AlgEstrategias/)
Implementar: BFS, DFS, Topological Sort (y opcionalmente Dijkstra, Floyd-Warshall, Kruskal).
Métodos:
calcular_ruta(origen, destino, grafo, autonomia=50, estaciones_recarga=None): Calcula ruta considerando autonomía y recargas.
_insertar_recargas_si_necesario: Inserta recargas si el trayecto excede autonomía.
Regla: Siempre operar con instancias únicas de Vertice y Arista.
5.2. Inyección de Estrategia
Método: set_estrategia(self, estrategia: IRutaEstrategia)
Lógica: Selección dinámica de estrategia según algoritmo solicitado.
6. Observadores y Eventos
6.1. Interfaces (Dominio/Interfaces/IntObs/)
ISujeto: Métodos para agregar, quitar y notificar observadores.
IObserver: Método actualizar(evento, datos=None).
6.2. Implementación
Eventos: Definir eventos relevantes (creación de pedido, entrega, cálculo de ruta, etc.).
Notificación: Implementar notificación de observadores en los puntos críticos del dominio.
7. Mapeadores y DTOs
7.1. Mapeadores (Dominio/Interfaces/IntMapeadores/)
IMapeador, IMapeadorDominioDTO: Métodos para convertir entidades de dominio a DTOs de respuesta.
Regla: Evitar ciclos de importación, seguir plan de relaciones.
8. Validación, Pruebas y Documentación
8.1. Pruebas
BDD y Unitarias: Verificar unicidad, relaciones, separación de responsabilidades y correcto funcionamiento de cada método.
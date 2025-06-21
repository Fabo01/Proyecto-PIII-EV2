Problemática
Correos Chile ha decidido implementar una red de drones autónomos para mejorar su cobertura y reducir los tiempos de entrega. Esta decisión busca superar las limitaciones del transporte terrestre, afectado por congestión y rutas ineficientes. 
Como no existe una infraestructura aérea preexistente, el sistema debe ser diseñado completamente desde cero. Este sistema debe contemplar:

Centros de distribución (Almacenamiento): Puntos donde los drones recogen paquetes.

Estaciones de carga: vertices estratégicos que los drones deben visitar para recargar si exceden su autonomía.
Destinos de entrega (Clientes): vertices dinámicos con prioridad asignada. Su ubicación y prioridad pueden variar.
Rutas seguras: Las rutas deben ser viables considerando el consumo energético. Si el trayecto excede el límite de autonomía, se debe forzar la visita a estaciones de recarga.
Registro de rutas: EI sistema debe registrar la frecuencia de uso de rutas y vertices, para análisis posterior.
Selección de rutas: A partir del registro anterior se debe crear una heurística basada en frecuencia que permita reutilizar rutas recurrentes a vertices más visitados, esto permitirá replicar recorridos ya realizados.
Rutas óptimas: El sistema debe calcular las rutas más óptimas considerando la autonomía de los drones y las estaciones de carga disponibles.
Rutas que deben pasar por estaciones de carga: Si un destino está fuera del alcance de un drone, se debe forzar una parada en una estación de carga antes de continuar hacia el destino final.
Registro de entregas: El sistema debe registrar cada entrega realizada, incluyendo el tiempo de entrega y la ruta utilizada.

Objetivo
Diseñar e implementar una simulación logística autónoma para drones, asegurando autonomía energética, optimización de rutas, conectividad, análisis de datos y visualización completa del sistema.
Para esto se ha dispuesto un video en youtube a modo de guía: https://youtu.be/AXj14zeKqTl

Parámetros de Simulación
Cantidad máxima de vertices: hasta 150 
Roles de vertices: 
• Almacenamiento: 20%
• Recarga: 20%
• Cliente: 60%
Todas las rutas se generan sobre grafos conectados.

Metas Funcionales

1. Gestión dinámica de rutas
Autonomía máxima del dron: 50 unidades de costo (suma de pesos de aristas)
Si una ruta supera el límite de batería, se fuerza el paso por vertices de recarga.
Crear rutas entre cualquier centro de almacenamiento y cliente.
Considerar estaciones de recarga si la energía del dron no alcanza.
Solo usar algoritmos BFS,DFS y Topological Sort para búsqueda de caminos.

2. Simulación funcional
Simulación inicial con 15 vertices, 20 aristas y 10 órdenes.
Soporta hasta 150 vertices y 300 aristas y 500 órdenes como máximo.
Optimizar uso de memoria y estructura de datos (AVL, mapas, grafos).

3. Análisis estadístico
Registrar cada ruta usada en un AVL.
Determinar las rutas más utilizadas.
Registrar frecuencia de vertices destino y origen.

4. Garantía de conectividad
Todos los grafos generados son conexos.
Se evita la generación de vertices aislados.

5. Visualización y Dashboard
La interfaz principal se desarrolla mediante Streamlit (Recomendado), y permite visualizar y operar el sistema en 5 pestañas organizadas funcionalmente. A continuación, se describe cada una:

Pestaña 1: Ejecutar Simulación
Propósito: Permitir la configuración e inicio de la simulación con parámetros personalizables.

Componentes:
• Slider: número de vertices (n_vertices, entre 10 y 150).
• Slider: número de aristas (m_aristas, entre 10 y 300).
• Slider: número de órdenes (n_pedidos, entre 10 y 300).
• Campo informativo: Texto informativo indicando la cantidad de vertices cliente, almacenamiento, abastecimiento y su porcentaje.
• Botón: Start Simulation (Inicia la simulación)

Validaciones:
• El número de aristas debe permitir un grafo conexo (n_vertices - 1)
• El valor de vertices no debe superar 150.
• Si se hace clic sin modificar parámetros, se mantiene la configuración por defecto (ítem de componentes).

Interacciones esperadas:
• Al presionar el botón, se genera un grafo aleatorio con roles asignados proporcionalmente:
• Almacenamiento: 20%
• Recarga: 20%
• Cliente: 60%

* Nota del docente:
Esta pestaña sirve como punto de entrada para validar la generación del entorno base y comprobar la
conectividad y escalabilidad. (Manejo de parámetros)

Pestaña 2: Explorar Red
Propósito: Visualizar la red de transporte y calcular rutas entre vertices, considerando recarga por batería.

Componentes:
• Gráfico: red de vertices coloreados por tipo (matplotlib)
• Selectbox: vertice origen
• Selectbox: vertice destino
• Calculate Route (Calculará la ruta entre 2 vertices)
• TextBox: muestra un mensaje de la ruta encontrada (lista de vertices + costo, ejemplo : Path: W -> I -> R -> I Costo: 25)
    • Luego de calcular una ruta debe dar la opción de completar la ruta Completar Delivery y Crear Pedido
• Leyenda: colores según tipo de vertice

Validaciones:
• Ambos vertices deben existir en el grafo.
• Si no hay ruta posible con la bateria actual, se busca obligatoriamente una alternativa que pase por vertices de recarga.

Interacciones esperadas:
• El grafo muestra rutas visualmente en color rojo.
• A1 seleccionar origen y destino y presionar el botön, se calcula Ia ruta más corta permitida, utilizando BFS, DFS o Topological Sort (Recomendado) modificado con bateria limite (50).
• Se muestra el camino recorrido y el costo.

* Nota docente:
Evaluar la integracion entre logica (bateria, vertices) y visualizacion. Es una parte central de la evaluacion funcional.

Pestaña 3: Clientes y pedidos
Propósito: Listar los clientes activos y los pedidos generados, mostrando atributos relevantes.
Componentes:
• Subsección: lista de clientes (st . j son)
    • Cliente: ID, nombre, tipo, total de pedidos O
• Subsección: lista de órdenes (st . j son)
    • Pedido: ID, cliente asociado,cliente ID, origen, destino, status,fecha de creación, prioridad, fecha entrega, costo total.

Validaciones:
• Se muestran sólo si hay simulación activa.

Interacciones esperadas:
• Al iniciar una simulación, esta sección se autoactualiza con los datos generados.

* Nota docente:
Es útil para verificar que el sistema esté registrando correctamente los pedidos y asociándose a clientes.

Pestaña 4: Análisis de Rutas
Propósito: Visualizar las rutas más frecuentes utilizadas, registradas en una estructura AVL.

Componentes:
• Lista: rutas más frecuentes (clave = camino, valor = frecuencia).
• Gráfico: visualización del árbol AVL con etiquetas "A -> B -> C\nFreq: X" usando networkx.

Validaciones:
• Solo disponible si se han generado pedidos y rutas.
• El AVL debe reflejar el uso repetido de rutas idénticas (por ejemplo, múltiples pedidos de un mismo cliente).

Interacciones esperadas:
• Las rutas se ordenan por recorrido (orden lexicográfico).
• Se visualiza gráficamente la estructura del AVL para apoyar aprendizaje en estructuras balanceadas.

* Nota docente:
Parte esencial de la evaluación por uso de TDA AVL. Refuerza estructuras y visualización de árboles.

Pestaña 5: Estadísticas generales
Propósito: Entregar una vista global del sistema en funcionamiento, con gráficas visuales.

Componentes:
• Gráfico de barras: comparación entre número de vertices clientes más visitados, vertices almacenamiento más visitados y vertices de abastecimiento más visitados.
• Gráfico de torta: proporción entre vertices por rol.

Validaciones:
• Se requiere simulación activa para mostrar los datos.

Interacciones esperadas:
• Se actualiza automáticamente luego de iniciar una simulación.

Estructura de Clases y Módulos sugerida
Clase / Módulo	         //                Función                             //        Ubicación
Graph, Vertex, Edge	     //       Modela el grafo base (vertices, conexiones)     //       model/
Simulation	             //        Controlador principal de la simulación      //       sim/
Simulationlnitializer	 //       Generación de grafos conectados y roles      //       sim/
Route, Order, Client	 //       Representan las entidades del sistema        //       domain/
AVL	                     //       Almacena rutas más frecuentes                //     tda/
Map (hash map propio)	 //       Acceso 0(1) a clientes y órdenes             //       tda/
NetworkXAdapter	         //       Adaptador visual de grafos para visual/      //      matplotlib
AVLVisualizer	         //       Dibuja gráficamente el árbol AVL visual/     //     dashboard.py  

El proyecto debe enfocarse en una ubicación jerárquica, dependencia lógica y modularidad, como si construyéramos un diagrama de arquitectura lógica por capas (layered architecture).


Interfaz Visual <- GUI /  Dashboard
Lógica de Aplicación <- Coordina simulaciones, entrega, análisis
Dominio del Problema <- Modelos: Pedido, Cliente, Ruta
Infraestructura TDA <- AVL, HahsMap
Estructuras Base <- Graph, Vertex, Edge, Inicializador

Ten en cuenta que esta estructura es una sugerencia y puede adaptarse según las necesidades específicas del proyecto. La clave es mantener una separación clara de responsabilidades y facilitar la escalabilidad y el mantenimiento del código. Siempre es recomendable seguir las mejores prácticas de programación y diseño de software, como la modularidad, la reutilización de código y la documentación adecuada.

El código siempre debe de ser en español, utilizando snake_case para nombres de varivables y funciones, y PascalCase para nombres de clases. Además, se debe evitar el uso de acentos en los nombres de variables y funciones para asegurar compatibilidad con diferentes sistemas y lenguajes de programación.
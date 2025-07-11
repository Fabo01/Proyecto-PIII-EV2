el mapa realista en una pestaña aparte, utilizando el grafo 

poder exportar a pdf estadisticas importantes

swagger de la api

Objetivo
Diseñar, extender e integrar un sistema logístico de drones autónomos, que permita:
1. Visualización de la red completa sobre un mapa interactivo real.
2. Selección de rutas entre nodos (almacenamiento a clientes) con control de autonomía.
3. Cálculo de rutas usando Dijkstra o Floyd-Warshall, con representación gráfica y resumen
energético.
4. Visualización del Árbol de Expansión Mínima (MST) usando Kruskal directamente en el mapa.
5. Registro de órdenes generadas desde rutas simuladas y visualización de su historial.
6. Generación de informes PDF, tanto desde la aplicación visual como desde una API externa.
7. Consumo y prueba de una API RESTful que sirva como backend para los datos de la simulación.

Visualización geográfica
● La vista permite:
○ Calcular rutas.
○ Ver costos y distancia.
○ Completar órdenes.
○ Mostrar MST generado.
○ Visualizar resumen de vuelo.

Generación de informes PDF
● Desde la pestaña de “Análisis de Rutas” y vía API, se puede generar un informe PDF
descargable que contiene:
○ Tabla de pedidos.
○ Clientes con más pedidos.
○ Rutas más usadas.
○ Gráficos con distribución y uso del sistema.
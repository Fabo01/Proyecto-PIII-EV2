# Instrucciones universales para GitHub Copilot en este proyecto

Este archivo contiene las instrucciones y lineamientos que GitHub Copilot debe seguir para el desarrollo del proyecto de simulación logística de drones para Correos Chile, según lo especificado en `Docs/Requisitos.md` y considerando las mejoras y feedback recientes.

### Estado y lineamientos clave
- Los vértices del grafo pueden ser de tipo cliente, almacenamiento o recarga, y solo almacenan el elemento asociado.
- La lógica de pedidos está completamente separada de la lógica de vértices.
- Cada cliente debe mantener una lista de pedidos asociados y exponer métodos para gestionarlos.
- Los pedidos se asocian a clientes y pueden ser consultados y gestionados desde la simulación y la interfaz visual.
- La simulación debe permitir calcular rutas para cada pedido desde el almacenamiento de origen al cliente destino.
- Mantener la modularidad, separación de responsabilidades y seguir las convenciones de código en español.

## 1. Fuente de Verdad
Siempre debes seguir el documento `Docs/Requisitos.md` como la base y documentación principal del proyecto. Todas las decisiones de diseño, estructura de carpetas, nombres de clases, funciones y validaciones deben alinearse con este documento y la documentación en `Docs/Documentacion/`.

## 2. Estado Actual del Proyecto
- Estructura modular implementada: Dominio, Modelos, TDA, Simulacion, Visual.
- Los vértices del grafo pueden ser de tipo Cliente, Almacenamiento o Recarga, cada uno con su propia lógica en su dominio.
- El vértice solo almacena el elemento asociado y no contiene lógica de cliente ni de pedido.
- La gestión de pedidos es completamente independiente de la lógica de Cliente y de los vértices.
- Dashboard funcional con Streamlit, visualización de grafos y rutas, árbol AVL y estadísticas básicas.
- Manejo de rutas y pedidos, registro en AVL, acceso O(1) con HashMap.
- Tests BDD para TDA, modelos y simulación, verificando la correcta clasificación de nodos y la separación de responsabilidades.
- Documentación técnica y funcional generada.
- Corrección de imports y compatibilidad multiplataforma.
- Visualización de la red con colores y leyendas por tipo de nodo.
- Manejo básico de errores en la interfaz visual.
- Implementación de un árbol AVL para gestionar pedidos y rutas.
- Implementación de un HashMap para acceso rápido a pedidos y clientes.
- Implementación de un grafo para representar la red de clientes y almacenes.
- Implementación de un sistema de pedidos que permite asociar pedidos a clientes y gestionar su estado.
- Implementación de una interfaz visual con Streamlit que permite interactuar con el sistema de pedidos y visualizar la red de clientes y almacenes.
- Implementación de un sistema de simulación que permite calcular rutas y gestionar pedidos.
- 
## 3. Convenciones de Código
- El código debe estar en español.
- Usa snake_case para variables y funciones.
- Usa PascalCase para nombres de clases.
- No utilices acentos en nombres de variables, funciones o clases.
- Documenta las clases y funciones principales con docstrings en español.

## 4. Modularidad y Buenas Prácticas
- Mantén una clara separación de responsabilidades entre módulos.
- Facilita la escalabilidad y el mantenimiento del código.
- Sigue las mejores prácticas de programación y diseño de software.
- Utiliza patrones y arquitectura de diseño adecuados para la arquitectura del proyecto.

## 5. Visualización
- La interfaz principal debe ser desarrollada con Streamlit.
- Utiliza matplotlib y networkx para la visualización de grafos y árboles AVL.

## 6. Documentación y Comentarios
- Documenta adecuadamente el código y las funciones.
- Incluye comentarios explicativos donde sea necesario para clarificar la lógica.

## 7. Uso de Archivos de Referencia en Docs/
- Los archivos `Docs/edge.py`, `Docs/vertex.py`, `Docs/graph.py` y `Docs/TDA-Map.py` deben ser utilizados como base lógica y documentación para la implementación de las estructuras de datos principales (grafo, vértice, arista y mapa/hash map).
- Refactoriza y adapta su lógica al español, siguiendo las convenciones y estructura de este proyecto.
- Considera estos archivos como referencia obligatoria para la implementación de los módulos correspondientes en `Modelos/` y `TDA/`.

---

Estas instrucciones deben ser consideradas en cada etapa del desarrollo del proyecto. Si surge alguna duda, consulta siempre el archivo `Docs/Requisitos.md` y las mejoras pendientes como referencia principal.

# Casos de Uso del Sistema de Simulación Logística

## Descripción General
Este documento describe los casos de uso principales del sistema de simulación logística de drones, definiendo actores, precondiciones, flujos principales y alternativos, y resultados esperados.

## 📋 Actores del Sistema

### Primarios
- **Operador de Simulación**: Usuario que configura y ejecuta simulaciones
- **Analista de Rutas**: Usuario que analiza patrones de rutas y estadísticas
- **Administrador del Sistema**: Usuario que gestiona configuraciones avanzadas

### Secundarios
- **Sistema de Drones**: Actor externo que representaría los drones reales
- **Sistema de Clientes**: Actor externo que genera pedidos de entrega

## 🎯 Casos de Uso Principales

### CU-01: Inicializar Simulación

#### Actor Principal
Operador de Simulación

#### Precondiciones
- El sistema está disponible y funcionando
- No hay simulación activa en curso

#### Flujo Principal
1. El operador accede a la pestaña "Ejecutar Simulación"
2. El sistema muestra los controles de configuración
3. El operador configura parámetros:
   - Número de vértices (10-150)
   - Número de aristas (mínimo para conectividad)
   - Número de pedidos iniciales (10-500)
4. El operador presiona "Start Simulation"
5. El sistema valida los parámetros ingresados
6. El sistema genera la red de vértices con distribución:
   - 60% Clientes
   - 20% Almacenes  
   - 20% Estaciones de recarga
7. El sistema crea las aristas garantizando conectividad
8. El sistema genera las entidades de negocio (clientes, almacenes, recargas)
9. El sistema crea los pedidos iniciales asociados a clientes
10. El sistema muestra confirmación de simulación inicializada

#### Flujos Alternativos
- **FA-01**: Parámetros inválidos
  - 5.1. El sistema detecta parámetros fuera de rango
  - 5.2. El sistema muestra mensaje de error específico
  - 5.3. Retorna al paso 3
  
- **FA-02**: Error en generación de red
  - 6.1. El sistema no puede generar una red conectada
  - 6.2. El sistema reintenta con parámetros ajustados
  - 6.3. Si falla múltiples veces, muestra error técnico

#### Postcondiciones
- **Éxito**: Simulación inicializada con red conectada y entidades creadas
- **Fallo**: Sistema mantiene estado anterior sin cambios

#### Reglas de Negocio
- RN-01: La red debe ser completamente conectada
- RN-02: Los vértices deben distribuirse según proporciones establecidas
- RN-03: Cada cliente debe tener al menos un pedido posible

---

### CU-02: Explorar Red y Calcular Rutas

#### Actor Principal
Operador de Simulación

#### Precondiciones
- Simulación está inicializada
- Red contiene vértices y aristas

#### Flujo Principal
1. El operador accede a la pestaña "Explorar Red"
2. El sistema muestra la visualización del grafo coloreada por tipos
3. El sistema muestra selectores de origen y destino
4. El operador selecciona vértice de origen
5. El operador selecciona vértice de destino
6. El operador presiona "Calculate Route"
7. El sistema valida que origen y destino sean diferentes
8. El sistema ejecuta algoritmo BFS considerando autonomía energética
9. El sistema calcula la ruta más corta factible
10. El sistema destaca la ruta en el grafo visual
11. El sistema muestra detalles de la ruta (camino, costo)
12. El sistema ofrece opción "Completar Delivery"

#### Flujos Alternativos
- **FA-01**: Origen y destino iguales
  - 7.1. El sistema muestra mensaje de error
  - 7.2. Retorna al paso 4

- **FA-02**: Ruta no encontrada por autonomía
  - 9.1. El sistema busca ruta con estaciones de recarga
  - 9.2. Si encuentra ruta con recarga, continúa con paso 10
  - 9.3. Si no encuentra ruta, muestra mensaje explicativo

- **FA-03**: Error técnico en cálculo
  - 9.1. El sistema registra el error en logs
  - 9.2. El sistema muestra mensaje genérico de error
  - 9.3. Retorna al paso 4

#### Postcondiciones
- **Éxito**: Ruta calculada y visualizada, opción de crear pedido disponible
- **Fallo**: Sistema mantiene estado de visualización anterior

#### Reglas de Negocio
- RN-04: Autonomía máxima de dron es 50 unidades
- RN-05: Si la ruta excede autonomía, debe incluir estaciones de recarga
- RN-06: Solo se permiten algoritmos BFS, DFS o Topological Sort

---

### CU-03: Gestionar Pedidos

#### Actor Principal
Operador de Simulación, Analista de Rutas

#### Precondiciones
- Simulación está inicializada
- Existen clientes en el sistema

#### Flujo Principal
1. El actor accede a la pestaña "Clientes y Pedidos"
2. El sistema muestra lista de clientes con sus datos
3. El sistema muestra lista de pedidos con detalles:
   - ID, cliente asociado, origen, destino, status, prioridad, fecha
4. El actor puede filtrar o buscar pedidos específicos
5. El actor selecciona un pedido para ver detalles
6. El sistema muestra información completa del pedido
7. El actor puede cambiar el status del pedido
8. El sistema actualiza el pedido y registra el cambio

#### Flujos Alternativos
- **FA-01**: Pedido no encontrado
  - 5.1. El sistema muestra mensaje de pedido inexistente
  - 5.2. Retorna al paso 3

- **FA-02**: Cambio de status inválido
  - 7.1. El sistema valida la transición de estado
  - 7.2. Si es inválida, muestra reglas de negocio aplicables
  - 7.3. Retorna al paso 6

#### Postcondiciones
- **Éxito**: Información de pedidos actualizada y consistente
- **Fallo**: Sistema mantiene estado anterior sin cambios

#### Reglas de Negocio
- RN-07: Un pedido solo puede pasar de PENDIENTE a EN_RUTA a ENTREGADO
- RN-08: Cada cliente puede tener múltiples pedidos activos
- RN-09: Solo pedidos PENDIENTES pueden ser modificados por rutas

---

### CU-04: Analizar Frecuencia de Rutas

#### Actor Principal
Analista de Rutas

#### Precondiciones
- Simulación está inicializada
- Se han calculado al menos algunas rutas

#### Flujo Principal
1. El analista accede a la pestaña "Análisis de Rutas"
2. El sistema consulta el árbol AVL de rutas
3. El sistema muestra lista de rutas ordenadas por frecuencia
4. El sistema genera visualización del árbol AVL
5. El analista puede expandir/contraer nodos del árbol
6. El analista puede filtrar rutas por criterios:
   - Origen específico
   - Destino específico  
   - Rango de frecuencia
7. El sistema actualiza la visualización según filtros
8. El analista puede exportar datos de análisis

#### Flujos Alternativos
- **FA-01**: No hay rutas registradas
  - 2.1. El sistema muestra mensaje informativo
  - 2.2. El sistema sugiere generar rutas primero

- **FA-02**: Error en visualización de AVL
  - 4.1. El sistema registra error técnico
  - 4.2. El sistema muestra vista de lista simple como alternativa

#### Postcondiciones
- **Éxito**: Análisis de frecuencia de rutas disponible y visualizado
- **Fallo**: Sistema muestra información básica disponible

#### Reglas de Negocio
- RN-10: Las rutas se agrupan por secuencia exacta de vértices
- RN-11: La frecuencia incrementa cada vez que se recalcula la misma ruta
- RN-12: El AVL mantiene balance automático para consultas eficientes

---

### CU-05: Visualizar Estadísticas Generales

#### Actor Principal
Operador de Simulación, Analista de Rutas

#### Precondiciones
- Simulación está inicializada
- Existen datos de actividad en el sistema

#### Flujo Principal
1. El actor accede a la pestaña "Estadísticas Generales"
2. El sistema recopila métricas actuales:
   - Vértices más visitados por tipo
   - Proporción de tipos de vértice
   - Eficiencia de entregas
   - Uso de estaciones de recarga
3. El sistema genera gráfico de barras comparativo
4. El sistema genera gráfico de torta de proporciones
5. El sistema muestra métricas numéricas clave
6. El actor puede cambiar período de análisis
7. El sistema actualiza visualizaciones según período seleccionado

#### Flujos Alternativos
- **FA-01**: Datos insuficientes
  - 2.1. El sistema muestra mensaje de datos limitados
  - 2.2. El sistema muestra métricas parciales disponibles

- **FA-02**: Error en generación de gráficos
  - 3.1. El sistema registra error técnico
  - 3.2. El sistema muestra datos en formato tabular

#### Postcondiciones
- **Éxito**: Estadísticas actualizadas y visualizadas correctamente
- **Fallo**: Datos básicos mostrados en formato alternativo

#### Reglas de Negocio
- RN-13: Las estadísticas se calculan en tiempo real
- RN-14: Los datos históricos se mantienen durante la sesión
- RN-15: Las métricas se agrupan por tipos de entidad

---

## 🔗 Casos de Uso Extendidos

### CU-06: Crear Pedido desde Ruta Calculada

#### Actor Principal
Operador de Simulación

#### Precondiciones
- Se ha calculado una ruta válida en CU-02
- El destino corresponde a un cliente válido

#### Flujo Principal
1. El operador presiona "Crear Pedido" tras calcular ruta
2. El sistema obtiene datos del cliente destino
3. El sistema pre-completa formulario de pedido:
   - Cliente destino (automático)
   - Almacén origen (automático)
   - Ruta calculada (automática)
4. El operador asigna prioridad al pedido
5. El operador confirma creación del pedido
6. El sistema valida datos del pedido
7. El sistema asigna ID único al pedido
8. El sistema registra pedido en repositorio
9. El sistema asocia pedido al cliente
10. El sistema registra ruta en AVL de frecuencias
11. El sistema muestra confirmación de pedido creado

#### Reglas de Negocio
- RN-16: El cliente destino debe estar activo
- RN-17: El almacén origen debe tener capacidad
- RN-18: La ruta debe ser energéticamente factible

---

### CU-07: Gestionar Conexión de Red

#### Actor Principal
Administrador del Sistema

#### Precondiciones
- Acceso a configuración avanzada del sistema

#### Flujo Principal
1. El administrador accede a herramientas de red
2. El sistema muestra métricas de conectividad
3. El administrador puede agregar/quitar aristas
4. El sistema valida que los cambios mantengan conectividad
5. El administrador confirma cambios
6. El sistema actualiza la estructura del grafo
7. El sistema recalcula métricas de conectividad
8. El sistema notifica cambios a usuarios activos

#### Reglas de Negocio
- RN-19: La red debe permanecer completamente conectada
- RN-20: Los cambios no deben afectar pedidos en proceso
- RN-21: Se debe mantener registro de cambios estructurales

---

## 📊 Matriz de Trazabilidad

| Caso de Uso | Requisitos Funcionales | Componentes Principales |
|-------------|----------------------|-------------------------|
| CU-01 | RF-01, RF-02, RF-03 | Simulación, Fábricas, Repositorios |
| CU-02 | RF-04, RF-05, RF-06 | Algoritmos Ruta, Grafo, Visualización |
| CU-03 | RF-07, RF-08, RF-09 | Dominio Pedido, Repositorios |
| CU-04 | RF-10, RF-11, RF-12 | AVL, Estadísticas, Visualización |
| CU-05 | RF-13, RF-14, RF-15 | Métricas, Gráficos, Dashboard |
| CU-06 | RF-16, RF-17 | Integración Ruta-Pedido |
| CU-07 | RF-18, RF-19 | Administración, Grafo |

## 📝 Notas de Implementación

### Validaciones Críticas
- Verificar conectividad antes de cualquier operación de red
- Validar autonomía energética en todos los cálculos de ruta
- Garantizar unicidad de IDs en todas las entidades
- Verificar estados válidos en transiciones de pedidos

### Casos de Error Comunes
- Red desconectada por configuración inválida
- Rutas imposibles por limitaciones energéticas
- Pedidos huérfanos por eliminación de clientes
- Sobrecarga de memoria por exceso de entidades

### Optimizaciones Recomendadas
- Cache de rutas frecuentes para mejorar rendimiento
- Índices en HashMap para búsquedas rápidas
- Paginación en listas de entidades grandes
- Compresión de datos de visualización para grafos grandes

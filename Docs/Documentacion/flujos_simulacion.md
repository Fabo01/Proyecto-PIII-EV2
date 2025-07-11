# Documentación de Flujos de Simulación

## Descripción General
Los flujos de simulación representan los procesos de negocio principales del sistema logístico de drones. Estos flujos coordinan la interacción entre todos los componentes para ejecutar entregas desde la creación de pedidos hasta la entrega final, pasando por el cálculo de rutas y la gestión de recursos.

## Flujos Principales del Sistema

### 1. Flujo de Inicialización de Simulación

#### Descripción
Proceso que prepara el entorno completo para ejecutar la simulación logística.

#### Actores
- **Usuario**: Configura parámetros de simulación
- **Sistema de Simulación**: Orquesta la inicialización
- **Generador de Red**: Crea la topología
- **Repositorios**: Almacenan entidades creadas

#### Secuencia de Pasos
```
1. Usuario especifica parámetros:
   - Número de vértices (10-150)
   - Número de aristas (mínimo para conectividad)
   - Número de pedidos iniciales (10-500)
   - Distribución de tipos de vértice

2. Sistema valida parámetros:
   - Verificar rangos válidos
   - Calcular aristas mínimas para conectividad
   - Validar proporciones de tipos de vértice

3. Generación de red:
   - Crear vértices según distribución:
     * 60% Clientes
     * 20% Almacenes
     * 20% Estaciones de recarga
   - Generar árbol de expansión (conectividad garantizada)
   - Agregar aristas adicionales aleatoriamente
   - Verificar conectividad final

4. Creación de entidades de negocio:
   - Crear clientes con datos aleatorios
   - Crear almacenes con capacidades
   - Crear estaciones de recarga
   - Registrar en repositorios con HashMap

5. Generación de pedidos iniciales:
   - Asignar pedidos aleatoriamente a clientes
   - Seleccionar almacenes de origen
   - Establecer prioridades variadas
   - Inicializar en estado PENDIENTE

6. Inicialización de estructuras auxiliares:
   - Preparar AVL para registro de rutas
   - Configurar observadores de eventos
   - Inicializar métricas y estadísticas

7. Verificación final:
   - Validar conectividad completa
   - Verificar integridad de datos
   - Confirmar estado inicial válido
```

#### Resultado
- **Red conectada** con vértices y aristas
- **Entidades de negocio** registradas en repositorios
- **Pedidos iniciales** listos para procesamiento
- **Sistema preparado** para calcular rutas y ejecutar entregas

### 2. Flujo de Cálculo de Rutas

#### Descripción
Proceso que determina la ruta óptima para entregar un pedido, considerando limitaciones energéticas y disponibilidad de estaciones de recarga.

#### Actores
- **Servicio de Simulación**: Inicia el cálculo
- **Estrategia de Ruta**: Implementa algoritmo específico
- **Grafo de Red**: Proporciona topología
- **Repositorios**: Suministran datos de entidades

#### Secuencia de Pasos
```
1. Identificación de pedido:
   - Seleccionar pedido en estado PENDIENTE
   - Verificar que cliente esté activo
   - Confirmar almacén origen operativo

2. Extracción de puntos de interés:
   - Obtener vértice de almacén origen
   - Obtener vértice de cliente destino
   - Identificar estaciones de recarga disponibles

3. Aplicación de algoritmo de ruta:
   - Ejecutar BFS modificado con autonomía
   - Considerar límite energético (50 unidades)
   - Incluir paradas de recarga si es necesario

4. Validación de ruta calculada:
   - Verificar conectividad completa
   - Confirmar factibilidad energética
   - Validar existencia de todos los vértices

5. Creación de objeto Ruta:
   - Construir secuencia de vértices
   - Calcular costo total
   - Identificar aristas utilizadas
   - Determinar estaciones de recarga utilizadas

6. Asignación al pedido:
   - Asociar ruta al pedido
   - Cambiar estado a EN_RUTA
   - Registrar timestamp de asignación

7. Registro estadístico:
   - Insertar ruta en AVL para frecuencia
   - Actualizar métricas de vértices
   - Notificar observadores del evento
```

#### Algoritmo BFS Detallado
```python
def calcular_ruta_bfs_autonomia(origen: str, destino: str, autonomia: float = 50.0):
    """
    Algoritmo BFS modificado que considera autonomía energética
    """
    # Inicialización
    cola = deque([(origen, [origen], autonomia, [])])  # (vértice, camino, energía, recargas)
    explorados = set()
    mejor_solucion = None
    
    while cola:
        actual, camino, energia, recargas_usadas = cola.popleft()
        
        # Evitar ciclos infinitos
        if (actual, energia) in explorados:
            continue
        explorados.add((actual, energia))
        
        # ¿Llegamos al destino?
        if actual == destino:
            return {
                'camino': camino,
                'costo_total': autonomia - energia + (len(recargas_usadas) * autonomia),
                'recargas_utilizadas': recargas_usadas
            }
        
        # Explorar vecinos
        for vecino in grafo.obtener_vecinos(actual):
            arista = grafo.obtener_arista(actual, vecino)
            costo_movimiento = arista.peso
            
            # ¿Tenemos energía suficiente?
            if energia >= costo_movimiento:
                nueva_energia = energia - costo_movimiento
                nuevo_camino = camino + [vecino]
                nuevas_recargas = recargas_usadas.copy()
                
                # Si es estación de recarga, recargar
                vertice_vecino = grafo.obtener_vertice(vecino)
                if vertice_vecino.tipo == TipoVertice.RECARGA:
                    nueva_energia = autonomia
                    nuevas_recargas.append(vecino)
                
                cola.append((vecino, nuevo_camino, nueva_energia, nuevas_recargas))
    
    return None  # No se encontró ruta válida
```

### 3. Flujo de Ejecución de Entrega

#### Descripción
Proceso que simula la ejecución física de una entrega, desde el despegue del dron hasta la entrega final.

#### Actores
- **Simulador de Drones**: Ejecuta la entrega
- **Objeto Ruta**: Guía el recorrido
- **Observadores**: Registran eventos
- **Repositorios**: Actualizan estados

#### Secuencia de Pasos
```
1. Preparación de entrega:
   - Verificar ruta asignada válida
   - Confirmar disponibilidad de recursos
   - Inicializar estado de seguimiento

2. Inicio de recorrido:
   - Posicionar dron en almacén origen
   - Cargar paquete del pedido
   - Inicializar energía completa (50 unidades)
   - Notificar inicio de entrega

3. Navegación por ruta:
   Para cada segmento en la ruta:
   - Mover de vértice actual al siguiente
   - Consumir energía según peso de arista
   - Actualizar posición actual
   - Verificar nivel de energía

4. Gestión de recargas:
   Si se encuentra estación de recarga:
   - Detenerse en estación
   - Simular tiempo de recarga
   - Restaurar energía completa
   - Continuar hacia próximo vértice

5. Entrega final:
   - Llegar al vértice del cliente
   - Simular entrega del paquete
   - Confirmar recepción exitosa
   - Registrar timestamp de entrega

6. Finalización:
   - Actualizar estado del pedido a ENTREGADO
   - Calcular costo final basado en ruta
   - Generar eventos de auditoría
   - Actualizar estadísticas del sistema
```

### 4. Flujo de Gestión de Eventos

#### Descripción
Sistema de notificaciones que mantiene coherencia entre componentes y registra actividad del sistema.

#### Tipos de Eventos
```python
class TipoEvento(Enum):
    SIMULACION_INICIADA = "simulacion_iniciada"
    PEDIDO_CREADO = "pedido_creado"
    RUTA_CALCULADA = "ruta_calculada"
    ENTREGA_INICIADA = "entrega_iniciada"
    RECARGA_REALIZADA = "recarga_realizada"
    ENTREGA_COMPLETADA = "entrega_completada"
    PEDIDO_CANCELADO = "pedido_cancelado"
    ERROR_ENTREGA = "error_entrega"
```

#### Observadores del Sistema
```python
# Observador de Auditoría
class AuditoriaObservador:
    def notificar(self, evento: Evento):
        """Registra todos los eventos para trazabilidad"""
        log_entry = {
            'timestamp': datetime.now(),
            'tipo': evento.tipo,
            'entidad_id': evento.entidad_id,
            'datos': evento.datos_adicionales
        }
        self.repositorio_auditoria.guardar(log_entry)

# Observador de Estadísticas
class EstadisticasObservador:
    def notificar(self, evento: Evento):
        """Actualiza métricas del sistema"""
        if evento.tipo == TipoEvento.ENTREGA_COMPLETADA:
            self.incrementar_entregas_completadas()
            self.actualizar_tiempo_promedio_entrega(evento.datos['tiempo_total'])
        elif evento.tipo == TipoEvento.RUTA_CALCULADA:
            self.registrar_ruta_utilizada(evento.datos['ruta'])

# Observador de Dashboard
class DashboardObservador:
    def notificar(self, evento: Evento):
        """Actualiza visualización en tiempo real"""
        self.cache_estado.invalidar()
        self.websocket.enviar_actualizacion(evento)
```

### 5. Flujo de Análisis de Rutas Frecuentes

#### Descripción
Proceso que identifica patrones de uso y optimiza el sistema basándose en rutas más utilizadas.

#### Secuencia de Pasos
```
1. Recolección de datos:
   - Consultar AVL de rutas utilizadas
   - Obtener frecuencias de cada ruta
   - Identificar patrones temporales

2. Análisis de frecuencia:
   - Ordenar rutas por frecuencia de uso
   - Identificar top 10 rutas más utilizadas
   - Calcular métricas de eficiencia

3. Optimización sugerida:
   - Identificar rutas que siempre requieren recarga
   - Sugerir ubicaciones adicionales de recarga
   - Optimizar distribución de almacenes

4. Actualización de cache:
   - Cachear rutas más frecuentes
   - Priorizar cálculos para estas rutas
   - Optimizar algoritmos basados en historial

5. Reportes y visualización:
   - Generar reportes de eficiencia
   - Crear visualizaciones de rutas frecuentes
   - Mostrar métricas en dashboard
```

## Consideraciones de Rendimiento

### 1. Optimizaciones Implementadas
- **Cache de rutas**: Rutas frecuentes se almacenan para acceso rápido
- **Índices optimizados**: HashMap para acceso O(1) a entidades
- **Algoritmos eficientes**: BFS modificado con poda inteligente
- **Procesamiento lazy**: Cálculos solo cuando son necesarios

### 2. Manejo de Concurrencia
- **Thread-safe**: Repositorios preparados para acceso concurrente
- **Locks mínimos**: Diseño que minimiza contención
- **Eventos asincrónicos**: Notificaciones no bloquean flujo principal

### 3. Escalabilidad
- **Arquitectura modular**: Fácil escalamiento horizontal
- **Separación de responsabilidades**: Componentes independientes
- **Recursos ajustables**: Configuración según carga esperada

## Manejo de Errores y Excepciones

### 1. Errores de Conectividad
```python
class ConectividadError(Exception):
    """Error cuando no existe camino entre origen y destino"""
    pass

def manejar_error_conectividad(origen: str, destino: str):
    """
    Maneja casos donde no hay ruta disponible
    """
    # Verificar si el problema es temporal
    if not grafo.existe_camino(origen, destino):
        # Buscar almacén alternativo
        almacenes_alternativos = buscar_almacenes_conectados(destino)
        if almacenes_alternativos:
            return calcular_ruta(almacenes_alternativos[0], destino)
    
    raise ConectividadError(f"No hay ruta disponible de {origen} a {destino}")
```

### 2. Errores de Energía
```python
class EnergiaInsuficienteError(Exception):
    """Error cuando no hay estaciones de recarga suficientes"""
    pass

def validar_factibilidad_energetica(ruta: List[str], autonomia: float):
    """
    Verifica que la ruta sea factible energéticamente
    """
    energia_actual = autonomia
    
    for i in range(len(ruta) - 1):
        arista = grafo.obtener_arista(ruta[i], ruta[i+1])
        energia_actual -= arista.peso
        
        if energia_actual < 0:
            # Buscar estación de recarga en camino
            if not hay_recarga_disponible(ruta[i]):
                raise EnergiaInsuficienteError(
                    f"Energía insuficiente en segmento {ruta[i]} -> {ruta[i+1]}"
                )
            energia_actual = autonomia
```

### 3. Recuperación y Contingencias
```python
class GestorContingencias:
    def manejar_fallo_entrega(self, pedido: Pedido, error: Exception):
        """
        Maneja fallos durante la entrega
        """
        # Registrar error
        self.auditoria.registrar_error(pedido.id_pedido, str(error))
        
        # Intentar ruta alternativa
        try:
            ruta_alternativa = self.calcular_ruta_alternativa(pedido)
            pedido.asignar_ruta(ruta_alternativa)
            return True
        except:
            # Marcar pedido como fallido
            pedido.marcar_como_fallido(f"Error: {error}")
            return False
    
    def calcular_ruta_alternativa(self, pedido: Pedido):
        """
        Calcula ruta alternativa cuando falla la principal
        """
        # Buscar almacén alternativo
        almacenes = self.repositorio_almacenes.listar_operativos()
        for almacen in almacenes:
            if almacen.id_almacenamiento != pedido.almacenamiento_origen.id_almacenamiento:
                try:
                    return self.calcular_ruta(almacen.id_almacenamiento, pedido.cliente.id_cliente)
                except:
                    continue
        
        raise Exception("No se encontró ruta alternativa viable")
```

## Métricas y Monitoreo

### 1. KPIs del Sistema
```python
class MetricasSimulacion:
    def calcular_kpis(self):
        return {
            'tasa_exito_entregas': self.entregas_exitosas / self.total_entregas,
            'tiempo_promedio_entrega': self.suma_tiempos / self.entregas_completadas,
            'eficiencia_energetica': self.entregas_sin_recarga / self.total_entregas,
            'utilizacion_red': self.aristas_utilizadas / self.total_aristas,
            'saturacion_almacenes': self.pedidos_por_almacen_promedio,
            'cobertura_clientes': self.clientes_con_entregas / self.total_clientes
        }
```

### 2. Alertas y Umbrales
```python
class SistemaAlertas:
    def verificar_umbrales(self, metricas: dict):
        """
        Verifica umbrales críticos y genera alertas
        """
        if metricas['tasa_exito_entregas'] < 0.95:
            self.generar_alerta("CRITICA", "Tasa de éxito por debajo del 95%")
        
        if metricas['tiempo_promedio_entrega'] > 120:  # minutos
            self.generar_alerta("ADVERTENCIA", "Tiempo promedio alto")
        
        if metricas['eficiencia_energetica'] < 0.70:
            self.generar_alerta("INFO", "Considerar más estaciones de recarga")
```

## Testing de Flujos

### 1. Pruebas de Integración
```python
def test_flujo_completo_entrega():
    """
    Prueba el flujo completo desde creación hasta entrega
    """
    # Inicializar simulación
    simulacion = inicializar_simulacion(vertices=15, aristas=20, pedidos=5)
    
    # Obtener pedido pendiente
    pedido = simulacion.obtener_pedido_pendiente()
    assert pedido.estado == EstadoPedido.PENDIENTE
    
    # Calcular ruta
    ruta = simulacion.calcular_ruta_para_pedido(pedido.id_pedido)
    assert ruta is not None
    assert pedido.estado == EstadoPedido.EN_RUTA
    
    # Ejecutar entrega
    resultado = simulacion.ejecutar_entrega(pedido.id_pedido)
    assert resultado == True
    assert pedido.estado == EstadoPedido.ENTREGADO
    assert pedido.fecha_entrega is not None
```

### 2. Pruebas de Rendimiento
```python
def test_rendimiento_calculo_rutas():
    """
    Verifica que el cálculo de rutas sea eficiente
    """
    simulacion = inicializar_simulacion(vertices=100, aristas=200, pedidos=50)
    
    inicio = time.time()
    
    # Calcular rutas para todos los pedidos
    for pedido in simulacion.obtener_pedidos_pendientes():
        simulacion.calcular_ruta_para_pedido(pedido.id_pedido)
    
    tiempo_total = time.time() - inicio
    
    # Debe completarse en menos de 10 segundos
    assert tiempo_total < 10.0
    
    # Verificar que todas las rutas fueron calculadas
    assert len(simulacion.obtener_pedidos_en_ruta()) == 50
```

Estos flujos representan la orquestación completa del sistema y garantizan que todos los componentes trabajen de manera coordinada para cumplir los objetivos del negocio.

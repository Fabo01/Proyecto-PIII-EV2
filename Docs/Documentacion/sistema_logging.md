# Sistema de Logging y Auditoría

## Descripción General
El sistema implementa un robusto sistema de logging y auditoría que permite el seguimiento detallado de todas las operaciones, eventos y transacciones del sistema de drones logísticos.

## 📊 Niveles de Logging

### Configuración de Niveles
```python
import logging

# Configuración por componente
LOGGING_CONFIG = {
    'API.Rutas': logging.INFO,
    'RutaEstrategiaBFS': logging.DEBUG,
    'RepositorioPedidos': logging.INFO,
    'Simulacion': logging.INFO,
    'MapeadorRuta': logging.INFO
}
```

### Jerarquía de Severidad
1. **DEBUG**: Información detallada para diagnóstico
2. **INFO**: Eventos normales del sistema
3. **WARNING**: Situaciones inesperadas pero manejables
4. **ERROR**: Errores que afectan funcionalidad
5. **CRITICAL**: Errores graves que comprometen el sistema

## 🏗️ Estructura de Logs

### Formato Estándar
```
[NIVEL] TIMESTAMP - COMPONENTE - MENSAJE
[INFO] 2025-07-03 03:47:33,016 - API.Rutas - POST /rutas/calcular/1/bfs llamado
```

### Componentes Principales

#### 1. API Endpoints
```python
logger = logging.getLogger("API.Rutas")

@router.post("/calcular/{id_pedido}/{algoritmo}")
def calcular_ruta(id_pedido: int, algoritmo: str):
    logger.info(f"POST /rutas/calcular/{id_pedido}/{algoritmo} llamado")
    try:
        # Lógica de cálculo
        logger.info(f"POST /rutas/calcular/{id_pedido}/{algoritmo}: Ruta calculada correctamente")
    except Exception as e:
        logger.error(f"POST /rutas/calcular/{id_pedido}/{algoritmo}: Error: {str(e)}")
```

#### 2. Algoritmos de Rutas
```python
logger = logging.getLogger("RutaEstrategiaBFS")

def calcular_ruta(self, origen, destino, grafo, autonomia=50):
    logger.info(f"[BFS] Preparando para calcular ruta: origen={origen}, destino={destino}")
    logger.info(f"[BFS] Vértices disponibles en grafo: {len(list(grafo.vertices()))}")
    
    # Durante la exploración
    logger.debug(f"[BFS] Visitando: {vertice_actual} | Energia: {energia_actual}")
    logger.debug(f"[BFS] Evaluando arista: {origen} -> {destino} | Peso: {peso}")
    
    # Resultados
    if encontrado:
        logger.info(f"[BFS] Destino alcanzado: camino={len(camino)} aristas, peso_total={peso}")
    else:
        logger.warning(f"[BFS] No se encontró ruta entre {origen} y {destino}")
```

#### 3. Repositorios
```python
logger = logging.getLogger("RepositorioPedidos")

def obtener(self, id_pedido):
    pedido = self._pedidos.buscar(id_pedido)
    logger.info(f"[RepositorioPedidos] Pedido obtenido: id={id_pedido} | pedido={pedido}")
    return pedido

def agregar(self, pedido):
    self._pedidos.insertar(pedido.id_pedido, pedido)
    logger.info(f"[RepositorioPedidos] Pedido agregado: {pedido}")
```

#### 4. Mapeadores y DTOs
```python
logger = logging.getLogger("MapeadorRuta")

def a_dto(ruta: 'Ruta') -> 'RespuestaRuta':
    logger.info(f"Mapeando ruta: {type(ruta).__name__}")
    logger.info(f"Ruta ID: {getattr(ruta, 'id_ruta', 'NO_ENCONTRADO')}")
    logger.info(f"Algoritmo: {getattr(ruta, 'algoritmo', 'NO_ENCONTRADO')}")
    logger.info(f"Peso total: {getattr(ruta, 'peso_total', 'NO_ENCONTRADO')}")
```

## 📁 Archivos de Log

### Estructura de Archivos
```
logs/
├── simulacion_estadisticas.log    # Métricas y estadísticas
├── simulacion_pedidos.log         # Operaciones de pedidos
├── simulacion.log                 # Log general del sistema
├── api_rutas.log                  # Endpoints de rutas
├── algoritmos_debug.log           # Debug detallado de algoritmos
└── errores_criticos.log           # Solo errores graves
```

### Configuración de Rotación
```python
import logging.handlers

# Rotación por tamaño
file_handler = logging.handlers.RotatingFileHandler(
    'logs/simulacion.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)

# Rotación por tiempo
time_handler = logging.handlers.TimedRotatingFileHandler(
    'logs/simulacion_diario.log',
    when='midnight',
    interval=1,
    backupCount=30
)
```

## 🔍 Patrones de Logging Específicos

### 1. Trazabilidad de Pedidos
```python
def procesar_pedido(pedido):
    logger.info(f"PEDIDO_TRACE|{pedido.id_pedido}|INICIO|{datetime.now()}")
    
    try:
        # Procesamiento
        logger.info(f"PEDIDO_TRACE|{pedido.id_pedido}|RUTA_CALCULADA|{ruta.algoritmo}")
        logger.info(f"PEDIDO_TRACE|{pedido.id_pedido}|ENTREGA_EXITOSA|{datetime.now()}")
    except Exception as e:
        logger.error(f"PEDIDO_TRACE|{pedido.id_pedido}|ERROR|{str(e)}")
```

### 2. Métricas de Rendimiento
```python
def log_metricas_algoritmo(algoritmo, tiempo, iteraciones, vertices_explorados):
    logger.info(f"METRICS|{algoritmo}|tiempo={tiempo:.4f}s|iteraciones={iteraciones}|vertices={vertices_explorados}")
```

### 3. Auditoría de Cambios
```python
def log_cambio_estado(entidad, estado_anterior, estado_nuevo):
    logger.info(f"AUDIT|{entidad.__class__.__name__}|ID={entidad.id}|{estado_anterior}->{estado_nuevo}|user={current_user}")
```

## 🚨 Sistema de Alertas

### Configuración de Alertas
```python
class AlertHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            self.enviar_alerta(record)
    
    def enviar_alerta(self, record):
        # Integración con sistema de notificaciones
        mensaje = f"ALERTA: {record.getMessage()}"
        # webhook, email, Slack, etc.
```

### Tipos de Alertas
1. **Error de Algoritmo**: Cuando no se encuentra ruta
2. **Fallo de Repositorio**: Problemas de acceso a datos
3. **Timeout de API**: Respuestas lentas
4. **Memoria Alta**: Uso excesivo de recursos

## 📈 Métricas y KPIs

### Métricas Automáticas
```python
class MetricsLogger:
    def __init__(self):
        self.metricas = {
            'rutas_calculadas': 0,
            'tiempo_promedio_calculo': 0,
            'algoritmo_mas_usado': None,
            'tasa_exito_rutas': 0
        }
    
    def log_calculo_ruta(self, algoritmo, tiempo, exito):
        self.metricas['rutas_calculadas'] += 1
        if exito:
            self.metricas['tiempo_promedio_calculo'] = (
                self.metricas['tiempo_promedio_calculo'] + tiempo
            ) / 2
```

### Dashboard de Métricas
```python
def generar_dashboard_metricas():
    """
    Genera métricas para dashboard en tiempo real
    """
    return {
        'timestamp': datetime.now(),
        'sistema': {
            'uptime': get_uptime(),
            'memoria_uso': get_memory_usage(),
            'cpu_uso': get_cpu_usage()
        },
        'rutas': {
            'total_calculadas': count_rutas_calculadas(),
            'promedio_tiempo': avg_tiempo_calculo(),
            'tasa_exito': success_rate()
        },
        'pedidos': {
            'pendientes': count_pedidos_pendientes(),
            'entregados': count_pedidos_entregados(),
            'tiempo_promedio_entrega': avg_tiempo_entrega()
        }
    }
```

## 🔧 Configuración de Logging

### Archivo de Configuración
```python
# logging_config.py
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
        },
        'detailed': {
            'format': '[%(levelname)s] %(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/simulacion.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed'
        },
        'json_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/simulacion.json',
            'formatter': 'json'
        }
    },
    'loggers': {
        'API.Rutas': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'RutaEstrategiaBFS': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'RepositorioPedidos': {
            'handlers': ['console', 'file', 'json_file'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    }
}
```

## 📊 Análisis de Logs

### Herramientas de Análisis
```bash
# Búsqueda de errores
grep "ERROR" logs/simulacion.log | tail -20

# Análisis de rendimiento por algoritmo
grep "METRICS|bfs" logs/simulacion.log | awk -F'|' '{print $3}' | sort -n

# Trazabilidad de pedido específico
grep "PEDIDO_TRACE|123" logs/simulacion.log
```

### Scripts de Monitoreo
```python
def analizar_logs_tiempo_real():
    """
    Analiza logs en tiempo real para detectar patrones
    """
    with open('logs/simulacion.log', 'r') as f:
        f.seek(0, 2)  # Ir al final del archivo
        while True:
            line = f.readline()
            if line:
                if 'ERROR' in line:
                    procesar_error(line)
                elif 'METRICS' in line:
                    actualizar_metricas(line)
            time.sleep(0.1)
```

## 🔐 Consideraciones de Seguridad

### Sanitización de Logs
```python
def sanitizar_mensaje_log(mensaje):
    """
    Elimina información sensible de los logs
    """
    # Eliminar números de teléfono, emails, etc.
    import re
    
    # Ocultar números de teléfono
    mensaje = re.sub(r'\b\d{9,}\b', '***TELEFONO***', mensaje)
    
    # Ocultar direcciones de email
    mensaje = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                    '***EMAIL***', mensaje)
    
    return mensaje
```

### Compliance y Retención
```python
RETENTION_POLICY = {
    'logs_operacionales': 90,      # días
    'logs_auditoria': 365,         # días
    'logs_debug': 30,              # días
    'logs_metricas': 180           # días
}
```

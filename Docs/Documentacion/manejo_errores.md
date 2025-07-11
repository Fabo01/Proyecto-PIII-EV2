# Manejo de Errores y Excepciones

## Descripción General
El sistema implementa una estrategia integral de manejo de errores que abarca desde validaciones de entrada hasta recuperación de fallos críticos, garantizando la robustez y confiabilidad del sistema de drones logísticos.

## 🚨 Jerarquía de Excepciones

### Excepciones Base del Sistema
```python
# Backend/Dominio/Excepciones/ExcepcionesDominio.py

class SimulacionException(Exception):
    """Excepción base para errores del sistema de simulación"""
    def __init__(self, mensaje, codigo_error=None, detalles=None):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        self.detalles = detalles or {}
        super().__init__(self.mensaje)

class RutaException(SimulacionException):
    """Errores relacionados con cálculo de rutas"""
    pass

class PedidoException(SimulacionException):
    """Errores relacionados con gestión de pedidos"""
    pass

class GrafoException(SimulacionException):
    """Errores relacionados con la estructura del grafo"""
    pass

class RepositorioException(SimulacionException):
    """Errores relacionados con acceso a datos"""
    pass
```

### Excepciones Específicas
```python
class RutaNoEncontradaException(RutaException):
    """Se lanza cuando no se puede calcular una ruta válida"""
    def __init__(self, origen, destino, algoritmo, razon=None):
        self.origen = origen
        self.destino = destino
        self.algoritmo = algoritmo
        self.razon = razon
        
        mensaje = f"No se encontró ruta de {origen} a {destino} usando {algoritmo}"
        if razon:
            mensaje += f". Razón: {razon}"
        
        super().__init__(mensaje, "RUTA_001")

class AutonomiaInsuficienteException(RutaException):
    """Se lanza cuando no hay suficiente autonomía para completar la ruta"""
    def __init__(self, autonomia_actual, autonomia_requerida):
        self.autonomia_actual = autonomia_actual
        self.autonomia_requerida = autonomia_requerida
        
        mensaje = f"Autonomía insuficiente: actual={autonomia_actual}, requerida={autonomia_requerida}"
        super().__init__(mensaje, "RUTA_002")

class PedidoNoEncontradoException(PedidoException):
    """Se lanza cuando un pedido no existe en el repositorio"""
    def __init__(self, id_pedido):
        self.id_pedido = id_pedido
        mensaje = f"Pedido con ID {id_pedido} no encontrado"
        super().__init__(mensaje, "PEDIDO_001")

class GrafoDesconectadoException(GrafoException):
    """Se lanza cuando el grafo no es conectado"""
    def __init__(self, componentes_inconexos):
        self.componentes_inconexos = componentes_inconexos
        mensaje = f"Grafo desconectado: {len(componentes_inconexos)} componentes inconexos"
        super().__init__(mensaje, "GRAFO_001")
```

## 🛡️ Estrategias de Manejo por Capa

### 1. Capa de Dominio
```python
# Backend/Dominio/AlgEstrategias/RutaEstrategiaBFS.py

def calcular_ruta(self, origen, destino, grafo, autonomia=50, estaciones_recarga=None):
    try:
        # Validaciones iniciales
        if origen not in grafo.vertices():
            raise GrafoException(f"Vértice origen {origen} no existe en el grafo")
        
        if destino not in grafo.vertices():
            raise GrafoException(f"Vértice destino {destino} no existe en el grafo")
        
        if autonomia <= 0:
            raise ValueError("Autonomía debe ser mayor que 0")
        
        # Lógica de cálculo
        resultado = self._ejecutar_bfs(origen, destino, grafo, autonomia)
        
        if not resultado:
            # Análisis de causas del fallo
            causa = self._diagnosticar_fallo_ruta(origen, destino, grafo, autonomia)
            raise RutaNoEncontradaException(origen, destino, "BFS", causa)
        
        return resultado
        
    except (GrafoException, RutaException):
        # Re-lanzar excepciones conocidas
        raise
    except Exception as e:
        # Envolver excepciones inesperadas
        logger.exception(f"Error inesperado en cálculo BFS: {e}")
        raise RutaException(f"Error interno en BFS: {str(e)}", "RUTA_999")

def _diagnosticar_fallo_ruta(self, origen, destino, grafo, autonomia):
    """Analiza por qué falló el cálculo de ruta"""
    try:
        # Verificar conectividad básica
        if not self._es_alcanzable(origen, destino, grafo):
            return "Vértices no conectados en el grafo"
        
        # Verificar autonomía
        ruta_directa = self._calcular_distancia_directa(origen, destino, grafo)
        if ruta_directa and ruta_directa > autonomia:
            return f"Autonomía insuficiente: ruta requiere {ruta_directa}, disponible {autonomia}"
        
        # Verificar disponibilidad de recargas
        if not self._hay_estaciones_recarga_intermedias(origen, destino, grafo):
            return "No hay estaciones de recarga intermedias disponibles"
        
        return "Causa desconocida"
    except:
        return "Error en diagnóstico"
```

### 2. Capa de Aplicación
```python
# Backend/Aplicacion/SimAplicacion/Aplicacion_Simulacion.py

def calcular_ruta(self, id_pedido: int, algoritmo: str):
    try:
        # Validación de entrada
        if not isinstance(id_pedido, int) or id_pedido <= 0:
            raise ValueError("ID de pedido debe ser un entero positivo")
        
        if algoritmo not in self.algoritmos_disponibles():
            raise ValueError(f"Algoritmo {algoritmo} no soportado")
        
        # Obtener pedido
        pedido = self._serv.obtener_pedido(id_pedido)
        if pedido is None:
            raise PedidoNoEncontradoException(id_pedido)
        
        # Calcular ruta
        ruta = self._serv.calcular_ruta(id_pedido, algoritmo)
        
        return ruta
        
    except (PedidoNoEncontradoException, RutaException):
        # Errores de dominio - re-lanzar
        raise
    except ValueError as e:
        # Errores de validación - convertir a excepción de dominio
        raise PedidoException(f"Error de validación: {str(e)}", "VALIDACION_001")
    except Exception as e:
        # Errores inesperados
        logger.exception(f"Error inesperado calculando ruta: {e}")
        raise SimulacionException(f"Error interno: {str(e)}", "SISTEMA_001")
```

### 3. Capa de API
```python
# Backend/API/rutas_enrutador.py

@router.post("/calcular/{id_pedido}/{algoritmo}", response_model=RespuestaRuta)
def calcular_ruta(id_pedido: int, algoritmo: str, service=Depends(get_simulacion_service)):
    try:
        logger.info(f"POST /rutas/calcular/{id_pedido}/{algoritmo} llamado")
        
        ruta = service.calcular_ruta(id_pedido, algoritmo)
        
        # Mapear a DTO
        resultado = MapeadorRuta.a_dto(ruta)
        
        logger.info(f"POST /rutas/calcular/{id_pedido}/{algoritmo}: Ruta calculada correctamente")
        return resultado
        
    except PedidoNoEncontradoException as e:
        logger.warning(f"Pedido no encontrado: {e}")
        raise HTTPException(
            status_code=404, 
            detail={
                "error": "PEDIDO_NO_ENCONTRADO",
                "mensaje": str(e),
                "id_pedido": e.id_pedido
            }
        )
    
    except RutaNoEncontradaException as e:
        logger.warning(f"Ruta no encontrada: {e}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "RUTA_NO_ENCONTRADA",
                "mensaje": str(e),
                "origen": str(e.origen),
                "destino": str(e.destino),
                "algoritmo": e.algoritmo,
                "razon": e.razon
            }
        )
    
    except RutaException as e:
        logger.error(f"Error de ruta: {e}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": e.codigo_error or "RUTA_ERROR",
                "mensaje": str(e),
                "detalles": e.detalles
            }
        )
    
    except SimulacionException as e:
        logger.error(f"Error de simulación: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": e.codigo_error or "SIMULACION_ERROR", 
                "mensaje": str(e)
            }
        )
    
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "ERROR_INTERNO",
                "mensaje": "Error interno del servidor"
            }
        )
```

## 🔄 Estrategias de Recuperación

### 1. Reintentos con Backoff
```python
import time
import random

def calcular_ruta_con_reintentos(self, pedido, algoritmo, max_reintentos=3):
    """Calcula ruta con estrategia de reintentos"""
    
    for intento in range(max_reintentos):
        try:
            return self._calcular_ruta_interno(pedido, algoritmo)
            
        except RutaNoEncontradaException as e:
            if intento == max_reintentos - 1:
                # Último intento - re-lanzar
                raise
            
            # Estrategia de recuperación
            if "autonomía insuficiente" in str(e):
                # Intentar con algoritmo alternativo
                algoritmo = self._seleccionar_algoritmo_alternativo(algoritmo)
                logger.info(f"Reintentando con algoritmo alternativo: {algoritmo}")
            
            # Backoff exponencial con jitter
            delay = (2 ** intento) + random.uniform(0, 1)
            time.sleep(delay)
            
        except Exception as e:
            # Error inesperado - no reintentar
            raise

def _seleccionar_algoritmo_alternativo(self, algoritmo_fallido):
    """Selecciona algoritmo alternativo basado en el que falló"""
    alternativas = {
        'bfs': 'dijkstra',
        'dfs': 'bfs', 
        'dijkstra': 'floydwarshall',
        'floydwarshall': 'bfs'
    }
    return alternativas.get(algoritmo_fallido, 'bfs')
```

### 2. Fallback a Datos Cached
```python
def obtener_ruta_con_fallback(self, pedido, algoritmo):
    """Obtiene ruta con fallback a cache"""
    try:
        # Intentar cálculo normal
        return self.calcular_ruta(pedido, algoritmo)
        
    except RutaNoEncontradaException:
        # Fallback 1: Buscar en cache de rutas similares
        ruta_cache = self._buscar_ruta_similar_cache(pedido.origen, pedido.destino)
        if ruta_cache:
            logger.info("Usando ruta desde cache")
            return ruta_cache
        
        # Fallback 2: Ruta pre-calculada más cercana
        ruta_precalculada = self._buscar_ruta_precalculada_cercana(pedido)
        if ruta_precalculada:
            logger.info("Usando ruta pre-calculada cercana")
            return ruta_precalculada
        
        # Sin fallbacks disponibles
        raise
```

### 3. Degradación Graceful
```python
def procesar_pedido_con_degradacion(self, pedido):
    """Procesa pedido con degradación de funcionalidad"""
    try:
        # Funcionamiento normal
        return self._procesar_pedido_completo(pedido)
        
    except RutaNoEncontradaException:
        # Degradación: marcar para procesamiento manual
        logger.warning(f"Degradando pedido {pedido.id} a procesamiento manual")
        pedido.estado = "procesamiento_manual"
        pedido.observaciones = "Ruta no calculable automáticamente"
        self._notificar_procesamiento_manual(pedido)
        return {"estado": "degradado", "requiere_atencion": True}
        
    except AutonomiaInsuficienteException:
        # Degradación: sugerir división del pedido
        logger.info(f"Sugiriendo división de pedido {pedido.id}")
        return {"estado": "requiere_division", "sugerencia": "dividir_pedido"}
```

## 📊 Monitoreo y Alertas de Errores

### Sistema de Métricas de Errores
```python
class ErrorMetrics:
    def __init__(self):
        self.contadores = {
            'rutas_no_encontradas': 0,
            'pedidos_no_encontrados': 0,
            'errores_autonomia': 0,
            'errores_grafo': 0,
            'errores_sistema': 0
        }
        
        self.tendencias = {
            'errores_por_hora': [],
            'algoritmos_con_mas_errores': {},
            'rutas_problematicas': {}
        }
    
    def registrar_error(self, excepcion):
        """Registra un error para análisis"""
        tipo_error = type(excepcion).__name__
        
        if isinstance(excepcion, RutaNoEncontradaException):
            self.contadores['rutas_no_encontradas'] += 1
            self._analizar_ruta_problematica(excepcion)
            
        elif isinstance(excepcion, PedidoNoEncontradoException):
            self.contadores['pedidos_no_encontrados'] += 1
            
        # Alertas automáticas
        if self._detectar_patron_critico():
            self._enviar_alerta_critica()
    
    def _detectar_patron_critico(self):
        """Detecta patrones críticos de errores"""
        # Más del 10% de rutas fallan
        if self.contadores['rutas_no_encontradas'] > 10:
            return True
        
        # Muchos errores en corto tiempo
        errores_recientes = sum(self.tendencias['errores_por_hora'][-3:])
        if errores_recientes > 50:
            return True
        
        return False
```

### Dashboard de Errores
```python
def generar_reporte_errores():
    """Genera reporte detallado de errores"""
    return {
        'resumen': {
            'total_errores': sum(ErrorMetrics.contadores.values()),
            'tasa_error': calcular_tasa_error(),
            'tiempo_promedio_recuperacion': calcular_mttr()
        },
        'por_categoria': ErrorMetrics.contadores,
        'tendencias': {
            'ultima_hora': ErrorMetrics.tendencias['errores_por_hora'][-1],
            'algoritmo_mas_problematico': max(
                ErrorMetrics.tendencias['algoritmos_con_mas_errores'],
                key=ErrorMetrics.tendencias['algoritmos_con_mas_errores'].get
            )
        },
        'acciones_recomendadas': generar_recomendaciones()
    }
```

## 🔧 Testing de Manejo de Errores

### Tests de Casos Excepcionales
```python
import pytest

class TestManejoErrores:
    
    def test_ruta_no_encontrada_bfs(self):
        """Test que BFS maneja correctamente cuando no hay ruta"""
        with pytest.raises(RutaNoEncontradaException) as exc_info:
            self.calculador.calcular_ruta(
                origen=self.vertice_aislado,
                destino=self.vertice_inaccesible,
                algoritmo='bfs'
            )
        
        assert exc_info.value.algoritmo == 'bfs'
        assert "no conectados" in exc_info.value.razon
    
    def test_autonomia_insuficiente(self):
        """Test manejo de autonomía insuficiente"""
        with pytest.raises(AutonomiaInsuficienteException) as exc_info:
            self.calculador.calcular_ruta(
                origen=self.almacen,
                destino=self.cliente_lejano,
                algoritmo='bfs',
                autonomia=10  # Muy baja
            )
        
        assert exc_info.value.autonomia_actual == 10
        assert exc_info.value.autonomia_requerida > 10
    
    def test_recuperacion_con_algoritmo_alternativo(self):
        """Test recuperación usando algoritmo alternativo"""
        # Simular fallo con BFS
        with patch.object(self.estrategia_bfs, 'calcular_ruta', 
                         side_effect=RutaNoEncontradaException):
            
            # Debe intentar con algoritmo alternativo
            resultado = self.calculador.calcular_ruta_con_recuperacion(
                self.pedido, 'bfs'
            )
            
            assert resultado is not None
            assert resultado.algoritmo == 'dijkstra'  # Algoritmo alternativo
```

## 📋 Catálogo de Códigos de Error

### Códigos de Error Estándar
```python
CODIGOS_ERROR = {
    # Errores de Ruta (RUTA_XXX)
    'RUTA_001': 'Ruta no encontrada',
    'RUTA_002': 'Autonomía insuficiente',
    'RUTA_003': 'Algoritmo no soportado',
    'RUTA_004': 'Grafo desconectado',
    'RUTA_005': 'Timeout en cálculo',
    
    # Errores de Pedido (PEDIDO_XXX)
    'PEDIDO_001': 'Pedido no encontrado',
    'PEDIDO_002': 'Pedido en estado inválido',
    'PEDIDO_003': 'Cliente no válido',
    'PEDIDO_004': 'Almacén no válido',
    
    # Errores de Grafo (GRAFO_XXX)
    'GRAFO_001': 'Grafo desconectado',
    'GRAFO_002': 'Vértice no encontrado',
    'GRAFO_003': 'Arista inválida',
    
    # Errores de Sistema (SISTEMA_XXX)
    'SISTEMA_001': 'Error interno',
    'SISTEMA_002': 'Recurso no disponible',
    'SISTEMA_003': 'Timeout del sistema'
}
```

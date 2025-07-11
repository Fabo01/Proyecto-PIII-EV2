# Documentación de Patrones Observer y Eventos

## Descripción General
El sistema implementa el patrón Observer para gestionar eventos y notificaciones de manera desacoplada. Este patrón permite que múltiples componentes reaccionen a cambios en el estado del sistema sin crear dependencias directas, facilitando la auditoría, estadísticas y actualizaciones en tiempo real.

## Ubicación en la Arquitectura
- **Capa de Servicios**: `Backend/Servicios/Observer/`
- **Patrón**: Observer Pattern con Event-Driven Architecture
- **Responsabilidad**: Gestión de eventos y notificaciones entre componentes

## Estructura del Sistema de Eventos

### 1. Jerarquía de Eventos
```python
# Backend/Servicios/Observer/eventos.py

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum

class TipoEvento(Enum):
    # Eventos de Simulación
    SIMULACION_INICIADA = "simulacion_iniciada"
    SIMULACION_REINICIADA = "simulacion_reiniciada"
    SIMULACION_FINALIZADA = "simulacion_finalizada"
    
    # Eventos de Pedidos
    PEDIDO_CREADO = "pedido_creado"
    PEDIDO_ACTUALIZADO = "pedido_actualizado"
    PEDIDO_CANCELADO = "pedido_cancelado"
    PEDIDO_ESTADO_CAMBIADO = "pedido_estado_cambiado"
    
    # Eventos de Rutas
    RUTA_CALCULADA = "ruta_calculada"
    RUTA_ASIGNADA = "ruta_asignada"
    RUTA_INICIADA = "ruta_iniciada"
    RUTA_COMPLETADA = "ruta_completada"
    RUTA_FALLIDA = "ruta_fallida"
    
    # Eventos de Entrega
    ENTREGA_INICIADA = "entrega_iniciada"
    ENTREGA_EN_PROGRESO = "entrega_en_progreso"
    ENTREGA_COMPLETADA = "entrega_completada"
    ENTREGA_FALLIDA = "entrega_fallida"
    
    # Eventos de Recarga
    RECARGA_INICIADA = "recarga_iniciada"
    RECARGA_COMPLETADA = "recarga_completada"
    
    # Eventos de Sistema
    ERROR_SISTEMA = "error_sistema"
    ADVERTENCIA_SISTEMA = "advertencia_sistema"
    METRICA_ACTUALIZADA = "metrica_actualizada"

class Evento(ABC):
    """Clase base para todos los eventos del sistema"""
    
    def __init__(self, tipo: TipoEvento, entidad_id: str, datos: Dict[str, Any] = None):
        self.tipo: TipoEvento = tipo
        self.entidad_id: str = entidad_id
        self.timestamp: datetime = datetime.now()
        self.datos: Dict[str, Any] = datos or {}
        self.id_evento: str = f"{tipo.value}_{entidad_id}_{int(self.timestamp.timestamp())}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el evento a diccionario para serialización"""
        return {
            'id_evento': self.id_evento,
            'tipo': self.tipo.value,
            'entidad_id': self.entidad_id,
            'timestamp': self.timestamp.isoformat(),
            'datos': self.datos
        }
```

### 2. Eventos Específicos
```python
class EventoPedido(Evento):
    """Eventos relacionados con pedidos"""
    
    def __init__(self, tipo: TipoEvento, pedido_id: str, estado_anterior: str = None, 
                 estado_nuevo: str = None, datos_adicionales: Dict[str, Any] = None):
        datos = datos_adicionales or {}
        if estado_anterior:
            datos['estado_anterior'] = estado_anterior
        if estado_nuevo:
            datos['estado_nuevo'] = estado_nuevo
            
        super().__init__(tipo, pedido_id, datos)

class EventoRuta(Evento):
    """Eventos relacionados con rutas"""
    
    def __init__(self, tipo: TipoEvento, ruta_id: str, pedido_id: str = None,
                 costo_total: float = None, requiere_recarga: bool = False,
                 datos_adicionales: Dict[str, Any] = None):
        datos = datos_adicionales or {}
        if pedido_id:
            datos['pedido_id'] = pedido_id
        if costo_total is not None:
            datos['costo_total'] = costo_total
        datos['requiere_recarga'] = requiere_recarga
        
        super().__init__(tipo, ruta_id, datos)

class EventoEntrega(Evento):
    """Eventos relacionados con entregas"""
    
    def __init__(self, tipo: TipoEvento, entrega_id: str, pedido_id: str,
                 ubicacion_actual: str = None, energia_restante: float = None,
                 datos_adicionales: Dict[str, Any] = None):
        datos = datos_adicionales or {}
        datos['pedido_id'] = pedido_id
        if ubicacion_actual:
            datos['ubicacion_actual'] = ubicacion_actual
        if energia_restante is not None:
            datos['energia_restante'] = energia_restante
            
        super().__init__(tipo, entrega_id, datos)

class EventoSistema(Evento):
    """Eventos del sistema general"""
    
    def __init__(self, tipo: TipoEvento, componente: str, mensaje: str,
                 nivel_severidad: str = "INFO", datos_adicionales: Dict[str, Any] = None):
        datos = datos_adicionales or {}
        datos['componente'] = componente
        datos['mensaje'] = mensaje
        datos['nivel_severidad'] = nivel_severidad
        
        super().__init__(tipo, componente, datos)
```

## 3. Interfaz de Observador

### Observador Base
```python
# Backend/Servicios/Observer/observador.py

from abc import ABC, abstractmethod
from typing import List, Callable, Optional

class IObservador(ABC):
    """Interfaz base para todos los observadores"""
    
    @abstractmethod
    def notificar(self, evento: Evento) -> None:
        """Procesa un evento recibido"""
        pass
    
    @abstractmethod
    def obtener_tipos_interes(self) -> List[TipoEvento]:
        """Retorna los tipos de eventos que le interesan al observador"""
        pass
    
    @abstractmethod
    def obtener_nombre(self) -> str:
        """Retorna el nombre identificador del observador"""
        pass

class ObservadorBase(IObservador):
    """Implementación base con funcionalidades comunes"""
    
    def __init__(self, nombre: str, tipos_interes: List[TipoEvento] = None):
        self._nombre: str = nombre
        self._tipos_interes: List[TipoEvento] = tipos_interes or []
        self._activo: bool = True
        self._eventos_procesados: int = 0
        self._ultimo_evento: Optional[datetime] = None
    
    def obtener_tipos_interes(self) -> List[TipoEvento]:
        return self._tipos_interes
    
    def obtener_nombre(self) -> str:
        return self._nombre
    
    def esta_activo(self) -> bool:
        return self._activo
    
    def activar(self) -> None:
        self._activo = True
    
    def desactivar(self) -> None:
        self._activo = False
    
    def notificar(self, evento: Evento) -> None:
        if not self._activo:
            return
        
        if not self._tipos_interes or evento.tipo in self._tipos_interes:
            try:
                self._procesar_evento(evento)
                self._eventos_procesados += 1
                self._ultimo_evento = evento.timestamp
            except Exception as e:
                self._manejar_error(evento, e)
    
    @abstractmethod
    def _procesar_evento(self, evento: Evento) -> None:
        """Lógica específica de procesamiento del evento"""
        pass
    
    def _manejar_error(self, evento: Evento, error: Exception) -> None:
        """Maneja errores durante el procesamiento"""
        print(f"Error en observador {self._nombre}: {error}")
```

## 4. Gestores de Eventos

### Gestor Principal
```python
# Backend/Servicios/Observer/gestor_eventos.py

class GestorEventos:
    """Gestor central del sistema de eventos"""
    
    def __init__(self):
        self._observadores: Dict[str, IObservador] = {}
        self._suscripciones: Dict[TipoEvento, List[str]] = {}
        self._historial_eventos: List[Evento] = []
        self._max_historial: int = 1000
        self._activo: bool = True
    
    def suscribir_observador(self, observador: IObservador) -> bool:
        """Registra un observador en el sistema"""
        nombre = observador.obtener_nombre()
        
        if nombre in self._observadores:
            return False
        
        self._observadores[nombre] = observador
        
        # Registrar suscripciones por tipo de evento
        for tipo_evento in observador.obtener_tipos_interes():
            if tipo_evento not in self._suscripciones:
                self._suscripciones[tipo_evento] = []
            self._suscripciones[tipo_evento].append(nombre)
        
        return True
    
    def desuscribir_observador(self, nombre_observador: str) -> bool:
        """Elimina un observador del sistema"""
        if nombre_observador not in self._observadores:
            return False
        
        observador = self._observadores[nombre_observador]
        
        # Remover de suscripciones
        for tipo_evento in observador.obtener_tipos_interes():
            if tipo_evento in self._suscripciones:
                if nombre_observador in self._suscripciones[tipo_evento]:
                    self._suscripciones[tipo_evento].remove(nombre_observador)
        
        # Remover observador
        del self._observadores[nombre_observador]
        return True
    
    def publicar_evento(self, evento: Evento) -> None:
        """Publica un evento a todos los observadores interesados"""
        if not self._activo:
            return
        
        # Agregar al historial
        self._agregar_al_historial(evento)
        
        # Notificar observadores suscritos
        observadores_a_notificar = self._suscripciones.get(evento.tipo, [])
        
        for nombre_observador in observadores_a_notificar:
            if nombre_observador in self._observadores:
                observador = self._observadores[nombre_observador]
                try:
                    observador.notificar(evento)
                except Exception as e:
                    self._manejar_error_notificacion(observador, evento, e)
    
    def _agregar_al_historial(self, evento: Evento) -> None:
        """Mantiene historial de eventos con límite de tamaño"""
        self._historial_eventos.append(evento)
        
        if len(self._historial_eventos) > self._max_historial:
            self._historial_eventos = self._historial_eventos[-self._max_historial:]
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema de eventos"""
        return {
            'observadores_registrados': len(self._observadores),
            'tipos_evento_con_suscripciones': len(self._suscripciones),
            'eventos_en_historial': len(self._historial_eventos),
            'sistema_activo': self._activo,
            'observadores': {
                nombre: {
                    'activo': obs.esta_activo() if hasattr(obs, 'esta_activo') else True,
                    'tipos_interes': len(obs.obtener_tipos_interes())
                }
                for nombre, obs in self._observadores.items()
            }
        }
```

## 5. Observadores Especializados

### Observador de Auditoría
```python
# Backend/Servicios/Observer/observador_auditoria.py

class ObservadorAuditoria(ObservadorBase):
    """Observador que registra todos los eventos para auditoría"""
    
    def __init__(self, repositorio_auditoria):
        super().__init__(
            "auditoria",
            list(TipoEvento)  # Interesado en todos los eventos
        )
        self._repositorio = repositorio_auditoria
    
    def _procesar_evento(self, evento: Evento) -> None:
        """Registra evento en el sistema de auditoría"""
        registro_auditoria = {
            'id_evento': evento.id_evento,
            'tipo_evento': evento.tipo.value,
            'entidad_afectada': evento.entidad_id,
            'timestamp': evento.timestamp,
            'datos_evento': evento.datos,
            'contexto': self._extraer_contexto(evento)
        }
        
        self._repositorio.guardar_registro(registro_auditoria)
    
    def _extraer_contexto(self, evento: Evento) -> Dict[str, Any]:
        """Extrae contexto adicional según el tipo de evento"""
        contexto = {}
        
        if evento.tipo in [TipoEvento.PEDIDO_CREADO, TipoEvento.PEDIDO_ESTADO_CAMBIADO]:
            contexto['categoria'] = 'gestion_pedidos'
        elif evento.tipo in [TipoEvento.RUTA_CALCULADA, TipoEvento.RUTA_COMPLETADA]:
            contexto['categoria'] = 'operaciones_ruta'
        elif evento.tipo in [TipoEvento.ENTREGA_COMPLETADA, TipoEvento.ENTREGA_FALLIDA]:
            contexto['categoria'] = 'entregas'
        
        return contexto

class ObservadorEstadisticas(ObservadorBase):
    """Observador que actualiza métricas y estadísticas del sistema"""
    
    def __init__(self, gestor_estadisticas):
        super().__init__(
            "estadisticas",
            [
                TipoEvento.PEDIDO_CREADO,
                TipoEvento.RUTA_CALCULADA,
                TipoEvento.ENTREGA_COMPLETADA,
                TipoEvento.ENTREGA_FALLIDA,
                TipoEvento.RECARGA_COMPLETADA
            ]
        )
        self._gestor_estadisticas = gestor_estadisticas
    
    def _procesar_evento(self, evento: Evento) -> None:
        """Actualiza estadísticas según el tipo de evento"""
        if evento.tipo == TipoEvento.PEDIDO_CREADO:
            self._gestor_estadisticas.incrementar_pedidos_creados()
        
        elif evento.tipo == TipoEvento.RUTA_CALCULADA:
            costo = evento.datos.get('costo_total', 0)
            requiere_recarga = evento.datos.get('requiere_recarga', False)
            self._gestor_estadisticas.registrar_ruta_calculada(costo, requiere_recarga)
        
        elif evento.tipo == TipoEvento.ENTREGA_COMPLETADA:
            tiempo_entrega = evento.datos.get('tiempo_total')
            if tiempo_entrega:
                self._gestor_estadisticas.registrar_entrega_exitosa(tiempo_entrega)
        
        elif evento.tipo == TipoEvento.ENTREGA_FALLIDA:
            motivo = evento.datos.get('motivo', 'desconocido')
            self._gestor_estadisticas.registrar_entrega_fallida(motivo)
        
        elif evento.tipo == TipoEvento.RECARGA_COMPLETADA:
            estacion_id = evento.datos.get('estacion_id')
            if estacion_id:
                self._gestor_estadisticas.incrementar_uso_estacion(estacion_id)

class ObservadorDashboard(ObservadorBase):
    """Observador que actualiza el dashboard en tiempo real"""
    
    def __init__(self, cache_dashboard):
        super().__init__(
            "dashboard",
            [
                TipoEvento.SIMULACION_INICIADA,
                TipoEvento.PEDIDO_ESTADO_CAMBIADO,
                TipoEvento.RUTA_ASIGNADA,
                TipoEvento.ENTREGA_EN_PROGRESO,
                TipoEvento.ENTREGA_COMPLETADA
            ]
        )
        self._cache = cache_dashboard
    
    def _procesar_evento(self, evento: Evento) -> None:
        """Actualiza cache del dashboard para visualización en tiempo real"""
        if evento.tipo == TipoEvento.SIMULACION_INICIADA:
            self._cache.invalidar_todo()
            self._cache.marcar_simulacion_activa(True)
        
        elif evento.tipo == TipoEvento.PEDIDO_ESTADO_CAMBIADO:
            pedido_id = evento.entidad_id
            nuevo_estado = evento.datos.get('estado_nuevo')
            self._cache.actualizar_estado_pedido(pedido_id, nuevo_estado)
        
        elif evento.tipo == TipoEvento.ENTREGA_EN_PROGRESO:
            ubicacion = evento.datos.get('ubicacion_actual')
            energia = evento.datos.get('energia_restante')
            self._cache.actualizar_posicion_entrega(evento.entidad_id, ubicacion, energia)
```

## 6. Eventos en el Flujo de Negocio

### Integración con Servicios
```python
# Backend/Servicios/SimServicios/Servicios_Simulacion.py

class ServiciosSimulacion:
    def __init__(self, gestor_eventos: GestorEventos):
        self._gestor_eventos = gestor_eventos
        # ... otros componentes
    
    def crear_pedido(self, datos_pedido: dict) -> Pedido:
        """Crea pedido y publica eventos correspondientes"""
        # Crear pedido
        pedido = self._fabrica_pedidos.crear_pedido(**datos_pedido)
        
        # Guardar en repositorio
        self._repositorio_pedidos.guardar(pedido)
        
        # Publicar evento
        evento = EventoPedido(
            TipoEvento.PEDIDO_CREADO,
            pedido.id_pedido,
            datos_adicionales={
                'cliente_id': pedido.cliente.id_cliente,
                'prioridad': pedido.prioridad.value,
                'descripcion': pedido.descripcion
            }
        )
        self._gestor_eventos.publicar_evento(evento)
        
        return pedido
    
    def calcular_ruta_para_pedido(self, pedido_id: str) -> Optional[Ruta]:
        """Calcula ruta y publica eventos de progreso"""
        pedido = self._repositorio_pedidos.obtener(pedido_id)
        if not pedido:
            return None
        
        # Publicar inicio de cálculo
        evento_inicio = EventoRuta(
            TipoEvento.RUTA_CALCULADA,
            f"ruta_temp_{pedido_id}",
            pedido_id=pedido_id,
            datos_adicionales={'estado': 'iniciando_calculo'}
        )
        self._gestor_eventos.publicar_evento(evento_inicio)
        
        # Calcular ruta
        ruta = self._estrategia_ruta.calcular_ruta(
            pedido.almacenamiento_origen.id_almacenamiento,
            pedido.cliente.id_cliente
        )
        
        if ruta:
            # Asignar ruta al pedido
            pedido.asignar_ruta(ruta)
            
            # Cambiar estado del pedido
            estado_anterior = pedido.estado
            pedido.iniciar_procesamiento()
            
            # Publicar eventos
            evento_ruta = EventoRuta(
                TipoEvento.RUTA_ASIGNADA,
                ruta.id_ruta,
                pedido_id=pedido_id,
                costo_total=ruta.obtener_costo_total(),
                requiere_recarga=len(ruta.obtener_estaciones_recarga()) > 0
            )
            self._gestor_eventos.publicar_evento(evento_ruta)
            
            evento_estado = EventoPedido(
                TipoEvento.PEDIDO_ESTADO_CAMBIADO,
                pedido_id,
                estado_anterior=estado_anterior.value,
                estado_nuevo=pedido.estado.value
            )
            self._gestor_eventos.publicar_evento(evento_estado)
        
        return ruta
```

## 7. Testing del Sistema de Eventos

### Pruebas Unitarias
```python
# tests/test_observer.py

class TestSistemaEventos:
    def test_suscripcion_observador(self):
        """Verifica suscripción correcta de observadores"""
        gestor = GestorEventos()
        observador = ObservadorMock("test", [TipoEvento.PEDIDO_CREADO])
        
        resultado = gestor.suscribir_observador(observador)
        
        assert resultado == True
        estadisticas = gestor.obtener_estadisticas()
        assert estadisticas['observadores_registrados'] == 1
    
    def test_publicacion_evento(self):
        """Verifica que los eventos se publican correctamente"""
        gestor = GestorEventos()
        observador_mock = ObservadorMock("test", [TipoEvento.PEDIDO_CREADO])
        gestor.suscribir_observador(observador_mock)
        
        evento = EventoPedido(TipoEvento.PEDIDO_CREADO, "PED001")
        gestor.publicar_evento(evento)
        
        assert observador_mock.eventos_recibidos == 1
        assert observador_mock.ultimo_evento.entidad_id == "PED001"
    
    def test_filtrado_por_tipo_evento(self):
        """Verifica que solo se notifican eventos de interés"""
        gestor = GestorEventos()
        observador = ObservadorMock("test", [TipoEvento.PEDIDO_CREADO])
        gestor.suscribir_observador(observador)
        
        # Evento de interés
        evento_interes = EventoPedido(TipoEvento.PEDIDO_CREADO, "PED001")
        gestor.publicar_evento(evento_interes)
        
        # Evento no de interés
        evento_no_interes = EventoRuta(TipoEvento.RUTA_CALCULADA, "RUT001")
        gestor.publicar_evento(evento_no_interes)
        
        assert observador.eventos_recibidos == 1

class ObservadorMock(ObservadorBase):
    def __init__(self, nombre: str, tipos_interes: List[TipoEvento]):
        super().__init__(nombre, tipos_interes)
        self.eventos_recibidos = 0
        self.ultimo_evento = None
    
    def _procesar_evento(self, evento: Evento) -> None:
        self.eventos_recibidos += 1
        self.ultimo_evento = evento
```

### Pruebas de Integración
```python
def test_flujo_completo_con_eventos():
    """Prueba el flujo completo con sistema de eventos"""
    # Configurar sistema
    gestor_eventos = GestorEventos()
    auditoria = RepositorioAuditoriaMock()
    estadisticas = GestorEstadisticasMock()
    
    # Suscribir observadores
    gestor_eventos.suscribir_observador(ObservadorAuditoria(auditoria))
    gestor_eventos.suscribir_observador(ObservadorEstadisticas(estadisticas))
    
    # Simular creación de pedido
    simulacion = ServiciosSimulacion(gestor_eventos)
    pedido = simulacion.crear_pedido({
        'cliente_id': 'CLI001',
        'almacenamiento_id': 'ALM001',
        'descripcion': 'Test'
    })
    
    # Verificar eventos de auditoría
    assert auditoria.registros_guardados == 1
    assert auditoria.ultimo_registro['tipo_evento'] == 'pedido_creado'
    
    # Verificar estadísticas
    assert estadisticas.pedidos_creados == 1
    
    # Calcular ruta
    ruta = simulacion.calcular_ruta_para_pedido(pedido.id_pedido)
    
    # Verificar más eventos
    assert auditoria.registros_guardados >= 2  # Al menos pedido creado + ruta asignada
    assert estadisticas.rutas_calculadas == 1
```

## 8. Métricas y Monitoreo

### Métricas del Sistema de Eventos
```python
class MetricasEventos:
    def __init__(self, gestor_eventos: GestorEventos):
        self._gestor = gestor_eventos
        self._inicio_monitoreo = datetime.now()
    
    def obtener_reporte_rendimiento(self) -> Dict[str, Any]:
        """Genera reporte de rendimiento del sistema de eventos"""
        estadisticas = self._gestor.obtener_estadisticas()
        
        return {
            'tiempo_operacion': (datetime.now() - self._inicio_monitoreo).total_seconds(),
            'observadores_activos': sum(
                1 for obs_info in estadisticas['observadores'].values() 
                if obs_info['activo']
            ),
            'eventos_procesados_total': len(self._gestor._historial_eventos),
            'tipos_evento_activos': len(self._gestor._suscripciones),
            'eficiencia_notificacion': self._calcular_eficiencia_notificacion(),
            'observadores_mas_activos': self._obtener_observadores_mas_activos()
        }
    
    def _calcular_eficiencia_notificacion(self) -> float:
        """Calcula eficiencia de las notificaciones"""
        total_notificaciones = 0
        notificaciones_exitosas = 0
        
        # Implementar lógica de cálculo basada en métricas internas
        # Esta sería una aproximación basada en eventos procesados
        
        return notificaciones_exitosas / max(total_notificaciones, 1)
```

El sistema de eventos y observadores proporciona una arquitectura robusta y extensible que permite monitorear, auditar y reaccionar a todos los cambios importantes en el sistema de manera desacoplada y eficiente.

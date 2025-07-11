# Documentación de Repositorios y Gestión de Datos

## Descripción General
Los repositorios implementan el patrón Repository proporcionando una abstracción para el acceso a datos y gestión de entidades del dominio. Utilizan estructuras de datos optimizadas (HashMap) para garantizar operaciones O(1) y mantienen la unicidad e integridad de las entidades del sistema.

## Ubicación en la Arquitectura
- **Capa de Infraestructura**: `Backend/Infraestructura/Repositorios/`
- **Patrón**: Repository Pattern con HashMap optimizado
- **Responsabilidad**: Persistencia en memoria y gestión de entidades únicas

## Estructura de Repositorios

### 1. Interfaz Base de Repositorio
```python
# Backend/Infraestructura/Repositorios/repositorio_base.py

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from Backend.Infraestructura.TDA.hashmap_optimizado import HashMapOptimizado

T = TypeVar('T')

class IRepositorio(Generic[T], ABC):
    """Interfaz base para todos los repositorios"""
    
    @abstractmethod
    def guardar(self, entidad: T) -> bool:
        """Guarda o actualiza una entidad"""
        pass
    
    @abstractmethod
    def obtener(self, id_entidad: str) -> Optional[T]:
        """Obtiene una entidad por su ID"""
        pass
    
    @abstractmethod
    def eliminar(self, id_entidad: str) -> bool:
        """Elimina una entidad por su ID"""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[T]:
        """Lista todas las entidades"""
        pass
    
    @abstractmethod
    def existe(self, id_entidad: str) -> bool:
        """Verifica si existe una entidad con el ID dado"""
        pass
    
    @abstractmethod
    def contar(self) -> int:
        """Cuenta el total de entidades"""
        pass

class RepositorioBase(IRepositorio[T], Generic[T]):
    """Implementación base del repositorio usando HashMap"""
    
    def __init__(self, capacidad_inicial: int = 16):
        self._hashmap: HashMapOptimizado = HashMapOptimizado(capacidad_inicial)
        self._entidades_creadas: int = 0
        self._entidades_eliminadas: int = 0
    
    def guardar(self, entidad: T) -> bool:
        """Guarda entidad garantizando unicidad"""
        id_entidad = self._extraer_id(entidad)
        
        if not id_entidad:
            raise ValueError("Entidad debe tener un ID válido")
        
        existe_previamente = self._hashmap.obtener(id_entidad) is not None
        resultado = self._hashmap.insertar(id_entidad, entidad)
        
        if resultado and not existe_previamente:
            self._entidades_creadas += 1
        
        return resultado
    
    def obtener(self, id_entidad: str) -> Optional[T]:
        """Obtiene entidad por ID con acceso O(1)"""
        return self._hashmap.obtener(id_entidad)
    
    def eliminar(self, id_entidad: str) -> bool:
        """Elimina entidad manteniendo integridad"""
        if self._hashmap.eliminar(id_entidad):
            self._entidades_eliminadas += 1
            return True
        return False
    
    def existe(self, id_entidad: str) -> bool:
        """Verifica existencia de entidad"""
        return self._hashmap.obtener(id_entidad) is not None
    
    def contar(self) -> int:
        """Cuenta entidades activas"""
        return self._hashmap.tamaño
    
    def listar_todos(self) -> List[T]:
        """Lista todas las entidades almacenadas"""
        entidades = []
        for bucket in self._hashmap.buckets:
            entrada = bucket
            while entrada:
                entidades.append(entrada.valor)
                entrada = entrada.siguiente
        return entidades
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas del repositorio"""
        stats_hashmap = self._hashmap.obtener_estadisticas()
        return {
            **stats_hashmap,
            'entidades_creadas': self._entidades_creadas,
            'entidades_eliminadas': self._entidades_eliminadas,
            'entidades_activas': self.contar()
        }
    
    @abstractmethod
    def _extraer_id(self, entidad: T) -> str:
        """Extrae el ID de la entidad - debe implementar cada repositorio específico"""
        pass
```

## 2. Repositorios Especializados

### Repositorio de Clientes
```python
# Backend/Infraestructura/Repositorios/repositorio_clientes.py

from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.Infraestructura.Repositorios.repositorio_base import RepositorioBase
from typing import List, Optional

class RepositorioClientes(RepositorioBase[Cliente]):
    """Repositorio especializado para gestión de clientes"""
    
    def __init__(self):
        super().__init__(capacidad_inicial=32)  # Más capacidad para clientes
        self._indice_email: Dict[str, str] = {}  # email -> id_cliente
    
    def _extraer_id(self, entidad: Cliente) -> str:
        """Extrae ID del cliente"""
        return entidad.id_cliente
    
    def guardar(self, cliente: Cliente) -> bool:
        """Guarda cliente con validación de email único"""
        # Verificar unicidad de email
        if self._email_existe(cliente.email, cliente.id_cliente):
            raise ValueError(f"Email {cliente.email} ya está registrado")
        
        # Guardar en repositorio base
        resultado = super().guardar(cliente)
        
        if resultado:
            # Actualizar índice de emails
            self._indice_email[cliente.email] = cliente.id_cliente
        
        return resultado
    
    def obtener_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        id_cliente = self._indice_email.get(email)
        if id_cliente:
            return self.obtener(id_cliente)
        return None
    
    def listar_activos(self) -> List[Cliente]:
        """Lista solo clientes activos"""
        return [cliente for cliente in self.listar_todos() if cliente.activo]
    
    def listar_con_pedidos_pendientes(self) -> List[Cliente]:
        """Lista clientes que tienen pedidos pendientes"""
        return [
            cliente for cliente in self.listar_todos() 
            if cliente.tiene_pedidos_pendientes()
        ]
    
    def buscar_por_patron_nombre(self, patron: str) -> List[Cliente]:
        """Busca clientes por patrón en el nombre"""
        patron_lower = patron.lower()
        return [
            cliente for cliente in self.listar_todos()
            if patron_lower in cliente.nombre.lower()
        ]
    
    def obtener_estadisticas_clientes(self) -> Dict[str, Any]:
        """Estadísticas específicas de clientes"""
        todos_clientes = self.listar_todos()
        activos = self.listar_activos()
        con_pedidos = self.listar_con_pedidos_pendientes()
        
        return {
            **self.obtener_estadisticas(),
            'clientes_activos': len(activos),
            'clientes_inactivos': len(todos_clientes) - len(activos),
            'clientes_con_pedidos_pendientes': len(con_pedidos),
            'tasa_actividad': len(activos) / max(len(todos_clientes), 1)
        }
    
    def _email_existe(self, email: str, excluir_id: str = None) -> bool:
        """Verifica si un email ya está registrado"""
        id_existente = self._indice_email.get(email)
        return id_existente is not None and id_existente != excluir_id
```

### Repositorio de Pedidos
```python
# Backend/Infraestructura/Repositorios/repositorio_pedidos.py

from Backend.Dominio.Dominio_Pedido import Pedido, EstadoPedido, PrioridadPedido
from Backend.Infraestructura.Repositorios.repositorio_base import RepositorioBase
from typing import List, Optional, Dict
from datetime import datetime, timedelta

class RepositorioPedidos(RepositorioBase[Pedido]):
    """Repositorio especializado para gestión de pedidos"""
    
    def __init__(self):
        super().__init__(capacidad_inicial=64)  # Mayor capacidad para pedidos
        self._indice_cliente: Dict[str, List[str]] = {}  # cliente_id -> [pedido_ids]
        self._indice_estado: Dict[EstadoPedido, List[str]] = {}  # estado -> [pedido_ids]
        self._indice_almacen: Dict[str, List[str]] = {}  # almacen_id -> [pedido_ids]
    
    def _extraer_id(self, entidad: Pedido) -> str:
        """Extrae ID del pedido"""
        return entidad.id_pedido
    
    def guardar(self, pedido: Pedido) -> bool:
        """Guarda pedido actualizando índices"""
        resultado = super().guardar(pedido)
        
        if resultado:
            self._actualizar_indices(pedido)
        
        return resultado
    
    def obtener_por_cliente(self, id_cliente: str) -> List[Pedido]:
        """Obtiene todos los pedidos de un cliente"""
        ids_pedidos = self._indice_cliente.get(id_cliente, [])
        return [self.obtener(id_pedido) for id_pedido in ids_pedidos if self.existe(id_pedido)]
    
    def obtener_por_estado(self, estado: EstadoPedido) -> List[Pedido]:
        """Obtiene pedidos filtrados por estado"""
        ids_pedidos = self._indice_estado.get(estado, [])
        return [self.obtener(id_pedido) for id_pedido in ids_pedidos if self.existe(id_pedido)]
    
    def obtener_pendientes(self) -> List[Pedido]:
        """Obtiene pedidos pendientes ordenados por prioridad"""
        pedidos_pendientes = self.obtener_por_estado(EstadoPedido.PENDIENTE)
        
        # Ordenar por prioridad (CRITICA > ALTA > MEDIA > BAJA) y fecha
        return sorted(
            pedidos_pendientes,
            key=lambda p: (p.prioridad.value, p.fecha_creacion),
            reverse=True
        )
    
    def obtener_por_almacen_origen(self, id_almacen: str) -> List[Pedido]:
        """Obtiene pedidos por almacén de origen"""
        ids_pedidos = self._indice_almacen.get(id_almacen, [])
        return [self.obtener(id_pedido) for id_pedido in ids_pedidos if self.existe(id_pedido)]
    
    def obtener_pedidos_antiguos(self, dias: int = 7) -> List[Pedido]:
        """Obtiene pedidos antiguos sin completar"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        pedidos_antiguos = []
        
        for pedido in self.listar_todos():
            if (pedido.fecha_creacion < fecha_limite and 
                pedido.estado in [EstadoPedido.PENDIENTE, EstadoPedido.EN_RUTA]):
                pedidos_antiguos.append(pedido)
        
        return pedidos_antiguos
    
    def obtener_estadisticas_pedidos(self) -> Dict[str, Any]:
        """Estadísticas específicas de pedidos"""
        todos_pedidos = self.listar_todos()
        
        # Contar por estado
        conteo_estados = {}
        for estado in EstadoPedido:
            conteo_estados[estado.value] = len(self.obtener_por_estado(estado))
        
        # Contar por prioridad
        conteo_prioridades = {}
        for prioridad in PrioridadPedido:
            conteo_prioridades[prioridad.value] = len([
                p for p in todos_pedidos if p.prioridad == prioridad
            ])
        
        # Métricas de tiempo
        pedidos_completados = self.obtener_por_estado(EstadoPedido.ENTREGADO)
        if pedidos_completados:
            tiempos_entrega = [
                (p.fecha_entrega - p.fecha_creacion).total_seconds() / 3600
                for p in pedidos_completados if p.fecha_entrega
            ]
            tiempo_promedio = sum(tiempos_entrega) / len(tiempos_entrega) if tiempos_entrega else 0
        else:
            tiempo_promedio = 0
        
        return {
            **self.obtener_estadisticas(),
            'conteo_por_estado': conteo_estados,
            'conteo_por_prioridad': conteo_prioridades,
            'tiempo_promedio_entrega_horas': tiempo_promedio,
            'tasa_completados': conteo_estados.get('entregado', 0) / max(len(todos_pedidos), 1),
            'pedidos_antiguos': len(self.obtener_pedidos_antiguos())
        }
    
    def _actualizar_indices(self, pedido: Pedido) -> None:
        """Actualiza índices auxiliares"""
        # Índice por cliente
        cliente_id = pedido.cliente.id_cliente
        if cliente_id not in self._indice_cliente:
            self._indice_cliente[cliente_id] = []
        if pedido.id_pedido not in self._indice_cliente[cliente_id]:
            self._indice_cliente[cliente_id].append(pedido.id_pedido)
        
        # Índice por estado
        if pedido.estado not in self._indice_estado:
            self._indice_estado[pedido.estado] = []
        if pedido.id_pedido not in self._indice_estado[pedido.estado]:
            self._indice_estado[pedido.estado].append(pedido.id_pedido)
        
        # Índice por almacén
        almacen_id = pedido.almacenamiento_origen.id_almacenamiento
        if almacen_id not in self._indice_almacen:
            self._indice_almacen[almacen_id] = []
        if pedido.id_pedido not in self._indice_almacen[almacen_id]:
            self._indice_almacen[almacen_id].append(pedido.id_pedido)
```

### Repositorio de Vértices
```python
# Backend/Infraestructura/Repositorios/repositorio_vertices.py

from Backend.Infraestructura.TDA.vertice import Vertice, TipoVertice
from Backend.Infraestructura.Repositorios.repositorio_base import RepositorioBase
from typing import List, Dict, Any

class RepositorioVertices(RepositorioBase[Vertice]):
    """Repositorio especializado para vértices del grafo"""
    
    def __init__(self):
        super().__init__(capacidad_inicial=64)
        self._indice_tipo: Dict[TipoVertice, List[str]] = {}
    
    def _extraer_id(self, entidad: Vertice) -> str:
        return entidad.id_vertice
    
    def guardar(self, vertice: Vertice) -> bool:
        """Guarda vértice actualizando índice por tipo"""
        resultado = super().guardar(vertice)
        
        if resultado:
            if vertice.tipo not in self._indice_tipo:
                self._indice_tipo[vertice.tipo] = []
            if vertice.id_vertice not in self._indice_tipo[vertice.tipo]:
                self._indice_tipo[vertice.tipo].append(vertice.id_vertice)
        
        return resultado
    
    def listar_por_tipo(self, tipo: TipoVertice) -> List[Vertice]:
        """Lista vértices filtrados por tipo"""
        ids_vertices = self._indice_tipo.get(tipo, [])
        return [self.obtener(id_vertice) for id_vertice in ids_vertices if self.existe(id_vertice)]
    
    def obtener_clientes(self) -> List[Vertice]:
        """Obtiene todos los vértices de tipo cliente"""
        return self.listar_por_tipo(TipoVertice.CLIENTE)
    
    def obtener_almacenes(self) -> List[Vertice]:
        """Obtiene todos los vértices de tipo almacenamiento"""
        return self.listar_por_tipo(TipoVertice.ALMACENAMIENTO)
    
    def obtener_estaciones_recarga(self) -> List[Vertice]:
        """Obtiene todos los vértices de tipo recarga"""
        return self.listar_por_tipo(TipoVertice.RECARGA)
    
    def obtener_distribucion_tipos(self) -> Dict[str, Any]:
        """Obtiene distribución de vértices por tipo"""
        total = self.contar()
        distribucion = {}
        
        for tipo in TipoVertice:
            cantidad = len(self.listar_por_tipo(tipo))
            distribucion[tipo.value] = {
                'cantidad': cantidad,
                'porcentaje': cantidad / max(total, 1) * 100
            }
        
        return distribucion
```

## 3. Gestión de Transacciones y Consistencia

### Gestor de Transacciones
```python
# Backend/Infraestructura/Repositorios/gestor_transacciones.py

class GestorTransacciones:
    """Gestiona operaciones transaccionales entre múltiples repositorios"""
    
    def __init__(self):
        self._operaciones_pendientes: List[Callable] = []
        self._rollback_operations: List[Callable] = []
        self._en_transaccion: bool = False
    
    def iniciar_transaccion(self) -> None:
        """Inicia una nueva transacción"""
        if self._en_transaccion:
            raise RuntimeError("Ya hay una transacción activa")
        
        self._en_transaccion = True
        self._operaciones_pendientes.clear()
        self._rollback_operations.clear()
    
    def agregar_operacion(self, operacion: Callable, rollback: Callable) -> None:
        """Agrega una operación a la transacción"""
        if not self._en_transaccion:
            raise RuntimeError("No hay transacción activa")
        
        self._operaciones_pendientes.append(operacion)
        self._rollback_operations.append(rollback)
    
    def confirmar_transaccion(self) -> bool:
        """Ejecuta todas las operaciones de la transacción"""
        if not self._en_transaccion:
            raise RuntimeError("No hay transacción activa")
        
        try:
            # Ejecutar todas las operaciones
            for operacion in self._operaciones_pendientes:
                operacion()
            
            self._finalizar_transaccion()
            return True
            
        except Exception as e:
            self._revertir_transaccion()
            raise e
    
    def revertir_transaccion(self) -> None:
        """Revierte la transacción actual"""
        if not self._en_transaccion:
            return
        
        self._revertir_transaccion()
    
    def _revertir_transaccion(self) -> None:
        """Ejecuta operaciones de rollback"""
        for rollback_op in reversed(self._rollback_operations):
            try:
                rollback_op()
            except Exception as e:
                # Log error pero continúa con rollback
                print(f"Error en rollback: {e}")
        
        self._finalizar_transaccion()
    
    def _finalizar_transaccion(self) -> None:
        """Limpia estado de transacción"""
        self._en_transaccion = False
        self._operaciones_pendientes.clear()
        self._rollback_operations.clear()

# Ejemplo de uso transaccional
class ServicioTransaccional:
    def __init__(self, repo_clientes, repo_pedidos, gestor_transacciones):
        self._repo_clientes = repo_clientes
        self._repo_pedidos = repo_pedidos
        self._gestor = gestor_transacciones
    
    def crear_cliente_con_pedido(self, datos_cliente: dict, datos_pedido: dict) -> bool:
        """Crea cliente y pedido en una transacción"""
        self._gestor.iniciar_transaccion()
        
        try:
            # Crear cliente
            cliente = Cliente(**datos_cliente)
            self._gestor.agregar_operacion(
                lambda: self._repo_clientes.guardar(cliente),
                lambda: self._repo_clientes.eliminar(cliente.id_cliente)
            )
            
            # Crear pedido
            pedido = Pedido(cliente=cliente, **datos_pedido)
            self._gestor.agregar_operacion(
                lambda: self._repo_pedidos.guardar(pedido),
                lambda: self._repo_pedidos.eliminar(pedido.id_pedido)
            )
            
            return self._gestor.confirmar_transaccion()
            
        except Exception:
            self._gestor.revertir_transaccion()
            return False
```

## 4. Cache y Optimizaciones

### Cache de Consultas Frecuentes
```python
# Backend/Infraestructura/Repositorios/cache_repositorio.py

from typing import Dict, Any, Optional, Callable
import time

class CacheRepositorio:
    """Cache para optimizar consultas frecuentes"""
    
    def __init__(self, ttl_segundos: int = 300):  # 5 minutos TTL
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._ttl: int = ttl_segundos
        self._hits: int = 0
        self._misses: int = 0
    
    def obtener(self, clave: str) -> Optional[Any]:
        """Obtiene valor del cache si está vigente"""
        if clave in self._cache:
            if self._es_vigente(clave):
                self._hits += 1
                return self._cache[clave]
            else:
                self._eliminar_entrada(clave)
        
        self._misses += 1
        return None
    
    def guardar(self, clave: str, valor: Any) -> None:
        """Guarda valor en cache con timestamp"""
        self._cache[clave] = valor
        self._timestamps[clave] = time.time()
    
    def invalidar(self, patron: str = None) -> None:
        """Invalida entradas del cache"""
        if patron is None:
            # Invalidar todo
            self._cache.clear()
            self._timestamps.clear()
        else:
            # Invalidar por patrón
            claves_a_eliminar = [
                clave for clave in self._cache.keys() 
                if patron in clave
            ]
            for clave in claves_a_eliminar:
                self._eliminar_entrada(clave)
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Estadísticas del cache"""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / max(total_requests, 1)
        
        return {
            'entradas_cache': len(self._cache),
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': hit_rate,
            'ttl_segundos': self._ttl
        }
    
    def _es_vigente(self, clave: str) -> bool:
        """Verifica si una entrada está vigente"""
        if clave not in self._timestamps:
            return False
        
        tiempo_actual = time.time()
        tiempo_entrada = self._timestamps[clave]
        return (tiempo_actual - tiempo_entrada) < self._ttl
    
    def _eliminar_entrada(self, clave: str) -> None:
        """Elimina entrada del cache"""
        self._cache.pop(clave, None)
        self._timestamps.pop(clave, None)

# Repositorio con cache integrado
class RepositorioConCache(RepositorioBase[T]):
    """Repositorio base con cache integrado"""
    
    def __init__(self, capacidad_inicial: int = 16, ttl_cache: int = 300):
        super().__init__(capacidad_inicial)
        self._cache = CacheRepositorio(ttl_cache)
    
    def obtener_con_cache(self, id_entidad: str) -> Optional[T]:
        """Obtiene entidad usando cache"""
        # Intentar obtener del cache
        entidad = self._cache.obtener(f"entidad_{id_entidad}")
        if entidad is not None:
            return entidad
        
        # Si no está en cache, obtener del repositorio
        entidad = self.obtener(id_entidad)
        if entidad is not None:
            self._cache.guardar(f"entidad_{id_entidad}", entidad)
        
        return entidad
    
    def guardar(self, entidad: T) -> bool:
        """Guarda entidad e invalida cache"""
        resultado = super().guardar(entidad)
        if resultado:
            id_entidad = self._extraer_id(entidad)
            # Invalidar cache para esta entidad
            self._cache.invalidar(f"entidad_{id_entidad}")
        return resultado
```

## 5. Testing y Validación

### Pruebas de Repositorios
```python
# tests/test_repositorios.py

class TestRepositorioClientes:
    def test_guardar_cliente_unico(self):
        """Verifica que se mantiene unicidad de clientes"""
        repo = RepositorioClientes()
        
        cliente1 = Cliente("CLI001", "Juan", "juan@email.com", "123456789")
        cliente2 = Cliente("CLI001", "Pedro", "pedro@email.com", "987654321")
        
        assert repo.guardar(cliente1) == True
        assert repo.guardar(cliente2) == True  # Actualiza el existente
        assert repo.contar() == 1
        
        # Verificar que se actualizó
        cliente_guardado = repo.obtener("CLI001")
        assert cliente_guardado.nombre == "Pedro"
    
    def test_email_unico(self):
        """Verifica unicidad de emails"""
        repo = RepositorioClientes()
        
        cliente1 = Cliente("CLI001", "Juan", "juan@email.com", "123456789")
        cliente2 = Cliente("CLI002", "Pedro", "juan@email.com", "987654321")
        
        repo.guardar(cliente1)
        
        with pytest.raises(ValueError):
            repo.guardar(cliente2)
    
    def test_busqueda_por_email(self):
        """Verifica búsqueda por email"""
        repo = RepositorioClientes()
        
        cliente = Cliente("CLI001", "Juan", "juan@email.com", "123456789")
        repo.guardar(cliente)
        
        encontrado = repo.obtener_por_email("juan@email.com")
        assert encontrado is not None
        assert encontrado.id_cliente == "CLI001"

class TestRepositorioPedidos:
    def test_indices_se_actualizan(self):
        """Verifica que los índices se actualizan correctamente"""
        repo = RepositorioPedidos()
        
        cliente = Cliente("CLI001", "Juan", "juan@email.com", "123456789")
        almacen = Almacenamiento("ALM001", "Almacén Central", 1000, True)
        
        pedido = Pedido("PED001", cliente, almacen, "Test", 1.0, PrioridadPedido.ALTA)
        repo.guardar(pedido)
        
        # Verificar índices
        pedidos_cliente = repo.obtener_por_cliente("CLI001")
        assert len(pedidos_cliente) == 1
        assert pedidos_cliente[0].id_pedido == "PED001"
        
        pedidos_pendientes = repo.obtener_por_estado(EstadoPedido.PENDIENTE)
        assert len(pedidos_pendientes) == 1
        
        pedidos_almacen = repo.obtener_por_almacen_origen("ALM001")
        assert len(pedidos_almacen) == 1

def test_integracion_repositorios():
    """Prueba integración entre repositorios"""
    repo_clientes = RepositorioClientes()
    repo_pedidos = RepositorioPedidos()
    
    # Crear cliente
    cliente = Cliente("CLI001", "Juan", "juan@email.com", "123456789")
    repo_clientes.guardar(cliente)
    
    # Crear pedido asociado
    almacen = Almacenamiento("ALM001", "Almacén Central", 1000, True)
    pedido = Pedido("PED001", cliente, almacen, "Test", 1.0, PrioridadPedido.ALTA)
    repo_pedidos.guardar(pedido)
    
    # Verificar relaciones
    cliente_guardado = repo_clientes.obtener("CLI001")
    pedidos_cliente = repo_pedidos.obtener_por_cliente("CLI001")
    
    assert cliente_guardado is not None
    assert len(pedidos_cliente) == 1
    assert pedidos_cliente[0].cliente.id_cliente == cliente_guardado.id_cliente
    
    # Verificar que son la misma instancia (unicidad)
    assert pedidos_cliente[0].cliente is cliente_guardado
```

## 6. Métricas y Monitoreo

### Monitor de Repositorios
```python
class MonitorRepositorios:
    """Monitorea rendimiento y salud de repositorios"""
    
    def __init__(self):
        self._repositorios: Dict[str, RepositorioBase] = {}
        self._inicio_monitoreo = time.time()
    
    def registrar_repositorio(self, nombre: str, repositorio: RepositorioBase):
        """Registra repositorio para monitoreo"""
        self._repositorios[nombre] = repositorio
    
    def obtener_reporte_salud(self) -> Dict[str, Any]:
        """Genera reporte de salud de todos los repositorios"""
        reporte = {
            'tiempo_monitoreo': time.time() - self._inicio_monitoreo,
            'repositorios': {}
        }
        
        for nombre, repo in self._repositorios.items():
            stats = repo.obtener_estadisticas()
            reporte['repositorios'][nombre] = {
                'entidades_activas': stats['entidades_activas'],
                'factor_carga': stats['factor_carga'],
                'eficiencia': stats['eficiencia'],
                'operaciones_total': stats['operaciones_total'],
                'estado': self._evaluar_estado_repositorio(stats)
            }
        
        return reporte
    
    def _evaluar_estado_repositorio(self, stats: Dict[str, Any]) -> str:
        """Evalúa el estado de salud de un repositorio"""
        if stats['factor_carga'] > 0.9:
            return 'SOBRECARGADO'
        elif stats['eficiencia'] < 0.8:
            return 'DEGRADADO'
        elif stats['factor_carga'] > 0.7:
            return 'ADVERTENCIA'
        else:
            return 'SALUDABLE'
```

Los repositorios proporcionan una capa de abstracción robusta y eficiente para la gestión de datos, garantizando unicidad, integridad y rendimiento óptimo para todas las operaciones del sistema logístico de drones.

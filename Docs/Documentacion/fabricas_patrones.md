# Fábricas y Patrones de Creación

## Descripción General
El sistema utiliza el patrón Factory para la creación controlada y consistente de entidades de dominio. Cada fábrica maneja la lógica de creación, validación e inicialización de sus respectivas entidades.

## 🏭 Fábricas Implementadas

### 1. FabricaClientes
**Archivo**: `Backend/Dominio/EntFabricas/FabricaClientes.py`

#### Responsabilidades
- Crear instancias de `Cliente` con datos válidos
- Generar IDs únicos secuenciales
- Gestionar el registro en repositorio
- Notificar eventos de creación

#### Implementación
```python
class FabricaClientes:
    def __init__(self):
        self._contador_id = 1
        self._repo = RepositorioClientes()
    
    def crear_cliente(self, nombre=None, direccion=None, telefono=None):
        cliente_id = self._contador_id
        self._contador_id += 1
        
        cliente = Cliente(
            id_cliente=cliente_id,
            nombre=nombre or f"Cliente_{cliente_id}",
            direccion=direccion or f"Direccion_{cliente_id}",
            telefono=telefono or f"Tel_{cliente_id}"
        )
        
        self._repo.agregar(cliente)
        self.notificar_observadores('cliente_creado', cliente)
        return cliente
```

#### Patrones de Generación
- **Nombres**: `Cliente_1`, `Cliente_2`, etc.
- **Direcciones**: `Direccion_1`, `Direccion_2`, etc.
- **Teléfonos**: `Tel_1`, `Tel_2`, etc.

### 2. FabricaAlmacenamientos
**Archivo**: `Backend/Dominio/EntFabricas/FabricaAlmacenamientos.py`

#### Características Especiales
- Gestión de capacidad de almacenamiento
- Asignación de ubicación estratégica
- Control de inventario inicial

```python
def crear_almacenamiento(self, nombre=None, ubicacion=None, capacidad=100):
    almacenamiento = Almacenamiento(
        id_almacenamiento=self._contador_id,
        nombre=nombre or f"Almacen_{self._contador_id}",
        ubicacion=ubicacion or f"Ubicacion_{self._contador_id}",
        capacidad=capacidad
    )
    
    # Configuración inicial
    almacenamiento.stock_actual = capacidad
    almacenamiento.estado = "operativo"
    
    return almacenamiento
```

### 3. FabricaRecargas
**Archivo**: `Backend/Dominio/EntFabricas/FabricaRecargas.py`

#### Funcionalidades
- Creación de estaciones de recarga
- Configuración de potencia de carga
- Disponibilidad 24/7

```python
def crear_recarga(self, ubicacion=None, potencia=50):
    recarga = Recarga(
        id_recarga=self._contador_id,
        ubicacion=ubicacion or f"Recarga_{self._contador_id}",
        potencia=potencia,
        estado="disponible"
    )
    
    # Configuración de servicios
    recarga.tiempo_recarga_completa = 30  # minutos
    recarga.tipo_energia = "electrica"
    
    return recarga
```

### 4. FabricaVertices
**Archivo**: `Backend/Dominio/EntFabricas/FabricaVertices.py`

#### Proceso de Creación
1. **Asociación con Entidad**: Vincula vértice con Cliente/Almacenamiento/Recarga
2. **Configuración de Tipo**: Establece el tipo según la entidad asociada
3. **Registro en Grafo**: Añade el vértice al grafo principal

```python
def crear_vertice(self, elemento, tipo_elemento):
    vertice = Vertice(elemento)
    vertice.id_vertice = self._contador_id
    vertice.tipo = tipo_elemento
    
    # Configuraciones específicas por tipo
    if tipo_elemento == "cliente":
        vertice.prioridad = elemento.obtener_prioridad()
    elif tipo_elemento == "almacenamiento":
        vertice.capacidad = elemento.capacidad
    elif tipo_elemento == "recarga":
        vertice.potencia = elemento.potencia
    
    self._grafo.agregar_vertice(vertice)
    return vertice
```

### 5. FabricaAristas
**Archivo**: `Backend/Dominio/EntFabricas/FabricaAristas.py`

#### Algoritmo de Generación
```python
def crear_arista(self, origen, destino, peso=None):
    # Generar peso aleatorio si no se especifica
    if peso is None:
        # Peso entre 1 y autonomía máxima (50)
        peso = random.randint(1, 50)
    
    # Validaciones
    if peso > AUTONOMIA_MAXIMA:
        raise ValueError(f"Peso {peso} excede autonomía máxima")
    
    arista = Arista(origen, destino, peso)
    arista.id_arista = f"{origen.id_vertice}-{destino.id_vertice}"
    
    # Configuraciones adicionales
    arista.tipo_ruta = self._determinar_tipo_ruta(origen, destino)
    arista.tiempo_estimado = peso * 2  # 2 minutos por unidad de peso
    
    return arista
```

#### Tipos de Rutas
- **Almacén -> Cliente**: Rutas de entrega
- **Cliente -> Recarga**: Rutas de emergencia energética
- **Recarga -> Almacén**: Rutas de retorno
- **Almacén -> Recarga**: Rutas de mantenimiento

### 6. FabricaPedidos
**Archivo**: `Backend/Dominio/EntFabricas/FabricaPedidos.py`

#### Proceso Complejo de Creación
```python
def crear_pedido(self, cliente=None, almacenamiento=None):
    # Selección automática si no se especifica
    if cliente is None:
        cliente = self._seleccionar_cliente_aleatorio()
    if almacenamiento is None:
        almacenamiento = self._seleccionar_almacenamiento_optimo(cliente)
    
    pedido = Pedido(
        id_pedido=self._contador_id,
        cliente=cliente,
        origen=almacenamiento,
        destino=cliente
    )
    
    # Configuración de prioridad
    pedido.prioridad = self._calcular_prioridad(cliente, almacenamiento)
    pedido.fecha_creacion = datetime.now()
    pedido.status = "pendiente"
    
    # Asignación bidireccional
    cliente.agregar_pedido(pedido)
    almacenamiento.agregar_pedido(pedido)
    
    return pedido
```

#### Estrategias de Asignación
- **Cliente Aleatorio**: Distribución uniforme
- **Almacén Óptimo**: Basado en distancia y capacidad
- **Prioridad Dinámica**: Considerando urgencia y cliente VIP

### 7. FabricaRutas
**Archivo**: `Backend/Dominio/EntFabricas/FabricaRutas.py`

#### Cálculo Multi-Algoritmo
```python
class FabricaRutas:
    def __init__(self):
        self.estrategias = {
            'bfs': RutaEstrategiaBFS(),
            'dfs': RutaEstrategiaDFS(),
            'dijkstra': RutaEstrategiaDijkstra(),
            'floydwarshall': RutaEstrategiaFloydWarshall(),
            'topologicalsort': RutaEstrategiaTopologicalSort(),
            'kruskal': RutaEstrategiaKruskal()
        }
    
    def calcular_ruta(self, pedido, grafo, algoritmo):
        estrategia = self.estrategias[algoritmo]
        
        origen = pedido.obtener_origen()
        destino = pedido.obtener_destino()
        
        # Cálculo de ruta con manejo de excepciones
        try:
            camino, peso_total = estrategia.calcular_ruta(
                origen, destino, grafo, 
                autonomia=50, 
                estaciones_recarga=self._obtener_estaciones_recarga(grafo)
            )
            
            # Crear objeto Ruta
            ruta = Ruta(
                id_ruta=f"{origen.id_vertice}-{destino.id_vertice}-{algoritmo}",
                origen=origen,
                destino=destino,
                camino=camino,
                peso_total=peso_total,
                algoritmo=algoritmo,
                requiere_recarga=self._verifica_recarga_necesaria(camino),
                tiempo_calculo=time.time() - inicio
            )
            
            return ruta
            
        except Exception as e:
            self.logger.error(f"Error calculando ruta: {e}")
            return None
```

## 🔄 Patrón Observer en Fábricas

### Eventos Notificados
```python
# Eventos típicos de las fábricas
eventos = [
    'cliente_creado',
    'almacenamiento_creado', 
    'recarga_creada',
    'vertice_agregado',
    'arista_creada',
    'pedido_generado',
    'ruta_calculada',
    'error_creacion'
]
```

### Implementación de Notificaciones
```python
def notificar_observadores(self, evento, datos):
    for observador in self._observadores:
        try:
            observador.notificar(evento, datos)
        except Exception as e:
            self.logger.error(f"Error notificando observador: {e}")
```

## 🎲 Generación Aleatoria Controlada

### Algoritmos de Distribución
```python
def generar_distribucion_vertices(n_vertices):
    """
    Distribución según requisitos:
    - Almacenamientos: 20%
    - Recargas: 20% 
    - Clientes: 60%
    """
    n_almacenamientos = max(1, n_vertices // 5)
    n_recargas = max(1, n_vertices // 5)
    n_clientes = n_vertices - n_almacenamientos - n_recargas
    
    return n_clientes, n_almacenamientos, n_recargas
```

### Generación de Grafos Conectados
```python
def garantizar_conectividad(vertices, aristas_objetivo):
    """
    Algoritmo para garantizar grafo conectado:
    1. Crear árbol de expansión (n-1 aristas)
    2. Agregar aristas adicionales aleatoriamente
    3. Verificar conectividad final
    """
    # Paso 1: Árbol de expansión mínima
    aristas_arbol = self._crear_arbol_expansion(vertices)
    
    # Paso 2: Aristas adicionales
    aristas_adicionales = self._generar_aristas_adicionales(
        vertices, aristas_objetivo - len(aristas_arbol)
    )
    
    # Paso 3: Validación
    if not self._es_conectado(vertices, aristas_arbol + aristas_adicionales):
        raise Exception("Fallo en generación de grafo conectado")
    
    return aristas_arbol + aristas_adicionales
```

## 🧪 Testing y Validación

### Tests Unitarios por Fábrica
```python
class TestFabricaClientes:
    def test_crear_cliente_con_datos_default(self):
        fabrica = FabricaClientes()
        cliente = fabrica.crear_cliente()
        
        assert cliente.id_cliente == 1
        assert cliente.nombre == "Cliente_1"
        assert cliente.direccion == "Direccion_1"
    
    def test_unicidad_ids(self):
        fabrica = FabricaClientes()
        cliente1 = fabrica.crear_cliente()
        cliente2 = fabrica.crear_cliente()
        
        assert cliente1.id_cliente != cliente2.id_cliente
```

### Validaciones de Integridad
1. **IDs Únicos**: Cada entidad tiene ID único en su tipo
2. **Referencias Válidas**: Todas las referencias entre entidades existen
3. **Constraints de Dominio**: Validaciones de negocio específicas
4. **Conectividad**: Grafos siempre conectados

## 📊 Métricas de Fábricas

### Estadísticas de Creación
```python
estadisticas_fabrica = {
    'entidades_creadas': {
        'clientes': 60,
        'almacenamientos': 12,  
        'recargas': 12,
        'pedidos': 50,
        'rutas': 145
    },
    'tiempo_promedio_creacion': {
        'cliente': 0.001,  # segundos
        'ruta_bfs': 0.045,
        'ruta_dijkstra': 0.089
    },
    'errores': {
        'rutas_no_encontradas': 3,
        'validaciones_fallidas': 1
    }
}
```

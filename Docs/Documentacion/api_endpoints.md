# Documentación de API y Endpoints

## Descripción General
La API del sistema proporciona una interfaz RESTful completa para gestionar todas las operaciones del sistema logístico de drones. Está diseñada siguiendo principios REST, con endpoints organizados por entidades y funcionalidades, incluyendo DTOs específicos y mapeadores para la transformación de datos.

## Ubicación en la Arquitectura
- **Capa de API**: `Backend/API/`
- **Patrón**: API REST con arquitectura de capas
- **Responsabilidad**: Interfaz externa del sistema y gestión de comunicación HTTP

## Estructura de la API

### Organización de Endpoints
```
Backend/API/
├── main.py                           # Aplicación principal FastAPI
├── almacenamientos_enrutador.py      # Endpoints de almacenes
├── clientes_enrutador.py            # Endpoints de clientes
├── pedidos_enrutador.py             # Endpoints de pedidos
├── rutas_enrutador.py               # Endpoints de rutas
├── vertices_enrutador.py            # Endpoints de vértices
├── aristas_enrutador.py             # Endpoints de aristas
├── recargas_enrutador.py            # Endpoints de estaciones de recarga
├── estadisticas_enrutador.py        # Endpoints de estadísticas
├── simulacion_endpoints_enrutador.py # Endpoints de simulación
├── DTOs/                            # Objetos de transferencia de datos
└── Mapeadores/                      # Conversores entre dominio y DTOs
```

## 1. Endpoints de Simulación

### Base URL: `/api/simulacion`

#### Inicializar Simulación
```http
POST /api/simulacion/inicializar
Content-Type: application/json

{
    "num_vertices": 15,
    "num_aristas": 20,
    "num_pedidos": 10,
    "porcentaje_clientes": 0.6,
    "porcentaje_almacenes": 0.2,
    "porcentaje_recargas": 0.2
}
```

**Respuesta Exitosa (200):**
```json
{
    "exito": true,
    "mensaje": "Simulación inicializada correctamente",
    "datos": {
        "simulacion_id": "SIM_20241201_001",
        "vertices_creados": 15,
        "aristas_creadas": 20,
        "pedidos_generados": 10,
        "conectividad_verificada": true,
        "distribución_vertices": {
            "clientes": 9,
            "almacenes": 3,
            "recargas": 3
        }
    },
    "timestamp": "2024-12-01T10:30:00Z"
}
```

#### Obtener Estado de Simulación
```http
GET /api/simulacion/estado
```

**Respuesta Exitosa (200):**
```json
{
    "simulacion_activa": true,
    "simulacion_id": "SIM_20241201_001",
    "tiempo_transcurrido": "00:15:30",
    "metricas_generales": {
        "total_vertices": 15,
        "total_aristas": 20,
        "total_pedidos": 10,
        "pedidos_completados": 7,
        "pedidos_en_proceso": 2,
        "pedidos_pendientes": 1
    },
    "estado_red": {
        "conectividad": "completa",
        "componentes_conexas": 1,
        "densidad": 0.35
    }
}
```

#### Reiniciar Simulación
```http
POST /api/simulacion/reiniciar
```

## 2. Endpoints de Pedidos

### Base URL: `/api/pedidos`

#### Crear Pedido
```http
POST /api/pedidos
Content-Type: application/json

{
    "cliente_id": "CLI001",
    "almacenamiento_origen_id": "ALM001",
    "descripcion": "Documentos urgentes",
    "peso": 0.5,
    "prioridad": "ALTA"
}
```

**Respuesta Exitosa (201):**
```json
{
    "exito": true,
    "pedido": {
        "id_pedido": "PED001",
        "cliente": {
            "id_cliente": "CLI001",
            "nombre": "Juan Pérez",
            "email": "juan.perez@email.com"
        },
        "almacenamiento_origen": {
            "id_almacenamiento": "ALM001",
            "nombre": "Almacén Central"
        },
        "descripcion": "Documentos urgentes",
        "peso": 0.5,
        "prioridad": "ALTA",
        "estado": "PENDIENTE",
        "fecha_creacion": "2024-12-01T10:35:00Z",
        "costo_estimado": null,
        "ruta_asignada": null
    }
}
```

#### Listar Pedidos con Filtros
```http
GET /api/pedidos?estado=PENDIENTE&cliente_id=CLI001&limite=10&pagina=1
```

**Respuesta Exitosa (200):**
```json
{
    "pedidos": [
        {
            "id_pedido": "PED001",
            "cliente_id": "CLI001",
            "cliente_nombre": "Juan Pérez",
            "estado": "PENDIENTE",
            "prioridad": "ALTA",
            "fecha_creacion": "2024-12-01T10:35:00Z",
            "descripcion": "Documentos urgentes",
            "peso": 0.5
        }
    ],
    "metadatos": {
        "total_elementos": 1,
        "pagina_actual": 1,
        "elementos_por_pagina": 10,
        "total_paginas": 1
    }
}
```

#### Obtener Pedido Específico
```http
GET /api/pedidos/PED001
```

#### Cancelar Pedido
```http
PATCH /api/pedidos/PED001/cancelar
Content-Type: application/json

{
    "motivo": "Cancelado por el cliente"
}
```

## 3. Endpoints de Rutas

### Base URL: `/api/rutas`

#### Calcular Ruta para Pedido
```http
POST /api/rutas/calcular-para-pedido
Content-Type: application/json

{
    "pedido_id": "PED001",
    "algoritmo": "BFS",
    "autonomia_maxima": 50.0
}
```

**Respuesta Exitosa (200):**
```json
{
    "exito": true,
    "ruta_calculada": {
        "id_ruta": "RUT001",
        "pedido_id": "PED001",
        "secuencia_vertices": ["ALM001", "REC001", "CLI001"],
        "aristas_utilizadas": [
            {
                "origen": "ALM001",
                "destino": "REC001",
                "peso": 25.0
            },
            {
                "origen": "REC001",
                "destino": "CLI001",
                "peso": 20.0
            }
        ],
        "costo_total": 45.0,
        "requiere_recarga": true,
        "estaciones_recarga": ["REC001"],
        "tiempo_estimado": "00:12:30",
        "distancia_total": 45.0,
        "energia_final": 5.0
    },
    "estado_pedido_actualizado": "EN_RUTA"
}
```

#### Calcular Ruta Directa
```http
POST /api/rutas/calcular-directa
Content-Type: application/json

{
    "origen_id": "ALM001",
    "destino_id": "CLI001",
    "algoritmo": "BFS",
    "autonomia_maxima": 50.0
}
```

#### Obtener Rutas Más Frecuentes
```http
GET /api/rutas/frecuentes?limite=10
```

**Respuesta Exitosa (200):**
```json
{
    "rutas_frecuentes": [
        {
            "secuencia": "ALM001 -> CLI002",
            "frecuencia_uso": 15,
            "costo_promedio": 22.5,
            "tiempo_promedio": "00:08:45",
            "eficiencia": 0.95
        },
        {
            "secuencia": "ALM002 -> REC001 -> CLI005",
            "frecuencia_uso": 12,
            "costo_promedio": 41.0,
            "tiempo_promedio": "00:14:20",
            "eficiencia": 0.87
        }
    ],
    "estadisticas_generales": {
        "total_rutas_unicas": 45,
        "ruta_mas_utilizada": "ALM001 -> CLI002",
        "eficiencia_promedio": 0.91
    }
}
```

## 4. Endpoints de Clientes

### Base URL: `/api/clientes`

#### Crear Cliente
```http
POST /api/clientes
Content-Type: application/json

{
    "nombre": "María González",
    "email": "maria.gonzalez@email.com",
    "telefono": "+56987654321"
}
```

#### Listar Clientes
```http
GET /api/clientes?activo=true&limite=20&pagina=1
```

#### Obtener Cliente con Pedidos
```http
GET /api/clientes/CLI001/detalle
```

**Respuesta Exitosa (200):**
```json
{
    "cliente": {
        "id_cliente": "CLI001",
        "nombre": "Juan Pérez",
        "email": "juan.perez@email.com",
        "telefono": "+56912345678",
        "activo": true,
        "fecha_registro": "2024-11-15T09:00:00Z"
    },
    "estadisticas_pedidos": {
        "total_pedidos": 5,
        "pedidos_pendientes": 1,
        "pedidos_completados": 4,
        "total_gastado": 25000.50,
        "pedido_mas_reciente": "2024-12-01T10:35:00Z"
    },
    "historial_pedidos": [
        {
            "id_pedido": "PED001",
            "estado": "PENDIENTE",
            "fecha_creacion": "2024-12-01T10:35:00Z",
            "descripcion": "Documentos urgentes"
        }
    ]
}
```

## 5. Endpoints de Estadísticas

### Base URL: `/api/estadisticas`

#### Estadísticas Generales
```http
GET /api/estadisticas/generales
```

**Respuesta Exitosa (200):**
```json
{
    "resumen_general": {
        "total_entregas": 150,
        "entregas_exitosas": 142,
        "tasa_exito": 0.947,
        "tiempo_promedio_entrega": "00:11:23",
        "costo_promedio": 1850.75
    },
    "metricas_red": {
        "vertices_mas_visitados": [
            {"id": "CLI001", "tipo": "cliente", "visitas": 15},
            {"id": "ALM001", "tipo": "almacenamiento", "visitas": 45},
            {"id": "REC001", "tipo": "recarga", "visitas": 8}
        ],
        "aristas_mas_utilizadas": [
            {"origen": "ALM001", "destino": "CLI002", "usos": 25},
            {"origen": "ALM002", "destino": "REC001", "usos": 18}
        ]
    },
    "rendimiento_algoritmos": {
        "bfs": {
            "tiempo_promedio_calculo": "0.045s",
            "rutas_exitosas": 140,
            "rutas_fallidas": 2
        }
    }
}
```

#### Estadísticas por Período
```http
GET /api/estadisticas/periodo?fecha_inicio=2024-12-01&fecha_fin=2024-12-01
```

#### Métricas de Rendimiento
```http
GET /api/estadisticas/rendimiento
```

## 6. DTOs (Data Transfer Objects)

### Estructura de DTOs de Respuesta

```python
# Backend/API/DTOs/DTOsRespuesta/

class RespuestaBase:
    def __init__(self):
        self.exito: bool = True
        self.mensaje: str = ""
        self.timestamp: str = datetime.now().isoformat()

class RespuestaRuta(RespuestaBase):
    def __init__(self):
        super().__init__()
        self.id_ruta: str = ""
        self.secuencia_vertices: List[str] = []
        self.aristas_utilizadas: List[dict] = []
        self.costo_total: float = 0.0
        self.requiere_recarga: bool = False
        self.estaciones_recarga: List[str] = []
        self.tiempo_estimado: str = ""

class RespuestaPedido(RespuestaBase):
    def __init__(self):
        super().__init__()
        self.id_pedido: str = ""
        self.cliente: dict = {}
        self.almacenamiento_origen: dict = {}
        self.estado: str = ""
        self.prioridad: str = ""
        self.descripcion: str = ""
        self.peso: float = 0.0
        self.fecha_creacion: str = ""
        self.ruta_asignada: Optional[dict] = None
```

### DTOs de Petición

```python
# Backend/API/DTOs/DTOsPeticion/

class PeticionCrearPedido:
    def __init__(self):
        self.cliente_id: str = ""
        self.almacenamiento_origen_id: str = ""
        self.descripcion: str = ""
        self.peso: float = 0.0
        self.prioridad: str = "MEDIA"

class PeticionCalcularRuta:
    def __init__(self):
        self.origen_id: str = ""
        self.destino_id: str = ""
        self.algoritmo: str = "BFS"
        self.autonomia_maxima: float = 50.0

class PeticionInicializarSimulacion:
    def __init__(self):
        self.num_vertices: int = 15
        self.num_aristas: int = 20
        self.num_pedidos: int = 10
        self.porcentaje_clientes: float = 0.6
        self.porcentaje_almacenes: float = 0.2
        self.porcentaje_recargas: float = 0.2
```

## 7. Mapeadores (Mappers)

### Mapeador de Rutas
```python
# Backend/API/Mapeadores/MapeadorRuta.py

class MapeadorRuta:
    @staticmethod
    def dominio_a_dto_respuesta(ruta: Ruta, pedido: Optional[Pedido] = None) -> RespuestaRuta:
        """
        Convierte objeto de dominio Ruta a DTO de respuesta
        """
        respuesta = RespuestaRuta()
        respuesta.id_ruta = ruta.id_ruta
        respuesta.secuencia_vertices = ruta.obtener_secuencia_vertices()
        respuesta.costo_total = ruta.obtener_costo_total()
        respuesta.requiere_recarga = len(ruta.obtener_estaciones_recarga()) > 0
        respuesta.estaciones_recarga = ruta.obtener_estaciones_recarga()
        
        # Mapear aristas utilizadas
        respuesta.aristas_utilizadas = [
            {
                "origen": arista.origen,
                "destino": arista.destino,
                "peso": arista.peso
            }
            for arista in ruta.obtener_aristas()
        ]
        
        # Calcular tiempo estimado
        respuesta.tiempo_estimado = ruta.calcular_tiempo_estimado()
        
        return respuesta
    
    @staticmethod
    def dto_peticion_a_parametros(dto: PeticionCalcularRuta) -> dict:
        """
        Convierte DTO de petición a parámetros para servicio
        """
        return {
            'origen_id': dto.origen_id,
            'destino_id': dto.destino_id,
            'algoritmo': dto.algoritmo,
            'autonomia_maxima': dto.autonomia_maxima
        }
```

### Mapeador de Pedidos
```python
class MapeadorPedido:
    @staticmethod
    def dominio_a_dto_completo(pedido: Pedido) -> RespuestaPedido:
        """
        Convierte Pedido de dominio a DTO completo
        """
        respuesta = RespuestaPedido()
        respuesta.id_pedido = pedido.id_pedido
        respuesta.estado = pedido.estado.value
        respuesta.prioridad = pedido.prioridad.value
        respuesta.descripcion = pedido.descripcion
        respuesta.peso = pedido.peso
        respuesta.fecha_creacion = pedido.fecha_creacion.isoformat()
        
        # Mapear cliente
        respuesta.cliente = {
            "id_cliente": pedido.cliente.id_cliente,
            "nombre": pedido.cliente.nombre,
            "email": pedido.cliente.email
        }
        
        # Mapear almacenamiento origen
        respuesta.almacenamiento_origen = {
            "id_almacenamiento": pedido.almacenamiento_origen.id_almacenamiento,
            "nombre": pedido.almacenamiento_origen.nombre
        }
        
        # Mapear ruta si existe
        if pedido.ruta_asignada:
            respuesta.ruta_asignada = MapeadorRuta.dominio_a_dto_respuesta(
                pedido.ruta_asignada, pedido
            ).__dict__
        
        return respuesta
```

## 8. Manejo de Errores y Validaciones

### Códigos de Error Estándar
```python
class CodigosErrorAPI:
    # Errores de cliente (4xx)
    PETICION_INVALIDA = 400
    NO_AUTORIZADO = 401
    RECURSO_NO_ENCONTRADO = 404
    CONFLICTO = 409
    DATOS_INVALIDOS = 422
    
    # Errores de servidor (5xx)
    ERROR_INTERNO = 500
    SERVICIO_NO_DISPONIBLE = 503

class RespuestaError(RespuestaBase):
    def __init__(self, codigo: int, mensaje: str, detalles: dict = None):
        super().__init__()
        self.exito = False
        self.codigo_error = codigo
        self.mensaje = mensaje
        self.detalles = detalles or {}
```

### Manejadores de Excepciones
```python
@app.exception_handler(PedidoNoEncontradoError)
async def manejar_pedido_no_encontrado(request: Request, exc: PedidoNoEncontradoError):
    return JSONResponse(
        status_code=404,
        content=RespuestaError(
            codigo=404,
            mensaje=f"Pedido {exc.id_pedido} no encontrado",
            detalles={"id_pedido": exc.id_pedido}
        ).__dict__
    )

@app.exception_handler(RutaNoCalculableError)
async def manejar_ruta_no_calculable(request: Request, exc: RutaNoCalculableError):
    return JSONResponse(
        status_code=422,
        content=RespuestaError(
            codigo=422,
            mensaje="No se pudo calcular ruta para los parámetros dados",
            detalles={
                "origen": exc.origen,
                "destino": exc.destino,
                "motivo": exc.motivo
            }
        ).__dict__
    )
```

## 9. Middleware y Configuración

### Middleware de Logging
```python
@app.middleware("http")
async def middleware_logging(request: Request, call_next):
    inicio = time.time()
    
    # Procesar petición
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    tiempo_procesamiento = time.time() - inicio
    
    # Logging estructurado
    logger.info({
        "metodo": request.method,
        "url": str(request.url),
        "codigo_respuesta": response.status_code,
        "tiempo_procesamiento": tiempo_procesamiento,
        "timestamp": datetime.now().isoformat()
    })
    
    return response
```

### Configuración CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
```

## 10. Documentación Automática

### Configuración OpenAPI
```python
app = FastAPI(
    title="API Sistema Logístico Drones",
    description="API REST para gestión de entregas con drones autónomos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Metadata para endpoints
@app.post(
    "/api/pedidos",
    response_model=RespuestaPedido,
    status_code=201,
    summary="Crear nuevo pedido",
    description="Crea un nuevo pedido de entrega asociado a un cliente",
    tags=["Pedidos"]
)
async def crear_pedido(peticion: PeticionCrearPedido):
    ...
```

### Ejemplos de Respuesta
```python
@app.get(
    "/api/rutas/frecuentes",
    responses={
        200: {
            "description": "Lista de rutas más frecuentes",
            "content": {
                "application/json": {
                    "example": {
                        "rutas_frecuentes": [
                            {
                                "secuencia": "ALM001 -> CLI002",
                                "frecuencia_uso": 15,
                                "costo_promedio": 22.5
                            }
                        ]
                    }
                }
            }
        }
    }
)
```

La API proporciona una interfaz completa y bien documentada que permite al frontend y otros clientes interactuar eficientemente con todas las funcionalidades del sistema logístico de drones.

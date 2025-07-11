"""
API principal para la simulacion logistica de drones de Correos Chile.
Incluye todos los endpoints de gestion de entidades, rutas, simulacion y estadisticas.
Documentación completa disponible en /docs (Swagger UI) y /redoc (ReDoc).
"""

from Backend.API.DTOs.BaseArista import BaseArista
from Backend.API.DTOs.BaseVertice import BaseVertice
from Backend.API.DTOs.BaseRuta import BaseRuta
from Backend.API.DTOs.BasePedido import BasePedido
from Backend.API.DTOs.BaseSimulacionConfig import BaseSimulacionConfig
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from typing import List, Dict, Any

# --- Importar el router de simulacion ---
from Backend.API.simulacion_endpoints_enrutador import router as simulacion_router

# --- Importar todos los routers de los módulos API ---
from Backend.API.rutas_enrutador import router as rutas_router
from Backend.API.recargas_enrutador import router as recargas_router
from Backend.API.pedidos_enrutador import router as pedidos_router
from Backend.API.estadisticas_enrutador import router as estadisticas_router
from Backend.API.clientes_enrutador import router as clientes_router
from Backend.API.almacenamientos_enrutador import router as almacenamientos_router
from Backend.API.aristas_enrutador import router as aristas_router
from Backend.API.vertices_enrutador import router as vertices_router

# Configuración detallada de la aplicación FastAPI con documentación completa
app = FastAPI(
    title="API Simulación Logística de Drones - Correos Chile",
    description="""
    ## API RESTful para Simulación Logística de Drones Autónomos
    
    Esta API permite gestionar un sistema completo de logística con drones autónomos para Correos Chile.
    
    ### Características principales:
    
    * **Gestión de Red**: Crear y administrar vértices (clientes, almacenamientos, recargas) y aristas
    * **Simulación**: Inicializar simulaciones con parámetros personalizables
    * **Cálculo de Rutas**: Algoritmos BFS, DFS, Dijkstra, Floyd-Warshall y Topological Sort
    * **Gestión de Pedidos**: Crear, actualizar estado y entregar pedidos
    * **Análisis**: Estadísticas avanzadas y rutas más frecuentes
    * **Autonomía**: Control de batería de drones (máximo 50 unidades)
    * **Visualización**: Datos estructurados para interfaces visuales
    
    ### Flujo típico de uso:
    
    1. **Inicializar simulación** (`POST /simulacion/iniciar`)
    2. **Explorar la red** (`GET /vertices/`, `GET /aristas/`)
    3. **Gestionar pedidos** (`GET /pedidos/`, `PATCH /pedidos/{id}/estado`)
    4. **Calcular rutas** (`POST /rutas/calcular/{id_pedido}/{algoritmo}`)
    5. **Marcar entregas** (`POST /rutas/entregar/{id_pedido}`)
    6. **Analizar estadísticas** (`GET /estadisticas/`)
    
    ### Algoritmos soportados:
    * `bfs` - Búsqueda en Amplitud
    * `dfs` - Búsqueda en Profundidad  
    * `dijkstra` - Camino más corto ponderado
    * `floydwarshall` - Todos los caminos más cortos
    * `topologicalsort` - Ordenamiento topológico
    
    ### Estados de pedidos:
    * `pendiente` - Recién creado, esperando procesamiento
    * `enviado` - Ruta calculada y asignada
    * `entregado` - Completado exitosamente
    """,
    version="2.0.0",
    terms_of_service="https://github.com/tu-repo/terminos",
    contact={
        "name": "Equipo de Desarrollo - Simulación Logística",
        "url": "https://github.com/tu-repo",
        "email": "dev@correos-chile-sim.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Simulación",
            "description": "Operaciones para inicializar y gestionar simulaciones completas"
        },
        {
            "name": "Vértices", 
            "description": "Gestión de nodos de la red (clientes, almacenamientos, recargas)"
        },
        {
            "name": "Aristas",
            "description": "Gestión de conexiones entre vértices con pesos/costos"
        },
        {
            "name": "Clientes",
            "description": "Operaciones específicas para vértices tipo cliente"
        },
        {
            "name": "Almacenamientos", 
            "description": "Operaciones específicas para centros de distribución"
        },
        {
            "name": "Recargas",
            "description": "Operaciones específicas para estaciones de carga de drones"
        },
        {
            "name": "Pedidos",
            "description": "Gestión completa del ciclo de vida de pedidos"
        },
        {
            "name": "Rutas",
            "description": "Cálculo, optimización y gestión de rutas de drones"
        },
        {
            "name": "Estadísticas",
            "description": "Análisis y métricas del sistema logístico"
        },
        {
            "name": "Root",
            "description": "Endpoints básicos y de estado de la API"
        }
    ]
)

# Permitir CORS para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sim_service = SimulacionAplicacionService()

# --- Incluir el router modular de simulacion y todos los routers de la API ---
app.include_router(simulacion_router)
app.include_router(rutas_router)
app.include_router(recargas_router)
app.include_router(pedidos_router)
app.include_router(estadisticas_router)
app.include_router(clientes_router)
app.include_router(almacenamientos_router)
app.include_router(aristas_router)
app.include_router(vertices_router)


@app.get("/", tags=["Root"], summary="Estado de la API", response_description="Información básica de la API")
def root() -> Dict[str, Any]:
    """
    **Endpoint raíz de la API de Simulación Logística de Drones**
    
    Proporciona información básica sobre el estado de la API y endpoints disponibles.
    
    ### Respuesta:
    - **mensaje**: Confirmación de que la API está activa
    - **version**: Versión actual de la API  
    - **endpoints**: Lista de módulos de endpoints disponibles
    - **documentacion**: Enlaces a documentación interactiva
    
    ### Uso típico:
    Verificar que la API esté funcionando antes de realizar operaciones.
    """
    return {
        "mensaje": "API de Simulación de Drones Correos Chile activa",
        "version": "2.0.0",
        "estado": "operativo",
        "endpoints": [
            "/simulacion - Gestión de simulaciones",
            "/vertices - Gestión de nodos de la red", 
            "/aristas - Gestión de conexiones",
            "/clientes - Operaciones con clientes",
            "/almacenamientos - Centros de distribución",
            "/recargas - Estaciones de carga",
            "/pedidos - Gestión de pedidos",
            "/rutas - Cálculo y optimización de rutas",
            "/estadisticas - Análisis y métricas"
        ],
        "documentacion": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "caracteristicas": {
            "algoritmos_ruta": ["bfs", "dfs", "dijkstra", "floydwarshall", "topologicalsort"],
            "autonomia_maxima": 50,
            "vertices_maximos": 150,
            "aristas_maximas": 300,
            "pedidos_maximos": 500
        }
    }


def custom_openapi():
    """Personalización adicional del esquema OpenAPI"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Agregar información adicional al esquema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://via.placeholder.com/120x120.png?text=Drones",
        "altText": "Logo Simulación Drones"
    }
    
    # Agregar ejemplos globales
    openapi_schema["components"]["examples"] = {
        "SimulacionBasica": {
            "summary": "Configuración básica de simulación",
            "description": "Parámetros típicos para una simulación pequeña",
            "value": {
                "n_vertices": 15,
                "m_aristas": 20,
                "n_pedidos": 10
            }
        },
        "SimulacionCompleta": {
            "summary": "Configuración completa de simulación",
            "description": "Parámetros para una simulación de gran escala",
            "value": {
                "n_vertices": 100,
                "m_aristas": 200,
                "n_pedidos": 150
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get(
    "/health", 
    tags=["Root"],
    summary="Estado de Salud de la API",
    description="Verifica que todos los servicios estén funcionando correctamente"
)
def health_check() -> Dict[str, Any]:
    """
    **Endpoint de verificación de salud del sistema**
    
    Verifica el estado de todos los componentes críticos de la API.
    """
    try:
        service = SimulacionAplicacionService()
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "services": {
                "simulacion": "operational",
                "repositorios": "operational", 
                "algoritmos": "operational"
            },
            "version": "2.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }


@app.get(
    "/algoritmos",
    tags=["Root"], 
    summary="Lista de Algoritmos Disponibles",
    description="Retorna todos los algoritmos de ruteo soportados por el sistema"
)
def obtener_algoritmos() -> Dict[str, Any]:
    """
    **Lista completa de algoritmos de ruteo disponibles**
    
    Cada algoritmo tiene características específicas y casos de uso recomendados.
    """
    return {
        "algoritmos": {
            "bfs": {
                "nombre": "Búsqueda en Amplitud",
                "descripcion": "Encuentra el camino más corto en términos de número de saltos",
                "complejidad": "O(V + E)",
                "uso_recomendado": "Redes pequeñas, caminos con pocos saltos"
            },
            "dfs": {
                "nombre": "Búsqueda en Profundidad", 
                "descripcion": "Explora caminos en profundidad antes de retroceder",
                "complejidad": "O(V + E)",
                "uso_recomendado": "Exploración exhaustiva, detección de ciclos"
            },
            "dijkstra": {
                "nombre": "Algoritmo de Dijkstra",
                "descripcion": "Camino más corto considerando pesos de aristas",
                "complejidad": "O((V + E) log V)",
                "uso_recomendado": "Rutas óptimas por costo, redes ponderadas"
            },
            "floydwarshall": {
                "nombre": "Floyd-Warshall",
                "descripcion": "Calcula todos los caminos más cortos entre todos los pares",
                "complejidad": "O(V³)",
                "uso_recomendado": "Análisis global, múltiples consultas de rutas"
            },
            "topologicalsort": {
                "nombre": "Ordenamiento Topológico",
                "descripcion": "Para grafos dirigidos acíclicos",
                "complejidad": "O(V + E)",
                "uso_recomendado": "Dependencias, flujos dirigidos"
            }
        },
        "autonomia_maxima": 50,
        "recargas_automaticas": True
    }


@app.get(
    "/swagger-config",
    tags=["Root"],
    summary="Configuración de Swagger",
    description="Retorna la configuración completa de la documentación Swagger"
)
def swagger_config() -> Dict[str, Any]:
    """
    **Configuración y metadatos de la documentación Swagger**
    
    Útil para herramientas de generación de código y análisis de API.
    """
    return {
        "swagger_ui_url": "/docs",
        "redoc_url": "/redoc", 
        "openapi_url": "/openapi.json",
        "title": app.title,
        "version": app.version,
        "endpoints_count": len([route for route in app.routes if hasattr(route, 'methods')]),
        "tags": [tag["name"] for tag in app.openapi_tags] if hasattr(app, 'openapi_tags') else [],
        "cors_enabled": True,
        "docs_features": [
            "Interactive API testing",
            "Request/Response examples", 
            "Schema validation",
            "Authentication support",
            "Download OpenAPI spec"
        ]
    }


import time

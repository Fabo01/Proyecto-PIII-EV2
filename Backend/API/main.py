from Backend.API.DTOs.Dtos2 import NodoBase, PedidoBase, RutaBase, SimulacionConfig, AristaBase
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# --- Importar el router de simulacion ---
from Backend.API.simulacion_endpoints import router as simulacion_router

# --- Importar todos los routers de los módulos API ---
from Backend.API.rutas import router as rutas_router
from Backend.API.recargas import router as recargas_router
from Backend.API.pedidos import router as pedidos_router
from Backend.API.estadisticas import router as estadisticas_router
from Backend.API.clientes import router as clientes_router
from Backend.API.almacenamientos import router as almacenamientos_router

app = FastAPI()

# Permitir CORS para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sim_service = SimulacionAplicacionService()

# --- Incluir el router modular de simulacion ---
app.include_router(simulacion_router)
app.include_router(rutas_router)
app.include_router(recargas_router)
app.include_router(pedidos_router)
app.include_router(estadisticas_router)
app.include_router(clientes_router)
app.include_router(almacenamientos_router)

@app.post("/simulacion/iniciar")
def iniciar_simulacion(config: SimulacionConfig):
    estado = sim_service.iniciar_simulacion(config.n_nodos, config.m_aristas, config.n_pedidos)
    if hasattr(estado, 'model_dump'):
        return estado.model_dump()
    return estado

@app.post("/simulacion/reiniciar")
def reiniciar_simulacion(config: SimulacionConfig):
    estado = sim_service.reiniciar_simulacion(config.n_nodos, config.m_aristas, config.n_pedidos)
    if hasattr(estado, 'model_dump'):
        return estado.model_dump()
    return estado

@app.get("/nodos", response_model=List[NodoBase])
def obtener_nodos():
    nodos = sim_service.obtener_nodos()
    # Serializar todos los nodos a DTOs robustos
    from Backend.API.DTOs.Dtos1 import NodoResponse, ClienteResponse, AlmacenamientoResponse, RecargaResponse
    nodos_serializados = []
    for n in nodos:
        el = n.elemento() if hasattr(n, 'elemento') else n
        tipo = getattr(el, 'tipo_elemento', None)
        if tipo == 'cliente':
            nodos_serializados.append(ClienteResponse.from_model(el))
        elif tipo == 'almacenamiento':
            nodos_serializados.append(AlmacenamientoResponse.from_model(el))
        elif tipo == 'recarga':
            nodos_serializados.append(RecargaResponse.from_model(el))
        else:
            nodos_serializados.append(NodoResponse.from_model(el))
    return [n.model_dump() if hasattr(n, 'model_dump') else dict(n) for n in nodos_serializados]

# --- Serializador de aristas para exponer solo IDs y peso ---
def serializar_arista(arista):
    # El origen y destino pueden ser vértices, extraer el id del elemento asociado
    def extraer_id(vertice):
        el = vertice.elemento() if hasattr(vertice, 'elemento') else vertice
        # Buscar el atributo de id más común
        for attr in ['id', 'id_cliente', 'id_almacenamiento', 'id_recarga']:
            if hasattr(el, attr):
                return getattr(el, attr)
        # Si no tiene id, usar hash
        return hash(el)
    return {
        'origen': extraer_id(arista.origen),
        'destino': extraer_id(arista.destino),
        'peso': arista.peso
    }

@app.get("/aristas", response_model=List[AristaBase])
def obtener_aristas():
    try:
        aristas = sim_service.obtener_aristas()
        if aristas is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        if not aristas:
            return []
        return [serializar_arista(a) for a in aristas]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener aristas: {e}")

@app.get("/clientes", response_model=List[NodoBase])
def listar_clientes():
    try:
        clientes = sim_service.listar_clientes()
        if clientes is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        if not clientes:
            return []
        from Backend.API.DTOs.Dtos1 import ClienteResponse
        return [ClienteResponse.from_model(c).model_dump() for c in clientes]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener clientes: {e}")

@app.get("/almacenamientos", response_model=List[NodoBase])
def listar_almacenamientos():
    try:
        almacenamientos = sim_service.listar_almacenamientos()
        if almacenamientos is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        if not almacenamientos:
            return []
        from Backend.API.DTOs.Dtos1 import AlmacenamientoResponse
        return [AlmacenamientoResponse.from_model(a).model_dump() for a in almacenamientos]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener almacenamientos: {e}")

@app.get("/recargas", response_model=List[NodoBase])
def listar_recargas():
    try:
        recargas = sim_service.listar_recargas()
        if recargas is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        if not recargas:
            return []
        from Backend.API.DTOs.Dtos1 import RecargaResponse
        return [RecargaResponse.from_model(r).model_dump() for r in recargas]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener recargas: {e}")

@app.get("/pedidos", response_model=List[PedidoBase])
def listar_pedidos():
    try:
        pedidos = sim_service.listar_pedidos()
        if pedidos is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        if not pedidos:
            return []
        from Backend.API.DTOs.Dtos1 import PedidoResponse
        return [PedidoResponse.from_model(p).model_dump() for p in pedidos]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener pedidos: {e}")

@app.get("/rutas", response_model=List[RutaBase])
def listar_rutas():
    try:
        rutas = sim_service.listar_rutas()
        if rutas is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        if not rutas:
            return []
        from Backend.API.DTOs.Dtos1 import RutaResponse
        return [RutaResponse.from_model(r).model_dump() for r in rutas]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener rutas: {e}")

@app.get("/estadisticas")
def obtener_estadisticas():
    estadisticas = sim_service.obtener_estadisticas()
    if hasattr(estadisticas, 'model_dump'):
        return estadisticas.model_dump()
    return estadisticas

@app.post("/pedidos/{id_pedido}/calcular_ruta", response_model=RutaBase)
def calcular_ruta_pedido(id_pedido: int, algoritmo: str):
    ruta = sim_service.calcular_ruta_pedido(id_pedido, algoritmo)
    if hasattr(ruta, 'model_dump'):
        return ruta.model_dump()
    return ruta

@app.post("/pedidos/{id_pedido}/ruta", response_model=RutaBase)
def obtener_ruta_pedido(id_pedido: int, algoritmo: str = 'dijkstra'):
    ruta = sim_service.calcular_ruta_pedido(id_pedido, algoritmo)
    if hasattr(ruta, 'model_dump'):
        return ruta.model_dump()
    return ruta

@app.post("/pedidos/{id_pedido}/entregar", response_model=PedidoBase)
def entregar_pedido(id_pedido: int):
    pedido = sim_service.entregar_pedido(id_pedido)
    if hasattr(pedido, 'model_dump'):
        return pedido.model_dump()
    return pedido

@app.get("/rutas/mas_frecuentes", response_model=List[RutaBase])
def rutas_mas_frecuentes():
    rutas = sim_service.rutas_mas_frecuentes()
    return [r.model_dump() if hasattr(r, 'model_dump') else r for r in rutas]

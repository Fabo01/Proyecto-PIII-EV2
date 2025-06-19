from pydantic import BaseModel
from typing import List, Optional
import logging
import warnings

class SimulacionInitRequest(BaseModel):
    n_nodos: int
    m_aristas: int
    n_pedidos: int

class NodoResponse(BaseModel):
    id: int
    tipo: str
    nombre: str

    @classmethod
    def from_model(cls, nodo):
        """
        Crea una instancia de NodoResponse a partir de un objeto de dominio.
        """
        el = nodo.elemento() if hasattr(nodo, 'elemento') else nodo
        return cls(
            id=get_id(el),
            tipo=getattr(el, 'tipo_elemento', ''),
            nombre=getattr(el, 'nombre', '')
        )

class ClienteResponse(NodoResponse):
    pedidos: List[int] = []

    @classmethod
    def from_model(cls, cliente):
        """
        Crea una instancia de ClienteResponse a partir de un objeto Cliente de dominio.
        Los pedidos se ordenan por prioridad usando obtener_pedidos().
        """
        pedidos = []
        if hasattr(cliente, 'obtener_pedidos'):
            pedidos = [getattr(p, 'id_pedido', 0) for p in cliente.obtener_pedidos()]
        return cls(
            id=getattr(cliente, 'id_cliente', 0),
            tipo='cliente',
            nombre=getattr(cliente, 'nombre', ''),
            pedidos=pedidos
        )

class AlmacenamientoResponse(NodoResponse):
    pedidos: List[int] = []

    @classmethod
    def from_model(cls, almacen):
        """
        Crea una instancia de AlmacenamientoResponse a partir de un objeto Almacenamiento de dominio.
        """
        pedidos = []
        if hasattr(almacen, 'obtener_pedidos'):
            pedidos = [getattr(p, 'id_pedido', 0) for p in almacen.obtener_pedidos()]
        return cls(
            id=getattr(almacen, 'id_almacenamiento', 0),
            tipo='almacenamiento',
            nombre=getattr(almacen, 'nombre', ''),
            pedidos=pedidos
        )

class RecargaResponse(NodoResponse):
    @classmethod
    def from_model(cls, recarga):
        """
        Crea una instancia de RecargaResponse a partir de un objeto Recarga de dominio.
        """
        return cls(
            id=getattr(recarga, 'id_recarga', 0),
            tipo='recarga',
            nombre=getattr(recarga, 'nombre', '')
        )

class PedidoResponse(BaseModel):
    id_pedido: int
    id_cliente: int
    id_almacenamiento: int
    prioridad: str
    status: str
    ruta: Optional[List[int]] = None
    peso_total: Optional[float] = None
    origen: Optional[int] = None  # ID del almacenamiento origen
    destino: Optional[int] = None  # ID del cliente destino
    fecha_creacion: Optional[str] = None
    fecha_entrega: Optional[str] = None

    @classmethod
    def from_model(cls, pedido):
        logger = logging.getLogger("DTO.PedidoResponse")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"Serializando PedidoResponse para pedido: {getattr(pedido, 'id_pedido', '?')}")
        logger.info(f"  pedido.origen: {getattr(pedido, 'origen', None)}")
        logger.info(f"  pedido.destino: {getattr(pedido, 'destino', None)}")
        logger.info(f"  pedido.fecha_creacion: {getattr(pedido, 'fecha_creacion', None)}")
        logger.info(f"  pedido.fecha_entrega: {getattr(pedido, 'fecha_entrega', None)}")
        logger.info(f"  pedido.prioridad: {getattr(pedido, 'prioridad', None)}")
        logger.info(f"  pedido.status: {getattr(pedido, 'status', None)}")

        def extraer_id_almacenamiento(vertice):
            if hasattr(vertice, 'elemento'):
                el = vertice.elemento()
                if hasattr(el, 'id_almacenamiento'):
                    return el.id_almacenamiento
            if hasattr(vertice, 'id_almacenamiento'):
                return vertice.id_almacenamiento
            if hasattr(vertice, 'id'):
                return vertice.id
            return -1

        def extraer_id_cliente(vertice):
            if hasattr(vertice, 'elemento'):
                el = vertice.elemento()
                if hasattr(el, 'id_cliente'):
                    return el.id_cliente
            if hasattr(vertice, 'id_cliente'):
                return vertice.id_cliente
            if hasattr(vertice, 'id'):
                return vertice.id
            return -1

        id_cliente = extraer_id_cliente(getattr(pedido, 'destino', None))
        id_almacenamiento = extraer_id_almacenamiento(getattr(pedido, 'origen', None))
        if id_cliente in (None, -1) or id_almacenamiento in (None, -1):
            logger.warning(f"Pedido {getattr(pedido, 'id_pedido', '?')} con origen o destino nulo o inválido.")
            warnings.warn(f"Pedido {getattr(pedido, 'id_pedido', '?')} con origen o destino nulo o inválido.")

        # Extraer lista de IDs de la ruta si existe
        ruta_ids = None
        if hasattr(pedido, 'ruta') and pedido.ruta is not None:
            if hasattr(pedido.ruta, 'camino'):
                ruta_ids = [get_id(n) for n in pedido.ruta.camino]
            elif isinstance(pedido.ruta, list):
                ruta_ids = [get_id(n) for n in pedido.ruta]

        # Formatear fechas a ISO 8601 o None
        fecha_creacion_raw = getattr(pedido, 'fecha_creacion', None)
        fecha_creacion_fmt = None
        if fecha_creacion_raw is not None:
            fecha_creacion_fmt = fecha_creacion_raw.isoformat() if hasattr(fecha_creacion_raw, 'isoformat') else str(fecha_creacion_raw)
        fecha_entrega_raw = getattr(pedido, 'fecha_entrega', None)
        fecha_entrega_fmt = None
        if fecha_entrega_raw is not None:
            fecha_entrega_fmt = fecha_entrega_raw.isoformat() if hasattr(fecha_entrega_raw, 'isoformat') else str(fecha_entrega_raw)

        return cls(
            id_pedido=getattr(pedido, 'id_pedido', 0),
            id_cliente=id_cliente,
            id_almacenamiento=id_almacenamiento,
            prioridad=getattr(pedido, 'prioridad', ''),
            status=getattr(pedido, 'status', ''),
            ruta=ruta_ids,
            peso_total=getattr(pedido, 'peso_total', None),
            origen=id_almacenamiento,
            destino=id_cliente,
            fecha_creacion=fecha_creacion_fmt,
            fecha_entrega=fecha_entrega_fmt
        )

def get_id(nodo):
    el = nodo.elemento() if hasattr(nodo, 'elemento') else nodo
    if hasattr(el, 'id_cliente') and isinstance(el.id_cliente, int):
        return el.id_cliente
    if hasattr(el, 'id_almacenamiento') and isinstance(el.id_almacenamiento, int):
        return el.id_almacenamiento
    if hasattr(el, 'id_recarga') and isinstance(el.id_recarga, int):
        return el.id_recarga
    if isinstance(el, int):
        return el
    return 0

class RutaResponse(BaseModel):
    origen: int
    destino: int
    camino: List[int]
    peso_total: float
    algoritmo: str

    @classmethod
    def from_model(cls, ruta):
        """
        Crea una instancia de RutaResponse a partir de un objeto Ruta de dominio.
        """
        camino_ids = [get_id(n) for n in getattr(ruta, 'camino', [])]
        origen_id = get_id(getattr(ruta, 'origen', 0))
        destino_id = get_id(getattr(ruta, 'destino', 0))
        return cls(
            origen=origen_id,
            destino=destino_id,
            camino=camino_ids,
            peso_total=getattr(ruta, 'peso_total', 0.0),
            algoritmo=getattr(ruta, 'algoritmo', '')
        )

class RutaAlgoritmoResponse(BaseModel):
    origen: int
    destino: int
    camino: List[int]
    peso_total: float
    algoritmo: str
    tiempo_respuesta: float

    @classmethod
    def from_resultado(cls, origen, destino, camino, peso_total, algoritmo, tiempo_respuesta):
        return cls(
            origen=origen,
            destino=destino,
            camino=camino,
            peso_total=peso_total,
            algoritmo=algoritmo,
            tiempo_respuesta=tiempo_respuesta
        )

class SimulacionEstadoResponse(BaseModel):
    clientes: List[ClienteResponse]
    almacenamientos: List[AlmacenamientoResponse]
    recargas: List[RecargaResponse]
    pedidos: List[PedidoResponse]
    rutas: List[RutaResponse]
    estado: str
    n_nodos: int = 0
    m_aristas: int = 0
    n_pedidos: int = 0
    ok: bool = True

class EstadisticasResponse(BaseModel):
    total_clientes: int
    total_almacenamientos: int
    total_recargas: int
    total_pedidos: int
    rutas_mas_frecuentes: List[RutaResponse]
    tiempo_respuesta: float = 0.0
    eficiencia: Optional[float] = None

class FloydWarshallResponse(BaseModel):
    distancias: dict  # {(origen, destino): distancia}
    caminos: dict     # {(origen, destino): [camino]}

    @classmethod
    def from_resultados(cls, distancias, caminos):
        # Serializa las claves de tuplas a strings para compatibilidad JSON
        distancias_str = {f"{o}-{d}": v for (o, d), v in distancias.items()}
        caminos_str = {f"{o}-{d}": c for (o, d), c in caminos.items()}
        return cls(distancias=distancias_str, caminos=caminos_str)

# Funciones utilitarias para conversión de modelos de dominio a DTOs

def cliente_a_dto(cliente):
    return ClienteResponse.from_model(cliente)

def almacen_a_dto(almacen):
    return AlmacenamientoResponse.from_model(almacen)

def recarga_a_dto(recarga):
    return RecargaResponse.from_model(recarga)

def pedido_a_dto(pedido):
    return PedidoResponse.from_model(pedido)

def ruta_a_dto(ruta):
    return RutaResponse.from_model(ruta)

def simulacion_estado_a_dto(simulacion, tiempo_respuesta=0.0):
    return SimulacionEstadoResponse(
        clientes=[ClienteResponse.from_model(c) for c in simulacion.listar_clientes()],
        almacenamientos=[AlmacenamientoResponse.from_model(a) for a in simulacion.listar_almacenamientos()],
        recargas=[RecargaResponse.from_model(r) for r in simulacion.listar_recargas()],
        pedidos=[PedidoResponse.from_model(p) for p in simulacion.listar_pedidos()],
        rutas=[RutaResponse.from_model(r) for r in simulacion.rutas],
        estado='iniciada',
        n_nodos=getattr(simulacion, 'n_nodos', 0),
        m_aristas=getattr(simulacion, 'm_aristas', 0),
        n_pedidos=getattr(simulacion, 'n_pedidos', 0),
        ok=True
    )

def estadisticas_a_dto(simulacion, tiempo_respuesta=0.0, eficiencia=None):
    return EstadisticasResponse(
        total_clientes=len(simulacion.listar_clientes()),
        total_almacenamientos=len(simulacion.listar_almacenamientos()),
        total_recargas=len(simulacion.listar_recargas()),
        total_pedidos=len(simulacion.listar_pedidos()),
        rutas_mas_frecuentes=[RutaResponse.from_model(r) for r in simulacion.rutas_mas_frecuentes()],
        tiempo_respuesta=tiempo_respuesta,
        eficiencia=eficiencia
    )

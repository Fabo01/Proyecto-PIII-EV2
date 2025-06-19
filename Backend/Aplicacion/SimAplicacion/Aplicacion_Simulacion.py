from Backend.Aplicacion.SimAplicacion.ISimulacionAplicacionService import ISimulacionAplicacionService
from Backend.Dominio.Simulacion_dominio import Simulacion
from Backend.API.DTOs.Dtos1 import ClienteResponse, AlmacenamientoResponse, RecargaResponse, PedidoResponse, RutaResponse
from Backend.API.DTOs.Dtos2 import *
from Backend.Servicios.SimServicios.Servicios_Simulacion import SimulacionDominioService
from fastapi import HTTPException
import logging

class SimulacionAplicacionService(ISimulacionAplicacionService):
    _dominio_service: SimulacionDominioService = SimulacionDominioService()
    logger = logging.getLogger("SimulacionAplicacionService")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    @classmethod
    def _check_simulacion(cls):
        if Simulacion._instancia is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")

    @classmethod
    def iniciar_simulacion(cls, n_nodos: int, m_aristas: int, n_pedidos: int):
        if n_nodos <= 0 or m_aristas <= 0 or n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para iniciar la simulación")
        Simulacion.reiniciar_instancia(n_nodos, m_aristas, n_pedidos)
        return cls.estado_actual()

    @classmethod
    def reiniciar_simulacion(cls, n_nodos: int, m_aristas: int, n_pedidos: int):
        if n_nodos <= 0 or m_aristas <= 0 or n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para reiniciar la simulación")
        Simulacion.reiniciar_instancia(n_nodos, m_aristas, n_pedidos)
        return cls.estado_actual()

    @classmethod
    def estado_actual(cls):
        if Simulacion._instancia is None:
            return {
                'clientes': [],
                'almacenamientos': [],
                'recargas': [],
                'pedidos': [],
                'rutas': [],
                'estado': 'no_iniciada',
                'n_nodos': 0,
                'm_aristas': 0,
                'n_pedidos': 0,
                'ok': False
            }
        sim = Simulacion.obtener_instancia()
        return {
            'clientes': [ClienteResponse.from_model(c).model_dump() for c in sim.listar_clientes()],
            'almacenamientos': [AlmacenamientoResponse.from_model(a).model_dump() for a in sim.listar_almacenamientos()],
            'recargas': [RecargaResponse.from_model(r).model_dump() for r in sim.listar_recargas()],
            'pedidos': [PedidoResponse.from_model(p).model_dump() for p in sim.listar_pedidos()],
            'rutas': [RutaResponse.from_model(r).model_dump() for r in sim.rutas],
            'estado': 'iniciada',
            'n_nodos': getattr(sim, 'n_nodos', 0),
            'm_aristas': getattr(sim, 'm_aristas', 0),
            'n_pedidos': getattr(sim, 'n_pedidos', 0),
            'ok': True
        }

    @classmethod
    def listar_clientes(cls):
        cls._check_simulacion()
        return [ClienteResponse.from_model(c) for c in Simulacion.obtener_instancia().listar_clientes()]

    @classmethod
    def listar_almacenamientos(cls):
        cls._check_simulacion()
        return [AlmacenamientoResponse.from_model(a) for a in Simulacion.obtener_instancia().listar_almacenamientos()]

    @classmethod
    def listar_recargas(cls):
        cls._check_simulacion()
        return [RecargaResponse.from_model(r) for r in Simulacion.obtener_instancia().listar_recargas()]

    @classmethod
    def listar_pedidos(cls):
        cls._check_simulacion()
        pedidos = [PedidoResponse.from_model(p) for p in Simulacion.obtener_instancia().listar_pedidos()]
        cls.logger.info(f"listar_pedidos: {len(pedidos)} pedidos retornados")
        for p in Simulacion.obtener_instancia().listar_pedidos():
            cls.logger.info(f"  Pedido.origen: {getattr(p, 'origen', None)}, Pedido.destino: {getattr(p, 'destino', None)}, Pedido.fecha_creacion: {getattr(p, 'fecha_creacion', None)}")
        return pedidos

    @classmethod
    def listar_rutas(cls):
        cls._check_simulacion()
        return [RutaResponse.from_model(r) for r in Simulacion.obtener_instancia().rutas]

    @classmethod
    def obtener_cliente(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for c in sim.clientes:
            if getattr(c, 'id_cliente', None) == id:
                return ClienteResponse.from_model(c)
        raise HTTPException(status_code=404, detail=f"Cliente con id {id} no encontrado")

    @classmethod
    def obtener_almacenamiento(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for a in sim.almacenamientos:
            if getattr(a, 'id_almacenamiento', None) == id:
                return AlmacenamientoResponse.from_model(a)
        raise HTTPException(status_code=404, detail=f"Almacenamiento con id {id} no encontrado")

    @classmethod
    def obtener_recarga(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for r in sim.estaciones_recarga:
            if getattr(r, 'id_recarga', None) == id:
                return RecargaResponse.from_model(r)
        raise HTTPException(status_code=404, detail=f"Recarga con id {id} no encontrada")

    @classmethod
    def obtener_pedido(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for p in sim.pedidos:
            if getattr(p, 'id_pedido', None) == id:
                cls.logger.info(f"obtener_pedido: Pedido encontrado {id}")
                return PedidoResponse.from_model(p)
        cls.logger.warning(f"obtener_pedido: Pedido no encontrado {id}")
        raise HTTPException(status_code=404, detail=f"Pedido con id {id} no encontrado")

    @classmethod
    def calcular_ruta_pedido(cls, id_pedido: int, algoritmo: str):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.calcular_ruta_pedido(id_pedido, algoritmo)

    @classmethod
    def obtener_estadisticas(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.obtener_estadisticas()

    @classmethod
    def obtener_nodos(cls):
        cls._check_simulacion()
        return Simulacion.obtener_instancia().obtener_nodos()

    @classmethod
    def obtener_aristas(cls):
        cls._check_simulacion()
        return Simulacion.obtener_instancia().obtener_aristas()

    @classmethod
    def marcar_pedido_entregado(cls, id_pedido: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.marcar_pedido_entregado(id_pedido)

    @classmethod
    def entregar_pedido(cls, id_pedido: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.marcar_pedido_entregado(id_pedido)

    @classmethod
    def rutas_mas_frecuentes(cls, top: int = 5):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.rutas_mas_frecuentes(top)

    @classmethod
    def obtener_ruta(cls, id_pedido: int, algoritmo: str):
        """
        Obtiene la ruta óptima para un pedido dado usando el algoritmo especificado.
        Devuelve un DTO de ruta o lanza HTTPException si no es posible calcularla.
        """
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        try:
            ruta = sim.calcular_ruta_pedido(id_pedido, algoritmo)
            if not ruta:
                raise HTTPException(status_code=404, detail=f"No se pudo calcular la ruta para el pedido {id_pedido}")
            # Se asume que ruta es una instancia de la clase de dominio Ruta
            return RutaResponse.from_model(ruta)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

    @classmethod
    def obtener_todos_los_caminos_floyd_warshall(cls):
        """
        Expone los resultados de Floyd-Warshall a la capa de aplicación.
        """
        if Simulacion._instancia is None:
            raise Exception("Simulación no iniciada")
        distancias, caminos = cls._dominio_service.obtener_todos_los_caminos_floyd_warshall()
        from Backend.API.DTOs.Dtos1 import FloydWarshallResponse
        return FloydWarshallResponse.from_resultados(distancias, caminos)

    @classmethod
    def calcular_camino_entre_nodos(cls, origen: int, destino: int, algoritmo: str):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        resultado = sim.calcular_camino_entre_nodos(origen, destino, algoritmo)
        return resultado

    @classmethod
    def obtener_errores_pedidos(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        errores = sim.obtener_errores_pedidos()
        cls.logger.info(f"obtener_errores_pedidos: {len(errores)} errores retornados")
        return errores


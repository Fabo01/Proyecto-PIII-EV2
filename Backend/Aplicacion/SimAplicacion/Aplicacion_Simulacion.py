from Backend.Aplicacion.SimAplicacion.ISimulacionAplicacionService import ISimulacionAplicacionService
from Backend.Dominio.Simulacion_dominio import Simulacion
from Backend.Servicios.SimServicios.Servicios_Simulacion import SimulacionDominioService
from fastapi import HTTPException
import logging
from Backend.API.DTOs.DTOsRespuesta.RespuestaCliente import RespuestaCliente
from Backend.API.DTOs.DTOsRespuesta.RespuestaAlmacenamiento import RespuestaAlmacenamiento
from Backend.API.DTOs.DTOsRespuesta.RespuestaRecarga import RespuestaRecarga
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaFloydWarshall import RespuestaFloydWarshall
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from Backend.API.DTOs.DTOsRespuesta.RespuestaEstadisticas import RespuestaEstadisticas
from Backend.Infraestructura.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.Infraestructura.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.Infraestructura.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.Infraestructura.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.Infraestructura.Mapeadores.MapeadorRuta import MapeadorRuta
from Backend.Servicios.Observer.ObserverEstadisticas import ObserverEstadisticas
from Backend.Servicios.Observer.SujetoObservable import SujetoObservable

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
    def iniciar_simulacion(cls, n_vertices: int, m_aristas: int, n_pedidos: int, estrategia_ruta: str = None):
        if n_vertices <= 0 or m_aristas <= 0 or n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para iniciar la simulación")
        sujeto_observable = SujetoObservable()
        Simulacion.reiniciar_instancia(n_vertices, m_aristas, n_pedidos, sujeto_observable)
        sim = Simulacion.obtener_instancia()
        # Registrar observer de estadísticas
        observer_estadisticas = ObserverEstadisticas(SimulacionDominioService())
        sim.agregar_observador(observer_estadisticas)
        if estrategia_ruta:
            Simulacion.obtener_instancia().set_estrategia_ruta(estrategia_ruta)
            cls._dominio_service.set_estrategia_ruta(estrategia_ruta)
        return cls.estado_actual()

    @classmethod
    def reiniciar_simulacion(cls, n_vertices: int, m_aristas: int, n_pedidos: int):
        if n_vertices <= 0 or m_aristas <= 0 or n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para reiniciar la simulación")
        sujeto_observable = SujetoObservable()
        Simulacion.reiniciar_instancia(n_vertices, m_aristas, n_pedidos, sujeto_observable)
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
                'n_vertices': 0,
                'm_aristas': 0,
                'n_pedidos': 0,
                'ok': False
            }
        sim = Simulacion.obtener_instancia()
        return {
            'clientes': [MapeadorCliente.a_dto(c).model_dump() for c in sim.listar_clientes()],
            'almacenamientos': [MapeadorAlmacenamiento.a_dto(a).model_dump() for a in sim.listar_almacenamientos()],
            'recargas': [MapeadorRecarga.a_dto(r).model_dump() for r in sim.listar_recargas()],
            'pedidos': [MapeadorPedido.a_dto(p).model_dump() for p in sim.listar_pedidos()],
            'rutas': [MapeadorRuta.a_dto(r).model_dump() for r in sim.rutas],
            'estado': 'iniciada',
            'n_vertices': getattr(sim, 'n_vertices', 0),
            'm_aristas': getattr(sim, 'm_aristas', 0),
            'n_pedidos': getattr(sim, 'n_pedidos', 0),
            'ok': True
        }

    @classmethod
    def listar_clientes(cls):
        cls._check_simulacion()
        # Retornar lista de clientes de dominio para que el mapeo se realice en la capa de API
        sim = Simulacion.obtener_instancia()
        return sim.clientes

    @classmethod
    def listar_almacenamientos(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.almacenamientos

    @classmethod
    def listar_recargas(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.estaciones_recarga

    @classmethod
    def listar_pedidos(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        pedidos_raw = sim.pedidos if hasattr(sim, 'pedidos') else []
        pedidos_dtos = []
        for p in pedidos_raw:
            try:
                dto = MapeadorPedido.a_dto(p)
            except Exception as e:
                cls.logger.warning(f"Pedido {getattr(p, 'id_pedido', None)} no pudo mapearse: {e}")
                sim.registrar_error_pedido(
                    id_pedido=getattr(p, 'id_pedido', None),
                    motivo=f"Error de mapeo: {e}",
                    datos=getattr(p, '__dict__', str(p))
                )
                continue
            if dto.origen is None or dto.destino is None:
                cls.logger.warning(f"Pedido {dto.id_pedido} incompleto filtrado y no será devuelto")
                sim.registrar_error_pedido(
                    id_pedido=getattr(p, 'id_pedido', None),
                    motivo="Pedido incompleto: origen o destino nulo",
                    datos={
                        'cliente': getattr(p, 'cliente', None),
                        'almacen': getattr(p, 'almacen', None),
                        'fecha': getattr(p, 'fecha_creacion', None),
                        'prioridad': getattr(p, 'prioridad', None)
                    }
                )
                continue
            pedidos_dtos.append(dto)
        cls.logger.info(f"listar_pedidos: {len(pedidos_dtos)} pedidos completos retornados de {len(pedidos_raw)}")
        return pedidos_dtos

    @classmethod
    def listar_rutas(cls):
        cls._check_simulacion()
        return [MapeadorRuta.a_dto(r) for r in Simulacion.obtener_instancia().rutas]

    @classmethod
    def obtener_cliente(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for c in sim.clientes:
            if getattr(c, 'id_cliente', None) == id:
                # Retornar objeto de dominio para mapeo en API
                return c
        raise HTTPException(status_code=404, detail=f"Cliente con id {id} no encontrado")

    @classmethod
    def obtener_almacenamiento(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for a in sim.almacenamientos:
            if getattr(a, 'id_almacenamiento', None) == id:
                return a
        raise HTTPException(status_code=404, detail=f"Almacenamiento con id {id} no encontrado")

    @classmethod
    def obtener_recarga(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        for r in sim.estaciones_recarga:
            if getattr(r, 'id_recarga', None) == id:
                return r
        raise HTTPException(status_code=404, detail=f"Recarga con id {id} no encontrada")

    @classmethod
    def obtener_pedido(cls, id: int):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        # Acceso O(1) usando hash_pedidos
        pedido = sim.hash_pedidos.get(id)
        if pedido:
            cls.logger.info(f"obtener_pedido: Pedido encontrado {id}")
            return pedido
        cls.logger.warning(f"obtener_pedido: Pedido no encontrado {id}")
        raise HTTPException(status_code=404, detail=f"Pedido con id {id} no encontrado")

    @classmethod
    def calcular_ruta_pedido(cls, id_pedido: int, algoritmo: str = None):
        import logging
        logger = logging.getLogger("SimulacionAplicacionService")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[SimulacionAplicacionService.calcular_ruta_pedido] Solicitando cálculo de ruta para pedido {id_pedido} con algoritmo {algoritmo}")
        cls._check_simulacion()
        resultado = cls._dominio_service.calcular_ruta_pedido(id_pedido, algoritmo)
        logger.info(f"[SimulacionAplicacionService.calcular_ruta_pedido] Resultado DTO: {resultado}")
        return resultado

    @classmethod
    def obtener_estadisticas(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        return sim.obtener_estadisticas()

    @classmethod
    def obtener_vertices(cls):
        cls._check_simulacion()
        return Simulacion.obtener_instancia().obtener_vertices()

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
            return MapeadorRuta.a_dto(ruta)
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
        from Backend.API.DTOs.DTOsRespuesta.RespuestaFloydWarshall import RespuestaFloydWarshall
        return RespuestaFloydWarshall.from_resultados(distancias, caminos)

    @classmethod
    def calcular_camino_entre_vertices(cls, origen: int, destino: int, algoritmo: str):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        resultado = sim.calcular_camino_entre_vertices(origen, destino, algoritmo)
        return resultado

    @classmethod
    def obtener_errores_pedidos(cls):
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        errores = sim.obtener_errores_pedidos()
        cls.logger.info(f"obtener_errores_pedidos: {len(errores)} errores retornados")
        return errores

    @classmethod
    def set_estrategia_ruta(cls, nombre_estrategia):
        Simulacion.obtener_instancia().set_estrategia_ruta(nombre_estrategia)
        cls._dominio_service.set_estrategia_ruta(nombre_estrategia)

    @classmethod
    def comparar_tiempos_algoritmos(cls, id_pedido: int):
        """
        Calcula la ruta para un pedido usando todos los algoritmos y retorna los tiempos de cálculo y resultados.
        """
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        algoritmos = ['dijkstra', 'bfs', 'dfs', 'floyd_warshall']
        resultados = {}
        for algoritmo in algoritmos:
            try:
                ruta = sim.calcular_ruta_pedido(id_pedido, algoritmo)
                resultados[algoritmo] = {
                    'camino': getattr(ruta, 'camino', []),
                    'peso_total': getattr(ruta, 'peso_total', None),
                    'tiempo_calculo': getattr(ruta, 'tiempo_calculo', None),
                    'valida': ruta.es_valida() if ruta else False
                }
            except Exception as e:
                resultados[algoritmo] = {'error': str(e)}
        return resultados

    @classmethod
    def obtener_arbol_expansion_minima(cls):
        """
        Devuelve el árbol de expansión mínima (lista de aristas y peso total) usando Kruskal.
        """
        cls._check_simulacion()
        sim = Simulacion.obtener_instancia()
        mst, peso_total = sim.calcular_arbol_expansion_minima()
        # Serializar aristas a DTOs
        aristas_dto = [MapeadorRuta.a_dto(a) for a in mst]
        return {'aristas': aristas_dto, 'peso_total': peso_total}

    @classmethod
    def obtener_clientes_hashmap(cls):
        """
        Retorna el hashmap de clientes (ID → Objeto Cliente).
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_clientes_hashmap()

    @classmethod
    def obtener_pedidos_hashmap(cls):
        """
        Retorna el hashmap de pedidos (ID → Objeto Pedido).
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_pedidos_hashmap()

    @classmethod
    def obtener_almacenamientos_hashmap(cls):
        """
        Retorna el hashmap de almacenamientos (ID → Objeto Almacenamiento).
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_almacenamientos_hashmap()

    @classmethod
    def obtener_recargas_hashmap(cls):
        """
        Retorna el hashmap de recargas (ID → Objeto Recarga).
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_recargas_hashmap()

    @classmethod
    def obtener_vertices_hashmap(cls):
        """
        Retorna el hashmap de vértices (ID → Objeto Vertice).
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_vertices_hashmap()

    @classmethod
    def obtener_aristas_hashmap(cls):
        """
        Retorna el hashmap de aristas (clave → Objeto Arista).
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_aristas_hashmap()

    @classmethod
    def obtener_rutas_hashmap(cls):
        """
        Retorna el hashmap de rutas (clave → Objeto Ruta) serializable.
        """
        cls._check_simulacion()
        return cls._dominio_service.obtener_rutas_hashmap()


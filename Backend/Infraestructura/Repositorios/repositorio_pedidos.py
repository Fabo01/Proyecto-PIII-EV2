"""
RepositorioPedidos: Acceso centralizado y unico a instancias de Pedido.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
Incluye logging detallado de operaciones y asociaciones.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio
import logging

class RepositorioPedidos(IRepositorio):
    """
    Repositorio para gestionar instancias unicas de Pedido.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    Incluye logging detallado de asociaciones.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._pedidos = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.logger = logging.getLogger("RepositorioPedidos")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
            cls._instancia.notificar_observadores('repositorio_pedidos_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, pedido):
        """
        Agrega una nueva instancia de Pedido al repositorio asegurando unicidad.
        Si el pedido ya existe, retorna la instancia existente.
        Si es nuevo, lo agrega y asocia cliente y vertices reales si existen.
        """
        existente = self._pedidos.buscar(pedido.id_pedido)
        if existente:
            self.logger.warning(f"[RepositorioPedidos] Pedido duplicado: id={pedido.id_pedido}")
            self.notificar_observadores('repositorio_pedidos_agregado_duplicado', {'pedido': existente})
            return existente
        # Asociar cliente y vertices reales si existen
        if hasattr(pedido, 'cliente') and pedido.cliente is not None:
            # Se asume que cliente es objeto real
            pass
        if hasattr(pedido, 'origen') and pedido.origen is not None:
            pass
        if hasattr(pedido, 'destino') and pedido.destino is not None:
            pass
        self._pedidos.insertar(pedido.id_pedido, pedido)
        self.logger.info(f"[RepositorioPedidos] Pedido agregado: id={pedido.id_pedido} | cliente={getattr(pedido, 'cliente', None)} | origen={getattr(pedido, 'origen', None)} | destino={getattr(pedido, 'destino', None)}")
        self.notificar_observadores('repositorio_pedidos_agregado', {'pedido': pedido})
        return pedido

    def asociar_cliente_a_pedido(self, id_pedido, cliente):
        """
        Asocia un objeto Cliente real a un pedido existente en el repositorio.
        Si el pedido no existe, no hace nada.
        """
        pedido = self._pedidos.buscar(id_pedido)
        if pedido is not None:
            pedido.cliente = cliente
            self.notificar_observadores('repositorio_pedidos_cliente_asociado', {'id_pedido': id_pedido, 'id_cliente': getattr(cliente, 'id_cliente', None)})

    def asociar_vertices_a_pedido(self, id_pedido, origen, destino):
        """
        Asocia los objetos Vertice reales de origen y destino a un pedido existente en el repositorio.
        Si el pedido no existe, no hace nada.
        """
        pedido = self._pedidos.buscar(id_pedido)
        if pedido is not None:
            pedido.origen = origen
            pedido.destino = destino
            self.notificar_observadores('repositorio_pedidos_vertices_asociados', {'id_pedido': id_pedido, 'origen': getattr(origen, 'id', None), 'destino': getattr(destino, 'id', None)})
    def obtener(self, id_pedido):
        """
        Obtiene una instancia de Pedido por su ID.
        :param id_pedido: Identificador unico del pedido.
        :return: Instancia de Pedido o None si no existe.
        """
        pedido = self._pedidos.buscar(id_pedido)
        self.logger.info(f"[RepositorioPedidos] Pedido obtenido: id={id_pedido} | pedido={pedido}")
        self.notificar_observadores('repositorio_pedidos_obtenido', {'id': id_pedido, 'pedido': pedido})
        return pedido

    def eliminar(self, id_pedido):
        """
        Elimina una instancia de Pedido por su ID.
        :param id_pedido: Identificador unico del pedido.
        """
        self._pedidos.eliminar(id_pedido)
        self.logger.info(f"[RepositorioPedidos] Pedido eliminado: id={id_pedido}")
        self.notificar_observadores('repositorio_pedidos_eliminado', {'id': id_pedido})

    def todos(self):
        """
        Retorna todos los pedidos registrados en el repositorio.
        """
        pedidos = self._pedidos.valores()
        self.logger.info(f"[RepositorioPedidos] Listando todos los pedidos: total={len(pedidos)}")
        return list(pedidos)

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Pedido.
        """
        self._pedidos = HashMap()
        self.notificar_observadores('repositorio_pedidos_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de pedidos (ID → Objeto Pedido) como dict.
        :return: Diccionario de pedidos.
        """
        self.notificar_observadores('repositorio_pedidos_hashmap', None)
        return dict(self._pedidos.items())

    def obtener_hashmap_serializable(self):
        """
        Retorna hashmap de pedidos serializado usando MapeadorPedido.
        Los objetos complejos se convierten a dicts planos para evitar errores de serialización.
        :return: Dict con pedidos serializados listos para API.
        """
        try:
            from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
            pedidos_dict = {}
            for id_pedido, pedido in self._pedidos.items():
                pedidos_dict[str(id_pedido)] = MapeadorPedido.a_hashmap(pedido)
            self.logger.info(f"[RepositorioPedidos] Hashmap serializable generado: {len(pedidos_dict)} pedidos")
            self.notificar_observadores('repositorio_pedidos_hashmap_serializable', {'total': len(pedidos_dict)})
            return pedidos_dict
        except Exception as e:
            self.logger.error(f"[RepositorioPedidos] Error generando hashmap serializable: {e}")
            return {}

    def obtener_por_cliente(self, id_cliente):
        """
        Obtiene todos los pedidos asociados a un cliente específico.
        :param id_cliente: Identificador único del cliente.
        :return: Lista de instancias de Pedido.
        """
        pedidos_cliente = []
        for pedido in self._pedidos.valores():
            try:
                cliente = pedido.obtener_cliente()
                if cliente and getattr(cliente, 'id_cliente', None) == id_cliente:
                    pedidos_cliente.append(pedido)
            except Exception:
                continue
        self.logger.info(f"[RepositorioPedidos] Pedidos del cliente {id_cliente}: {len(pedidos_cliente)}")
        self.notificar_observadores('repositorio_pedidos_por_cliente', {'id_cliente': id_cliente, 'total': len(pedidos_cliente)})
        return pedidos_cliente

    def obtener_por_almacenamiento(self, id_almacenamiento):
        """
        Obtiene todos los pedidos cuyo origen es un almacenamiento específico.
        :param id_almacenamiento: Identificador único del almacenamiento.
        :return: Lista de instancias de Pedido.
        """
        pedidos_en_almacen = []
        for pedido in self._pedidos.valores():
            try:
                origen = pedido.obtener_origen()
                if origen and getattr(origen, 'id_almacenamiento', None) == id_almacenamiento:
                    pedidos_en_almacen.append(pedido)
            except Exception:
                continue
        self.logger.info(f"[RepositorioPedidos] Pedidos en almacen {id_almacenamiento}: {len(pedidos_en_almacen)}")
        self.notificar_observadores('repositorio_pedidos_por_almacen', {'id_almacenamiento': id_almacenamiento, 'total': len(pedidos_en_almacen)})
        return pedidos_en_almacen

    def obtener_todos_serializables(self):
        """
        Retorna todos los pedidos serializados como dict plano.
        """
        return self.obtener_hashmap_serializable()

    def obtener_por_tipo(self, tipo_elemento):
        """
        Para pedidos, filtra por tipo de prioridad o status.
        """
        pedidos_filtrados = []
        for pedido in self._pedidos.valores():
            if hasattr(pedido, 'prioridad') and pedido.prioridad == tipo_elemento:
                pedidos_filtrados.append(pedido)
            elif hasattr(pedido, 'status') and pedido.status == tipo_elemento:
                pedidos_filtrados.append(pedido)
        return pedidos_filtrados

    def serializar_relaciones(self):
        """
        Retorna mapeo de relaciones pedido-cliente-almacenamiento.
        """
        relaciones = {
            'pedidos_por_cliente': {},
            'pedidos_por_almacenamiento': {},
            'total_pedidos': len(list(self._pedidos.valores()))
        }
        for pedido in self._pedidos.valores():
            # Relación pedido-cliente
            if hasattr(pedido, 'cliente') and hasattr(pedido.cliente, 'id_cliente'):
                id_cliente = pedido.cliente.id_cliente
                if id_cliente not in relaciones['pedidos_por_cliente']:
                    relaciones['pedidos_por_cliente'][id_cliente] = []
                relaciones['pedidos_por_cliente'][id_cliente].append(pedido.id_pedido)
            # Relación pedido-almacenamiento (origen)
            if hasattr(pedido, 'origen') and hasattr(pedido.origen, 'elemento'):
                elemento = pedido.origen.elemento
                if hasattr(elemento, 'id_almacenamiento'):
                    id_almacen = elemento.id_almacenamiento
                    if id_almacen not in relaciones['pedidos_por_almacenamiento']:
                        relaciones['pedidos_por_almacenamiento'][id_almacen] = []
                    relaciones['pedidos_por_almacenamiento'][id_almacen].append(pedido.id_pedido)
        return relaciones

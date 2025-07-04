"""
RepositorioClientes: Acceso centralizado y unico a instancias de Cliente.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio

class RepositorioClientes(IRepositorio):
    """
    Repositorio para gestionar instancias unicas de Cliente.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._clientes = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_clientes_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, cliente):
        """
        Agrega una nueva instancia de Cliente al repositorio asegurando unicidad.
        Si el cliente ya existe, retorna la instancia existente.
        Si el cliente es nuevo, lo agrega y asocia sus pedidos reales si existen.
        """
        existente = self._clientes.buscar(cliente.id_cliente)
        if existente:
            # Si el cliente ya existe, fusionar pedidos si hay nuevos
            nuevos_pedidos = [p for p in getattr(cliente, '_pedidos', []) if p not in existente._pedidos]
            for pedido in nuevos_pedidos:
                existente.agregar_pedido(pedido)
            self.notificar_observadores('repositorio_clientes_agregado_duplicado', {'cliente': existente})
            return existente
        # Si es nuevo, asegurar que los pedidos asociados sean objetos reales
        if hasattr(cliente, '_pedidos'):
            pedidos_reales = []
            for pedido in cliente._pedidos:
                if hasattr(pedido, 'id_pedido'):
                    pedidos_reales.append(pedido)
            cliente._pedidos = pedidos_reales
        self._clientes.insertar(cliente.id_cliente, cliente)
        self.notificar_observadores('repositorio_clientes_agregado', {'cliente': cliente})
        return cliente

    def asociar_pedido_a_cliente(self, id_cliente, pedido):
        """
        Asocia un objeto Pedido real a un cliente existente en el repositorio.
        Si el cliente no existe, no hace nada.
        """
        cliente = self._clientes.buscar(id_cliente)
        if cliente is not None:
            cliente.agregar_pedido(pedido)
            self.notificar_observadores('repositorio_clientes_pedido_asociado', {'id_cliente': id_cliente, 'id_pedido': getattr(pedido, 'id_pedido', None)})
        # Si el cliente no existe, no se asocia

    def obtener(self, id_cliente):
        """
        Obtiene una instancia de Cliente por su ID.
        :param id_cliente: Identificador unico del cliente.
        :return: Instancia de Cliente o None si no existe.
        """
        cliente = self._clientes.buscar(id_cliente)
        self.notificar_observadores('repositorio_clientes_obtenido', {'id': id_cliente, 'cliente': cliente})
        return cliente

    def eliminar(self, id_cliente):
        """
        Elimina una instancia de Cliente por su ID.
        :param id_cliente: Identificador unico del cliente.
        """
        self._clientes.eliminar(id_cliente)
        self.notificar_observadores('repositorio_clientes_eliminado', {'id': id_cliente})

    def todos(self):
        """
        Retorna todos los clientes registrados en el repositorio.
        :return: Lista de instancias de Cliente.
        """
        clientes = self._clientes.valores()
        self.notificar_observadores('repositorio_clientes_todos', {'total': len(clientes)})
        return list(clientes)

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Cliente.
        """
        self._clientes.limpiar()
        self.notificar_observadores('repositorio_clientes_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de clientes (ID → Objeto Cliente) como dict.
        :return: Diccionario de clientes.
        """
        self.notificar_observadores('repositorio_clientes_hashmap', None)
        return dict(self._clientes.items())

    def obtener_hashmap_serializable(self):
        """
        Retorna el hashmap de clientes serializado como dict plano usando MapeadorCliente.
        :return: Dict con clientes serializados para API.
        """
        try:
            from Backend.API.Mapeadores.MapeadorCliente import MapeadorCliente
            resultado = {}
            for id_cliente, cliente in self._clientes.items():
                resultado[str(id_cliente)] = MapeadorCliente.a_hashmap(cliente)
            self.notificar_observadores('repositorio_clientes_hashmap_serializable', {'total': len(resultado)})
            return resultado
        except Exception as e:
            import logging
            logging.getLogger("RepositorioClientes").error(f"Error generando hashmap serializable: {e}")
            return {}

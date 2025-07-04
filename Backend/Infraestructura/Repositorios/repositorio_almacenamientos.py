"""
RepositorioAlmacenamientos: Acceso centralizado y unico a instancias de Almacenamiento.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio

class RepositorioAlmacenamientos(IRepositorio):
    """
    Repositorio para gestionar instancias unicas de Almacenamiento.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._almacenamientos = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_almacenamientos_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, almacen):
        """
        Agrega una nueva instancia de Almacenamiento al repositorio asegurando unicidad.
        Si el almacenamiento ya existe, retorna la instancia existente.
        Si el almacenamiento es nuevo, lo agrega y asocia sus pedidos reales si existen.
        """
        existente = self._almacenamientos.buscar(almacen.id_almacenamiento)
        if existente:
            # Si el almacenamiento ya existe, fusionar pedidos si hay nuevos
            nuevos_pedidos = [p for p in getattr(almacen, '_pedidos', []) if p not in existente._pedidos]
            for pedido in nuevos_pedidos:
                existente.agregar_pedido(pedido)
            self.notificar_observadores('repositorio_almacenamientos_agregado_duplicado', {'almacen': existente})
            return existente
        # Si es nuevo, asegurar que los pedidos asociados sean objetos reales
        if hasattr(almacen, '_pedidos'):
            pedidos_reales = []
            for pedido in almacen._pedidos:
                if hasattr(pedido, 'id_pedido'):
                    pedidos_reales.append(pedido)
            almacen._pedidos = pedidos_reales
        self._almacenamientos.insertar(almacen.id_almacenamiento, almacen)
        self.notificar_observadores('repositorio_almacenamientos_agregado', {'almacen': almacen})
        return almacen

    def asociar_pedido_a_almacenamiento(self, id_almacenamiento, pedido):
        """
        Asocia un objeto Pedido real a un almacenamiento existente en el repositorio.
        Si el almacenamiento no existe, no hace nada.
        :param id_almacenamiento: Identificador unico del almacenamiento.
        :param pedido: Objeto Pedido a asociar.
        """
        almacen = self._almacenamientos.buscar(id_almacenamiento)
        if almacen is not None:
            almacen.agregar_pedido(pedido)
            self.notificar_observadores('repositorio_almacenamientos_pedido_asociado', {'id_almacenamiento': id_almacenamiento, 'id_pedido': getattr(pedido, 'id_pedido', None)})

    def obtener(self, id_almacenamiento):
        """
        Obtiene una instancia de Almacenamiento por su ID.
        :param id_almacenamiento: Identificador unico del almacenamiento.
        :return: Instancia de Almacenamiento o None si no existe.
        """
        almacen = self._almacenamientos.buscar(id_almacenamiento)
        self.notificar_observadores('repositorio_almacenamientos_obtenido', {'id': id_almacenamiento, 'almacen': almacen})
        return almacen

    def eliminar(self, id_almacenamiento):
        """
        Elimina una instancia de Almacenamiento por su ID.
        :param id_almacenamiento: Identificador unico del almacenamiento.
        """
        self._almacenamientos.eliminar(id_almacenamiento)
        self.notificar_observadores('repositorio_almacenamientos_eliminado', {'id': id_almacenamiento})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Almacenamiento.
        :return: Lista de instancias de Almacenamiento.
        """
        almacenamientos = list(self._almacenamientos.valores())
        self.notificar_observadores('repositorio_almacenamientos_todos', {'cantidad': len(almacenamientos)})
        return almacenamientos

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Almacenamiento.
        """
        self._almacenamientos = HashMap()
        self.notificar_observadores('repositorio_almacenamientos_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de almacenamientos (ID → Objeto Almacenamiento) como dict.
        :return: Diccionario de almacenamientos.
        """
        self.notificar_observadores('repositorio_almacenamientos_hashmap', None)
        return dict(self._almacenamientos.items())

    def obtener_hashmap_serializable(self):
        """
        Retorna el hashmap de almacenamientos serializado como dict plano usando MapeadorAlmacenamiento.
        :return: Dict con almacenamientos serializados para API.
        """
        try:
            from Backend.API.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
            resultado = {}
            for id_alm, almacen in self._almacenamientos.items():
                resultado[str(id_alm)] = MapeadorAlmacenamiento.a_hashmap(almacen)
            self.notificar_observadores('repositorio_almacenamientos_hashmap_serializable', {'total': len(resultado)})
            return resultado
        except Exception as e:
            import logging
            logging.getLogger("RepositorioAlmacenamientos").error(f"Error generando hashmap serializable: {e}")
            return {}

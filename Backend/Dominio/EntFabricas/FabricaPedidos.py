"""
FabricaPedidos: Fábrica centralizada para la creación y validación de pedidos en la simulación logística de drones.
Incluye trazabilidad detallada de asociaciones y errores.
"""
from Backend.Dominio.Dominio_Pedido import Pedido
from datetime import datetime
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz
import logging

class FabricaPedidos(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaPedidos")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, id_pedido, vertice_cliente, vertice_almacen, prioridad, fecha_creacion=None):
        """
        Crea un pedido y lo registra en el repositorio si no existe. Si falla, registra el error y lo documenta.
        Notifica a los observadores la creación y errores. Loguea todas las asociaciones relevantes.
        """
        repo = RepositorioPedidos()
        existente = repo.obtener(id_pedido)
        if existente:
            self.logger.info(f"Pedido {id_pedido} ya existe, retornando instancia existente.")
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('pedido_existente', {'id_pedido': id_pedido})
            return existente
        try:
            self.logger.info(f"Creando pedido {id_pedido} | Cliente: {getattr(vertice_cliente, 'elemento', vertice_cliente)} | Almacen: {getattr(vertice_almacen, 'elemento', vertice_almacen)} | Prioridad: {prioridad}")
            pedido = Pedido(
                id_pedido=id_pedido,
                cliente_v=vertice_cliente,
                origen_v=vertice_almacen,
                destino_v=vertice_cliente,
                prioridad=prioridad,
                fecha_creacion=fecha_creacion or datetime.now()
            )
            repo.agregar(pedido)
            self.logger.info(f"Pedido {id_pedido} creado y registrado. Asociaciones: Cliente={pedido.cliente}, Origen={pedido.origen}, Destino={pedido.destino}")
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('pedido_creado', {'id_pedido': id_pedido})
            return pedido
        except Exception as e:
            self.logger.error(f"Error creando pedido {id_pedido}: {e} | Cliente: {vertice_cliente} | Almacen: {vertice_almacen}")
            self.errores.append({'id_pedido': id_pedido, 'error': str(e)})
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('error_pedido', {'id_pedido': id_pedido, 'error': str(e)})
            return None

    def obtener(self, clave):
        """
        Obtiene un pedido existente del repositorio.
        """
        return RepositorioPedidos().obtener(clave)

    def todos(self):
        """
        Retorna todos los pedidos registrados en el repositorio.
        """
        return RepositorioPedidos().todos()

    def limpiar(self):
        """
        Limpia el repositorio de pedidos y los errores registrados.
        """
        RepositorioPedidos().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de pedidos.
        """
        return self.errores


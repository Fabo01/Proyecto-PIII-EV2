"""
FabricaPedidos: Fábrica centralizada para la creación y validación de pedidos en la simulación logística de drones.
Cumple SOLID, patrones de diseño y requisitos del proyecto.
"""
from Backend.Dominio.Dominio_Pedido import Pedido
from datetime import datetime
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaPedidos(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
        return cls._instancia

    def crear(self, id_pedido, vertice_cliente, vertice_almacen, prioridad, fecha_creacion=None):
        """
        Crea un pedido y lo registra en el repositorio si no existe. Si falla, registra el error y lo documenta.
        Notifica a los observadores la creación y errores.
        """
        repo = RepositorioPedidos()
        existente = repo.obtener(id_pedido)
        if existente:
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('pedido_existente', {'id_pedido': id_pedido})
            return existente
        try:
            pedido = Pedido(
                id_pedido=id_pedido,
                cliente_v=vertice_cliente,
                origen_v=vertice_almacen,
                destino_v=vertice_cliente,
                prioridad=prioridad,
                fecha_creacion=fecha_creacion or datetime.now()
            )
            repo.agregar(pedido)
            if hasattr(self, 'notificar_observadores'):
                self.notificar_observadores('pedido_creado', {'id_pedido': id_pedido})
            return pedido
        except Exception as e:
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
        Limpia el repositorio y el estado interno de la fábrica, eliminando referencias y reseteando estructuras.
        """
        RepositorioPedidos().limpiar()
        self.errores = []

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante creación de pedidos.
        """
        return self.errores

    # Métodos protegidos para extensión de reglas de validación
    def _validar_regla_personalizada(self, *args, **kwargs):
        pass

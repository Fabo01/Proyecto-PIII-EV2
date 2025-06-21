"""
FabricaPedidos: Fábrica centralizada para la creación y validación de pedidos en la simulación logística de drones.
Cumple SOLID, patrones de diseño y requisitos del proyecto.
"""
from Backend.Dominio.Dominio_Pedido import Pedido
from datetime import datetime
import logging
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

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
        """
        repo = RepositorioPedidos()
        existente = repo.obtener(id_pedido)
        if existente:
            self.logger.info(f"Pedido {id_pedido} ya existe, retornando instancia existente.")
            return existente
        self.logger.info(f"Intentando crear pedido {id_pedido}:")
        self.logger.info(f"  vertice_cliente: {vertice_cliente}")
        self.logger.info(f"  vertice_cliente.elemento: {getattr(vertice_cliente, 'elemento', lambda: None)() if vertice_cliente else None}")
        self.logger.info(f"  vertice_almacen: {vertice_almacen}")
        self.logger.info(f"  vertice_almacen.elemento: {getattr(vertice_almacen, 'elemento', lambda: None)() if vertice_almacen else None}")
        self.logger.info(f"  prioridad: {prioridad}")
        self.logger.info(f"  fecha_creacion: {fecha_creacion}")
        errores = []
        if vertice_cliente is None:
            error_msg = f"vertice_cliente es None"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        elif not hasattr(vertice_cliente, 'elemento'):
            error_msg = f"vertice_cliente no tiene método elemento"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        elif getattr(vertice_cliente.elemento(), 'tipo_elemento', None) != 'cliente':
            error_msg = f"vertice_cliente no es de tipo cliente"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        if vertice_almacen is None:
            error_msg = f"vertice_almacen es None"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        elif not hasattr(vertice_almacen, 'elemento'):
            error_msg = f"vertice_almacen no tiene método elemento"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        elif getattr(vertice_almacen.elemento(), 'tipo_elemento', None) != 'almacenamiento':
            error_msg = f"vertice_almacen no es de tipo almacenamiento"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        if fecha_creacion is not None and not isinstance(fecha_creacion, datetime):
            error_msg = f"fecha_creacion inválida: {fecha_creacion}"
            self.logger.warning(f"Pedido {id_pedido}: {error_msg}")
            errores.append(error_msg)
        if errores:
            # Volcado de todos los argumentos y sus atributos
            datos = {
                'id_pedido': id_pedido,
                'vertice_cliente': str(vertice_cliente),
                'vertice_cliente_atributos': vars(vertice_cliente) if hasattr(vertice_cliente, '__dict__') else str(vertice_cliente),
                'vertice_almacen': str(vertice_almacen),
                'vertice_almacen_atributos': vars(vertice_almacen) if hasattr(vertice_almacen, '__dict__') else str(vertice_almacen),
                'prioridad': prioridad,
                'fecha_creacion': str(fecha_creacion)
            }
            self.logger.error(f"Pedido {id_pedido} descartado por errores: {errores} | Datos: {datos}")
            self.errores.append({
                'id_pedido': id_pedido,
                'error': '; '.join(errores),
                'datos': datos
            })
            return None
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
            self.logger.info(f"Pedido {id_pedido} creado correctamente: {pedido}")
            self.logger.info(f"  Pedido.origen: {pedido.origen}, Pedido.destino: {pedido.destino}, Pedido.fecha_creacion: {pedido.fecha_creacion}")
            return pedido
        except Exception as e:
            # Volcado de todos los argumentos y sus atributos en caso de excepción
            datos = {
                'id_pedido': id_pedido,
                'vertice_cliente': str(vertice_cliente),
                'vertice_cliente_atributos': vars(vertice_cliente) if hasattr(vertice_cliente, '__dict__') else str(vertice_cliente),
                'vertice_almacen': str(vertice_almacen),
                'vertice_almacen_atributos': vars(vertice_almacen) if hasattr(vertice_almacen, '__dict__') else str(vertice_almacen),
                'prioridad': prioridad,
                'fecha_creacion': str(fecha_creacion)
            }
            self.logger.error(f"Excepción al crear pedido {id_pedido}: {e} | Datos: {datos}")
            self.errores.append({
                'id_pedido': id_pedido,
                'error': f'Excepción al crear pedido: {e}',
                'datos': datos
            })
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

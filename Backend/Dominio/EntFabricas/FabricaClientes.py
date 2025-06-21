"""
FabricaClientes: Fábrica centralizada para la creación y validación de clientes.
Garantiza unicidad y registro de errores.
"""
from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
import logging
from Backend.Dominio.Interfaces.IntFab.FabricaInterfaz import FabricaInterfaz

class FabricaClientes(FabricaInterfaz):
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.errores = []
            cls._instancia.logger = logging.getLogger("FabricaClientes")
            if not cls._instancia.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
                handler.setFormatter(formatter)
                cls._instancia.logger.addHandler(handler)
            cls._instancia.logger.setLevel(logging.INFO)
        return cls._instancia

    def crear(self, id_cliente, nombre):
        """
        Crea un cliente con id y nombre y lo registra en el repositorio si no existe.
        """
        repo = RepositorioClientes()
        existente = repo.obtener(id_cliente)
        if existente:
            self.logger.info(f"Cliente {id_cliente} ya existe, retornando instancia existente.")
            return existente
        try:
            cliente = Cliente(id_cliente, nombre)
            repo.agregar(cliente)
            return cliente
        except Exception as e:
            self.logger.error(f"Error creando cliente {id_cliente}: {e}")
            self.errores.append({'id_cliente': id_cliente, 'error': str(e)})
            return None

    def obtener(self, clave):
        """
        Obtiene un cliente existente del repositorio.
        """
        return RepositorioClientes().obtener(clave)

    def todos(self):
        """
        Retorna todos los clientes registrados en el repositorio.
        """
        return RepositorioClientes().todos()

    def limpiar(self):
        """
        Limpia el repositorio de clientes y los errores registrados.
        """
        RepositorioClientes().limpiar()
        self.errores.clear()

    def obtener_errores(self):
        """
        Retorna la lista de errores registrados durante la creación o gestión de clientes.
        """
        return self.errores

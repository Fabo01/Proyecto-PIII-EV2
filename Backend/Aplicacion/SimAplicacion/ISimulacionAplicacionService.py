from abc import ABC, abstractmethod
from typing import Any

class ISimulacionAplicacionService(ABC):
    @abstractmethod
    def iniciar_simulacion(self, request: Any) -> Any:
        pass

    @abstractmethod
    def estado_actual(self) -> Any:
        pass

    @abstractmethod
    def listar_clientes(self) -> Any:
        pass

    @abstractmethod
    def listar_almacenamientos(self) -> Any:
        pass

    @abstractmethod
    def listar_recargas(self) -> Any:
        pass

    @abstractmethod
    def listar_pedidos(self) -> Any:
        pass

    @abstractmethod
    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str) -> Any:
        pass

    @abstractmethod
    def listar_rutas(self) -> Any:
        pass

    @abstractmethod
    def obtener_estadisticas(self) -> Any:
        pass

    @abstractmethod
    def obtener_cliente(self, id: int) -> Any:
        pass

    @abstractmethod
    def obtener_almacenamiento(self, id: int) -> Any:
        pass

    @abstractmethod
    def obtener_recarga(self, id: int) -> Any:
        pass

    @abstractmethod
    def obtener_pedido(self, id: int) -> Any:
        pass

    @abstractmethod
    def obtener_ruta(self, id: int) -> Any:
        pass
    
    @abstractmethod
    def obtener_nodos(self) -> Any:
        pass

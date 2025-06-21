from abc import ABC, abstractmethod
from typing import Any, List

class ISimulacionDominioService(ABC):
    @abstractmethod
    def iniciar_simulacion(self, n_vertices: int, m_aristas: int, n_pedidos: int) -> Any:
        pass

    @abstractmethod
    def obtener_vertices(self) -> List[Any]:
        pass

    @abstractmethod
    def obtener_aristas(self) -> List[Any]:
        pass

    @abstractmethod
    def obtener_clientes(self) -> List[Any]:
        pass

    @abstractmethod
    def obtener_almacenamientos(self) -> List[Any]:
        pass

    @abstractmethod
    def obtener_recargas(self) -> List[Any]:
        pass

    @abstractmethod
    def obtener_pedidos(self) -> List[Any]:
        pass

    @abstractmethod
    def calcular_ruta_pedido(self, id_pedido: int, algoritmo: str) -> Any:
        pass

    @abstractmethod
    def marcar_pedido_entregado(self, id_pedido: int) -> Any:
        pass

    @abstractmethod
    def buscar_pedido(self, id_pedido: int) -> Any:
        pass

    @abstractmethod
    def obtener_rutas_mas_frecuentes(self, top: int = 5) -> Any:
        pass

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
    def obtener_vertices(self) -> Any:
        pass
    
    @abstractmethod
    def obtener_clientes_hashmap(self) -> dict:
        """Retorna el hashmap de clientes (ID → Objeto Cliente)."""
        pass

    @abstractmethod
    def obtener_pedidos_hashmap(self) -> dict:
        """Retorna el hashmap de pedidos (ID → Objeto Pedido)."""
        pass

    @abstractmethod
    def obtener_almacenamientos_hashmap(self) -> dict:
        """Retorna el hashmap de almacenamientos (ID → Objeto Almacenamiento)."""
        pass

    @abstractmethod
    def obtener_recargas_hashmap(self) -> dict:
        """Retorna el hashmap de recargas (ID → Objeto Recarga)."""
        pass

    @abstractmethod
    def obtener_vertices_hashmap(self) -> dict:
        """Retorna el hashmap de vértices (ID → Objeto Vertice)."""
        pass

    @abstractmethod
    def obtener_aristas_hashmap(self) -> dict:
        """Retorna el hashmap de aristas (clave → Objeto Arista)."""
        pass

    @abstractmethod
    def obtener_rutas_hashmap(self) -> dict:
        """Retorna el hashmap de rutas (clave → Objeto Ruta)."""
        pass

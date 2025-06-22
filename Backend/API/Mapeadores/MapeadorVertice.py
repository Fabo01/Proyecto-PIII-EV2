from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
from Backend.API.DTOs.DTOsRespuesta.RespuestaVertice import RespuestaVertice

class MapeadorVertice:
    """
    Clase utilitaria para mapear objetos Vertice del dominio a DTOs serializables para la API.
    """
    @staticmethod
    def a_dto(vertice: Vertice) -> RespuestaVertice:
        """
        Convierte un objeto Vertice a su representación DTO serializable.
        Args:
            vertice (Vertice): El objeto de dominio Vertice.
        Returns:
            RespuestaVertice: DTO serializable para la API.
        """
        elemento = vertice.elemento
        # Determinar tipo y nombre del elemento asociado
        tipo = getattr(elemento, 'tipo_elemento', 'desconocido')
        nombre = getattr(elemento, 'nombre', str(elemento))
        id_elemento = vertice.id_elemento()
        return RespuestaVertice(
            id=id_elemento,
            tipo=tipo,
            nombre=nombre
        )

from .RespuestaVertice import RespuestaVertice
from .RespuestaRecarga import RespuestaRecarga
from .RespuestaRuta import RespuestaRuta
from .RespuestaAlmacenamiento import RespuestaAlmacenamiento
from .RespuestaCliente import RespuestaCliente
from .RespuestaPedido import RespuestaPedido
from .RespuestaSimulacionEstado import RespuestaSimulacionEstado

# Actualizar referencias adelantadas SOLO aquí, cuando todos los modelos están cargados
RespuestaCliente.model_rebuild()
RespuestaAlmacenamiento.model_rebuild()
RespuestaPedido.model_rebuild()
RespuestaSimulacionEstado.model_rebuild()

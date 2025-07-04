"""
MapeadorRuta: Convierte entre modelo de dominio Ruta y RutaResponse DTO.
"""
from Backend.Dominio.Dominio_Ruta import Ruta
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta, RespuestaMultiplesRutas
import logging

logger = logging.getLogger("MapeadorRuta")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class MapeadorRuta:
    """
    Clase para mapear objetos Ruta del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(ruta: 'Ruta') -> 'RespuestaRuta':
        """
        Convierte Ruta de dominio a RespuestaRuta DTO.
        Si la ruta es None, lanza una excepción clara para manejo en el endpoint.
        """
        if ruta is None:
            raise ValueError("No se puede mapear una ruta nula. La ruta no fue encontrada o no es válida.")

        logger.info(f"Mapeando ruta: {type(ruta).__name__} - Atributos disponibles: {[attr for attr in dir(ruta) if not attr.startswith('_')]}")
        logger.info(f"Ruta ID: {getattr(ruta, 'id_ruta', 'NO_ENCONTRADO')}")
        logger.info(f"Algoritmo: {getattr(ruta, 'algoritmo', 'NO_ENCONTRADO')}")
        logger.info(f"Peso total: {getattr(ruta, 'peso_total', 'NO_ENCONTRADO')}")
        logger.info(f"Origen: {getattr(ruta, 'origen', 'NO_ENCONTRADO')}")
        logger.info(f"Destino: {getattr(ruta, 'destino', 'NO_ENCONTRADO')}")

        def extraer_info_vertice(vertice):
            if vertice is None:
                return None
            elemento = getattr(vertice, 'elemento', None) or vertice
            if isinstance(elemento, dict):
                # Si ya es dict, intentar extraer campos
                id_cliente = elemento.get('id_cliente')
                id_almacenamiento = elemento.get('id_almacenamiento')
                id_recarga = elemento.get('id_recarga')
                nombre = elemento.get('nombre') or f"Vertice_{id_cliente or id_almacenamiento or id_recarga}"
            else:
                id_cliente = getattr(elemento, 'id_cliente', None)
                id_almacenamiento = getattr(elemento, 'id_almacenamiento', None)
                id_recarga = getattr(elemento, 'id_recarga', None)
                nombre = getattr(elemento, 'nombre', None) or f"Vertice_{id_cliente or id_almacenamiento or id_recarga}"
            if id_cliente is not None:
                tipo = "cliente"
                id_ = id_cliente
            elif id_almacenamiento is not None:
                tipo = "almacenamiento"
                id_ = id_almacenamiento
            elif id_recarga is not None:
                tipo = "recarga"
                id_ = id_recarga
            else:
                tipo = "desconocido"
                id_ = None
            return {"id": id_, "nombre": nombre, "tipo": tipo}

        origen_info = extraer_info_vertice(getattr(ruta, 'origen', None))
        destino_info = extraer_info_vertice(getattr(ruta, 'destino', None))

        # Extraer IDs de aristas recorridas usando clave "origen-destino" y secuencia de vértices
        aristas_ids = []
        camino_vertices = []
        camino = getattr(ruta, 'camino', [])
        if camino and isinstance(camino, list):
            # Agregar el primer vértice origen si existe al menos una arista
            if camino:
                primer_origen = extraer_info_vertice(getattr(camino[0], 'origen', None))
                if primer_origen and primer_origen['id'] is not None:
                    camino_vertices.append(primer_origen['id'])
            
            # Procesar cada arista
            for arista in camino:
                ori = extraer_info_vertice(getattr(arista, 'origen', None))
                dst = extraer_info_vertice(getattr(arista, 'destino', None))
                if ori and dst and ori['id'] is not None and dst['id'] is not None:
                    aristas_ids.append(f"{ori['id']}-{dst['id']}")
                    # Agregar el destino al camino (el origen ya está agregado o se agregará)
                    if dst['id'] not in camino_vertices:
                        camino_vertices.append(dst['id'])

        # id_pedido debe ser int o None
        id_pedido = getattr(ruta, 'id_pedido', None)
        if id_pedido is not None:
            try:
                id_pedido = int(id_pedido)
            except (ValueError, TypeError):
                id_pedido = None

        # Obtener otros campos con valores por defecto seguros
        peso_total = getattr(ruta, 'peso_total', None)
        if peso_total is not None:
            try:
                peso_total = float(peso_total)
            except (ValueError, TypeError):
                peso_total = None

        algoritmo = getattr(ruta, 'algoritmo', None) or "desconocido"
        tiempo_calculo = getattr(ruta, 'tiempo_calculo', 0.0)
        if tiempo_calculo is None:
            tiempo_calculo = 0.0

        # Generar id_ruta por defecto si no existe
        id_ruta = getattr(ruta, 'id_ruta', None)
        if not id_ruta:
            origen_id = origen_info.get("id") if origen_info else "X"
            destino_id = destino_info.get("id") if destino_info else "X"
            id_ruta = f"{origen_id}-{destino_id}-{algoritmo}"

        fecha_creacion = getattr(ruta, 'fecha_creacion', '')
        if fecha_creacion:
            try:
                fecha_creacion = fecha_creacion.isoformat()
            except Exception:
                fecha_creacion = str(fecha_creacion)
        else:
            fecha_creacion = ""

        return RespuestaRuta(
            id_ruta=id_ruta,
            id_pedido=id_pedido,
            origen=origen_info,
            destino=destino_info,
            aristas_ids=aristas_ids,
            camino=camino_vertices,
            peso_total=peso_total,
            algoritmo=algoritmo,
            tiempo_calculo=tiempo_calculo,
            fecha_creacion=fecha_creacion
        )

    @staticmethod
    def rutas_multiples_a_dto(rutas_dict: dict, id_pedido: int) -> RespuestaMultiplesRutas:
        """
        Convierte diccionario de rutas a DTO de múltiples rutas.
        """
        resultados = {alg: MapeadorRuta.a_dto(r) for alg, r in rutas_dict.items() if r is not None}
        tiempo_total = sum(r.tiempo_calculo for r in rutas_dict.values() if getattr(r, 'tiempo_calculo', None) is not None)
        return RespuestaMultiplesRutas(
            id_pedido=id_pedido,
            resultados=resultados,
            tiempo_total=tiempo_total
        )

    @staticmethod
    def lista_a_dto(rutas):
        if not rutas:
            return []
        return [MapeadorRuta.a_dto(r) for r in rutas if r is not None]

    @staticmethod
    def lista_a_hashmap(rutas):
        """
        Convierte lista de rutas a diccionario de hashmaps para debugging.
        """
        if not rutas:
            return {}
        return {i: MapeadorRuta.a_hashmap(r) for i, r in enumerate(rutas) if r is not None}
    
    @staticmethod
    def a_hashmap(ruta: 'Ruta') -> dict:
        """
        Convierte Ruta de dominio a diccionario serializable para debugging.
        Maneja casos donde la ruta puede tener campos nulos.
        """
        if ruta is None:
            return {}
        
        try:
            # Información básica de la ruta
            hashmap = {
                'id_ruta': getattr(ruta, 'id_ruta', 'sin_id'),
                'id_pedido': getattr(ruta, 'id_pedido', None),
                'peso_total': getattr(ruta, 'peso_total', None),
                'algoritmo': getattr(ruta, 'algoritmo', 'desconocido'),
                'tiempo_calculo': getattr(ruta, 'tiempo_calculo', 0.0)
            }
            
            # Información del origen
            try:
                origen = getattr(ruta, 'origen', None)
                if origen and hasattr(origen, 'elemento'):
                    elemento_origen = origen.elemento
                    origen_id = (getattr(elemento_origen, 'id_cliente', None) or 
                               getattr(elemento_origen, 'id_almacenamiento', None) or 
                               getattr(elemento_origen, 'id_recarga', None))
                    origen_nombre = getattr(elemento_origen, 'nombre', f"Vertice_{origen_id}")
                    origen_tipo = "cliente" if hasattr(elemento_origen, 'id_cliente') else \
                                 "almacenamiento" if hasattr(elemento_origen, 'id_almacenamiento') else \
                                 "recarga" if hasattr(elemento_origen, 'id_recarga') else "desconocido"
                    hashmap['origen'] = {
                        'id': origen_id,
                        'nombre': origen_nombre,
                        'tipo': origen_tipo
                    }
                else:
                    hashmap['origen'] = None
            except Exception:
                hashmap['origen'] = None
            
            # Información del destino
            try:
                destino = getattr(ruta, 'destino', None)
                if destino and hasattr(destino, 'elemento'):
                    elemento_destino = destino.elemento
                    destino_id = (getattr(elemento_destino, 'id_cliente', None) or 
                                getattr(elemento_destino, 'id_almacenamiento', None) or 
                                getattr(elemento_destino, 'id_recarga', None))
                    destino_nombre = getattr(elemento_destino, 'nombre', f"Vertice_{destino_id}")
                    destino_tipo = "cliente" if hasattr(elemento_destino, 'id_cliente') else \
                                  "almacenamiento" if hasattr(elemento_destino, 'id_almacenamiento') else \
                                  "recarga" if hasattr(elemento_destino, 'id_recarga') else "desconocido"
                    hashmap['destino'] = {
                        'id': destino_id,
                        'nombre': destino_nombre,
                        'tipo': destino_tipo
                    }
                else:
                    hashmap['destino'] = None
            except Exception:
                hashmap['destino'] = None
            
            # Información del camino
            try:
                camino = getattr(ruta, 'camino', [])
                hashmap['camino'] = []
                for i, arista in enumerate(camino):
                    arista_info = {
                        'indice': i,
                        'peso': getattr(arista, 'peso', None),
                        'origen_id': None,
                        'destino_id': None
                    }
                    # Origen de la arista
                    if hasattr(arista, 'origen') and hasattr(arista.origen, 'elemento'):
                        elem_ori = arista.origen.elemento
                        arista_info['origen_id'] = (getattr(elem_ori, 'id_cliente', None) or 
                                                   getattr(elem_ori, 'id_almacenamiento', None) or 
                                                   getattr(elem_ori, 'id_recarga', None))
                    # Destino de la arista
                    if hasattr(arista, 'destino') and hasattr(arista.destino, 'elemento'):
                        elem_dst = arista.destino.elemento
                        arista_info['destino_id'] = (getattr(elem_dst, 'id_cliente', None) or 
                                                    getattr(elem_dst, 'id_almacenamiento', None) or 
                                                    getattr(elem_dst, 'id_recarga', None))
                    hashmap['camino'].append(arista_info)
            except Exception:
                hashmap['camino'] = []
            
            return hashmap
        except Exception as e:
            return {'error': f'Error mapeando ruta: {str(e)}', 'tipo_ruta': type(ruta).__name__}

"""
Clase HashMap para acceso rápido a clientes y órdenes.
Basado en Docs/TDA-Map.py
"""

class HashMap:
    """
    Implementación de un mapa hash para acceso O(1) a clientes y pedidos.
    Garantiza referencias únicas, no re-instancia claves/valores.
    """
    def __init__(self):
        self._datos = {}

    def insertar(self, clave, valor):
        """
        Inserta un elemento en el HashMap. Si la clave existe, sobreescribe la referencia.
        """
        self._datos[clave] = valor

    def buscar(self, clave):
        """
        Busca un elemento en el HashMap. Retorna el valor o None si no existe.
        """
        return self._datos.get(clave, None)

    def eliminar(self, clave):
        """
        Elimina un elemento del HashMap. No lanza excepción si la clave no existe.
        """
        if clave in self._datos:
            del self._datos[clave]

    def __getitem__(self, clave):
        if clave not in self._datos:
            raise KeyError(f"Clave {clave} no encontrada en HashMap")
        return self._datos[clave]

    def __setitem__(self, clave, valor):
        self._datos[clave] = valor

    def __delitem__(self, clave):
        if clave in self._datos:
            del self._datos[clave]

    def __len__(self):
        return len(self._datos)

    def __iter__(self):
        return iter(self._datos)

    def __contains__(self, clave):
        return clave in self._datos

    def obtener(self, clave, defecto=None):
        return self._datos.get(clave, defecto)

    def establecer_defecto(self, clave, defecto=None):
        return self._datos.setdefault(clave, defecto)

    def extraer(self, clave, defecto=None):
        return self._datos.pop(clave, defecto)

    def extraer_item(self):
        return self._datos.popitem()

    def limpiar(self):
        self._datos.clear()

    def claves(self):
        return self._datos.keys()

    def valores(self):
        return self._datos.values()

    def items(self):
        return self._datos.items()

    def actualizar(self, otro):
        self._datos.update(otro)

    def __eq__(self, otro):
        if not isinstance(otro, HashMap):
            return False
        return self._datos == otro._datos

    def __ne__(self, otro):
        return not self.__eq__(otro)

    def __str__(self):
        return str(self._datos)

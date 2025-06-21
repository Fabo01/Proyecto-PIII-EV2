"""
Clase HashMap para acceso rápido a clientes y órdenes.
Basado en Docs/TDA-Map.py
"""

class HashMap:
    """
    Implementación de un mapa hash para acceso O(1) a clientes y pedidos.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    def __init__(self):
        self._mapa = dict()
        self._observadores = set()
        self.notificar_observadores('hashmap_creado', None)

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def insertar(self, clave, valor):
        self._mapa[clave] = valor
        self.notificar_observadores('hashmap_insertar', {'clave': clave, 'valor': valor})

    def buscar(self, clave):
        """
        Busca un elemento en el HashMap. Retorna el valor o None si no existe.
        """
        resultado = self._mapa.get(clave)
        self.notificar_observadores('hashmap_buscar', {'clave': clave, 'resultado': resultado})
        return resultado

    def eliminar(self, clave):
        """
        Elimina un elemento del HashMap. No lanza excepción si la clave no existe.
        """
        if clave in self._mapa:
            valor = self._mapa.pop(clave)
            self.notificar_observadores('hashmap_eliminar', {'clave': clave, 'valor': valor})
        else:
            self.notificar_observadores('hashmap_eliminar_inexistente', {'clave': clave})

    def limpiar(self):
        self._mapa.clear()
        self.notificar_observadores('hashmap_limpiado', None)

    def items(self):
        self.notificar_observadores('hashmap_items', None)
        return self._mapa.items()

    def valores(self):
        """
        Retorna los valores almacenados en el HashMap.
        """
        self.notificar_observadores('hashmap_valores', None)
        return self._mapa.values()

    def serializar(self):
        self.notificar_observadores('hashmap_serializado', None)
        return dict(self._mapa)

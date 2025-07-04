"""
Clase Recarga para representar una estacion de recarga en la simulacion logistica de drones.
Incluye soporte para observadores de eventos de dominio.
"""

class Recarga:
    """
    Representa una estacion de recarga en la red de drones.
    Permite agregar observadores para auditar eventos de negocio.
    """
    def __init__(self, id_recarga, nombre):
        """
        Inicializa una estacion de recarga con su identificador y nombre.
        """
        self.id_recarga = id_recarga
        self.nombre = nombre
        self.tipo_elemento = 'recarga'
        self._observadores = set()
        self.notificar_observadores('recarga_creada', {'id_recarga': id_recarga, 'nombre': nombre})

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def serializar(self):
        """
        Serializa la recarga como dict plano.
        """
        return {
            'id': self.id_recarga,
            'tipo': self.tipo_elemento,
            'nombre': self.nombre
        }

    def __str__(self):
        return f"Recarga {self.id_recarga}: {self.nombre}"

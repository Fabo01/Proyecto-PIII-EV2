"""
Implementación base de Sujeto Observable para el patrón observer.
"""
from Backend.Dominio.Interfaces.IntObs.ISujeto import ISujeto

class SujetoObservable(ISujeto):
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def quitar_observador(self, observador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, evento, datos=None):
        for observador in self._observadores:
            observador.actualizar(evento, datos)

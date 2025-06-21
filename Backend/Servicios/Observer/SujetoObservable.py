"""
Implementacion base de Sujeto Observable para el patron observer.
"""
from Backend.Dominio.Interfaces.IntObs.ISujeto import ISujeto

class SujetoObservable(ISujeto):
    def __init__(self):
        """
        Inicializa la lista de observadores.
        """
        self._observadores = []

    def agregar_observador(self, observador):
        """
        Agrega un observador si no esta ya registrado.
        """
        if observador not in self._observadores:
            self._observadores.append(observador)

    def quitar_observador(self, observador):
        """
        Quita un observador si esta registrado.
        """
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores registrados sobre un evento.
        """
        for observador in self._observadores:
            observador.actualizar(evento, datos)

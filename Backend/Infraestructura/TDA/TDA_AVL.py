"""
Clase AVL para almacenar rutas más frecuentes.
Implementación de un árbol AVL para registrar rutas y su frecuencia.
"""

class NodoAVL:
    def __init__(self, clave, valor=None):
        # Aseguro que la clave sea un hashable simple (por ejemplo, int o str)
        if isinstance(clave, tuple) and len(clave) == 1:
            clave = clave[0]
        self.clave = clave
        self.valor = valor if valor is not None else 1  # Frecuencia
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    """
    Árbol AVL para registrar rutas y su frecuencia de uso.
    """
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, valor=None):
        # Aseguro que la clave sea simple antes de insertar
        if isinstance(clave, tuple) and len(clave) == 1:
            clave = clave[0]
        self.raiz = self._insertar(self.raiz, clave, valor)

    def _insertar(self, nodo, clave, valor=None):
        if not nodo:
            return NodoAVL(clave, valor)
        if clave == nodo.clave:
            if valor is not None:
                nodo.valor = valor
            else:
                nodo.valor += 1
            return nodo
        elif clave < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, clave, valor)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, valor)
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo)

    def buscar(self, clave):
        # Aseguro que la clave sea simple antes de buscar
        if isinstance(clave, tuple) and len(clave) == 1:
            clave = clave[0]
        nodo = self.raiz
        while nodo:
            if clave == nodo.clave:
                return nodo.valor
            elif clave < nodo.clave:
                nodo = nodo.izquierda
            else:
                nodo = nodo.derecha
        return None

    def eliminar(self, clave):
        """
        Elimina una clave del árbol AVL.
        """
        self.raiz = self._eliminar(self.raiz, clave)

    def _eliminar(self, nodo, clave):
        if not nodo:
            return None
        if clave < nodo.clave:
            nodo.izquierda = self._eliminar(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha = self._eliminar(nodo.derecha, clave)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda
            temp = self._minimo(nodo.derecha)
            nodo.clave = temp.clave
            nodo.valor = temp.valor
            nodo.derecha = self._eliminar(nodo.derecha, temp.clave)
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo)

    def _minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _factor_balance(self, nodo):
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha) if nodo else 0

    def _rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        x.altura = 1 + max(self._altura(x.izquierda), self._altura(x.derecha))
        return x

    def _rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        x.altura = 1 + max(self._altura(x.izquierda), self._altura(x.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        return y

    def _balancear(self, nodo):
        balance = self._factor_balance(nodo)
        if balance > 1:
            if self._factor_balance(nodo.izquierda) < 0:
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1:
            if self._factor_balance(nodo.derecha) > 0:
                nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)
        return nodo

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izquierda, resultado)
            resultado.append((nodo.clave, nodo.valor))
            self._inorden(nodo.derecha, resultado)

    def obtener_frecuencia(self, clave):
        nodo = self.raiz
        while nodo:
            if clave == nodo.clave:
                return nodo.valor
            elif clave < nodo.clave:
                nodo = nodo.izquierda
            else:
                nodo = nodo.derecha
        return 0

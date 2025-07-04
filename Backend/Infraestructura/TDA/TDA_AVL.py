"""
Clase AVL para almacenar rutas más frecuentes.
Implementación de un árbol AVL para registrar rutas y su frecuencia.
"""

class verticeAVL:
    def __init__(self, clave, valor=None, ruta=None):
        # Aseguro que la clave sea un hashable simple (por ejemplo, int o str)
        if isinstance(clave, tuple) and len(clave) == 1:
            clave = clave[0]
        self.clave = clave
        self.valor = valor if valor is not None else 1  # Frecuencia
        self.ruta = ruta  # Objeto ruta completo para metadatos
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    """
    Árbol AVL para registrar rutas y su frecuencia de uso.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    def __init__(self):
        self.raiz = None
        self._observadores = set()
        self.notificar_observadores('avl_creado', None)

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def insertar(self, clave, valor=None, ruta=None):
        # Aseguro que la clave sea simple antes de insertar
        if isinstance(clave, tuple) and len(clave) == 1:
            clave = clave[0]
        self.raiz = self._insertar(self.raiz, clave, valor, ruta)
        self.notificar_observadores('avl_insertar', {'clave': clave, 'valor': valor, 'ruta': ruta})

    def _insertar(self, vertice, clave, valor=None, ruta=None):
        if not vertice:
            return verticeAVL(clave, valor, ruta)
        if clave == vertice.clave:
            vertice.valor += 1 if valor is None else valor
            # Actualizar la ruta si se proporciona una nueva
            if ruta is not None:
                vertice.ruta = ruta
            return vertice
        elif clave < vertice.clave:
            vertice.izquierda = self._insertar(vertice.izquierda, clave, valor, ruta)
        else:
            vertice.derecha = self._insertar(vertice.derecha, clave, valor, ruta)
        vertice.altura = 1 + max(self._altura(vertice.izquierda), self._altura(vertice.derecha))
        return self._balancear(vertice)

    def eliminar(self, clave):
        self.raiz = self._eliminar(self.raiz, clave)
        self.notificar_observadores('avl_eliminar', {'clave': clave})

    def _eliminar(self, vertice, clave):
        if not vertice:
            return None
        if clave < vertice.clave:
            vertice.izquierda = self._eliminar(vertice.izquierda, clave)
        elif clave > vertice.clave:
            vertice.derecha = self._eliminar(vertice.derecha, clave)
        else:
            if not vertice.izquierda:
                return vertice.derecha
            elif not vertice.derecha:
                return vertice.izquierda
            temp = self._minimo(vertice.derecha)
            vertice.clave, vertice.valor = temp.clave, temp.valor
            vertice.derecha = self._eliminar(vertice.derecha, temp.clave)
        vertice.altura = 1 + max(self._altura(vertice.izquierda), self._altura(vertice.derecha))
        return self._balancear(vertice)

    def buscar(self, clave):
        resultado = self._buscar(self.raiz, clave)
        self.notificar_observadores('avl_buscar', {'clave': clave, 'resultado': resultado})
        return resultado

    def _buscar(self, vertice, clave):
        if not vertice:
            return None
        if clave == vertice.clave:
            return vertice
        elif clave < vertice.clave:
            return self._buscar(vertice.izquierda, clave)
        else:
            return self._buscar(vertice.derecha, clave)

    def _minimo(self, vertice):
        while vertice.izquierda:
            vertice = vertice.izquierda
        return vertice

    def _altura(self, vertice):
        return vertice.altura if vertice else 0

    def _factor_balance(self, vertice):
        return self._altura(vertice.izquierda) - self._altura(vertice.derecha) if vertice else 0

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

    def _balancear(self, vertice):
        balance = self._factor_balance(vertice)
        if balance > 1:
            if self._factor_balance(vertice.izquierda) < 0:
                vertice.izquierda = self._rotar_izquierda(vertice.izquierda)
            return self._rotar_derecha(vertice)
        if balance < -1:
            if self._factor_balance(vertice.derecha) > 0:
                vertice.derecha = self._rotar_derecha(vertice.derecha)
            return self._rotar_izquierda(vertice)
        return vertice

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, vertice, resultado):
        if vertice:
            self._inorden(vertice.izquierda, resultado)
            resultado.append((vertice.clave, vertice.valor))
            self._inorden(vertice.derecha, resultado)

    def obtener_frecuencia(self, clave):
        vertice = self.buscar(clave)
        return vertice.valor if vertice else 0

    def serializar(self):
        self.notificar_observadores('avl_serializado', None)
        return self._serializar_vertice(self.raiz)

    def _serializar_vertice(self, vertice):
        if not vertice:
            return None
        return {
            'clave': vertice.clave,
            'valor': vertice.valor,
            'ruta_id': getattr(vertice.ruta, 'id_ruta', None) if vertice.ruta else None,
            'izq': self._serializar_vertice(vertice.izquierda),
            'der': self._serializar_vertice(vertice.derecha)
        }

    def obtener_rutas(self):
        """
        Obtiene todas las rutas almacenadas en el AVL.
        Retorna lista de objetos Ruta.
        """
        rutas = []
        self._obtener_rutas_inorden(self.raiz, rutas)
        return rutas

    def _obtener_rutas_inorden(self, vertice, rutas):
        """
        Recorre el AVL en orden y recolecta las rutas.
        """
        if vertice:
            self._obtener_rutas_inorden(vertice.izquierda, rutas)
            if vertice.ruta:
                rutas.append(vertice.ruta)
            self._obtener_rutas_inorden(vertice.derecha, rutas)

    def obtener_rutas_mas_frecuentes(self, limite=10):
        """
        Obtiene las rutas más frecuentes del AVL.
        Retorna lista de tuplas (ruta, frecuencia) ordenadas por frecuencia descendente.
        """
        rutas_con_frecuencia = []
        self._obtener_rutas_con_frecuencia(self.raiz, rutas_con_frecuencia)
        # Ordenar por frecuencia descendente
        rutas_con_frecuencia.sort(key=lambda x: x[1], reverse=True)
        return rutas_con_frecuencia[:limite]

    def _obtener_rutas_con_frecuencia(self, vertice, resultado):
        """
        Recorre el AVL y recolecta rutas con su frecuencia.
        """
        if vertice:
            self._obtener_rutas_con_frecuencia(vertice.izquierda, resultado)
            if vertice.ruta:
                resultado.append((vertice.ruta, vertice.valor))
            self._obtener_rutas_con_frecuencia(vertice.derecha, resultado)

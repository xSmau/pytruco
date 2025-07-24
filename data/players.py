class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def robar_carta(self, carta):
        self.mano.append(carta)

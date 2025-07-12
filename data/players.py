class jugadores:
    def __init__(self, ID: int):
        self.id = ID
        self.mano = list()
    
    def recibirCarta(self, carta):
        self.mano.append(carta)
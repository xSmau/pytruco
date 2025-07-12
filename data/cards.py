class cartas:
    def __init__(self, palo: str, val: str, puntos: int):
        self.pinta = palo
        self.valor = int(val)
        self.puntos = puntos
        self.id = f"{palo}{val}"
        self.skin = f'pytruco\\textures\\{self.id}.png'
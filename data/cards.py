class Carta:
    def __init__(self, palo: str, val: str, puntos: int):
        self.pinta = palo
        self.valor = int(val)
        self.puntos = puntos
        inicial_palo = {"copa": "C", "espada": "E", "basto": "B", "oro": "O"}[palo.lower()]
        self.id = f"{inicial_palo}{val}"
        self.skin = f'textures/pytrucofondobackcarta/{self.id}.png'

    @staticmethod
    def generar_mazo():
        palos = ["espada", "basto", "oro", "copa"]
        valores = {
            "1": 14,
            "2": 9,
            "3": 10,
            "4": 1,
            "5": 2,
            "6": 3,
            "7": 12,
            "10": 4,
            "11": 5,
            "12": 6
        }

        mazo = []
        for palo in palos:
            for val, pts in valores.items():
                carta = Carta(palo, val, pts)
                mazo.append(carta)
        return mazo

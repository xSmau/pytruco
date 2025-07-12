from data.cards import cartas
from data.players import jugadores
import random

IDs = [
        ["M1", 8], ["M2", 9], ["M3", 10], ["M4", 1], ["M5", 2], ["M6", 3], ["M7", 11], ["M10", 5], ["M11", 6], ["M12", 7],
        ["E1", 14], ["E2", 9], ["E3", 10], ["E4", 1], ["E5", 2], ["E6", 3], ["E7", 12], ["E10", 5], ["E11", 6], ["E12", 7],
        ["C1", 8], ["C2", 9], ["C3", 10], ["C4", 1], ["C5", 2], ["C6", 3], ["C7", 4], ["C10", 5], ["C11", 6], ["C12", 7],
        ["B1", 13], ["B2", 9], ["B3", 10], ["B4", 1], ["B5", 2], ["B6", 3], ["B7", 4], ["B10", 5], ["B11", 6], ["B12", 7]
       ]

random.shuffle(IDs)
mazo = list()

jugador1 = jugadores(1)
jugador2 = jugadores(2)

for carta in IDs:
    if len(carta) < 3:
        cartaSeleccionada = cartas(palo=carta[0][0], val=carta[0][1], puntos=carta[1])
    else:
        cartaSeleccionada = cartas(palo=carta[0][0], val=carta[0][1:3], puntos=carta[1])

    mazo.append(cartaSeleccionada)


def repartir():
    global vira
    for turno in range(3):
        jugador1.recibirCarta(mazo.pop(0))
        jugador2.recibirCarta(mazo.pop(0))
    vira = mazo.pop(0)

repartir()

print(f"Vira: {vira.pinta}, {vira.skin}")

print(f"Cartas jugador 1: ")
for carta in jugador1.mano:
    print(str(carta.skin))
#print(f"Cartas jugador 2: {jugador2.mano}")

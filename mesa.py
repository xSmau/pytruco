import pygame
import random
from data.cards import Carta
from data.players import Jugador
from network import Network

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Truco Venezolano")

fondo = pygame.image.load("textures/pytrucofondobackcarta/Bfondomesa.png")
fondo = pygame.transform.scale(fondo, (screen_width, screen_height))

reloj = pygame.time.Clock()

# Colores y fuentes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
font = pygame.font.Font(None, 36)

# Estados del juego
jugador1 = Jugador("Jugador")
jugador2 = Jugador("PC")
turno_jugador = True
ronda_en_curso = True
cartas_en_mesa = []
historial_cartas = []
manos_jugador = 0
manos_pc = 0
puntos_jugador = 0
puntos_pc = 0

# Truco Venezolano y Envido
envido_en_juego = False
truco_en_juego = False
nivel_truco = 0  # 0 = no cantado, 1 = Truco, 2 = Retruco, 3 = Vale Nueve, 4 = Vale Juego
niveles_truco = ["", "Truco", "Retruco", "Vale Nueve", "Vale Juego"]
puntos_truco = [0, 1, 2, 3, 4]  # Puntos que otorga cada nivel
puntos_envido = 0

#Crear la conexion 
def crearConexion():
    global n
    n = Network()


# Animación de repartir
def repartir_animado():
    jugador1.mano = []
    jugador2.mano = []
    mazo = Carta.generar_mazo()
    random.shuffle(mazo)
    for i in range(3):
        animar_carta("jugador", i)
        jugador1.robar_carta(mazo.pop())
        animar_carta("pc", i)
        jugador2.robar_carta(mazo.pop())

def animar_carta(destino, index):
    img_carta = pygame.image.load("textures/pytrucofondobackcarta/back.png")
    img_carta = pygame.transform.scale(img_carta, (100, 150))
    for i in range(30):
        screen.blit(fondo, (0, 0))
        mostrar_puntaje()
        mostrar_cartas()
        mostrar_cartas_en_mesa()
        x = screen_width // 2 - 50 + (i * 5 if destino == "jugador" else -i * 5)
        y = screen_height // 2 - 75 + (index * 20 if destino == "jugador" else -index * 20)
        screen.blit(img_carta, (x, y))
        pygame.display.flip()
        reloj.tick(60)

def mostrar_cartas():
    for i, carta in enumerate(jugador1.mano):
        imagen = pygame.image.load(carta.skin).convert_alpha()
        imagen = pygame.transform.scale(imagen, (100, 150))
        screen.blit(imagen, (100 + i * 120, screen_height - 180))
    for i, carta in enumerate(jugador2.mano):
        imagen = pygame.image.load("textures/pytrucofondobackcarta/back.png")
        imagen = pygame.transform.scale(imagen, (100, 150))
        screen.blit(imagen, (100 + i * 120, 30))

def mostrar_cartas_en_mesa():
    for i, carta in enumerate(cartas_en_mesa):
        x = screen_width // 2 - 120 + (i % 2) * 160
        y = screen_height // 2 - 150 + (i // 2) * 120
        imagen = pygame.image.load(carta.skin).convert_alpha()
        imagen = pygame.transform.scale(imagen, (100, 150))
        screen.blit(imagen, (x, y))

def mostrar_puntaje():
    pj = font.render(f"Jugador: {puntos_jugador} (manos: {manos_jugador})", True, BLANCO)
    pc = font.render(f"PC: {puntos_pc} (manos: {manos_pc})", True, BLANCO)
    screen.blit(pj, (10, screen_height - 40))
    screen.blit(pc, (10, 10))
    if envido_en_juego:
        screen.blit(font.render("ENVIDO", True, ROJO), (300, 10))
    if truco_en_juego:
        screen.blit(font.render(f"{niveles_truco[nivel_truco].upper()} x{puntos_truco[nivel_truco]}", True, ROJO), (300, 40))

def jugar_carta(jugador, indice):
    global turno_jugador
    carta = jugador.mano.pop(indice)
    cartas_en_mesa.append(carta)
    if len(cartas_en_mesa) == 2:
        evaluar_mano()
    turno_jugador = not turno_jugador

def evaluar_mano():
    global manos_jugador, manos_pc, cartas_en_mesa, historial_cartas
    if len(cartas_en_mesa) < 2:
        return
    c1, c2 = cartas_en_mesa[-2], cartas_en_mesa[-1]
    if c1.puntos > c2.puntos:
        manos_jugador += 1
    elif c1.puntos < c2.puntos:
        manos_pc += 1
    historial_cartas.extend(cartas_en_mesa)
    cartas_en_mesa = []

def chequear_ronda():
    global manos_jugador, manos_pc, puntos_jugador, puntos_pc, ronda_en_curso, historial_cartas, nivel_truco, truco_en_juego
    if manos_jugador >= 2:
        puntos_jugador += puntos_truco[nivel_truco]
        ronda_en_curso = False
    elif manos_pc >= 2:
        puntos_pc += puntos_truco[nivel_truco]
        ronda_en_curso = False
    if not ronda_en_curso:
        pygame.time.wait(1500)
        historial_cartas.clear()
        nivel_truco = 0
        truco_en_juego = False

def cantar_envido():
    global envido_en_juego, puntos_envido
    envido_en_juego = True
    puntos_envido = 2
    print("¡Cantaste Envido!")

def cantar_truco():
    global truco_en_juego, nivel_truco
    if nivel_truco < 4:
        nivel_truco += 1
        truco_en_juego = True
        print(f"¡Cantaste {niveles_truco[nivel_truco]}!")

def aceptar_canto():
    global envido_en_juego, truco_en_juego, puntos_jugador, puntos_pc
    if envido_en_juego:
        ganador = comparar_envido()
        if ganador == "jugador":
            puntos_jugador += puntos_envido
            print("Ganaste el Envido")
        else:
            puntos_pc += puntos_envido
            print("Perdiste el Envido")
        envido_en_juego = False
    elif truco_en_juego:
        print(f"Aceptaste el {niveles_truco[nivel_truco]}")

def rechazar_canto():
    global envido_en_juego, truco_en_juego, puntos_pc, puntos_jugador, ronda_en_curso, nivel_truco
    if envido_en_juego:
        puntos_pc += 1
        envido_en_juego = False
        print("Rechazaste el Envido")
    elif truco_en_juego:
        puntos_pc += puntos_truco[nivel_truco - 1]
        truco_en_juego = False
        ronda_en_curso = False
        print(f"Rechazaste el {niveles_truco[nivel_truco]}")
        nivel_truco = 0

def comparar_envido():
    def calcular_envido(mano):
        palos = {}
        for carta in mano:
            if carta.palo not in palos:
                palos[carta.palo] = []
            if int(carta.valor) <= 7:
                palos[carta.palo].append(int(carta.valor))
        max_puntos = 0
        for valores in palos.values():
            if len(valores) >= 2:
                puntos = 20 + sum(sorted(valores)[-2:])
                max_puntos = max(max_puntos, puntos)
            elif len(valores) == 1:
                max_puntos = max(max_puntos, valores[0])
        return max_puntos
    p_jug = calcular_envido(jugador1.mano)
    p_pc = calcular_envido(jugador2.mano)
    return "jugador" if p_jug >= p_pc else "pc"

def run_online_game():
    global turno_jugador, ronda_en_curso, manos_jugador, manos_pc, nivel_truco
    repartir_animado()
    ronda_en_curso = True
    manos_jugador = 0
    manos_pc = 0
    nivel_truco = 0
    corriendo = True

    crearConexion()

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turno_jugador and ronda_en_curso:
                x, y = pygame.mouse.get_pos()
                for i, carta in enumerate(jugador1.mano):
                    rect = pygame.Rect(100 + i * 120, screen_height - 180, 100, 150)
                    if rect.collidepoint(x, y):
                        jugar_carta(jugador1, i)
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    cantar_envido()
                elif event.key == pygame.K_t:
                    cantar_truco()
                elif event.key == pygame.K_y:
                    aceptar_canto()
                elif event.key == pygame.K_n:
                    rechazar_canto()

        screen.blit(fondo, (0, 0))
        mostrar_puntaje()
        mostrar_cartas()
        mostrar_cartas_en_mesa()

        if not turno_jugador and ronda_en_curso and jugador2.mano:
            pygame.time.wait(1000)
            jugar_carta(jugador2, 0)

        chequear_ronda()

        pygame.display.flip()
        reloj.tick(60)

def run_game():
    global turno_jugador, ronda_en_curso, manos_jugador, manos_pc, nivel_truco
    repartir_animado()
    ronda_en_curso = True
    manos_jugador = 0
    manos_pc = 0
    nivel_truco = 0
    corriendo = True

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turno_jugador and ronda_en_curso:
                x, y = pygame.mouse.get_pos()
                for i, carta in enumerate(jugador1.mano):
                    rect = pygame.Rect(100 + i * 120, screen_height - 180, 100, 150)
                    if rect.collidepoint(x, y):
                        jugar_carta(jugador1, i)
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    cantar_envido()
                elif event.key == pygame.K_t:
                    cantar_truco()
                elif event.key == pygame.K_y:
                    aceptar_canto()
                elif event.key == pygame.K_n:
                    rechazar_canto()

        screen.blit(fondo, (0, 0))
        mostrar_puntaje()
        mostrar_cartas()
        mostrar_cartas_en_mesa()

        if not turno_jugador and ronda_en_curso and jugador2.mano:
            pygame.time.wait(1000)
            jugar_carta(jugador2, 0)

        chequear_ronda()

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    run_game()

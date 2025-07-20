import pygame
import random
import time

from data.cards import cartas
from data.players import jugadores

pygame.init()  # Inicializa todos los módulos de pygame
pygame.mixer.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Truco - VS PC")

font = pygame.font.Font(None, 36)

mazo = []
cartas_en_mesa = []
puntos_jugador = 0
puntos_pc = 0
manos_jugador = 0
manos_pc = 0
ronda_en_curso = True
turno_jugador = True

# ---------- FUNCIONES DE JUEGO ----------
def barajeo():
    global mazo
    IDs = [["{}{}".format(p, v), pts] for p, valores in zip("MECB", [[1,2,3,4,5,6,7,10,11,12]]*4)
           for v, pts in zip(valores, [14 if v==1 and p=='E' else 13 if v==1 and p=='B' else 12 if v==7 and p=='E' else 11 if v==7 and p=='M' else 8 for v in valores])]
    random.shuffle(IDs)
    mazo.clear()
    for info in IDs:
        palo, val = info[0][0], info[0][1:]
        mazo.append(cartas(palo=palo, val=val, puntos=info[1]))

def iniJugadores():
    global jugador1, jugador2
    jugador1 = jugadores(1)
    jugador2 = jugadores(2)

def repartir_animado():
    repartir()
    for i in range(3):
        animar_carta("jugador", i)
        animar_carta("pc", i)

def repartir():
    global vira
    for _ in range(3):
        jugador1.recibirCarta(mazo.pop(0))
        jugador2.recibirCarta(mazo.pop(0))
    vira = mazo.pop(0)

def animar_carta(destino, idx):
    x_final = 300 + idx * 80 if destino == "jugador" else 300 + idx * 80
    y_final = 450 if destino == "jugador" else 50
    img_carta = pygame.image.load("textures/pytrucofondobackcarta/back.png")
    img_carta = pygame.transform.scale(img_carta, (100, 150))
    for i in range(30):
        t = i / 30
        x = screen_width // 2 + (x_final - screen_width // 2) * t
        y = screen_height // 2 + (y_final - screen_height // 2) * t
        screen.fill((0, 0, 0))
        screen.blit(fondo_img, fondo_rect)
        screen.blit(img_carta, (x, y))
        pygame.display.flip()
        pygame.time.delay(10)

def mostrar_mano_estatica():
    # Cartas del jugador abajo
    for i, carta in enumerate(jugador1.mano):
        imagen = pygame.image.load(carta.skin).convert_alpha()
        imagen = pygame.transform.scale(imagen, (100, 150))
        x = 300 + i * 80
        y = 450
        screen.blit(imagen, (x, y))
    # Cartas de la PC arriba (mostrando reverso)
    for i, carta in enumerate(jugador2.mano):
        imagen = pygame.image.load("textures/pytrucofondobackcarta/back.png")
        imagen = pygame.transform.scale(imagen, (100, 150))
        x = 300 + i * 80
        y = 50
        screen.blit(imagen, (x, y))

def mostrar_cartas_en_mesa():
    posiciones = {
        "jugador": (screen_width // 2 - 40, screen_height // 2 + 50),
        "pc": (screen_width // 2 - 40, screen_height // 2 - 150)
    }
    if len(cartas_en_mesa) >= 1:
        carta_j = cartas_en_mesa[-2] if len(cartas_en_mesa) == 2 else cartas_en_mesa[-1]
        imagen_j = pygame.image.load(carta_j.skin).convert_alpha()
        imagen_j = pygame.transform.scale(imagen_j, (100, 150))
        screen.blit(imagen_j, posiciones["jugador"])
    if len(cartas_en_mesa) == 2:
        carta_pc = cartas_en_mesa[-1]
        imagen_pc = pygame.image.load(carta_pc.skin).convert_alpha()
        imagen_pc = pygame.transform.scale(imagen_pc, (100, 150))
        screen.blit(imagen_pc, posiciones["pc"])

def elegir_carta_pc():
    return max(jugador2.mano, key=lambda c: c.puntos)

def animar_colocacion(carta, destino):
    x_inicial = 300 if destino == "jugador" else 300
    y_inicial = 450 if destino == "jugador" else 50
    x_final = screen_width // 2
    y_final = screen_height // 2
    imagen = pygame.image.load(carta.skin).convert_alpha()
    imagen = pygame.transform.scale(imagen, (70, 100))
    for i in range(20):
        t = i / 20
        x = x_inicial + (x_final - x_inicial) * t
        y = y_inicial + (y_final - y_inicial) * t
        screen.blit(fondo_img, fondo_rect)
        screen.blit(imagen, (x, y))
        pygame.display.flip()
        pygame.time.delay(15)

def evaluar_mano():
    global manos_jugador, manos_pc, cartas_en_mesa
    if len(cartas_en_mesa) < 2:
        return
    c1, c2 = cartas_en_mesa[-2], cartas_en_mesa[-1]
    if c1.puntos > c2.puntos:
        manos_jugador += 1
    elif c1.puntos < c2.puntos:
        manos_pc += 1
    cartas_en_mesa = []

def chequear_ronda():
    global puntos_jugador, puntos_pc, manos_jugador, manos_pc, ronda_en_curso
    if manos_jugador >= 2:
        puntos_jugador += 1
        mostrar_mensaje("¡Ganaste la ronda!")
        manos_jugador = manos_pc = 0
        ronda_en_curso = False
    elif manos_pc >= 2:
        puntos_pc += 1
        mostrar_mensaje("La PC ganó la ronda")
        manos_jugador = manos_pc = 0
        ronda_en_curso = False

def mostrar_mensaje(texto):
    mensaje = font.render(texto, True, (255, 255, 255))
    rect = mensaje.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(mensaje, rect)
    pygame.display.flip()
    pygame.time.delay(1500)

def mostrar_puntaje():
    pj = font.render(f"Jugador: {puntos_jugador}", True, (255, 255, 255))
    pc = font.render(f"PC: {puntos_pc}", True, (255, 255, 255))
    screen.blit(pj, (10, 10))
    screen.blit(pc, (10, 40))

# ---------- LOOP PRINCIPAL ----------
def run_game():
    global ronda_en_curso, turno_jugador
    clock = pygame.time.Clock()

    global fondo_img, fondo_rect
    fondo_img = pygame.image.load("textures/pytrucofondobackcarta/Bfondomesa.png")
    fondo_rect = fondo_img.get_rect()

    barajeo()
    iniJugadores()
    repartir_animado()

    imagen_virada = pygame.image.load(vira.skin).convert_alpha()
    imagen_virada = pygame.transform.scale(imagen_virada, (100, 150))
    rect_virada = imagen_virada.get_rect(center=(700, 200))

    carta_pc_pendiente = None
    delay_pc = 30
    pc_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and turno_jugador and ronda_en_curso:
                mouse_x, mouse_y = event.pos
                for carta in jugador1.mano:
                    imagen = pygame.image.load(carta.skin).convert_alpha()
                    imagen = pygame.transform.scale(imagen, (100, 150))
                    rect = imagen.get_rect(center=(300 + jugador1.mano.index(carta)*80, 450))
                    if rect.collidepoint(mouse_x, mouse_y):
                        jugador1.mano.remove(carta)
                        animar_colocacion(carta, "jugador")
                        cartas_en_mesa.append(carta)
                        turno_jugador = False
                        carta_pc_pendiente = elegir_carta_pc()
                        pc_timer = delay_pc
                        break

        if not turno_jugador and carta_pc_pendiente and ronda_en_curso:
            pc_timer -= 1
            if pc_timer <= 0:
                jugador2.mano.remove(carta_pc_pendiente)
                animar_colocacion(carta_pc_pendiente, "pc")
                cartas_en_mesa.append(carta_pc_pendiente)
                carta_pc_pendiente = None
                turno_jugador = True
                evaluar_mano()
                chequear_ronda()

        if not ronda_en_curso:
            pygame.time.delay(1000)
            barajeo()
            iniJugadores()
            repartir_animado()
            ronda_en_curso = True
            turno_jugador = True

        screen.blit(fondo_img, fondo_rect)
        screen.blit(imagen_virada, rect_virada)
        mostrar_mano_estatica()
        mostrar_cartas_en_mesa()
        mostrar_puntaje()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    run_game()

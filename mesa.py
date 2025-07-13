import pygame

from data.cards import cartas
from data.players import jugadores
import random

def barajeo():
    global mazo
    IDs = [
            ["M1", 8], ["M2", 9], ["M3", 10], ["M4", 1], ["M5", 2], ["M6", 3], ["M7", 11], ["M10", 5], ["M11", 6], ["M12", 7],
            ["E1", 14], ["E2", 9], ["E3", 10], ["E4", 1], ["E5", 2], ["E6", 3], ["E7", 12], ["E10", 5], ["E11", 6], ["E12", 7],
            ["C1", 8], ["C2", 9], ["C3", 10], ["C4", 1], ["C5", 2], ["C6", 3], ["C7", 4], ["C10", 5], ["C11", 6], ["C12", 7],
            ["B1", 13], ["B2", 9], ["B3", 10], ["B4", 1], ["B5", 2], ["B6", 3], ["B7", 4], ["B10", 5], ["B11", 6], ["B12", 7]
        ]

    random.shuffle(IDs)
    mazo = list()


    for carta in IDs:
        if len(carta) < 3:
            cartaSeleccionada = cartas(palo=carta[0][0], val=carta[0][1], puntos=carta[1])
        else:
            cartaSeleccionada = cartas(palo=carta[0][0], val=carta[0][1:3], puntos=carta[1])

        mazo.append(cartaSeleccionada)

def iniJugadores():
    global jugador1, jugador2
    jugador1 = jugadores(1)
    jugador2 = jugadores(2)

def repartir():
    global vira, turno
  
    for turno in range(3):
        jugador1.recibirCarta(mazo.pop(0))
        jugador2.recibirCarta(mazo.pop(0))
    vira = mazo.pop(0)


#print(f"Cartas jugador 2: {jugador2.mano}")


def run_game():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Troco")

    running = True
    clock = pygame.time.Clock()

    barajeo()
    iniJugadores()
    repartir()

    # mano = []
    cartasImg = []
    image_rect=[]
    aumentada= []
    auRect=[]
    move = []
    x=250
    # angle = 0
    for carta in range(len(jugador1.mano)):
        # print(angle)
        # angle +=60
        move.append(False)
        cartasImg.append(pygame.image.load(jugador1.mano[carta].skin))
        cartasImg[carta] = pygame.transform.scale(cartasImg[carta], (100, 150))
        image_rect.append(cartasImg[carta].get_rect())

        x += 80
        image_rect[carta].centerx = x 
        image_rect[carta].centery = 450

        # cartasImg[carta] = pygame.transform.rotate(cartasImg[carta], angle)

        aumento = 1.5 
        aumentada.append(pygame.transform.scale(cartasImg[carta], (int(cartasImg[carta].get_width() * aumento),
                                                          int(cartasImg[carta].get_height() * aumento))))
        auRect.append(aumentada[carta].get_rect())
        auRect[carta].centerx = x 
        auRect[carta].centery = 450
        # aumentada[carta]=pygame.transform.rotate(aumentada[carta], angle)


    virada = pygame.image.load(vira.skin)
    # virada = pygame.image.load("textures\B1.png")

    virada = pygame.transform.scale(virada, (100, 150))
    v = virada.get_rect()
    v.centerx = 700
    v.centery = 200
    


   
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Allow exiting game with ESC
                    running = False
        screen.fill((0, 0, 0))


        mouse_pos = pygame.mouse.get_pos()
                
                

        screen.blit(virada, v)
        for carta in range(len(cartasImg)):
            if image_rect[carta].collidepoint(mouse_pos):
                screen.blit(aumentada[carta], auRect[carta])

            else:
                screen.blit(cartasImg[carta],image_rect[carta])
                # if event.type == pygame.MOUSEBUTTONDOWN 
                #     if image_rect[carta].collidepoint(event.pos):
                #         


        pygame.display.flip()
        clock.tick(60)
    pygame.quit()






        
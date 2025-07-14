import pygame
import random

from data.cards import cartas
from data.players import jugadores

pygame.mixer.init()

def barajeo():
    global mazo
    IDs = [
        ["M1", 8], ["M2", 9], ["M3", 10], ["M4", 1], ["M5", 2], ["M6", 3], ["M7", 11], ["M10", 5], ["M11", 6], ["M12", 7],
        ["E1", 14], ["E2", 9], ["E3", 10], ["E4", 1], ["E5", 2], ["E6", 3], ["E7", 12], ["E10", 5], ["E11", 6], ["E12", 7],
        ["C1", 8], ["C2", 9], ["C3", 10], ["C4", 1], ["C5", 2], ["C6", 3], ["C7", 4], ["C10", 5], ["C11", 6], ["C12", 7],
        ["B1", 13], ["B2", 9], ["B3", 10], ["B4", 1], ["B5", 2], ["B6", 3], ["B7", 4], ["B10", 5], ["B11", 6], ["B12", 7]
    ]
    random.shuffle(IDs)
    mazo = []

    for info_id_carta in IDs:
        if len(info_id_carta[0]) < 3:
            palo_cadena = info_id_carta[0][0]
            valor_cadena = info_id_carta[0][1:]
            cartaSeleccionada = cartas(palo=palo_cadena, val=valor_cadena, puntos=info_id_carta[1])
        else:
            palo_cadena = info_id_carta[0][0]
            valor_cadena = info_id_carta[0][1:]
            cartaSeleccionada = cartas(palo=palo_cadena, val=valor_cadena, puntos=info_id_carta[1])

        mazo.append(cartaSeleccionada)

def iniJugadores():
    global jugador1, jugador2
    jugador1 = jugadores(1)
    jugador2 = jugadores(2)

def repartir():
    global vira
 
    for _ in range(3):
        jugador1.recibirCarta(mazo.pop(0))
        jugador2.recibirCarta(mazo.pop(0))
    vira = mazo.pop(0)

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

    cartasImg = []
    image_rect = []
    aumentada = []
    auRect = []
    
    cartas_en_mesa = [] 

    posicion_inicial_mano_x = 300
    espacio_entre_cartas = 80

    fondo_img = pygame.image.load("textures\pytrucofondobackcarta\Bfondomesa.png")
    fondo_rect = fondo_img.get_rect()

    for carta_obj_in_hand in jugador1.mano:
        imagen_carta_actual = pygame.image.load(carta_obj_in_hand.skin).convert_alpha()
        imagen_carta_actual = pygame.transform.scale(imagen_carta_actual, (100, 150))
        cartasImg.append(imagen_carta_actual)

        rect_carta_actual = imagen_carta_actual.get_rect()
        rect_carta_actual.centerx = posicion_inicial_mano_x
        rect_carta_actual.centery = 450
        image_rect.append(rect_carta_actual)

        factor_aumento = 1.5 
        imagen_carta_aumentada = pygame.transform.scale(imagen_carta_actual, (int(imagen_carta_actual.get_width() * factor_aumento),
                                                                            int(imagen_carta_actual.get_height() * factor_aumento)))
        aumentada.append(imagen_carta_aumentada)
        
        rect_carta_aumentada = imagen_carta_aumentada.get_rect(center=rect_carta_actual.center)
        auRect.append(rect_carta_aumentada)

        posicion_inicial_mano_x += espacio_entre_cartas

    imagen_virada = pygame.image.load(vira.skin).convert_alpha()
    imagen_virada = pygame.transform.scale(imagen_virada, (100, 150))
    rect_virada = imagen_virada.get_rect(center=(700, 200))

    try:
        sond = pygame.mixer.Sound("sounds/card1.ogg")
        lanz = pygame.mixer.Sound("sounds\cardSlide2.ogg")
        sond.set_volume(0.6) 
        lanz.set_volume(1)
    except pygame.error as e:
        print(f"Error al cargar el sonido: {e}")
        pygame.quit()
        exit()

    sonido_reproducido_sel = [False] * len(cartasImg) 
    sonido_reproducido_lan = [False] * len(cartasImg) 

    while running:

        indice_carta_a_eliminar = -1 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                for idx, objeto_carta_en_mano in enumerate(jugador1.mano):
                    if image_rect[idx].collidepoint(mouse_x, mouse_y):
                        print(f"¡Clic en la carta {objeto_carta_en_mano.valor}{objeto_carta_en_mano.pinta}! Eliminando...")
                        indice_carta_a_eliminar = idx
                        lanz.play() 
                         
                        break 

        if indice_carta_a_eliminar != -1:
            objeto_carta_lanzada = jugador1.mano[indice_carta_a_eliminar]
            
            cartas_en_mesa.append(objeto_carta_lanzada) 
            print(f"Carta '{objeto_carta_lanzada.valor}{objeto_carta_lanzada.pinta}' lanzada a la mesa. Total en mesa: {len(cartas_en_mesa)}")

            jugador1.mano.pop(indice_carta_a_eliminar)
            
            cartasImg.pop(indice_carta_a_eliminar)
            image_rect.pop(indice_carta_a_eliminar)
            aumentada.pop(indice_carta_a_eliminar)
            auRect.pop(indice_carta_a_eliminar)
            sonido_reproducido_sel.pop(indice_carta_a_eliminar)

            current_x_reposition = 250 
            for i in range(len(image_rect)):
                image_rect[i].centerx = current_x_reposition
                auRect[i].centerx = current_x_reposition
                current_x_reposition += espacio_entre_cartas
            
        screen.fill((0, 0, 0))
        screen.blit(fondo_img,fondo_rect)

        screen.blit(imagen_virada, rect_virada)

        for carta_idx in range(len(cartasImg)):
            mouse_pos = pygame.mouse.get_pos() 

            mouse_sobre_carta = image_rect[carta_idx].collidepoint(mouse_pos)

            if mouse_sobre_carta:
                screen.blit(aumentada[carta_idx], auRect[carta_idx])
                if not sonido_reproducido_sel[carta_idx]:
                    sond.play() 
                    sonido_reproducido_sel[carta_idx] = True
                
            else:
                screen.blit(cartasImg[carta_idx], image_rect[carta_idx])
                sonido_reproducido_sel[carta_idx] = False
                

                
        # --- Modificaciones para dibujar las cartas en la mesa centradas ---
        ancho_carta_mesa = 70
        alto_carta_mesa = 100
        espacio_entre_cartas_mesa = 10 # Espacio adicional entre cartas en la mesa

        # Calcular el ancho total que ocuparán todas las cartas en la mesa
        total_ancho_cartas_mesa = len(cartas_en_mesa) * ancho_carta_mesa + \
                                 (len(cartas_en_mesa) - 1) * espacio_entre_cartas_mesa

        # Calcular la posición X de inicio para centrar el grupo
        posicion_mesa_x_inicio = (screen_width / 2) - (total_ancho_cartas_mesa / 2)
        posicion_mesa_y = screen_height / 2 - alto_carta_mesa / 2 # Centrar verticalmente

        cur_x_mesa = posicion_mesa_x_inicio
        for objeto_carta_lanzada in cartas_en_mesa:
            try:
                
                imagen_mesa = pygame.image.load(objeto_carta_lanzada.skin).convert_alpha()
                imagen_mesa = pygame.transform.scale(imagen_mesa, (ancho_carta_mesa, alto_carta_mesa))
                
                # Dibujar cada carta usando la posición calculada
                rect_mesa = imagen_mesa.get_rect(topleft=(cur_x_mesa, posicion_mesa_y))
                screen.blit(imagen_mesa, rect_mesa)
                
                cur_x_mesa += 20
            except pygame.error as e:
                print(f"Error al dibujar carta en mesa '{objeto_carta_lanzada.skin}': {e}")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit() 

if __name__ == '__main__':
    run_game()
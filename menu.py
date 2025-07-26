import pygame
from mesa import run_game
import math
import socket

def get_local_ip_address():
    """
    Retrieves and returns the local IP address of the machine.
    """
    try:
        # Get the hostname of the local machine
        hostname = socket.gethostname()
        # Resolve the hostname to its corresponding IP address
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        return f"Error getting IP address: {e}"
    
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menú Principal - Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (50, 50, 200)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 100, 0)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
SHADOW_COLOR = (0, 0, 0, 100)

font = pygame.font.Font(None, 50)

# Estados del menú
MENU_PRINCIPAL = 0
PANTALLA_JUEGO_MENU = 1
PANTALLA_2_JUG = 2
ESTADO_HOST = 3
ESTADO_CLIENTE = 4

current_game_state = MENU_PRINCIPAL
boton_sonido= pygame.mixer.Sound('sounds\paper1.ogg')
# -------------------- Botón --------------------
class Button:
    def __init__(self, x, y, width, height, text, action=None,sound_effect=None, color=None, hover_color=None):
        if color is None:
            color = LIGHT_BLUE
        if hover_color is None:
            hover_color = DARK_BLUE

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.sound_effect = boton_sonido
        self.color = color
        self.hover_color = hover_color
        self.text_color = WHITE
        self.is_hovered = False

    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered else self.color
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=12)
        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: # Clic izquierdo y está en hover
                if self.sound_effect: # <-- ¡Si hay un sonido asignado!
                    self.sound_effect.play() # <-- ¡Reproduce el sonido!
                if self.action:
                    self.action() # Ejecuta la acción asociada al botón
                return True # Retorna True para indicar que el botón fue clickeado
        return False

# -------------------- Acciones --------------------
def play_game_menu():
    global current_game_state
    print("¡Cambiando a Pantalla de Juego!")
    current_game_state = PANTALLA_JUEGO_MENU

def show_credits():
    print("Mostrando créditos...")

def exit_game():
    print("Saliendo del juego...")
    global running
    running = False

def join_game_menu():
    global current_game_state
    current_game_state = PANTALLA_2_JUG
    print("¡Uniéndome a una partida existente!")

def back_to_main_menu():
    global current_game_state
    print("Volviendo al menú principal...")
    current_game_state = MENU_PRINCIPAL

def back_to_game_menu():
    global current_game_state
    print("Volviendo al menú de jugar...")
    current_game_state = PANTALLA_JUEGO_MENU

def host_menu():
    global current_game_state
    print("Host menu")
    current_game_state = ESTADO_HOST

def join_menu():
    global current_game_state
    print("join menu")
    current_game_state = ESTADO_CLIENTE

def back_to_join_menu():
    global current_game_state
    current_game_state = PANTALLA_2_JUG
    print("Volviendo al menu de 2 jugadores")

# -------------------- Botones --------------------
button_width = 200
button_height = 70
padding = 30
margin_right = 50
button_x = SCREEN_WIDTH - button_width - margin_right
total_buttons_height = (3 * button_height) + (2 * padding)
start_y = (SCREEN_HEIGHT - 500) // 2

#vs_ia_button = Button(button_x, start_y, button_width, button_height, "Jugar vs IA", run_game)
play_button = Button(button_x, start_y + (button_height + padding) * 1, button_width, button_height, "Jugar", play_game_menu,)
credits_button = Button(button_x, start_y + (button_height + padding) * 2, button_width, button_height, "Créditos", show_credits,)
exit_button = Button(button_x, start_y + (button_height + padding) * 3, button_width, button_height, "Salir", exit_game,)

#main_menu_buttons = [vs_ia_button, play_button, credits_button, exit_button]
main_menu_buttons = [play_button, credits_button, exit_button]

# Botones de pantalla de juego 
game_button_width = 250
game_button_height = 80
game_padding_horizontal = 50 
game_center_y = (SCREEN_HEIGHT - game_button_height) // 2
total_buttons_occupied_width = (2 * game_button_width) + game_padding_horizontal
start_x_group = (SCREEN_WIDTH - total_buttons_occupied_width) // 2


unjugador = Button(start_x_group, game_center_y, game_button_width, game_button_height, "1 jugador", run_game, GREEN, DARK_GREEN)
dosjugadores = Button(start_x_group + game_button_width + game_padding_horizontal, game_center_y, game_button_width, game_button_height, "2 jugadores", join_game_menu, GREEN, DARK_GREEN)

back_button = Button(20, SCREEN_HEIGHT - 50 - 20, 150, 50, "Back", back_to_main_menu, (150, 150, 0), (100, 100, 0))

game_screen_buttons = [unjugador, dosjugadores, back_button]

#Botones de pantalla dos jugadores--------------------------------------------------------------------------------------------------
two_jug_button_width = 250
two_jug_button_height = 80
two_jug_padding_horizontal = 50 
two_jug_center_y = (SCREEN_HEIGHT - game_button_height) // 2
two_jug_start_x_group = (SCREEN_WIDTH - total_buttons_occupied_width) // 2

host_button = Button(start_x_group, game_center_y, game_button_width, game_button_height, "Hostear Juego", host_menu, LIGHT_BLUE, DARK_BLUE)
join_button = Button(start_x_group + game_button_width + game_padding_horizontal, game_center_y, game_button_width, game_button_height, "Unirse Juego", join_menu, LIGHT_BLUE, DARK_BLUE)
back_game_button = Button(20, SCREEN_HEIGHT - 50 - 20, 150, 50, "Back", back_to_game_menu, (150, 150, 0), (100, 100, 0))

pantalla_2_jug_buttons = [host_button, join_button, back_game_button]
#-------------------------------------------
#HOST MENU
pygame.font.init()
host_button_width = 250
host_button_height = 80
host_padding_horizontal = 50 
host_center_y = (SCREEN_HEIGHT - game_button_height) // 2
host_start_x_group = (SCREEN_WIDTH - total_buttons_occupied_width) // 2


back_host_button = Button(20, SCREEN_HEIGHT - 50 - 20, 150, 50, "Back", back_to_join_menu, (150, 150, 0), (100, 100, 0))

host_buttons = [back_host_button]

text_surface = font.render("Menu host!", True, (255,255,255))
text_rect = text_surface.get_rect()
text_rect.center = (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//6)
local_ip = get_local_ip_address()

ip_surface = font.render(f"IP: {local_ip}", True, (255,255,255))
ip_rect = ip_surface.get_rect()
ip_rect.center = (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//4)

texto = []
#-------------------------------------------
#JOIN MENU

join_button_width = 250
join_button_height = 80
join_padding_horizontal = 50 
join_center_y = (SCREEN_HEIGHT - game_button_height) // 2
join_start_x_group = (SCREEN_WIDTH - total_buttons_occupied_width) // 2


back_join_button = Button(20, SCREEN_HEIGHT - 50 - 20, 150, 50, "Back", back_to_join_menu, (150, 150, 0), (100, 100, 0))

join_buttons = [back_join_button]

join_txt_surface = font.render("Menu join!", True, (255,255,255))
join_txt_rect = join_txt_surface.get_rect()
join_txt_rect.center = (SCREEN_WIDTH//1.3, SCREEN_HEIGHT//6)
local_ip = get_local_ip_address()

BLUE = (0, 0, 255)
input_box = pygame.Rect(SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 4, 200, 40)
color_inactive = GRAY
color_active = WHITE
color = color_inactive
active = False
text = ''  # Aquí se guardará el texto ingresado
done = False



# -------------------- Imágenes -------------------------------------------------------------
menu_image = pygame.image.load('textures/menu/logo.png')
menu_fondo = pygame.image.load("textures/pytrucofondobackcarta/Fondomenu.png")
menu_fondo_rect = menu_fondo.get_rect()
menu_image = pygame.transform.scale(menu_image, (300, 300))
image_rect = menu_image.get_rect()
image_rect.centerx = (SCREEN_WIDTH - button_width - margin_right) // 2 
image_rect.centery = SCREEN_HEIGHT // 2 

# -------------------- Animación --------------------
angle = 0
def animate_logo():
    global angle
    scale = 1 + 0.02 * math.sin(angle)
    angle += 0.1
    scaled_size = int(300 * scale)
    scaled_logo = pygame.transform.smoothscale(pygame.image.load('textures/menu/logo.png'), (scaled_size, scaled_size))
    rect = scaled_logo.get_rect()
    rect.center = image_rect.center
    screen.blit(scaled_logo, rect)

# -------------------- LOOP PRINCIPAL --------------------
running = True

while running:
    screen.blit(menu_fondo, menu_fondo_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hizo clic en el input_box
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            # Cambiar el color de la caja
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN: # Si se presiona Enter, se "envía" el texto
                    print(f"Texto ingresado: {text}")
                    # Aquí puedes hacer algo con la variable 'text'
                    # Por ejemplo, podrías almacenarla en una lista, base de datos, etc.
                    # Para este ejemplo, solo la imprimimos y reseteamos la caja
                    text = '' # Resetea el texto después de presionar Enter si lo deseas
                elif event.key == pygame.K_BACKSPACE: # Si se presiona Backspace, borra el último carácter
                    text = text[:-1]
                else: # Cualquier otra tecla se añade al texto
                    text += event.unicode

        if current_game_state == MENU_PRINCIPAL:
            for button in main_menu_buttons:
                button.handle_event(event)
        elif current_game_state == PANTALLA_JUEGO_MENU:
            for button in game_screen_buttons:
                button.handle_event(event)
        elif current_game_state == PANTALLA_2_JUG:
            for button in pantalla_2_jug_buttons:
                button.handle_event(event)
        elif current_game_state == ESTADO_HOST:
            for button in host_buttons:
                button.handle_event(event)
        elif current_game_state == ESTADO_CLIENTE:
            for button in join_buttons:
                button.handle_event(event)

    if current_game_state == MENU_PRINCIPAL:
        animate_logo()
        for button in main_menu_buttons:
            button.draw(screen)
    elif current_game_state == PANTALLA_JUEGO_MENU:
        screen.blit(menu_fondo, menu_fondo_rect)
        for button in game_screen_buttons:
            button.draw(screen)
    elif current_game_state == PANTALLA_2_JUG:
        screen.blit(menu_fondo, menu_fondo_rect)
        for button in pantalla_2_jug_buttons:
            button.draw(screen)
    elif current_game_state == ESTADO_HOST:
        screen.blit(text_surface,text_rect)
        screen.blit(ip_surface,ip_rect)
        for button in host_buttons:
            button.draw(screen)  
    elif current_game_state == ESTADO_CLIENTE:
            # Renderizar el texto de la entrada
        txt_surface = font.render(text, True, BLACK)
        # Redimensionar la caja si el texto es más largo que la caja inicial
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Dibujar el rectángulo de la caja
        pygame.draw.rect(screen, color, input_box, 2)
        # Dibujar el texto dentro de la caja
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        screen.blit(join_txt_surface,join_txt_rect)

        for button in join_buttons:
            button.draw(screen) 

    pygame.display.flip()

pygame.quit()
print("Pygame ha finalizado correctamente.")


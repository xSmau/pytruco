import pygame
from mesa import run_game
import math

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

current_game_state = MENU_PRINCIPAL

# -------------------- Botón --------------------
class Button:
    def __init__(self, x, y, width, height, text, action=None, color=None, hover_color=None):
        if color is None:
            color = LIGHT_BLUE
        if hover_color is None:
            hover_color = DARK_BLUE

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
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
            if event.button == 1 and self.is_hovered:
                if self.action:
                    self.action()

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

def host_game():
    print("¡Creando una partida como host!")

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

# -------------------- Botones --------------------
button_width = 200
button_height = 70
padding = 30
margin_right = 50
button_x = SCREEN_WIDTH - button_width - margin_right
total_buttons_height = (3 * button_height) + (2 * padding)
start_y = (SCREEN_HEIGHT - 500) // 2

#vs_ia_button = Button(button_x, start_y, button_width, button_height, "Jugar vs IA", run_game)
play_button = Button(button_x, start_y + (button_height + padding) * 1, button_width, button_height, "Play", play_game_menu)
credits_button = Button(button_x, start_y + (button_height + padding) * 2, button_width, button_height, "Créditos", show_credits)
exit_button = Button(button_x, start_y + (button_height + padding) * 3, button_width, button_height, "Salir", exit_game)

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

host_button = Button(start_x_group, game_center_y, game_button_width, game_button_height, "Hostear Juego", host_game, LIGHT_BLUE, DARK_BLUE)
join_button = Button(start_x_group + game_button_width + game_padding_horizontal, game_center_y, game_button_width, game_button_height, "Unirse Juego", join_game_menu, LIGHT_BLUE, DARK_BLUE)
back_game_button = Button(20, SCREEN_HEIGHT - 50 - 20, 150, 50, "Back", back_to_game_menu, (150, 150, 0), (100, 100, 0))

pantalla_2_jug_buttons = [host_button, join_button, back_game_button]

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

        if current_game_state == MENU_PRINCIPAL:
            for button in main_menu_buttons:
                button.handle_event(event)
        elif current_game_state == PANTALLA_JUEGO_MENU:
            for button in game_screen_buttons:
                button.handle_event(event)
        elif current_game_state == PANTALLA_2_JUG:
            for button in pantalla_2_jug_buttons:
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
    pygame.display.flip()

pygame.quit()
print("Pygame ha finalizado correctamente.")

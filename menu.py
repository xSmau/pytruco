import pygame
from mesa import run_game

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

font = pygame.font.Font(None, 50)
correr = False
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
        pygame.draw.rect(screen, current_color, self.rect)

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

def play_game():
    print("¡Iniciando juego!")

def show_credits():
    print("Mostrando créditos...")

def exit_game():
    print("Saliendo del juego...")
    global running
    running = False
    
MENU_PRINCIPAL = 0
PANTALLA_JUEGO = 1
current_game_state = MENU_PRINCIPAL

def play_game():
    global current_game_state
    print("¡Cambiando a Pantalla de Juego!")
    current_game_state = PANTALLA_JUEGO

def show_credits():
    print("Mostrando créditos...")

def exit_game():
    print("Saliendo del juego...")
    global running
    running = False

def host_game():
    print("¡Creando una partida como host!")
    global correr
    correr = True

def join_game():
    print("¡Uniéndome a una partida existente!")

def back_to_main_menu():
    global current_game_state
    print("Volviendo al menú principal...")
    current_game_state = MENU_PRINCIPAL

button_width = 200
button_height = 70
padding = 30

margin_right = 50
button_x = SCREEN_WIDTH - button_width - margin_right

total_buttons_height = (3 * button_height) + (2 * padding)
start_y = (SCREEN_HEIGHT - total_buttons_height) // 2

play_button = Button(button_x, start_y, button_width, button_height, "Play", play_game)
exit_button = Button(button_x, start_y + button_height + padding, button_width, button_height, "Exit", exit_game)
credits_button = Button(button_x, start_y + 2 * (button_height + padding), button_width, button_height, "Credits", show_credits)

main_menu_buttons = [play_button, exit_button, credits_button]

game_button_width = 250
game_button_height = 80
game_padding_horizontal = 50 
game_padding_vertical = 30

game_center_y = (SCREEN_HEIGHT - game_button_height) // 2

total_buttons_occupied_width = (2 * game_button_width) + game_padding_horizontal
start_x_group = (SCREEN_WIDTH - total_buttons_occupied_width) // 2

host_button_x = start_x_group
join_button_x = start_x_group + game_button_width + game_padding_horizontal

host_button = Button(host_button_x, game_center_y, game_button_width, game_button_height, "Host Game", host_game, GREEN, DARK_GREEN)
join_button = Button(join_button_x, game_center_y, game_button_width, game_button_height, "Join Game", join_game, GREEN, DARK_GREEN)

back_button = Button(20, SCREEN_HEIGHT - 50 - 20, 150, 50, "Back", back_to_main_menu, (150, 150, 0), (100, 100, 0))

game_screen_buttons = [host_button, join_button, back_button]

menu_image = pygame.image.load('textures\menu\logo.png')
menu_fondo= pygame.image.load("textures\pytrucofondobackcarta\Fondomenu.png")
menu_fondo_rect = menu_fondo.get_rect()
menu_image = pygame.transform.scale(menu_image, (300, 300))
image_rect = menu_image.get_rect()
image_rect.centerx = (SCREEN_WIDTH - button_width - margin_right) // 2 
image_rect.centery = SCREEN_HEIGHT // 2 

running = True
while running:
    screen.fill(BLACK)
    screen.blit(menu_fondo,menu_fondo_rect)
    if correr == True:

        pygame.quit()
        running = False
        run_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_game_state == MENU_PRINCIPAL:
            for button in main_menu_buttons:
                button.handle_event(event)
        elif current_game_state == PANTALLA_JUEGO:
            for button in game_screen_buttons:
                button.handle_event(event)


    screen.blit(menu_image, image_rect)
    if current_game_state == MENU_PRINCIPAL:
        screen.blit(menu_image, image_rect)
        for button in main_menu_buttons:
            button.draw(screen)
    elif current_game_state == PANTALLA_JUEGO:
        screen.fill(BLACK)
        for button in game_screen_buttons:
            button.draw(screen)

    pygame.display.flip()

pygame.quit()
print("Pygame ha finalizado correctamente.")
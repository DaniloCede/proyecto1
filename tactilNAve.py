import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 400, 600  # Cambiar dimensiones para pantalla vertical
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquivar Obstáculos")

# Colores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Jugador
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Obstáculos
obstacle_width_range = (30, 70)
obstacle_height = 20
obstacle_speed = 3  # Velocidad inicial
obstacles = []
obstacle_timer = 0
obstacle_interval = 50
points_to_change_color = 25
points_to_speed_up = 25  # Aumentar la velocidad cada 25 puntos
speed_increase_amount = 1
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (138, 43, 226)]  # Colores disponibles para los obstáculos

# Puntuación
score = 0
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 20)  # Fuente más pequeña
points_since_last_change = 0

clock = pygame.time.Clock()

def draw_player():
    pygame.draw.polygon(win, WHITE, [(player_x + player_width // 2, player_y),
                                     (player_x, player_y + player_height),
                                     (player_x + player_width, player_y + player_height)])

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(win, obstacle.color, obstacle.rect)

def move_obstacles():
    global score, points_since_last_change, obstacle_speed
    for obstacle in obstacles:
        obstacle.rect.y += obstacle_speed
        if obstacle.rect.y > HEIGHT:
            obstacles.remove(obstacle)
            score += 1
            points_since_last_change += 1

def spawn_obstacle():
    width = random.randint(*obstacle_width_range)
    x = random.randint(0, WIDTH - width)
    color = colors[score // points_to_change_color % len(colors)]  # Cambiar el color cada 25 puntos
    obstacles.append(Obstacle(pygame.Rect(x, 0, width, obstacle_height), color))

def draw_score():
    score_text = font.render("Puntuación: " + str(score), True, YELLOW)
    win.blit(score_text, (10, 10))

def draw_restart_text():
    restart_text = big_font.render("Volver a Empezar", True, YELLOW)
    text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    win.blit(restart_text, text_rect)

def draw_final_score(final_score):
    final_score_text = font.render("Puntuación Final: " + str(final_score), True, WHITE)
    text_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    win.blit(final_score_text, text_rect)

def draw_footer():
    footer_text = small_font.render("Creado por Cdño", True, YELLOW)  # Usar la fuente más pequeña
    win.blit(footer_text, (10, HEIGHT - 20))  # Ajustar la posición para que esté en la parte inferior izquierda

def restart_game():
    global score, points_since_last_change, obstacle_speed, obstacles, game_over
    score = 0
    points_since_last_change = 0
    obstacle_speed = 3
    obstacles = []
    game_over = False

class Obstacle:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

# Bucle principal del juego
running = True
game_over = False
while running:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100) and (HEIGHT // 2 + 50 <= mouse_y <= HEIGHT // 2 + 100):
                restart_game()

    if not game_over:
        # Control táctil
        touch = pygame.mouse.get_pos()
        if player_x < touch[0] < player_x + player_width:
            player_x = touch[0] - player_width // 2
            if player_x < 0:
                player_x = 0
            elif player_x + player_width > WIDTH:
                player_x = WIDTH - player_width

        # Generar obstáculos
        obstacle_timer += 1
        if obstacle_timer == obstacle_interval:
            spawn_obstacle()
            obstacle_timer = 0

        move_obstacles()

        # Aumentar la velocidad cada 25 puntos
        if points_since_last_change >= points_to_speed_up:
            obstacle_speed += speed_increase_amount
            points_since_last_change = 0

        # Colisiones
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                game_over = True

        draw_player()
        draw_obstacles()
        draw_score()

    if game_over:
        draw_restart_text()
        draw_final_score(score)

    draw_footer()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
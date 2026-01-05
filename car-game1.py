import pygame
import random
import sys

# ------------------ INIT ------------------
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

clock = pygame.time.Clock()
FPS = 60

# ------------------ COLORS ------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)

# ------------------ ROAD ------------------
ROAD_LEFT = 50
ROAD_RIGHT = WIDTH - 50

# ------------------ CAR ------------------
car_width, car_height = 50, 100

player = pygame.Rect(
    WIDTH // 2 - car_width // 2,
    HEIGHT - 120,
    car_width,
    car_height
)

enemy = pygame.Rect(
    random.randint(ROAD_LEFT + 5, ROAD_RIGHT - car_width - 5),
    -300,
    car_width,
    car_height
)

# ------------------ IMAGES ------------------
try:
    player_img = pygame.image.load("player_car.jpeg").convert_alpha()
    enemy_img = pygame.image.load("enemy_car.jpeg").convert_alpha()
except pygame.error as e:
    print("Image loading error:", e)
    pygame.quit()
    sys.exit()

player_img = pygame.transform.scale(player_img, (car_width, car_height))
enemy_img = pygame.transform.scale(enemy_img, (car_width, car_height))

# ------------------ SOUNDS (SAFE LOAD) ------------------
def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Sound error ({file}):", e)
        return None

engine_sound = load_sound("engine.mp3")
crash_sound = load_sound("Crash.mp3")

if engine_sound:
    engine_sound.play(-1)

# ------------------ GAME VALUES ------------------
player_speed = 5
enemy_speed = 6
score = 0

font = pygame.font.SysFont("Arial", 30)

# ------------------ GAME LOOP ------------------
running = True
while running:
    screen.fill(GRAY)

    # Road
    pygame.draw.rect(screen, BLACK, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > ROAD_LEFT + 5:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < ROAD_RIGHT - 5:
        player.x += player_speed

    # Enemy movement
    enemy.y += enemy_speed
    if enemy.top > HEIGHT:
        enemy.y = -300
        enemy.x = random.randint(ROAD_LEFT + 5, ROAD_RIGHT - car_width - 5)
        score += 1
        enemy_speed = min(enemy_speed + 0.4, 15)

    # Collision
    if player.colliderect(enemy):
        if engine_sound:
            engine_sound.stop()
        if crash_sound:
            crash_sound.play()

        screen.fill(RED)
        game_over = font.render("GAME OVER!", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        screen.blit(game_over, (WIDTH // 2 - 90, HEIGHT // 2 - 40))
        screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2))
        pygame.display.update()

        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Draw
    screen.blit(player_img, player)
    screen.blit(enemy_img, enemy)

    # Score
    score_display = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_display, (10, 10))

    pygame.display.update()
    clock.tick(FPS)

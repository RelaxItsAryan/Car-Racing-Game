import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Racer")

# Colors
WHITE = (255, 255, 255)

# Load Images (Ensure these files exist in your folder!)
try:
    player_img = pygame.image.load('player.png') # Your red car
    enemy_img = pygame.image.load('enemy.png')   # Other cars
    road_img = pygame.image.load('road.png')     # The road image
    
    # Resize images to fit the game scale
    player_img = pygame.transform.scale(player_img, (50, 80))
    enemy_img = pygame.transform.scale(enemy_img, (50, 80))
    road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))
except:
    print("Error: Make sure 'player.png', 'enemy.png', and 'road.png' are in the folder.")
    pygame.quit()
    exit()

# Game Variables
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 100
player_speed = 5

enemy_speed = 7
enemies = []

def spawn_enemy():
    x_pos = random.randint(50, WIDTH - 100)
    y_pos = -100
    enemies.append([x_pos, y_pos])

# Game Loop
clock = pygame.time.Clock()
running = True
score = 0
spawn_timer = 0

while running:
    screen.fill(WHITE)
    screen.blit(road_img, (0, 0)) # Draw Road

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 40:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 90:
        player_x += player_speed

    # Enemy Logic
    spawn_timer += 1
    if spawn_timer > 40:
        spawn_enemy()
        spawn_timer = 0

    for enemy in enemies[:]:
        enemy[1] += enemy_speed # Move enemy down
        screen.blit(enemy_img, (enemy[0], enemy[1]))

        # Collision Detection
        player_rect = pygame.Rect(player_x, player_y, 50, 80)
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 80)
        
        if player_rect.colliderect(enemy_rect):
            print(f"Game Over! Score: {score}")
            running = False

        # Remove off-screen enemies
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
            score += 1

    # Draw Player
    screen.blit(player_img, (player_x, player_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
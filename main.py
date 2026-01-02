import pygame, random, os, sys
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Highway Car Racing")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
font_large = pygame.font.SysFont(None, 64)

BASE = os.path.dirname(__file__)
IMG = os.path.join(BASE,"assets/images")
SND = os.path.join(BASE,"assets/sounds")

player_img = pygame.image.load(os.path.join(IMG,"player.png")).convert_alpha()
enemy_imgs = [
    pygame.image.load(os.path.join(IMG,"enemy1.png")).convert_alpha(),
    pygame.image.load(os.path.join(IMG,"enemy2.png")).convert_alpha()
]
coin_img = pygame.image.load(os.path.join(IMG,"coin.png")).convert_alpha()
road_img = pygame.image.load(os.path.join(IMG,"road.png"))

coin_sound = pygame.mixer.Sound(os.path.join(SND,"coin.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(SND,"crash.wav"))

player = pygame.Rect(WIDTH//2-25, HEIGHT-110, 50, 90)
speed = 7

road_y1, road_y2 = 0, -HEIGHT
scroll_speed = 6

enemies = []
coins = []
score = 0
coins_collected = 0

def spawn_enemy():
    enemies.append({
        "rect": pygame.Rect(random.choice([140,220,300]), random.randint(-600,-100), 50, 90),
        "img": random.choice(enemy_imgs)
    })

def spawn_coin():
    coins.append(pygame.Rect(random.choice([150,230,310]), random.randint(-800,-200), 30, 30))

def reset_game():
    global player, enemies, coins, score, coins_collected, road_y1, road_y2
    player = pygame.Rect(WIDTH//2-25, HEIGHT-110, 50, 90)
    enemies.clear()
    coins.clear()
    for _ in range(3): spawn_enemy()
    for _ in range(2): spawn_coin()
    score = 0
    coins_collected = 0
    road_y1, road_y2 = 0, -HEIGHT

for _ in range(3): spawn_enemy()
for _ in range(2): spawn_coin()

running = True
game_over = False

while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and game_over:
            if e.key in (pygame.K_SPACE, pygame.K_r):
                reset_game()
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 120: player.x -= speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH-170: player.x += speed

        road_y1 += scroll_speed
        road_y2 += scroll_speed
        if road_y1 >= HEIGHT: road_y1 = -HEIGHT
        if road_y2 >= HEIGHT: road_y2 = -HEIGHT

        for en in enemies:
            en["rect"].y += scroll_speed
            if en["rect"].y > HEIGHT:
                en["rect"].y = random.randint(-600,-100)
                score += 1
            if player.colliderect(en["rect"]):
                crash_sound.play()
                game_over = True

        for c in coins:
            c.y += scroll_speed
            if c.y > HEIGHT:
                c.y = random.randint(-800,-200)
            if player.colliderect(c):
                coin_sound.play()
                coins_collected += 1
                c.y = random.randint(-800,-200)

    screen.blit(road_img,(0,road_y1))
    screen.blit(road_img,(0,road_y2))

    for en in enemies:
        screen.blit(en["img"], en["rect"])
    for c in coins:
        screen.blit(coin_img, c)

    screen.blit(player_img, player)

    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20,20))
    screen.blit(font.render(f"Coins: {coins_collected}", True, (255,215,0)), (20,50))

    if game_over:
        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        go_text = font_large.render("GAME OVER", True, (255, 0, 0))
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 80))
        
        # Final score
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 10))
        
        coins_text = font.render(f"Coins Collected: {coins_collected}", True, (255, 215, 0))
        screen.blit(coins_text, (WIDTH//2 - coins_text.get_width()//2, HEIGHT//2 + 30))
        
        # Restart prompt
        restart_text = font.render("Press SPACE or R to Restart", True, (200, 200, 200))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 90))

    pygame.display.update()

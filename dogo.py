import pygame
import random
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

resources_path = os.path.join(os.path.dirname(__file__), 'resources')

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
obstacle_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 4)
food_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)

score = 0
font = pygame.font.SysFont("Arial", 24)

player_image = pygame.image.load(os.path.join(resources_path, "dog.png"))
player_image = pygame.transform.scale(player_image, (50, 50))

food_image = pygame.image.load(os.path.join(resources_path, "image.png"))
food_image = pygame.transform.scale(food_image, (50, 50))

obstacle_image = pygame.image.load(os.path.join(resources_path, "image copy.png"))
obstacle_image = pygame.transform.scale(obstacle_image, (160, 160))

eat_sound = pygame.mixer.Sound(os.path.join(resources_path, "Rise01.wav"))

def spawn_obstacle():
    x = random.randint(0, screen.get_width() - 160)
    y = random.randint(0, screen.get_height() - 160)
    return pygame.Vector2(x, y)

def spawn_food():
    x = random.randint(0, screen.get_width() - 50)
    y = random.randint(0, screen.get_height() - 50)
    return pygame.Vector2(x, y)

def reset_game():
    global player_pos, obstacle_pos, food_pos, score, running
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    obstacle_pos = spawn_obstacle()
    food_pos = spawn_food()
    score = 0
    running = True

obstacle_pos = spawn_obstacle()
food_pos = spawn_food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if not running and keys[pygame.K_w]: 
        reset_game()

    if running:
        screen.fill("purple")

        obstacle_rect = pygame.Rect(obstacle_pos.x, obstacle_pos.y, 160, 160)
        screen.blit(obstacle_image, obstacle_rect.topleft)

        food_rect = pygame.Rect(food_pos.x, food_pos.y, 50, 50)
        screen.blit(food_image, food_rect.topleft)

        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        player_rect = pygame.Rect(player_pos.x, player_pos.y, 50, 50)
        screen.blit(player_image, player_rect.topleft)

        if player_rect.colliderect(food_rect):
            score += 1
            food_pos = spawn_food()
            eat_sound.play()  

        if player_rect.colliderect(obstacle_rect):
            running = False

        if player_pos.y > 720:
            player_pos.y = 0
        elif player_pos.y < 0:
            player_pos.y = 720

        if player_pos.x > 1280:
            player_pos.x = 0
        elif player_pos.x < 0:
            player_pos.x = 1280

        direction = player_pos - obstacle_pos
        if direction.length() != 0:
            direction = direction.normalize()
        obstacle_pos += direction * 250 * dt  

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        screen.fill("black")
        game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press 'W' to Restart", True, (255, 255, 255))
        screen.blit(game_over_text, (screen.get_width() / 2 - game_over_text.get_width() / 2, screen.get_height() / 2 - 50))
        screen.blit(restart_text, (screen.get_width() / 2 - restart_text.get_width() / 2, screen.get_height() / 2 + 10))

    pygame.display.flip()

    dt = clock.tick(60) / 1000
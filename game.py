import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo com Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


clock = pygame.time.Clock()

def draw_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Pressione ESPAÇO para jogar", True, BLACK)
    screen.blit(text, (50, SCREEN_HEIGHT // 2 - 50))
    
    pygame.display.flip()




def move_player(player, speed):
    keys = pygame.key.get_pressed()
    moved_horizontal = False
    moved_vertical = False
    
    if keys[pygame.K_LEFT] and player['rect'].left > 0:
        player['rect'].x -= speed
        moved_horizontal = True
    if keys[pygame.K_RIGHT] and player['rect'].right < SCREEN_WIDTH:
        player['rect'].x += speed
        moved_horizontal = True
    if keys[pygame.K_UP] and player['rect'].top > 0:
        player['rect'].y -= speed
        moved_vertical = True
    if keys[pygame.K_DOWN] and player['rect'].bottom < SCREEN_HEIGHT:
        player['rect'].y += speed
        moved_vertical = True

    if moved_horizontal:
        player['angle'] += 5 if keys[pygame.K_RIGHT] else -5
    if moved_vertical:
        player['angle'] += 5 if keys[pygame.K_DOWN] else -5

def create_enemy():
    enemy_size = 50
    enemy = pygame.Rect(random.randint(0, SCREEN_WIDTH - enemy_size), 
                        random.randint(0, SCREEN_HEIGHT - enemy_size), 
                        enemy_size, enemy_size)
    return enemy

def create_obstacle(enemies):
    while True:
        obstacle_width = random.randint(50, 100)
        obstacle_height = random.randint(50, 100)
        obstacle = pygame.Rect(random.randint(0, SCREEN_WIDTH - obstacle_width),
                                random.randint(0, SCREEN_HEIGHT - obstacle_height),
                                obstacle_width, obstacle_height)
        if not any(enemy.colliderect(obstacle) for enemy in enemies):
            return obstacle

def check_collision(player, enemies):
    for enemy in enemies[:]:
        if player['rect'].colliderect(enemy):
            enemies.remove(enemy)
            return True
    return False

def check_obstacle_collision(player, obstacles):
    for obstacle in obstacles:
        if player['rect'].colliderect(obstacle):
            return True
    return False

def draw_player(player):
    player_surface = pygame.Surface((player['rect'].width, player['rect'].height))
    player_surface.fill(GREEN)
    
    rotated_surface = pygame.transform.rotate(player_surface, player['angle'])
    rotated_rect = rotated_surface.get_rect(center=player['rect'].center)

    screen.blit(rotated_surface, rotated_rect.topleft)

def game_loop():
    player = {
        'rect': pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, 50),
        'angle': 0
    }
    player_speed = 5
    enemies = [create_enemy() for _ in range(5)]
    obstacles = [create_obstacle(enemies) for _ in range(6)]

    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_player(player, player_speed)

        if check_collision(player, enemies):
            player['rect'].width += 10

        if check_obstacle_collision(player, obstacles):  # Verifica colisão com obstáculos
            font = pygame.font.Font(None, 74)
            text = font.render("Você perdeu!", True, RED)
            screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)  # Espera 2 segundos antes de reiniciar
            game_loop() 

        screen.fill(WHITE)
        draw_player(player) 

        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 0, 0), obstacle)

        if not enemies:
            font = pygame.font.Font(None, 74)
            text = font.render("Você ganhou!", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50))
            
            restart_button = pygame.Rect(260, SCREEN_HEIGHT // 2 + 20, 235, 50)
            pygame.draw.rect(screen, BLACK, restart_button)
            font = pygame.font.Font(None, 50)
            text = font.render("Recomeçar", True, WHITE)
            screen.blit(text, (restart_button.x + 20, restart_button.y + 10))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                if restart_button.collidepoint(mouse_x, mouse_y):
                    game_loop()

        pygame.display.flip()
        clock.tick(30)

def main():
    in_menu = True
    while in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_menu = False
                    game_loop()

if __name__ == "__main__":
    main()

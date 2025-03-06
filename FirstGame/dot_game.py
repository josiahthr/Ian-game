import pygame
import random


def main():

    pygame.init()
    running = True
    screen = pygame.display.set_mode((1280, 720))
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    coll_pos = pygame.Vector2(random.randint(50, 1230), random.randint(50, 670))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    pygame.display.set_caption("Dot Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    score = 0
    coll_radius = 15
    player_radius = 10
    coll_visible = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("red")
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        player_rect = pygame.Rect(int(player_pos.x) - player_radius, int(player_pos.y) - player_radius, player_radius * 2, player_radius * 2)
        coll_rect = pygame.Rect(int(coll_pos.x) - coll_radius, int(coll_pos.y) - coll_radius, coll_radius * 2, coll_radius * 2)
        if coll_visible and player_rect.colliderect(coll_rect):
            coll_visible = False
            score += 1
            coll_pos = pygame.Vector2(random.randint(50, 1230), random.randint(50, 670))
            coll_visible = True
        pygame.draw.circle(screen, "white", player_pos, 10)
        pygame.draw.circle(screen, "blue", coll_pos, 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        if player_pos.x < 10:  # left
            player_pos.x = 10
        if player_pos.y < 10:  # top
            player_pos.y = 10
        if player_pos.x > screen.get_width() - 10:  # right
            player_pos.x = screen.get_width() - 10
        if player_pos.y > screen.get_height() - 10:  # bottom
            player_pos.y = screen.get_height() - 10
        pygame.display.flip()


if __name__ == '__main__':
    main()

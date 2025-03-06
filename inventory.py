import pygame

def draw_inventory(screen, screen_width, screen_height, inventory_active, player_inventory):
    if inventory_active:
            inventory_rect = pygame.Rect(0, 0, screen_width, screen_height)
            pygame.draw.rect(screen, "gray", inventory_rect)
            font = pygame.font.Font(None, 36)
            text = font.render("Inventory", True, "black")
            text_rect = text.get_rect(center=(screen_width / 2, 50))
            screen.blit(text, text_rect)
                    
            item_x, item_y = 100, 100
            for item in player_inventory:
                item_rect = item["image"].get_rect(topleft=(item_x, item_y))
                screen.blit(item["image"], item_rect)
                item_x += 100
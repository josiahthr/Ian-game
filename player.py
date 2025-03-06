import pygame

class Player:
    def __init__(self, x, y):
        self.player_pos = pygame.Vector2(x, y)
        self.player_east = pygame.image.load('images/player_east.png').convert_alpha()
        self.player_west = pygame.image.load('images/player_west.png').convert_alpha()
        self.player_north = pygame.image.load('images/player_north.png').convert_alpha()
        self.player_south = pygame.image.load('images/player_south.png').convert_alpha()
        self.player_east_left = pygame.image.load('images/east_left.png').convert_alpha()
        self.player_east_right = pygame.image.load('images/east_right.png').convert_alpha()
        self.player_west_left = pygame.image.load('images/west_left.png').convert_alpha()
        self.player_west_right = pygame.image.load('images/west_right.png').convert_alpha()
        self.player_north_left = pygame.image.load('images/north_left.png').convert_alpha()
        self.player_north_right = pygame.image.load('images/north_right.png').convert_alpha()
        self.player_south_left = pygame.image.load('images/south_left.png').convert_alpha()
        self.player_south_right = pygame.image.load('images/south_right.png').convert_alpha()
        self.direction = "south"
        self.player_image = self.player_south
        self.player_rect = self.player_image.get_rect(center=self.player_pos)
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 15

    def update(self, dt, keys):
        old_player_pos = self.player_pos.copy()
        moving = False

        if keys[pygame.K_w]:
            self.player_pos.y -= 300 * dt
            self.direction = "north"
            moving = True
        if keys[pygame.K_s]:
            self.player_pos.y += 300 * dt
            self.direction = "south"
            moving = True
        if keys[pygame.K_a]:
            self.player_pos.x -= 300 * dt
            self.direction = "west"
            moving = True
        if keys[pygame.K_d]:
            self.player_pos.x += 300 * dt
            self.direction = "east"
            moving = True

        if self.player_pos.x < 10:
            self.player_pos.x = 10
        if self.player_pos.y < 10:
            self.player_pos.y = 10
        if self.player_pos.x > 1270:
            self.player_pos.x = 1270
        if self.player_pos.y > 710:
            self.player_pos.y = 710

        self.player_rect.center = self.player_pos

        if moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = 1 - self.animation_frame

                if self.direction == "east":
                    self.player_image = self.player_east_left if self.animation_frame == 0 else self.player_east_right
                elif self.direction == "west":
                    self.player_image = self.player_west_left if self.animation_frame == 0 else self.player_west_right
                elif self.direction == "north":
                    self.player_image = self.player_north_left if self.animation_frame == 0 else self.player_north_right
                elif self.direction == "south":
                    self.player_image = self.player_south_left if self.animation_frame == 0 else self.player_south_right
        else:
            if self.direction == "east":
                self.player_image = self.player_east
            elif self.direction == "west":
                self.player_image = self.player_west
            elif self.direction == "north":
                self.player_image = self.player_north
            elif self.direction == "south":
                self.player_image = self.player_south

        return old_player_pos

    def draw(self, screen):
        screen.blit(self.player_image, self.player_rect)
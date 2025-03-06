import pygame
import inventory
import player as player
import dialogue
import random



def main():
    pygame.init()
    pygame.mixer.init()
    running = True
    screen = pygame.display.set_mode((1280, 720))
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    pygame.display.set_caption("Final Game")
    clock = pygame.time.Clock()
    inventory_active = False
    dev_mode = False
    pygame.mixer.init(frequency=44100)

    key_pickup_sound = pygame.mixer.Sound("sound/key_pickup.mp3")
    door_open_sound = pygame.mixer.Sound("sound/open.mp3")
    car_sound = pygame.mixer.Sound("sound/car.mp3")
    dialogue_active = False
    dialogue_text = ""

    poster_rect = pygame.Rect(931, 130, 187, 144)
    car_rect = pygame.Rect(596, 85, 250, 160)
    jaden_rect = pygame.Rect(159, 179, 240, 164)
    mattress_rect = pygame.Rect(10, 260, 155, 300)
    jamian_rect = pygame.Rect(159, 179, 200, 264)
    desk_rect = pygame.Rect(865, 200, 320, 264)
    kyle_rect = pygame.Rect(634, 10, 520, 264)

    visited_rooms = set()

    current_dialogue_index = 0

    rooms = {
        0: {
            "color": "black",
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "doors": [
                {"x": 1200, "y": 360, "next_room": 1, "entry_x": 100, "entry_y": 360, "required_item": "Key"},
            ],
            "items": [{"name": "Key", "image": pygame.image.load("images/key.png").convert_alpha(), "x": 308, "y": 248}],
            "objects": [
                {"image": pygame.image.load("images/mattress.png").convert_alpha(), "x": 80, "y": 415, "solid": True},
                {"image": pygame.image.load("images/rug.png").convert_alpha(), "x": 627, "y": 448, "solid": False},
                {"image": pygame.image.load("images/wall.png").convert_alpha(), "x": 630, "y": 10, "solid": True},
                {"image": pygame.image.load("images/poster.png").convert_alpha(), "x": 1000, "y": 70, "solid": True}
            ],
            "interactables": [
                {
                    "name": "poster",
                    "rect": pygame.Rect(742, 167, 187, 144),
                    "position": (100, 600)
                }
            ]
        },
        1: {
            "color": "gray",
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "transition_text": "Ian needs to get to class",
            "doors": [
                {"x": 50, "y": 360, "next_room": 0, "entry_x": 1150, "entry_y": 360},
                {"x": 640, "y": 650, "next_room": 2, "entry_x": 310, "entry_y": 247}
            ],
            "objects": [
                {"image": pygame.image.load("images/wall.jpg").convert_alpha(), "x": 630, "y": 10, "solid": True},
                {"image": pygame.image.load("images/wayne.png").convert_alpha(), "x": 900, "y": 523, "solid": True, "interactive": True},
                {"image": pygame.image.load("images/desk.jpg").convert_alpha(), "x": 790, "y": 530, "solid": True},
                {"image": pygame.image.load("images/sign.png").convert_alpha(), "x": 1000, "y": 70, "solid": True},

            ],
            "rects": [
                {"x": 900, "y": 523, "width": 100, "height": 100}
            ]
        },
        2: {
            "color": (17, 156, 47),
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "transition_text": "Outside Orange Street Campus",
            "doors": [{"x": 300, "y": 175, "next_room": 1, "entry_x": 640, "entry_y": 600},
                      {"x": 750, "y": 640, "next_room": 3, "entry_x": 640, "entry_y": 600}
                     ],
            "objects": [
                {"image": pygame.image.load("images/TSCT.jpg").convert_alpha(), "x": 630, "y": 10, "solid": True}
            ]
        },
        3: {
            "color": (17, 156, 47),
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "transition_text": "Ian gets a little lost",
            "doors": [{"x": 300, "y": 175, "next_room": 4, "entry_x": 345, "entry_y": 663}],
            "objects": [
                {"image": pygame.image.load("images/space.jpg").convert_alpha(), "x": 640, "y": 320, "solid": False}

            ]
        },
        4: {
            "color": (17, 156, 47),
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "transition_text": "Ian gets a little more lost",
            "doors": [{"x": 1000, "y": 60, "next_room": 5, "entry_x": 640, "entry_y": 600}],
            "objects": [
                {"image": pygame.image.load("images/roads.jpg").convert_alpha(), "x": 640, "y": 320, "solid": False}
            ]
        },
        5: {
            "color": (17, 156, 47),
            "door_image": pygame.image.load("images/shuttle.png").convert_alpha(),
            "transition_text": "Ian decides to drive to class",
            "doors": [{"x": 1182, "y": 428, "next_room": 6, "entry_x": 640, "entry_y": 600}],
            "objects": [
                {"image": pygame.image.load("images/parking.jpg").convert_alpha(), "x": 640, "y": 320, "solid": False},
                {"image": pygame.image.load("images/car.png").convert_alpha(), "x": 742, "y": 167, "solid": True}
            ],
            "interactables": [
                {
                    "name": "car",
                    "rect": pygame.Rect(742, 167, 187, 144),
                    "position": (100, 600)
                }
            ]
        },
        6: {
            "color": (17, 156, 47),
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "transition_text": "Thaddeus Stevens Main Campus",
            "doors": [{"x": 1182, "y": 428, "next_room": 7, "entry_x": 640, "entry_y": 600}],
            "objects": [
                {"image": pygame.image.load("images/main.jpg").convert_alpha(), "x": 630, "y": 10, "solid": True},
                {"image": pygame.image.load("images/kreider.png").convert_alpha(), "x": 1029, "y": 301, "solid": False},
                {"image": pygame.image.load("images/jaden.png").convert_alpha(), "x": 235, "y": 269, "solid": True}
            ],
            "interactables": [
                {
                    "name": "jaden",
                    "rect": pygame.Rect(742, 167, 187, 144),
                    "position": (100, 600)
                }
            ]
        },
        7: {
            "color": (0, 0, 0),
            "door_image": pygame.image.load("images/transition.png").convert_alpha(),
            "transition_text": "Computer and Network Systems Administration(CNSA)",
            "doors": [{"x": 670, "y": 621, "next_room": 8, "entry_x": 640, "entry_y": 600}],
            "objects": [
                {"image": pygame.image.load("images/carpet.jpg").convert_alpha(), "x": 640, "y": 362, "solid": False},
                {"image": pygame.image.load("images/cnsa.jpg").convert_alpha(), "x": 630, "y": 10, "solid": True},
                {"image": pygame.image.load("images/jamian.png").convert_alpha(), "x": 235, "y": 269, "solid": True},
                {"image": pygame.image.load("images/cdesk.png").convert_alpha(), "x": 1050, "y": 270, "solid": True},
            ],
        },
        8: {
            "color": (0, 0, 0),
            "door_image": pygame.image.load("images/work.png").convert_alpha(),
            "transition_text": "Ian needs to find a way to work",
            "doors": [{"x": 1140, "y": 503, "next_room": 9, "entry_x": 640, "entry_y": 648}],
            "objects": [
                {"image": pygame.image.load("images/parking.jpg").convert_alpha(), "x": 640, "y": 320, "solid": False},
                {"image": pygame.image.load("images/kyle.png").convert_alpha(), "x": 897, "y": 121, "solid": True, "speed": 10, "size": 50, "direction": 1, "moving": True}
            ],
        },
        9: {
            "color": (0, 0, 0),
            "door_image": pygame.image.load("images/work.png").convert_alpha(),
            "transition_text": "Ian needs to cross the road",
            "doors": [{"x": 646, "y": 30, "next_room": 10, "entry_x": 640, "entry_y": 600}],
            "objects": [
                {"image": pygame.image.load("images/frog.png").convert_alpha(), "x": 640, "y": 320, "solid": False, "speed": 10, "size": 50, "direction": 1, "moving": True},
                {"image": pygame.image.load("images/frog.png").convert_alpha(), "x": 219, "y": 197, "solid": False, "speed": 10, "size": 5, "direction": 1, "moving": True},
                {"image": pygame.image.load("images/frog.png").convert_alpha(), "x": 1054, "y": 468, "solid": False, "speed": 10, "size": 50, "direction": 1, "moving": True},
            ],
        },
        10: {
            "color": (0, 0, 0),
            "door_image": pygame.image.load("images/work.png").convert_alpha(),
            "transition_text": "You have made it to work",
            "doors": [{"x": 646, "y": 30, "next_room": 10, "entry_x": 640, "entry_y": 600}],
            "objects": [
                {"image": pygame.image.load("images/work.jpg").convert_alpha(), "x": 630, "y": 10, "solid": True},
            ],
        },
    }
    
    


    current_room = 7   # MAKE SURE THIS IS 0!!!!!
    font = pygame.font.Font(None, 36)
    door_image = pygame.image.load('images/transition.png').convert_alpha()
    player_inventory = []
    door_rect = door_image.get_rect()
    player_instance = player.Player(screen_width / 2, screen_height / 2)



    while running:
        dt = clock.tick(60) / 1000
        transitioning_to_new_room = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory_active = not inventory_active
                if event.key == pygame.K_F1:
                    dev_mode = not dev_mode
                if event.key == pygame.K_e:
                    wayne_rect = pygame.Rect(660, 430, 100, 200)
                    if player_instance.player_rect.colliderect(poster_rect) and current_room == 0:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.poster_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["poster"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.poster_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0 
                            else:
                                dialogue_text = dialogue.poster_dialogue[current_dialogue_index]
                    if player_instance.player_rect.colliderect(mattress_rect) and current_room == 0:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.mattress_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["mattress"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.mattress_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0 
                            else:
                                dialogue_text = dialogue.mattress_dialogue[current_dialogue_index]
                    if player_instance.player_rect.colliderect(wayne_rect) and current_room == 1:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.wayne_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["wayne"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.wayne_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0 
                            else:
                                dialogue_text = dialogue.wayne_dialogue[current_dialogue_index]

                    if player_instance.player_rect.colliderect(car_rect) and current_room == 5:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.car_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["car"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.car_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0
                            else:
                                dialogue_text = dialogue.car_dialogue[current_dialogue_index]

                    if player_instance.player_rect.colliderect(jaden_rect) and current_room == 6:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.jaden_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["jaden"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.jaden_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0
                            else:
                                dialogue_text = dialogue.jaden_dialogue[current_dialogue_index]

                    if player_instance.player_rect.colliderect(jamian_rect) and current_room == 7:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.jamian_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["jamian"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.jamian_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0
                            else:
                                dialogue_text = dialogue.jamian_dialogue[current_dialogue_index]
                    if player_instance.player_rect.colliderect(desk_rect) and current_room == 7:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = dialogue.desk_dialogue[current_dialogue_index]
                            dialogue_position = dialogue.dialogue_positions["desk"]
                        else:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(dialogue.desk_dialogue):
                                dialogue_active = False
                                current_dialogue_index = 0
                            else:
                                dialogue_text = dialogue.desk_dialogue[current_dialogue_index]
                    if player_instance.player_rect.colliderect(kyle_rect) and current_room == 8:
                        if not dialogue_active:
                            dialogue_active = True
                            dialogue_text = random.choice(dialogue.kyle_dialogue)
                            dialogue_position = dialogue.dialogue_positions["kyle"]
                        else:
                            dialogue_active = False

        if current_room == 9:
            for obj in rooms[9]["objects"]:
                image_rect = pygame.Rect(obj["x"], obj["y"], obj["size"], obj["size"])
                if obj.get("moving", False):
                    obj["x"] += obj["speed"] * obj["direction"]
                    if obj["x"] <= 0 or obj["x"] >= screen_width - obj["size"]:
                        obj["direction"] *= -1
                    screen.blit(obj["image"], (obj["x"], obj["y"]))
                if player_instance.player_rect.colliderect(image_rect):
                    player_instance = player.Player(640, 648)

        keys = pygame.key.get_pressed()
        old_player_pos = player_instance.update(dt, keys)

        screen.fill(rooms[current_room]["color"])

        if current_room == 3:
            pygame.mixer.music.load('sound/city.mp3')
            pygame.mixer.music.play(-1)
        if current_room == 5:
            pygame.mixer.music.stop()
        if current_room == 7:
            pygame.mixer.music.load('sound/car.mp3')
            pygame.mixer.music.play(-1)

        if "objects" in rooms[current_room]:
            for obj in rooms[current_room]["objects"]:
                obj_rect = obj["image"].get_rect(center=(obj["x"], obj["y"]))
                screen.blit(obj["image"], obj_rect)

        for door in rooms[current_room]["doors"]:
            door_image = rooms[current_room]["door_image"]
            door_rect.center = (door["x"], door["y"])
            screen.blit(door_image, door_rect)
            if abs(player_instance.player_pos.x - door["x"]) < 20 and abs(player_instance.player_pos.y - door["y"]) < 20:
                required_item = door.get("required_item")
                if required_item:
                                if any(item["name"] == required_item for item in player_inventory):
                                    door_open_sound.play()
                                    next_room = door["next_room"]
                                    if next_room not in visited_rooms:
                                        transition_text = rooms[next_room].get("transition_text", "Ian's Dorm")
                                        print(f"Transitioning to room {next_room} at position ({door['entry_x']}, {door['entry_y']})")
                                        screen.fill((0, 0, 0))
                                        text_surface = font.render(transition_text, True, (255, 255, 255))
                                        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
                                        screen.blit(text_surface, text_rect)
                                        pygame.display.flip()
                                        pygame.time.wait(5000)
                                        visited_rooms.add(next_room)
                                    player_instance.player_pos.x = door["entry_x"]
                                    player_instance.player_pos.y = door["entry_y"]
                                    current_room = next_room
                                    transitioning_to_new_room = True
                                else:
                                    dialogue_surface = font.render(f"The door is locked. You need a {required_item}!", True, (255, 0, 0))
                                    screen.blit(dialogue_surface, (screen_width // 2 - 100, screen_height - 50))

                else:
                    door_open_sound.play()
                    next_room = door["next_room"]
                    if next_room not in visited_rooms:
                        transition_text = rooms[next_room].get("transition_text", "Ian's Dorm")
                        print(f"Transitioning to room {next_room} at position ({door['entry_x']}, {door['entry_y']})")
                        screen.fill((0, 0, 0))
                        text_surface = font.render(transition_text, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
                        screen.blit(text_surface, text_rect)
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        visited_rooms.add(next_room)
                    player_instance.player_pos.x = door["entry_x"]
                    player_instance.player_pos.y = door["entry_y"]
                    current_room = next_room
                    transitioning_to_new_room = True



        if "items" in rooms[current_room]:
            for item in rooms[current_room]["items"][:]:
                item_rect = item["image"].get_rect(center=(item["x"], item["y"]))
                screen.blit(item["image"], item_rect)
                if player_instance.player_rect.colliderect(item_rect):
                    item_name = item["name"]
                    dialogue_surface = font.render(f"Do you want the {item_name}?", True, (255, 0, 0))
                    screen.blit(dialogue_surface, (screen_width // 2 - 100, screen_height - 50))
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_y] or keys[pygame.K_RETURN] or keys[pygame.K_e]:
                        key_pickup_sound.play()
                        player_inventory.append(item)
                        rooms[current_room]["items"].remove(item)

        if not transitioning_to_new_room and "objects" in rooms[current_room]:
            for obj in rooms[current_room]["objects"]:
                obj_rect = obj["image"].get_rect(center=(obj["x"], obj["y"]))
                if obj["solid"] and player_instance.player_rect.colliderect(obj_rect):
                    player_instance.player_pos = old_player_pos
                    player_instance.player_rect.center = player_instance.player_pos

        if dialogue_active:
            dialogue_surface = font.render(dialogue_text, True, (0, 0, 0))
            screen.blit(dialogue_surface, dialogue_position)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dialogue_active = False
        if dialogue_active and current_room == 0:
            dialogue_surface = font.render(dialogue_text, True, (255, 255, 255))
            screen.blit(dialogue_surface, dialogue_position)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dialogue_active = False

        player_instance.draw(screen)

        inventory.draw_inventory(screen, screen_width, screen_height, inventory_active, player_inventory)


        if dev_mode:
            if current_room == 1:
                pygame.draw.rect(screen, (255, 0, 0), wayne_rect, 2)
            if current_room == 5:
                pygame.draw.rect(screen, (255, 0, 0), car_rect, 2)
            if current_room == 6:
                pygame.draw.rect(screen, (255, 0, 0), jaden_rect, 2)
            if current_room == 0:
                pygame.draw.rect(screen, (255, 0, 0), poster_rect, 2)
                pygame.draw.rect(screen, (255, 0, 0), mattress_rect, 2)
            if current_room == 7:
                pygame.draw.rect(screen, (255, 0, 0), jamian_rect, 2)
                pygame.draw.rect(screen, (255, 0, 0), desk_rect, 2)
            if current_room == 8:
                pygame.draw.rect(screen, (255, 0, 0), kyle_rect, 2)
                
            coordinates_text = font.render(
                f"Player: ({player_instance.player_pos.x:.2f}, {player_instance.player_pos.y:.2f})", True, "white"
            )
            coordinates_rect = coordinates_text.get_rect(topleft=(10, 10))
            screen.blit(coordinates_text, coordinates_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
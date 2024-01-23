import pygame
import sys

from utils.get_number_of_levels import get_number_of_levels
from utils.load_image import load_image
from utils.load_level import load_level
from utils.terminate import terminate

from scenes.start_screen import start_screen
from scenes.level_choice_screen import level_choice_screen

from labyrinth.labyrith_generation import Labyrinth, level_view_of_the_matrix

pygame.init()

FPS = 50
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 550, 550
TILE_WIDTH = TILE_HEIGHT = 50
NUMBER_OF_LEVELS = get_number_of_levels()
IS_COOLDOWN = False
screen = pygame.display.set_mode(SIZE)


tile_images = {
    'wall': load_image('stone.png'),
    'empty': load_image('parquet.png'),
    'finish': load_image('ladder.png')
}
player_image = load_image('character.png')
player_image_states = {'direction': 'RIGHT', 'stepped': False}


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '~':
                Tile('empty', x, y)
                Tile('finish', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.x = self.rect.x // TILE_WIDTH   # положение игрока по X (в клетках)
        self.y = self.rect.y // TILE_HEIGHT  # положение игрока по Y (в клетках)

    def move(self, move_direction):
        global MAP

        def left():
            if MAP[self.y][self.x - 1] != '#':
                for line_number in range(len(MAP)):
                    self.map_shift('RIGHT', line_number)
                    self.change_at_to_dot(line_number)
                self.character_animate('LEFT')
                self.set_at_by_x_and_y()

        def right():
            if MAP[self.y][self.x + 1] != '#':
                for line_number in range(len(MAP)):
                    self.map_shift('LEFT', line_number)
                    self.change_at_to_dot(line_number)
                self.character_animate('RIGHT')
                self.set_at_by_x_and_y()

        def up():
            if MAP[self.y - 1][self.x] != '#':
                self.map_shift('DOWN')
                for line_number in range(len(MAP)):
                    self.change_at_to_dot(line_number)
                self.set_at_by_x_and_y()

        def down():
            if MAP[self.y + 1][self.x] != '#':
                self.map_shift('UP')
                for line_number in range(len(MAP)):
                    self.change_at_to_dot(line_number)
                self.set_at_by_x_and_y()

        move_direction_dict = {
            'LEFT': left,
            'RIGHT': right,
            'UP': up,
            'DOWN': down
        }

        move_direction_dict[move_direction]()

        # print('-' * 15)
        # print(*(''.join(row) for row in MAP), sep='\n')

    @staticmethod
    def map_shift(map_shift_direction, i=None):
        def left():
            global player_image
            MAP[i] = MAP[i][1:] + MAP[i][0]

        def right():
            global player_image
            MAP[i] = MAP[i][-1] + MAP[i][:-1]

        def up():
            global MAP
            MAP = MAP[1:] + [MAP[0]]

        def down():
            global MAP
            MAP = [MAP[-1]] + MAP[:-1]

        map_shift_direction_dict = {
            'LEFT': left,
            'RIGHT': right,
            'UP': up,
            'DOWN': down
        }

        map_shift_direction_dict[map_shift_direction]()

    def set_at_by_x_and_y(self):
        MAP[self.y] = MAP[self.y][:self.x] + '@' + MAP[self.y][self.x + 1:]

    @staticmethod
    def change_at_to_dot(line_number):
        """
        Замена "@" на "." в строке под указанным номером.
        Меняет содержимое клетки:
        Персонаж -> пустое место.
        """
        MAP[line_number] = MAP[line_number].replace('@', '.')

    @staticmethod
    def character_animate(direction):
        global player_image

        if direction == 'LEFT':
            if player_image_states['direction'] == 'RIGHT':
                player_image = pygame.transform.flip(load_image("character.png"), True, False)
            player_image_states['direction'] = 'LEFT'
            if player_image_states['stepped'] is False:
                player_image = pygame.transform.flip(load_image("character_stepped.png"), True, False)
            else:
                player_image = pygame.transform.flip(load_image("character.png"), True, False)
        elif direction == 'RIGHT':
            if player_image_states['direction'] == 'LEFT':
                player_image = load_image("character.png")
            player_image_states['direction'] = 'RIGHT'
            if player_image_states['stepped'] is False:
                player_image = load_image("character_stepped.png")
            else:
                player_image = load_image("character.png")
                
        player_image_states['stepped'] = not player_image_states['stepped']


start_screen(WIDTH, HEIGHT, FPS, screen, clock)
selected_level_number = level_choice_screen(screen)
MAP = None

if selected_level_number + 1 < NUMBER_OF_LEVELS:
    try:
        MAP = load_level(f'map{selected_level_number + 1}.txt', 5, 5)
    except FileNotFoundError:
        print('Такого файла не существует!')
        sys.exit()
else:
    labyrinth = Labyrinth(20, 20)
    level_view_of_the_matrix(labyrinth.create_labyrinth())
    MAP = load_level('map_generated.txt', 5, 5)

vignette_image = load_image('vignette.png')
player = None
running = True
while running:
    WIDTH, HEIGHT = pygame.display.get_window_size()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()

    keys = pygame.key.get_pressed()

    if not IS_COOLDOWN:
        if keys[pygame.K_LEFT]:
            player.move('LEFT')
            IS_COOLDOWN = True
        if keys[pygame.K_RIGHT]:
            player.move('RIGHT')
            IS_COOLDOWN = True
        if keys[pygame.K_UP]:
            player.move('UP')
            IS_COOLDOWN = True
        if keys[pygame.K_DOWN]:
            player.move('DOWN')
            IS_COOLDOWN = True
    else:
        pygame.time.wait(200)
        IS_COOLDOWN = False

    player, level_x, level_y = generate_level(MAP)
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    screen.blit(vignette_image, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)

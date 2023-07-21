import pygame
from settings import *
from items import all_items
import os
from ImageTools import set_image, load_image
from BaseCharacter import SuperBaseCharacter
from Panels import *
import Player_stats


class Player(SuperBaseCharacter):
    moveset_atlas = pygame.Surface((0, 0))
    movesets_pose = dict()

    def __init__(self, x, y):
        self.folder = characters_folder + 'Hero'
        file_names = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]
        self.moveset_atlas = pygame.Surface((0, 0)).convert_alpha()
        moveset_poses = dict()
        self.movesets_poses["Hero"] = moveset_poses
        self.speed = 0  # скорость игрока с которой он двигается
        self.inventory = [all_items['apple'], all_items['apple'], all_items['bat']]
        self.player_commands = None
        self.health = 99
        for file_name in file_names:
            if file_name[-3:] == 'png':
                moveset_image = load_image(self.folder + '/' + file_name, 4)
                moveset_poses[file_name[:-4]] = pygame.Rect(self.moveset_atlas.get_width(), 0, moveset_image.get_width(), moveset_image.get_height())
                self.moveset_atlas = set_image(self.moveset_atlas, moveset_image)

        super().__init__("Hero", x, y, "hero")
        self.damage_timer = 0

    def execute_commands(self):
        for command in self.player_commands:
            if command.type == pygame.KEYUP:
                if command.key == pygame.K_LEFT:
                    pass
            if command.type == pygame.KEYDOWN or command.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.speed = speed
                    self.vel = LEFT
                    self.sprite_col = 1
                    self.set_current_moveset("walk")
                    self.set_current_sprite((self.sprite_col, self.sprite_row))
                    self.frametimer = 0
                    self.current_frame = 0

                elif keys[pygame.K_d]:
                    self.speed = speed
                    self.vel = RIGHT
                    self.sprite_col = 2
                    self.set_current_moveset("walk")
                    self.set_current_sprite((self.sprite_col, self.sprite_row))
                    self.frametimer = 0
                    self.current_frame = 0

                elif keys[pygame.K_w]:
                    self.speed = speed
                    self.vel = UP
                    self.sprite_col = 0
                    self.set_current_moveset("walk")
                    self.set_current_sprite((self.sprite_col, self.sprite_row))
                    self.frametimer = 0
                    self.current_frame = 0

                elif keys[pygame.K_s]:
                    self.speed = speed
                    self.vel = DOWN
                    self.sprite_col = 3
                    self.set_current_moveset("walk")
                    self.set_current_sprite((self.sprite_col, self.sprite_row))
                    self.frametimer = 0
                    self.current_frame = 0

                elif not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
                    self.stand(self.vel)
                    self.speed = 0
                    self.frametimer = 0

        if self.moveset_name == "walk":
            self.move()

    def tp(self, x, y):
        pass

    def set_player_commands(self, keys):
        self.player_commands = keys

    def set_damage_timer(self, time):
        self.damage_timer = time

    def timer_tick(self):
        if self.damage_timer >= 0:
            self.damage_timer -= dt.dt

    def get_damage(self, damage, state=False):
        if self.damage_timer <= 0:
            self.health -= damage
            self.set_damage_timer(0.5)
        if self.health <= 0:
            exit(0)

    def get_item_by_index(self, index):
        if len(self.inventory) != 0:
            return self.inventory[index]
        return None

    def load_template_moveset(self):
        file_names = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]
        moveset_atlas = pygame.Surface((0, 0)).convert_alpha()
        moveset_poses = dict()
        for file_name in file_names:
            if file_name[-3:] == 'png':
                moveset_image = pygame.image.load(self.folder + '/' + file_name).convert_alpha()
                moveset_poses[file_name[:-4]] = pygame.Rect(self.moveset_atlas.get_width(), 0, moveset_image.get_width(), moveset_image.get_height())
                moveset_atlas = set_image(self.moveset_atlas, moveset_image)
        self.movesets_poses["Hero"] = moveset_poses
        return moveset_atlas


file_names = [f for f in os.listdir(characters_folder + 'Hero') if os.path.isfile(os.path.join(characters_folder + 'Hero', f))]
moveset_atlas = pygame.Surface((0, 0)).convert_alpha()
movesets_pose = dict()
for file_name in file_names:
    if file_name[-3:] == 'png':
        moveset_image = pygame.image.load(characters_folder + 'Hero' + '/' + file_name).convert_alpha()
        movesets_pose[file_name[:-4]] = pygame.Rect(moveset_atlas.get_width(), 0, moveset_image.get_width(), moveset_image.get_height())
        moveset_atlas = set_image(moveset_atlas, moveset_image)

Player.movesets_poses = {"Hero": movesets_pose}
textures.update_texture(moveset_atlas, Player.source_id)

# player = Player(2002*4, 1629*4)
player = Player(896, 320)
# player = Player(60 * 64, 63 * 64)
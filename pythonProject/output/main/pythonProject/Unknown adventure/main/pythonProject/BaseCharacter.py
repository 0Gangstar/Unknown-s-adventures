import pygame

import game_functions
from settings import *
from Sprite import ActiveSprite
characters = pygame.sprite.Group()
from numpy import array, float32
from pygame.math import Vector2
from replics import all_replices, all_properties
from Panels import dialog_menu, DialogWindow
from ImageTools import get_obstacle

import Player_stats
from game_functions import game_events
from Events import events, Events
from items import all_items
def get_moveset_by_command_name():
    pass


class SuperBaseCharacter(ActiveSprite):
    folder = characters_folder
    source_id = 5
    movesets_poses = dict()  # словарь где ключ - имя шаблона, а значение - словарь с положениями текстур мувсетов
    group = None

    def __init__(self, template_name, x=300, y=300, name=None):  #TODO
        self.folder = self.folder + f'{template_name}/'
        self.template_name = template_name
        self.char_name = name
        self.sprite_width, self.sprite_height = 64, 64

        self.moveset_name = "stand"  # имя текущего мувсета для персонажа TODO (мб не надо)
        self.moveset_texture_pos = self.get_moveset_pos(self.moveset_name)  # положение на атласе текущей текстуры мувсета для персонажа
        self.template = movesets_scheme_by_name[self.moveset_name]  # текущий шаблон мувсета для персонажа TODO (мб не надо)
        self.moveset_size = movesets_size_by_name[self.moveset_name]

        self.sprite_width, self.sprite_height = self.moveset_texture_pos.width / self.moveset_size[0], self.moveset_texture_pos.height / self.moveset_size[1]
        self.sprite_row, self.sprite_col = 0, 0

        self.timer = False
        self.time = 0
        self.damage_timer = 0

        super().__init__(self.get_sprite_texture_pos(standing_template["down"]), x, y, characters)
        self.convert_texture_pos()

        self.hit_polygon = pygame.Rect(self.rect.left, int(self.rect.top + self.rect.height * 0.75), self.rect.width, int(self.rect.height * 0.25))
        self.hit_polygon_x = 0  # Положение относительно верхней левой точки игрока
        self.hit_polygon_y = self.rect.height - self.hit_polygon.height

        self.interaction_box_width = int(self.hit_polygon.width / 2) * 2
        self.interaction_box_height = int(self.hit_polygon.width)
        self.pos = Vector2(*self.pos)
        self.speed = 0
        self.vel = DOWN  # вектро указывающий, куда движется персонаж

        self.frametimer = 0
        self.current_frame = 0
        # print(self.texture_pos, 'sas')

    def set_speed(self, speed):
        self.speed = speed

    def get_moveset_pos(self, name):
        return self.movesets_poses[self.template_name][name]

    def get_sprite_texture_pos(self, pos):  # заменят текущий спрайт на новый
        return pygame.Rect((self.moveset_texture_pos.x + pos[0] * self.sprite_width,
                            self.moveset_texture_pos.y + pos[1] * self.sprite_height,
                            self.sprite_width, self.sprite_height))
        # self.convert_texture_pos()

    def set_current_moveset(self, moveset_name):  # меняет используемый мувсет на новый и сразу ещё меняет спрайт на новый из нового мувсета
        if self.moveset_name != moveset_name:
            self.moveset_name = moveset_name
            self.moveset_texture_pos = self.movesets_poses[self.template_name][moveset_name]
            moveset_size = movesets_size_by_name[moveset_name]
            self.moveset_size = moveset_size
            self.sprite_width, self.sprite_height = self.moveset_texture_pos.width / moveset_size[0], self.moveset_texture_pos.height / moveset_size[1]
            self.set_current_sprite((3, 0))

    def set_current_sprite(self, pos):  # заменят текущий спрайт на новый
        self.update_texture_pos(pygame.Rect((self.moveset_texture_pos.x + pos[0] * self.sprite_width,
                            self.moveset_texture_pos.y + pos[1] * self.sprite_height,
                            self.sprite_width, self.sprite_height)))

    def set_sight_side(self, direction):  # изменяет направление спрайта и вектор движения
        self.vel = direction
        if direction is UP:
            self.sprite_row = 0
        elif direction is LEFT:
            self.sprite_row = 1
        elif direction is RIGHT:
            self.sprite_row = 2
        elif direction is DOWN:
            self.sprite_row = 3
        self.set_current_sprite((self.sprite_row, self.sprite_col))

    def stand(self, direction):
        self.moveset_name = "stand"
        if direction is DOWN:
            self.sprite_col, self.sprite_row = 3, 0
        elif direction is UP:
            self.sprite_col, self.sprite_row = 0, 0
        elif direction is LEFT:
            self.sprite_col, self.sprite_row = 1, 0
        elif direction is RIGHT:
            self.sprite_col, self.sprite_row = 2, 0

        self.set_current_moveset("stand")
        self.set_current_sprite((self.sprite_col, self.sprite_row))

        self.moveset_size = movesets_size_by_name[self.moveset_name]
        self.vel = direction

    def move(self):
        x, y = self.vel[0] * self.speed * dt.dt, self.vel[1] * self.speed * dt.dt
        self.pos[0] = round(self.pos[0] + x, 6)
        self.pos[1] = round(self.pos[1] + y, 6)
        self.hit_polygon.topleft = (self.pos[0] + self.hit_polygon_x, self.pos[1] + self.hit_polygon_y)
        self.rect.topleft = self.pos
        if self.moveset_size[1] > 1:  # ASS убрать если не пригодится
            if self.speed == 0:
                self.frametimer = 0
                last_frame = self.current_frame
                self.current_frame = 0
                if last_frame != self.current_frame:
                    self.set_current_sprite((self.sprite_col, self.current_frame))
            else:
                self.frametimer += dt.dt * sps * self.speed / default_character_speed
                last_frame = self.current_frame
                self.current_frame = int(self.frametimer) % (self.moveset_size[1] - 1) + 1
                if last_frame != self.current_frame:
                    self.set_current_sprite((self.sprite_col, self.current_frame))

    def move_by_hit_polygon(self, deltax, deltay):
        self.hit_polygon.topleft = (deltax, deltay)
        self.rect.topleft = self.hit_polygon.x - self.hit_polygon_x, self.hit_polygon.y - self.hit_polygon_y
        self.pos = list(self.rect.topleft)

    def move_ip_by_hit_polygon(self, deltax, deltay):
        self.hit_polygon.topleft = (self.hit_polygon.left + deltax, self.hit_polygon.top + deltay)
        self.rect.topleft = self.hit_polygon.x - self.hit_polygon_x, self.hit_polygon.y - self.hit_polygon_y
        self.pos = list(self.rect.topleft)

    def move_by_rect(self, deltax, deltay):
        self.rect.move(deltax, deltay)
        self.hit_polygon.topleft = (self.rect.x + self.hit_polygon_x, self.rect.y + self.hit_polygon_y)
        self.pos = list(self.rect.topleft)

    def move_ip(self, x, y):
        self.pos[0] = round(self.pos[0] + x, 6)
        self.pos[1] = round(self.pos[1] + y, 6)
        self.rect.topleft = self.pos
        self.hit_polygon.topleft = (self.rect.x + self.hit_polygon_x, self.rect.y + self.hit_polygon_y)

    def get_moveset_sprite_texture_poses(self, col, row):
        moveset_pos = self.movesets_poses[self.template_name][self.moveset_name]
        moveset_size_by_sprites = movesets_size_by_name[self.moveset_name]
        sprite_width, sprite_height = moveset_pos.width / moveset_size_by_sprites[0], moveset_pos.height / moveset_size_by_sprites[1]
        sprite_texture_pos = (moveset_pos.x + col * sprite_width, moveset_pos.y + row * sprite_height, sprite_width, sprite_height)
        return sprite_texture_pos

    def get_texture_pos(self, sprite_name):
        # moveset_x += movesets_scheme_by_name[self.moveset_name][sprite_name]
        pass

    def get_interaction_box(self):
        if self.vel is UP:
            return pygame.Rect(self.hit_polygon.left, self.hit_polygon.top - self.interaction_box_width,
                               self.hit_polygon.width, self.interaction_box_width)
        elif self.vel is DOWN:
            return pygame.Rect(self.hit_polygon.left, self.hit_polygon.bottom,
                               self.hit_polygon.width, self.interaction_box_width)
        elif self.vel is RIGHT:
            return pygame.Rect(self.hit_polygon.right, self.hit_polygon.top,
                               self.interaction_box_width, self.hit_polygon.height)
        elif self.vel is LEFT:
            return pygame.Rect(self.hit_polygon.left - self.interaction_box_width,
                               self.hit_polygon.top, self.interaction_box_width, self.hit_polygon.height)

    def interaction(self, target):
        pass


class BaseCharacter2(SuperBaseCharacter):
    source_id = 5
    characters_folder = characters_folder
    command_movesets = {"spawn": "walk", "repeat": None, "wait": None, "walk": "walk", "stand": "stand", "rotate": "walk"}
    group = characters

    templates_by_name = dict()  # ключ - имя челика, а значение - его шаблон персонажа
    npcs_commands = dict()  # ключ - имя челика, а значение - его набор команд

    def __init__(self, x, y, name, properties=None):
        super().__init__(self.templates_by_name[name], x, y, name)
        self.properties = properties if properties else []
        for i in range(len(self.properties)):  # TODO
            self.properties[i] = all_properties[self.properties[i]].copy()

        self.commands = self.npcs_commands[name]
        self.set_current_moveset("walk")
        self.active_command = None  # команда, которую персононаж исполняет в текущий момент
        self.active_command_params = None  # параметры которые загружаются в active_command
        self.last = 0

        self.can_move = True

        self.frametimer = 0
        self.current_frame = 0
        self.current_property = 0

        self.cycle = False
        self.cycle_start = 0

    def move_by_hit_polygon(self, deltax, deltay):
        self.hit_polygon.topleft = (deltax, deltay)
        self.rect.topleft = self.hit_polygon.x - self.hit_polygon_x, self.hit_polygon.y - self.hit_polygon_y
        self.pos = list(self.rect.topleft)

    def move_ip(self, x, y):
        self.pos[0] = round(self.pos[0] + x, 6)
        self.pos[1] = round(self.pos[1] + y, 6)
        self.rect.topleft = self.pos
        self.hit_polygon.topleft = (self.rect.x + self.hit_polygon_x, self.rect.y + self.hit_polygon_y)

    def count_time(self, waiting_time):
        if waiting_time - dt.dt > 0:
            return [waiting_time - dt.dt]
        self.active_command = None
        return None

    def move_to_place(self, place_pos):
        self.move()
        dx, dy = place_pos[0] - self.pos[0], place_pos[1] - self.pos[1]
        self.frametimer += dt.dt * sps * self.speed / 200
        last_frame = self.current_frame
        self.current_frame = int(self.frametimer % 4) + 1
        if last_frame != self.current_frame:
            self.set_current_sprite((self.sprite_col, self.current_frame))
        if dx * self.vel[0] <= 0 and dy * self.vel[1] <= 0:
            self.move_ip(dx, dy)
            self.speed = 0
            self.active_command = None
            self.set_current_sprite((self.sprite_col, 0))
            return None
        return [place_pos]

    def execute_commands(self):

        if self.active_command is not None:
            self.active_command_params = self.active_command(*self.active_command_params)
        else:
            for i in range(self.last + 1, len(self.commands)):
                if self.commands[i][0:5] == "stand":
                    a = self.commands[i].split('(')
                    b = a[1].split(')')
                    direction = b[0].split()[0].lower()
                    self.stand(Directions[direction])
                    self.last = i
                    break
                elif self.commands[i][0:4] == 'wait':
                    a = self.commands[i].split('(')
                    b = a[1].split(')')
                    wait_time = int(b[0].split()[0])
                    self.active_command = self.count_time
                    self.active_command_params = [wait_time]  # TODO
                    self.last = i
                    break
                elif self.commands[i][0:4] == 'walk':
                    self.set_current_moveset("walk")
                    a = self.commands[i].split('(')
                    b = a[1].split(')')
                    distance = int(b[0])
                    self.active_command = self.move_to_place

                    if self.speed == 0:
                        self.set_speed(default_character_speed)

                    place_x = self.pos[0] + distance * map_tilewidth * self.vel[0]
                    place_y = self.pos[1] + distance * map_tilewidth * self.vel[1]
                    self.active_command_params = [(place_x, place_y)]
                    self.last = i
                    break
                elif self.commands[i][:9] == "set_speed":
                    a = self.commands[i].split('(')
                    b = a[1].split(')')
                    walk_speed = int(b[0])
                    self.set_speed(walk_speed)
                elif self.commands[i][:6] == "repeat":
                    self.cycle_start = i
                    self.cycle = True
                    self.last = i
                if self.cycle is True and '}' in self.commands[i]:
                    self.last = self.cycle_start




    def interaction(self, target=None):
        for i in range(len(self.properties)):
            property = self.properties[i]
            if property[1] == 0:
                continue
            property_condition = property[0]
            if property_condition is not None:
                if property_condition[0][:9] == "have_item":
                    item_name = property_condition[0].split('(')[1].split(')')[0]
                    if game_functions.have_item(item_name) is not property_condition[1]:
                        continue
            mini_props = []
            for mini_prop in property[2]:
                if mini_prop[0] == "replic":
                    mini_props.append([game_functions.talk, all_replices[mini_prop[1]], 0])
                elif mini_prop[0] == "get_item":
                    mini_props.append([game_functions.give_item, *mini_prop[1:], 0])
            game_events.add_chain_events(mini_props)
            self.properties[i][1] -= 1
            break
        # if len(self.properties) == 0:
        #     return None
        # print('ass')
        # prop = properties[self.properties[0]]
        # if prop[1] == 0:
        #     self.properties.pop(0)
        #     self.current_property = 0
        # else:
        #     # if self.current_property == len(prop[2]):
        #     #     self.current_property = 0
        #     #     prop[1] -= 1
        #     # else:
        #     #
        #     #     mini_prop = prop[2][self.current_property]
        #     #     if mini_prop[0] == "replic":
        #     #         game_events.add_event(self.talk, all_replices[mini_prop[1]], 0)
        #     #
        #     #     if mini_prop[0] == "get_item":
        #     #         game_events.add_event(self.give_item, *mini_prop[1:], 0)
        #     #     self.current_property += 1
        #
        #     mini_props = []
        #     for mini_prop in prop[2]:
        #         if mini_prop[0] == "replic":
        #             mini_props.append([self.talk, all_replices[mini_prop[1]], 0])
        #
        #         elif mini_prop[0] == "get_item":
        #             mini_props.append([self.give_item, *mini_prop[1:], 0])
        #     prop[1] -= 1
        #     game_events.add_chain_events(mini_props)

    def talk(self, text, state=0):
        if Events.text_event is False:
            if state == 0:
                DialogWindow.set_dialog_text(*text)
                dialog_menu.open()
                return 1
            return 0
        return 1

    def give_item(self, item_name, count=1, state=0):
        if Events.text_event is False:
            if state == 0:
                item = all_items[item_name]
                count = int(count)
                Player_stats.inventory.extend([item for _ in range(count)])
                DialogWindow.set_dialog_text(f"You got a {item.name}")
                dialog_menu.open()
            else:
                return 0
        return 1

    @staticmethod
    def get_moveset_poses_by_name(name):
        return BaseCharacter2.movesets_poses[name]

    @staticmethod
    def get_npc_template_by_name(name):
        return BaseCharacter2.templates[name]


# class BaseCharacter(ActiveSprite):
#     source_id = 5
#     characters_folder = characters_folder
#     sprite_poses = {'up': (0, 0), 'left': (1, 0), 'right': (2, 0), 'down': (3, 0)}
#     command_movesets = {"spawn": "walk", "repeat": None, "wait": None, "walk": "walk", "stand": "stand", "rotate": "walk"}
#     character_names_count = dict()
#     group = characters
#
#     def __init__(self, name, x, y, movesets_positions, current_moveset_name="stand", current_sprite_name="down"):
#         print('sadas')
#         self.moveset_poses = movesets_positions  # позиции текстур каждого мувсета, которые использует персонаж
#         self.current_moveset_name = current_moveset_name
#         self.current_sprite_name = current_sprite_name
#         self.vel = (0, 1)
#         self.speed = 0
#         self.folder = BaseCharacter.characters_folder + f'{name}/'
#         self.character_names_count[name] = self.character_names_count.get(name, 0) + 1
#
#         self.commands = []
#         self.timer = False
#         self.time = 0
#         self.active_command = None
#         self.active_command_params = None
#         self.last = 0
#
#         if self.character_names_count[name] > 1:
#             self.name = name + '_' + str(self.character_names_count[name])
#         else:
#             self.name = name
#
#         self.damage_timer = 0
#         self.activities_file = open(self.folder + 'activities.txt', 'r').readlines()
#         self.moveset_parameters = dict()
#         parameters_find = False
#         activity = ""
#         parameters = ['', '']  # name of activity and width and height of each sprite of activity
#         cnt = 0
#         for line in self.activities_file:
#             line = line.strip()
#             if parameters_find:
#                 if 'sprite_width' in line:
#                     cnt += 1
#                     parameters[0] = int(line.split()[1])
#                 elif 'sprite_height' in line:
#                     cnt += 1
#                     parameters[1] = int(line.split()[1])
#                 if cnt == 2:
#                     self.moveset_parameters[activity] = parameters
#                     parameters = ['', '']
#                     cnt = 0
#                     parameters_find = False
#             else:
#                 for obj in line.split():
#                     if obj != '':
#                         parameters_find = True
#                         if obj[-1] == ':':
#                             activity = obj[:-1]
#                         else:
#                             activity = obj
#                         break
#
#         self.moveset_texture_pos = self.moveset_poses[current_moveset_name]  # положение текущего мувсета
#         self.sprite_width, self.sprite_height = self.moveset_parameters[current_moveset_name]
#         texture_pos = pygame.Rect(self.sprite_poses[current_sprite_name][0] * self.sprite_width + self.moveset_texture_pos.x,
#                                   self.sprite_poses[current_sprite_name][1] * self.sprite_height + self.moveset_texture_pos.y,
#                                   self.sprite_width, self.sprite_height)
#         super().__init__(texture_pos, x, y, characters)
#         self.hit_polygon = pygame.Rect(self.rect.left, int(self.rect.top + self.rect.height * 0.75), self.rect.width, int(self.rect.height * 0.25))
#         self.hit_polygon_x = 0  # Положение относительно верхней левой точки игрока
#         self.hit_polygon_y = self.rect.height - self.hit_polygon.height
#         self.interaction_box_width = int(self.hit_polygon.width / 2)
#         self.interaction_box_height = int(self.hit_polygon.width)
#
#     def get_interaction_box(self):
#         if self.vel == (0, -1):
#             return pygame.Rect(self.hit_polygon.left, self.hit_polygon.top - self.interaction_box_width,
#                                self.interaction_box_height, self.interaction_box_width)
#         elif self.vel == (0, 1):
#             return pygame.Rect(self.hit_polygon.left, self.hit_polygon.bottom,
#                                self.interaction_box_height, self.interaction_box_width)
#         elif self.vel == (-1, 0):
#             return pygame.Rect(self.hit_polygon.right - self.interaction_box_width, int(self.hit_polygon.centery - self.interaction_box_height / 2),
#                                self.interaction_box_width, self.interaction_box_height)
#         elif self.vel == (1, 0):
#             return pygame.Rect(self.hit_polygon.left, int(self.hit_polygon.centery - self.interaction_box_height / 2),
#                                self.interaction_box_width, self.interaction_box_height)
#
#     def set_current_moveset(self, moveset_name, sprite_name):  # меняет используемый мувсет на новый и сразу ещё меняет спрайт на новый из нового мувсета
#         if self.current_moveset_name != moveset_name:
#             self.current_moveset_name = moveset_name
#             self.current_sprite_name = sprite_name
#             self.moveset_texture_pos = self.moveset_poses[moveset_name]
#             self.sprite_width, self.sprite_height = self.moveset_parameters[moveset_name]
#         self.set_current_sprite(sprite_name)
#
#     def set_current_sprite(self, pos):  # заменят текущий спрайт на новый
#         self.texture_pos = pygame.Rect((self.moveset_texture_pos.x + pos[0] * self.sprite_width,
#                             self.moveset_texture_pos.y + pos[1] * self.sprite_height,
#                             self.sprite_width, self.sprite_height))
#         self.convert_texture_pos()
#
#     def set_sight_side(self, direction):  # изменяет направление, куда герой будет выполнять действие
#         if direction == 'up':
#             self.vel = UP
#         elif direction == 'down':
#             self.vel = DOWN
#         elif direction == 'left':
#             self.vel = LEFT
#         elif direction == 'right':
#             self.vel = RIGHT
#
#     def move(self):
#         x, y = self.vel[0] * self.speed * dt.dt, self.vel[1] * self.speed * dt.dt
#         self.pos[0] = round(self.pos[0] + x, 6)
#         self.pos[1] = round(self.pos[1] + y, 6)
#         self.hit_polygon.topleft = (self.pos[0] + self.hit_polygon_x, self.pos[1] + self.hit_polygon_y)
#         self.rect.topleft = self.pos
#         # self.collide_with_characters()  # TODO
#
#     def move_by_hit_polygon(self, deltax, deltay):
#         self.hit_polygon.topleft = (deltax, deltay)
#         self.rect.topleft = self.hit_polygon.x - self.hit_polygon_x, self.hit_polygon.y - self.hit_polygon_y
#         self.pos = list(self.rect.topleft)
#
#     def move_by_rect(self, deltax, deltay):
#         self.rect.move(deltax, deltay)
#         self.hit_polygon.topleft = (self.rect.x + self.hit_polygon_x, self.rect.y + self.hit_polygon_y)
#         self.pos = list(self.rect.topleft)
#
#     def move_ip(self, x, y):
#         self.pos[0] = round(self.pos[0] + x, 6)
#         self.pos[1] = round(self.pos[1] + y, 6)
#         self.rect.topleft = self.pos
#         self.hit_polygon.topleft = (self.rect.x + self.hit_polygon_x, self.rect.y + self.hit_polygon_y)
#
#     # def colliderect(self, sprite):
#     #     if sprite.hit_polygon is not None and self.hit_polygon is not None:
#     #         if self.hit_polygon.colliderect(sprite.hit_polygon):
#     #             return True
#     #         return False
#
#     def count_time(self, waiting_time):
#         if waiting_time - dt.dt > 0:
#             return [waiting_time - dt.dt]
#         self.active_command = None
#         return None
#
#     def move_to_place(self, place_pos):
#         dx, dy = place_pos[0] - self.pos[0], place_pos[1] - self.pos[1]
#         if dx * self.vel[0] <= 0 and dy * self.vel[1] <= 0:
#             self.move_ip(dx, dy)
#             self.speed = 0
#             self.active_command = None
#             return None
#         return [place_pos]
#
#     def stand(self, direction):  # ставит героя в положение стоя в указанную сторону и меняет направление взгляда
#         self.set_current_moveset('walk', self.sprite_poses[direction])
#         self.set_sight_side(direction)
#
#     def execute_commands(self):
#
#         if self.active_command is not None:
#             self.active_command_params = self.active_command(*self.active_command_params)
#         else:
#             for i in range(self.last + 1, len(self.commands)):
#                 if self.commands[i][0:5] == "stand":
#                     a = self.commands[i].split('(')
#                     b = a[1].split(')')
#                     direction = b[0].split()[0].lower()
#                     self.stand(direction)
#                     self.last = i
#                     break
#                 elif self.commands[i][0:4] == 'wait':
#                     a = self.commands[i].split('(')
#                     b = a[1].split(')')
#                     wait_time = int(b[0].split()[0])
#                     self.active_command = self.count_time
#                     self.active_command_params = [wait_time]  # TODO
#                     self.last = i
#                     break
#                 elif self.commands[i][0:4] == 'walk':
#                     a = self.commands[i].split('(')
#                     b = a[1].split(')')
#                     distance, walk_speed = map(int, b[0].split(', '))
#                     self.speed = walk_speed
#                     self.active_command = self.move_to_place
#                     place_x = self.pos[0] + distance * map_tilewidth * self.vel[0]
#                     place_y = self.pos[1] + distance * map_tilewidth * self.vel[1]
#                     self.active_command_params = [(place_x, place_y)]
#                     self.last = i
#                     break

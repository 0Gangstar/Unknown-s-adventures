import pygame
import pytmx
import os
import moderngl
import numpy as np
from math import ceil

from items import all_items
from Events import Events
from settings import *
from render_setup import *

from Sprite import ActiveSprite
from BaseCharacter import BaseCharacter2
from BaseCharacter import characters
from Player import player
from Enemy import Enemy
import Player_stats
from Textures import textures
from ImageTools import set_image


class CustomException(Exception):
    def __init__(self, message='Something wrong...'):
        # Call the base class constructor with the parameters it needs
        super(CustomException, self).__init__(message)


from Sprite import ActiveSprite
import pygame


class Objects(ActiveSprite):
    source = None
    source_id = 2
    source_size = None
    walls_obstacles = dict()
    texture_poses = dict()

    def __init__(self, map_id, x, y):
        self.gid = map_id
        self.properties = []
        super().__init__(self.get_texture_poses_by_id(map_id), x, y, location_map.all_sprites, location_map.objects)
        self.convert_texture_pos()
        for collider in self.get_obstacles_by_id(map_id):
            self.hit_polygon = pygame.Rect(round(collider.x) + x, round(collider.y) + y,
                                           round(collider.width), round(collider.height))

    def get_tile_pos(self):
        return self.pos[0] // 64, self.pos[1] // 64

    def set_sprites_pos(self, id):
        self.texture_pos = self.texture_poses[id]
        self.spite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.spite_size)
        self.rect.topleft = self.pos
        self.convert_texture_pos()

    def set_sprite_colliders(self, id):
        for collider in self.walls_obstacles[id]:
            if collider.template_name == 'bottom_layer':
                self.down_layer = pygame.Rect(collider.x + self.pos[0], collider.y + self.pos[1], collider.width,
                                              collider.height)
            elif collider.template_name is None:
                try:
                    pass
                    # self.hit_polygon = Polygon(collider.points, self.pos)
                except AttributeError:
                    self.hit_polygon = pygame.Rect(collider.x + self.pos[0], collider.y + self.pos[1], collider.width,
                                                   collider.height)

    def set_object(self, map_id):
        self.kill()
        for key, value in location_map.tmxdata.tiledgidmap.items():
            if value == map_id:
                self.__init__(key, *self.pos)
                break

    def set_texture_pos(self, map_id):
        for key, value in location_map.tmxdata.tiledgidmap.items():
            if value == map_id:
                self.texture_pos = self.texture_poses[key]
                break
        self.convert_texture_pos()

    def change_to_next(self):
        tileset = location_map.tmxdata.get_tileset_from_gid(self.gid)
        tileset_len = tileset.firstgid
        tilecount = tileset.tilecount
        new_gid = location_map.listtiles[self.gid - 1] + 1

        print(location_map.listtiles, "sad")

        if new_gid < tileset.firstgid + tileset.tilecount:
            for gid in range(len(location_map.listtiles)):
                if location_map.listtiles[gid] == new_gid:
                    new_gid = gid + 1
                    break
            self.texture_pos = self.texture_poses[new_gid]
            self.gid = new_gid
            self.convert_texture_pos()


    @staticmethod
    def set_obstacles(sprite_obstacles):
        Objects.walls_obstacles = sprite_obstacles

    @staticmethod
    def set_texture_poses(texture_position):
        Objects.texture_poses = texture_position

    @staticmethod
    def get_obstacles_by_id(gid):
        try:
            return Objects.walls_obstacles[gid]
        except KeyError:
            return []

    @staticmethod
    def get_texture_poses_by_id(gid):
        return Objects.texture_poses[gid]

    def set_properties(self, properties):
        self.properties = properties


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, object):
        self.groups = location_map.all_sprites, location_map.obstacles
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.data = object
        self.rect = pygame.Rect(object.x, object.y, object.width, object.height)
        self.pos = [object.x, object.y]
        # print(self.rect)
        self.hit_polygon = pygame.Rect(round(object.x), round(object.y), round(object.width), round(object.height))
        # self.hit_polygon = []
        # for points in self.data.points:
        #     self.hit_polygon.append([points[0], points[1]])
        # self.hit_polygon.append([self.data.points[0][0], self.data.points[0][1]])

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        self.rect.center = (x, y)


class TiledMap:
    source = None
    source_id = 1
    source_size = None

    def __init__(self, filename):
        self.map_folder = filename
        tm = pytmx.load_pygame(f"maps/{self.map_folder}/{self.map_folder}.tmx", pixelalpha=True)
        self.name = tm.filename.split('/')[1]
        self.tilewidth = tm.tilewidth
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        TiledMap.source_size = (self.width, self.height)
        self.map_rect = pygame.Rect(0, 0, self.width, self.height)
        self.texture_pos = (0, 0, 0, 0)

        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.characters.add(player)
        self.objects_map = []

        self.render()

    def render(self):
        self.all_sprites.empty()
        self.objects.empty()
        self.objects.empty()
        self.characters.empty()

        self.characters.add(player)
        map_image = pygame.Surface(self.map_rect.size).convert_alpha()

        ti = self.tmxdata.get_tile_image_by_gid
        objects_atlas = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        atlas_pos = dict()

        for tileset in self.tmxdata.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                try:
                    tile = ti(gid)
                    atlas_pos[gid] = pygame.Rect(objects_atlas.get_width(), 0, *tile.get_size())  # TODO сделать класс атласа, где изображения будут эффективно складываться
                    objects_atlas = set_image(objects_atlas, tile)
                except IndexError:
                    pass


        # for tileset in self.tmxdata.tilesets:
        #     for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
        #         try:
        #             for key, value in self.tmxdata.tiledgidmap.items():
        #                 if value == gid:
        #                     tile = ti(gid)
        #                     print(tile.get_size())
        #                     atlas_pos[gid] = pygame.Rect(objects_atlas.get_width(), 0, *tile.get_size())  # TODO сделать класс атласа, где изображения будут эффективно складываться
        #                     objects_atlas = set_image(objects_atlas, tile)
        #                     break
        #         except IndexError:
        #             pass


        # Считываю все тайлы, что есть на карте

        self.listtiles = [z for z in self.tmxdata.gidmap]  # cписок, в котором по айди объекта в pytmx можно получить его реальный айди из файла карты (хз)

        tile_obj = dict()
        for gid in atlas_pos.keys():
            properties = self.tmxdata.get_tile_properties_by_gid(gid)
            if properties is None:
                continue
            tile_obj[gid] = properties["colliders"]

        self.objects.set_obstacles(tile_obj)
        self.objects.set_texture_poses(atlas_pos)

        textures.update_texture(objects_atlas, 2)
        self.objects.source_size = objects_atlas.get_size()

        enemies = dict()
        enemies_movesets_atlas = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        enemies_movesets_poses = {}

        for object in self.tmxdata.objects:
            if object.name is not None and object.name[:5] == "enemy":
                enemy_name = object.name.split(': ')[1].strip()

                if enemy_name in enemies.keys():
                    continue

                propereties = {"vision": 0, "speed": 0, "type": "Common"}
                with open(enemy_folder + enemy_name + '/parameters.txt', "r") as file:
                    for line in file.readlines():
                        line = line.split(' = ')
                        if line[0] == 'vision' or line[0] == 'speed':
                            propereties[line[0]] = int(line[1])
                        elif line[0] == 'type':
                            propereties[line[0]] = line[1].strip()

                movesets = {}
                image = pygame.image.load(enemy_folder + enemy_name + "/stand.png")
                movesets["stand"] = movesets.setdefault("stand", pygame.Rect(enemies_movesets_atlas.get_width(), 0, *image.get_size()))
                enemies_movesets_atlas = set_image(enemies_movesets_atlas, image)
                image = pygame.image.load(enemy_folder + enemy_name + "/walk.png")
                movesets["walk"] = movesets.setdefault("walk", pygame.Rect(enemies_movesets_atlas.get_width(), 0, *image.get_size()))
                enemies[enemy_name] = propereties.copy()
                enemies_movesets_poses[enemy_name] = enemies_movesets_poses.setdefault(enemy_name, movesets)

        Enemy.source_size = enemies_movesets_atlas.get_size()

        textures.update_texture(enemies_movesets_atlas, 6)

        Enemy.movesets_poses = enemies_movesets_poses
        Enemy.property = enemies

        for object in self.tmxdata.objects:
            if object.name is not None and object.name[:5] == "enemy":
                enemy_name = object.name.split(': ')[1].strip()
                Enemy(enemy_name, object.x, object.y)

        npcs_commands = dict()
        npc_file = open(f"maps/{self.map_folder}/npcs.txt", 'r')
        lines = npc_file.readlines()
        npc_file.close()
        npc_name = None
        commands = []
        opening, closing = 0, 0
        npc_find = False
        template = None
        templates_by_name = dict()  # словарь, где ключ - имя персонажа, а значение - имя шаблона, который исп. перс
        npcs_poses = dict()
        npc_replics = dict()  # ключ - имя персонажа, а ключ - все его реплики на этой локации

        for i in range(len(lines)):
            if npc_find:
                if "spawn" in lines[i]:
                    pos = lines[i].strip().split('(')[1].split(')')[0].split(',')
                    npcs_poses[npc_name] = (int(pos[0]) * self.tilewidth, int(pos[1]) * self.tilewidth)
                elif "replics" in lines[i]:
                    line = lines[i].split('=')[1].strip()
                    replices = line.split(',')
                    for i in range(len(replices)):
                        replices[i] = replices[i].strip()
                    npc_replics[npc_name] = replices
                elif "template" in lines[i]:
                    template = lines[i].strip().split(' = ')[1]
                    continue
                elif '}' in lines[i]:
                    closing += 1
                elif '{' in lines[i]:
                    opening += 1
                if opening == closing:
                    commands.append(lines[i].strip().split('}')[0])
                    npcs_commands[npc_name] = commands.copy()
                    templates_by_name[npc_name] = template
                    npc_find = False
                else:
                    commands.append(lines[i].strip())
            else:
                if "name" in lines[i]:
                    opening, closing = 1, 0
                    line_name = lines[i][5:]
                    npc_name = npc_name.replace(' ', '')
                    commands.clear()
                    npc_find = True
                    npc_replics[npc_name] = []
                    try:
                        npcs_commands[npc_name]
                        raise CustomException(f"Имя НПС: {npc_name} использовано более одного раза")
                    except KeyError:
                        pass

        npcs_moveset_textures = player.moveset_atlas.copy()
        templates_used_movesets = dict()  # словарь где ключ - это имя шаблона, а значение - мувсеты, которые используются на этой локации
        for npc_name in npcs_commands.keys():
            template_name = templates_by_name[npc_name]
            templates_used_movesets[template_name] = templates_used_movesets.setdefault(template_name, dict())
            template_folder = characters_folder + f'{template_name}/'
            for command in npcs_commands[npc_name]:
                command_name = command.split('(')[0]
                if len(command_name) <= 1:
                    continue
                try:
                    moveset = command_name
                except KeyError:
                    moveset = None
                if moveset not in all_movesets_names:
                    continue
                if moveset in templates_used_movesets[template_name]:
                    continue
                moveset_image = pygame.image.load(template_folder + moveset + ".png").convert_alpha()
                templates_used_movesets[template_name][moveset] = pygame.Rect(npcs_moveset_textures.get_width(), 0, moveset_image.get_width(), moveset_image.get_height())
                npcs_moveset_textures = set_image(npcs_moveset_textures, moveset_image)
        BaseCharacter2.movesets_poses = templates_used_movesets
        BaseCharacter2.npcs_commands = npcs_commands.copy()
        BaseCharacter2.templates_by_name = templates_by_name

        textures.update_texture(npcs_moveset_textures, BaseCharacter2.source_id)
        for npc_name in npcs_commands.keys():
            BaseCharacter2(*npcs_poses[npc_name], npc_name, npc_replics[npc_name])

        map = [[[] for i in range(self.tmxdata.width)] for i in range(self.tmxdata.width)]
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        x_pos = x * self.tmxdata.tilewidth
                        y_pos = (y + 1) * self.tmxdata.tileheight - tile.get_size()[1]
                        map_image.blit(tile, (x_pos, y_pos))
                        if layer.name == 'Objects':
                            object = Objects(gid, x_pos, y_pos)
                            for obj_y in range(object.rect.height // self.tmxdata.tileheight):
                                if y - obj_y < 0:
                                    continue
                                for obj_x in range(object.rect.width // self.tmxdata.tilewidth):
                                    if x + obj_x == self.tmxdata.width:
                                        break
                                    map[y - obj_y][x + obj_x].append(object)


        self.objects_map = map


        for group in self.tmxdata.objectgroups:
            if group.name == 'Obstacles':
                for obs in group:
                    if obs.gid != 0:  # если gid = 0, то обстакл не связан с объектом на карте
                        x, y = int(obs.x / self.tilewidth), int(obs.y / self.tilewidth)
                        for obj in map[y][x]:
                            if obj.get_tile_pos() == (x, y):
                                if obs.name is None:
                                    continue
                                properties = obs.name.split(';')
                                for i in range(len(properties)):
                                    properties[i] = properties[i].strip().split(' ')
                                obj.set_properties(properties)
                                print(obj.properties)
                    else:
                        Obstacle(obs)
                break
        textures.update_texture(map_image, 1)
        self.texture_pos = textures.convert_texture_pos(self.map_rect, self.source_id)

    def load_level(self, filename):
        self.__init__(filename)

    def get_rect(self):
        return self.map_rect

    def get_tile(self, gid):
        return self.tmxdata.ge

    # удаляет спрайт со всех карт
    def del_sprite(self, sprite):
        pass

    def get_tile_occupancy(self, x, y):
        return self.objects_map[y][x]




location_map = TiledMap(Player_stats.current_map)

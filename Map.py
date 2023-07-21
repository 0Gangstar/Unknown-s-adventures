import pytmx
import pygame
from Textures import textures
from ImageTools import set_image


all_sprites = pygame.sprite.LayeredUpdates()
walls = pygame.sprite.Group()  # все стены
objects = pygame.sprite.Group()  # все объекты
characters = pygame.sprite.Group()


def clear_line(line):  # delete all space from text line
    new_line = ''
    text_found = False
    for symb in line:
        if symb == ' ':
            if text_found is True:
                break
        else:
            if text_found is False:
                text_found = True
            new_line += symb
    return new_line


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
        self.render()

    def render(self):
        all_sprites.empty()
        objects.empty()
        walls.empty()
        characters.empty()

        characters.add(player)
        map_image = pygame.Surface(self.map_rect.size).convert_alpha()
        objects_atlas = pygame.Surface((0, 0), pygame.SRCALPHA, 32)

        ti = self.tmxdata.get_tile_image_by_gid
        atlas_pos = dict()
        for tileset in self.tmxdata.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                try:
                    tile = ti(gid)
                    atlas_pos[gid] = pygame.Rect(objects_atlas.get_width(), 0, *tile.get_size())# TODO
                    objects_atlas = set_image(objects_atlas, tile)
                except IndexError:
                    pass

        textures.update_texture(objects_atlas, 2)
        Walls.source_size = objects_atlas.get_size()

        npcs_commands = dict()
        npc_file = open(f"maps/{self.map_folder}/npcs.txt", 'r').readlines()
        npc_name = None
        commands = []
        opening, closing = 0, 0
        npc_find = False
        for i in range(len(npc_file)):
            if npc_find:
                if '}' in npc_file[i]:
                    closing += 1
                elif '{' in npc_file[i]:
                    opening += 1
                if opening == closing:
                    commands.append(npc_file[i].strip().split('}')[0])
                    npcs_commands.setdefault(npc_name, []).append(commands.copy())
                    npc_find = False
                else:
                    commands.append(npc_file[i].strip())

            else:
                if "name" in npc_file[i]:
                    opening, closing = 1, 0
                    npc_find = True
                    line_name = npc_file[i][5:]
                    npc_name = clear_line(line_name)
                    commands.clear()

        npcs_moveset_textures = player.moveset_atlas.copy()  # атлас текстур со всеми мувстетами, которые каждый нпс использует на этой локации
        npcs_moveset_positions = dict()  # словарь, где ключ - это имя нпс и значение - это словарь, где ключ - это имя мувсета и значение - это положение этого мувсета на npcs_moveset_textures
        npcs_moveset_positions['Hero'] = player.moveset_poses
        for npc_name in npcs_commands.keys():
            npc_folder = Character.characters_folder + f'{npc_name}/'
            same_npcs_moveset_positions = []
            used_movesets = []
            for commands in npcs_commands[npc_name]:
                npc_moveset_positions = dict()
                for command in commands:
                    command_name = command.split('(')[0]
                    if len(command_name) > 1:
                        moveset = Character.command_movesets[command_name]
                        if moveset is not None:
                            if moveset not in used_movesets:
                                moveset_image = pygame.image.load(npc_folder + moveset + ".png").convert_alpha()
                                npc_moveset_positions[moveset] = pygame.Rect(npcs_moveset_textures.get_width(), 0, moveset_image.get_width(), moveset_image.get_height())
                                npcs_moveset_textures = set_image(npcs_moveset_textures, moveset_image)
                                used_movesets.append(moveset)
                            else:
                                if moveset not in npc_moveset_positions.keys():
                                    npc_moveset_positions[moveset] = same_npcs_moveset_positions[0][moveset]
                same_npcs_moveset_positions.append(npc_moveset_positions)
            npcs_moveset_positions[npc_name] = same_npcs_moveset_positions
        BaseCharacter.source_size = npcs_moveset_textures.get_size()
        textures.update_texture(npcs_moveset_textures, BaseCharacter.source_id)

        for npc_name in npcs_commands.keys():
            for i in range(len(npcs_commands[npc_name])):
                Character(npc_name, npcs_commands[npc_name][i], npcs_moveset_positions[npc_name][i], self.tilewidth)

        tile_obj = dict()
        for gid, colliders in self.tmxdata.get_tile_colliders():  # возвращает все объекты спрайтов
            tile_obj[gid] = colliders

        Walls.set_obstacles(tile_obj)
        Walls.set_texture_poses(atlas_pos)

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
                            object = Walls(gid, x_pos, y_pos)
                            for obj_y in range(object.rect.height // self.tmxdata.tileheight):
                                if y - obj_y < 0:
                                    continue
                                for obj_x in range(object.rect.width // self.tmxdata.tilewidth):
                                    if x + obj_x == self.tmxdata.width:
                                        break
                                    map[y - obj_y][x + obj_x].append(object)

        object_map.set_map(map)

        for group in self.tmxdata.objectgroups:
            if group.name == 'Obstacles':
                for obj in group:
                    Obstacle(obj)
                break
        textures.update_texture(map_image, 1)
        self.texture_pos = textures.convert_texture_pos(self.map_rect, self.source_id)

    def load_level(self, filename):
        self.__init__(filename)

    def get_rect(self):
        return self.map_rect

import pygame

import pytmx
import os
import moderngl
import numpy as np
from math import ceil

import settings
from items import all_items
from Events import Events, events
from settings import *

from render_setup import *
print('asdasaass')
from game_functions import game_events
from replics import all_properties, all_replices
from Panels import *
from Sprite import ActiveSprite
from BaseCharacter import BaseCharacter2, SuperBaseCharacter
from BaseCharacter import characters
from Player import player
from Enemy import Enemy
import Player_stats
from Events import events


from ImageTools import load_image


# TODO добавить change_to_next() объектам
# присваивать свойство самим объектам -
# вернуть взаимодействие -





# TODO
# панели допилить
# нпс поворачиваются к игроку лицом, игра не останавливается,
# улучшить выбор нпс для диалога (выбирается ближайший, убрать возможность разговаривать скозь стены)
# у нпс есть переменная, которая указывает есть ли у нпс возможность двигаться
# класс таймера, который хранит события и таймер, через сколько они должны произойти
# вынести Tiled map в отдельный файл
# cкейл панелек
# увеличивать изображения, хибоксы и скорость передвижения объектов, если экран 2к и больше
# добавить в мувсет доп спрайт, который показвается, когда герой только заканчивает действие (например, когда герй движется, за мгновение до остановки, доп спрайт для плавности)
# c помощью TiledMap создавать наборы мувстеов персонажей и там же хранить и хитбоксы, если его нету, то использовать по умолчанию
# множественные хитбоксы
# плавнее повороты персонажа
# починить спавн врагов
# класс игрового спрайта с хитбоксом
# отдельный слой обстаклов, который позволяет наносить на объекты дополнительные приколы в любом метсе (надписи на стенах, следы на земле и т.д.)
# в самом начале загрузки карты пройтись по всему и заскейлить
# как сделать калитки и т.д.

print('Start')
# хранить данные об изменении карт в файлах
# по х, у и layer находить свойства объекта
# при изменении карты, в файл добавлять ид нового или заменяющего спрайта
# sprite info в tiled location_map
# walls, objects, all_sprites в tiledmap

# подправить столкновение прямоугольников
# класс полигона ---
# наследственность -
# прямоугольники и полигоны (одновременная поддержка) -
# столкновение между полигонами, прямоугольниками и смешанное -
# смешать столкновение и взаимодействие персонажа - (вроде не надо)
# сделать взаимодействие по нажатию клавиши и отдельный хитбокс взаимводействия -
# анимация перса -
# смена хитбокса при повороте или квадратом сделать - (пока скип)
# отход персонажа при повороте если хитбокс не вмещается - (скип так как прошлое скип)
# сделать множества спрайтов и обновлять размеры текстур через них
# отрисовка хрень кста. Слои неверные. Переделать

# изменять переменную direction, когда повороты -
# преписать переходы с использованием тп -
# дописать столковение для всех направлений -
# добавить отталкивание при столкновении-
# округлять точки препятствий -
# прямоугольные тригеры
# обстаклы - тригеры отдельно на карте или в составе объектов?
# отдельная список-карта, которая содержит информацию, какие обстаклы находятся в клетках карты
# невидимые стены-барьеры, программа должна распознавать их и не тратить время на отрисовоку
# обстаклы объектов знают к какому предмету они привязаны

# что должен уметь соприкосновение с объектами
# 1 Переход между локациями
# 1.1 Анимации / эффекты при переходе
# 1.2 сменить локацию и положение персонажа (направление взгляда, хитбоксов, координаты)
#
# 2 Простое взаимодействие
# 2.1 Получить предмет (Какой, сколько его, сколько раз получить, переодичность, проверить на условиz)
# 2.2 Поменять текстуру (Какую (по клетке), На какую (id), место новой текстуры, навсегда)
# 2.3 проиграть анимацию/эффекты/звук
# 2.4 добавить новый объект (куда (клетку), какой(id), хитбокс(id))
# 2.5 Выдать диалоговое окно (текст)
# 2.6 выдать инвентарь, чтобы использоловать предмет
# 2.7 запустить события (бой, переход, катсцена, что-то забрать, прокачать и т.д.)
#
# (?) двигать только хит полигон у перссонажей и сохранять положение хиполигона и interaction box относительно персонажа
#

# Диалоговое окно (текст-, менять текст-, перенос слов-, перенос на новое окно-, настройки для выбранного слова (шрифт, размер, цвет и т.д), вынужденный перенос текста на новое окно-, перелистывание-)
# примититивные статы героя (хп, уровень, ехп, атака, защита)
# НПС
# Бои
# Инвентарь визуальный, удаление предметов, чек инфы, использовать вещи
# атлас текстур как объект (добавлять новую текутсуру, хранить айди каждой текстуры и положение её)

# ?совместить параметры мувсета и положение мувстета в одном словаре?
# условия в командах нпс и дополнительно обозначить появление с условием, чтобы не ломалось ничего, если нпс не заспавнивался без выполненного условия, а висел в памяти, до условия
# автопилот для нпс, который может разное делать (просто прогулка, ходить за игроком или другим нпс)

# (на будущее) сохранить данные больших локаций, чтобы при заходе в маленькие (домики в городе например), не грузилось долго при выходе
# отчищать данные больших локаций, только при переходе в другую большую локацию

# переменную pos у всех спрайтов перенести в левый нижний угол self.rect
# класс игрока тоже должен быть унаследован от BaseCharacter
# мб отдельный класс объектов с которыми можно взаимодействовать.
# не проверять на столкновение если чел стоит

# Допилить столкновение. Хранить размеры объекта в клетках. в карте объектов объекты расставлять по хитбоксам
# тайлсеты медленно делаются аааааа
# настройки в отдельный файл
# яркость для каждого слоя отдельно


def scale_image(image, scale, size=16):
    return pygame.transform.scale(image, (int(image.get_size()[0] * scale * size / Player_stats.tile_size), int(image.get_size()[1] * scale * size / Player_stats.tile_size)))


def get_obstacle(obstacle: pygame.Rect , scale, size=16):
    return pygame.Rect(int(obstacle.x * scale * size / Player_stats.tile_size), int(obstacle.y * scale * size / Player_stats.tile_size), int(obstacle.width * scale * size / Player_stats.tile_size), int(obstacle.height * scale * size / Player_stats.tile_size))


def load_texture(image, location):
    dirt_bytes = pygame.image.tostring(image, 'RGBA', False)
    texture = ctx.texture(image.get_size(), 4, bytes(dirt_bytes))
    texture.use(location=location)
    return texture


def save_image(image):
    pygame.image.save(image, 'test.png')


def set_image(initial_image, new_change):  # adds new image to another image
    size = initial_image.get_size()
    new_image = pygame.Surface((size[0] + new_change.get_width(), max(size[1], new_change.get_height())),
                                        pygame.SRCALPHA, 32)
    new_image.blit(initial_image, (0, 0))
    new_image.blit(new_change, (size[0], 0))
    return new_image


def crop_image(initial_image, image):
    a = pygame.Surface(image.bottomleft)
    b = pygame.Surface((initial_image.get_width() - image.right, initial_image.get_height() - image.bottom))
    new_image = pygame.Surface((0, 0))
    new_image = set_image(new_image, a)
    new_image = set_image(new_image, b)
    return new_image


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


def set_uniform(u_name, u_value):
    try:
        program[u_name] = u_value
    except KeyError:
        print(f'uniform: {u_name} - not used in shader')


def convert_vertex(pt, surface_size):
    return pt[0] / surface_size[0] * 2 - 1, 1 - pt[1] / surface_size[1] * 2


def get_vertices(objects, window_size):  # finds relative vertices position of object relatively to size of game window
    verts = []
    for object in objects:
        rect = camera.apply_rect(object.get_rect())
        image_pos = object.texture_pos
        source = object.source_id
        vert1 = convert_vertex((rect[0], rect[1]), window_size)
        vert2 = convert_vertex((rect[0] + rect[2], rect[1]), window_size)
        vert3 = convert_vertex((rect[0] + rect[2], rect[1] + rect[3]), window_size)
        vert4 = convert_vertex((rect[0], rect[1] + rect[3]), window_size)
        img_vert1 = image_pos[0], image_pos[1]
        img_vert2 = image_pos[2], image_pos[1]
        img_vert3 = image_pos[2], image_pos[3]
        img_vert4 = image_pos[0], image_pos[3]
        verts.append([*vert1, *img_vert1, source, *vert2, *img_vert2, source, *vert3, *img_vert3, source,
                      *vert1, *img_vert1, source, *vert3, *img_vert3, source, *vert4, *img_vert4, source])
    return verts


def get_object_verts(rect, image_pos, source, window_size):
    vert1 = convert_vertex((rect[0], rect[1]), window_size)
    vert2 = convert_vertex((rect[0] + rect[2], rect[1]), window_size)
    vert3 = convert_vertex((rect[0] + rect[2], rect[1] + rect[3]), window_size)
    vert4 = convert_vertex((rect[0], rect[1] + rect[3]), window_size)
    img_vert1 = image_pos[0], image_pos[1]
    img_vert2 = image_pos[2], image_pos[1]
    img_vert3 = image_pos[2], image_pos[3]
    img_vert4 = image_pos[0], image_pos[3]
    # print(*vert1, *img_vert1, source, *vert2, *img_vert2, source, *vert3, *img_vert3, source,
    #         *vert1, *img_vert1, source, *vert3, *img_vert3, source, *vert4, *img_vert4, source)
    # print('----')
    # print(*vert1, *img_vert1, source, 0, *vert2, *img_vert2, source, 0, *vert3, *img_vert3, source, 0
    #         *vert1, *img_vert1, source, 0, *vert3, *img_vert3, source, 0, *vert4, *img_vert4, source, 0)
    return (*vert1, *img_vert1, source, dt.dark, *vert2, *img_vert2, source, dt.dark, *vert3, *img_vert3, source, dt.dark,
            *vert1, *img_vert1, source, dt.dark, *vert3, *img_vert3, source, dt.dark, *vert4, *img_vert4, source, dt.dark)


def get_points(points):  # find all int points of all sides of polygon by points
    side_points = []
    x_lines = dict()
    y_lines = dict()
    if len(points) > 0:
        for i in range(len(points) - 1):
            point = points[i]
            point2 = points[i + 1]
            if point2[0] > point[0]:
                lesser_x, greater_x = point[0], point2[0]
            else:
                lesser_x, greater_x = point2[0], point[0]
            if point2[1] > point[1]:
                lesser_y, greater_y = point[1], point2[1]
            else:
                lesser_y, greater_y = point2[1], point[1]

            if point2[1] == point[1]:
                y = point2[1]
                for x in range(lesser_x, greater_x + 1):
                    side_points.append((x, y))
            elif point2[0] == point[0]:
                x = point2[0]
                for y in range(lesser_y, greater_y + 1):
                    side_points.append((x, y))

            else:
                k = (point2[1] - point[1]) / (point2[0] - point[0])
                b = point2[1] - k * point2[0]
                for x in range(lesser_x, greater_x + 1):
                    y = round(k * x + b)
                    side_points.append((x, y))

                for y in range(lesser_y, greater_y + 1):
                    x = round((y - b) / k)
                    side_points.append((x, y))
        side_points = set(side_points)
        for point in side_points:
            try:
                x_lines[point[1]].append(point[0])
            except KeyError:
                x_lines[point[1]] = [point[0]]
            try:
                y_lines[point[0]].append(point[1])
            except KeyError:
                y_lines[point[0]] = [point[1]]
        for y in x_lines.keys():
            x_lines[y] = sorted(x_lines[y])
        for x in y_lines.keys():
            y_lines[x] = sorted(y_lines[x])
    return side_points, x_lines, y_lines


def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2):
    # normalized direction of the lines and start of the lines
    P = pygame.math.Vector2(*l1_p1)
    line1_vec = pygame.math.Vector2(*l1_p2) - P
    R = line1_vec.normalize()
    Q = pygame.math.Vector2(*l2_p1)
    line2_vec = pygame.math.Vector2(*l2_p2) - Q
    S = line2_vec.normalize()

    # normal vectors to the lines
    RNV = pygame.math.Vector2(R[1], -R[0])
    SNV = pygame.math.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False

    # distance to the intersection point
    QP = Q - P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN

    return t > 0 and u > 0 and t * t < line1_vec.magnitude_squared() and u * u < line2_vec.magnitude_squared()


def colideRectLine(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
            collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
            collideLineLine(p1, p2, rect.bottomright, rect.topright) or
            collideLineLine(p1, p2, rect.topright, rect.topleft))


def collidePolygonLine(polygon, p1, p2):
    for point in polygon.points:
        if collideLineLine(p1, p2, point[0], point[1]):
            return True
    return False


def collideRectPolygon(rect, polygon):
    points = polygon.points
    for i in range(len(points) - 1):
        if colideRectLine(rect, points[i], points[i + 1]):
            return True
    return False


def collide_with_objects(character, group):
    for object in group:
        if character.hit_polygon.colliderect(object.hit_polygon):
            if character.vel  is UP:
                character.move_by_hit_polygon(character.hit_polygon.topleft[0], object.hit_polygon.bottom)
            elif character.vel is DOWN:
                character.move_by_hit_polygon(character.hit_polygon.topleft[0],
                                          object.hit_polygon.top - character.hit_polygon.height)
            elif character.vel is LEFT:
                character.move_by_hit_polygon(object.hit_polygon.right, character.hit_polygon.topleft[1])
            elif character.vel is RIGHT:
                character.move_by_hit_polygon(object.hit_polygon.left - character.hit_polygon.width,
                                          character.hit_polygon.topleft[1])


def collide_with_objects2(character, object):
    if character.hit_polygon.colliderect(object.hit_polygon):
        if character.vel is UP:
            character.move_by_hit_polygon(character.hit_polygon.topleft[0], object.hit_polygon.bottom)
        elif character.vel is DOWN:
            character.move_by_hit_polygon(character.hit_polygon.topleft[0],
                                      object.hit_polygon.top - character.hit_polygon.height)
        elif character.vel is LEFT:
            character.move_by_hit_polygon(object.hit_polygon.right, character.hit_polygon.topleft[1])
        elif character.vel is RIGHT:
            character.move_by_hit_polygon(object.hit_polygon.left - character.hit_polygon.width,
                                      character.hit_polygon.topleft[1])


def load_opengl_image(image, source):
    bytes_image = bytes(pygame.image.tostring(image, 'RGBA', False))
    new_texture = ctx.texture(image.get_size(), 4, bytes_image)
    new_texture.use(location=source)


def draw(vertices):
    vertices = np.array(vertices, dtype='f4').tobytes()
    buffer = ctx.buffer(vertices)
    vao = ctx.vertex_array(program, [(buffer, "2f4 2f4 f4 f4", "in_position", "in_uv", "num", "dark")])
    vao.render()
    buffer.release()
    vao.release()


def draw_with_layers(first_layer, second_layer, characters): # отрсивовывает сначала пол потом объекты и нпс в порядке их Y координаты и текстовое окно
    sprites = [first_layer, *second_layer]
    for spr in sorted(characters.sprites(), key=lambda x: x.rect.bottom):
        sprite_added = False
        for i in range(1, len(sprites)):
            if spr.rect.bottom <= sprites[i].rect.bottom:
                sprites.insert(i, spr)
                sprite_added = True
                break
        if sprite_added is False:
            sprites.append(spr)

    # for panel1 in panels:
    #     # panel1.convert_texture_pos()
    #     print(sprites[0].texture_pos)
    #     print(panel1.texture_pos)
    #     print('------')

    # vertices = get_vertices(sprites, screen_size)

    vertices = []

    for object in sprites:
        rect = camera.apply_rect(object.get_rect())
        texture_pos = object.texture_pos
        source_id = object.source_id
        vertices.append(get_object_verts(rect, texture_pos, source_id, screen_size))

    # vertices.append(get_object_verts(camera.apply_rect(pygame.Rect(864, 1148, 64, 64)), (0.0, 1.0, 1.0 / 4, 0.0), 6, screen_size))
    if draw_black_screen:
        vertices
    for panel in panels:
        if panel.visible is True:
            vertices.append(get_object_verts(panel.rect, textures.convert_texture_pos(panel.image_pos, 4), panel.source_id, screen_size))
    vertices = vertices
    draw(vertices)


# def save_game():
#     # saves_folder = path.join(game_folder, 'saves')
#     player_info = dict()
#     player_info['rect'] = list(player.rect)
#     player_info['hit_polygon_rect'] = list(player.hit_polygon)
#     player_info['interaction_box'] = list(player.interaction_box)
#     player_info['source'] = Player.source
#     player_info['texture_pos'] = player.texture_pos
#     player_info['location'] = location_map.tmxdata.filename
#     json_player_info = json.dumps(player_info, indent=4)
#
#     with open('saves/slot 1/player_info.json', 'w') as outfile:
#         outfile.write(json_player_info)
#         outfile.close()
#
#
# def load_game():
#     with open(f'saves/slot 1/player_info.json', 'r') as infile:
#         player_info = json.load(infile)
#         location_map.load_level(player_info['location'])
#         player.rect = pygame.Rect(player_info['rect'])
#         player.pos = [*player.rect.center]
#         player.hit_polygon = pygame.Rect(player_info['hit_polygon_rect'])
#         player.hit_polygon_pos = [*player.hit_polygon.topleft]
#         player.interaction_box = pygame.Rect(player_info['interaction_box'])
#         player.interaction_box_pos = [*player.interaction_box.topleft]
#         Player.source = player_info['source']
#         player.texture_pos = player_info['texture_pos']
#         infile.close()

# def get_tile(tmx_data, gid):
#     for tileset in tmx_data.tilesets:
#         for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
#             if gid


def replace_sprite_by_id(old_sprite, new_sprite_id):
    old_sprite.set_sprite_pos(new_sprite_id)
    old_sprite.set_sprite_colliders(new_sprite_id)


def display_info():
    print('x', player.rect.centerx)
    print('y', player.rect.centery)
    print('source', player.source)
    print('texture_pos', player.texture_pos)
    print('location', location_map.tmxdata.filename)


class Polygon:
    def __init__(self, points, pos=(0, 0)):
        self.points = []
        self.top = points[0][1]
        self.bottom = points[0][1]
        for point in points:
            if point[1] < self.top:
                self.top = point[1]
            if point[1] > self.bottom:
                self.bottom = point[1]
            self.points.append([round(point[0]) + pos[0], round(point[1]) + pos[-1]])
        self.points.append(self.points[0])
        self.side_points, self.x_lines, self.y_lines = get_points(self.points)  # sussy
        self.top += pos[1]
        self.bottom += pos[1]

    def collidepoint(self, point, side):
        try:
            lines = None
            if side == "x":
                lines = self.x_lines
            elif side == "y":
                lines = self.y_lines
            # print(lines[point[1]], 'y', point[1], 'x', point[0], player.hit_polygon.top)
            x1 = lines[point[1]][0]
            x2 = lines[point[1]][-1]
            if x1 < point[0] < x2:
                return True
            return False
        except KeyError:
            return False

    def get_collidepoint(self, point, side):
        try:
            lines = None
            if side == "x":
                lines = self.x_lines
            elif side == "y":
                lines = self.y_lines
            # print(lines[point[1]], 'y', point[1], 'x', point[0], player.hit_polygon.top)
            x1 = lines[point[1]][0]
            x2 = lines[point[1]][-1]
            if x1 < point[0] < x2:
                return [x1, x2]
            return []
        except KeyError:
            return []

    def move_ip(self, x, y):
        pass


class TextureAtlas:
    pass


class TiledMap:
    source = None
    source_id = 1
    source_size = None

    def __init__(self, filename):
        self.map_folder = filename
        tm = pytmx.load_pygame(f"maps/{self.map_folder}/{self.map_folder}.tmx", pixelalpha=True)
        self.width_by_tile = tm.width
        self.height_by_tile = tm.height
        self.name = tm.filename.split('/')[1]
        self.map_scale = Player_stats.game_tile_size // tm.tilewidth  # показывает насколько во сколько раз увеличить объекты на карте
        self.tilewidth = tm.tilewidth * self.map_scale
        self.width = tm.width * self.tilewidth
        self.height = tm.height * self.tilewidth
        self.tmxdata = tm
        TiledMap.source_size = (self.width, self.height)
        self.map_rect = pygame.Rect(0, 0, self.width, self.height)
        self.texture_pos = (0, 0, 0, 0)
        self.object_map = []
        self.all_sprites = pygame.sprite.Group()  # временные хранилища
        self.walls = pygame.sprite.Group()  # все стены
        self.objects = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.render()

    def render(self):

        print('start settings')
        all_sprites.empty()
        obstacles.empty()
        objects.empty()
        characters.empty()
        trigger_obstacles.empty()

        characters.add(player)
        map_image = pygame.Surface(self.map_rect.size).convert_alpha()
        ti = self.tmxdata.get_tile_image_by_gid
        objects_atlas = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        atlas_pos = dict()
        print('end settings')

        print('start creating tileset')
        for tileset in self.tmxdata.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                try:
                    tile = scale_image(ti(gid), self.map_scale)
                    atlas_pos[gid] = pygame.Rect(objects_atlas.get_width(), 0, *tile.get_size())  # TODO сделать класс атласа, где изображения будут эффективно складываться
                    objects_atlas = set_image(objects_atlas, tile)
                except IndexError:
                    pass
        print('end creating tilesets')
        save_image(objects_atlas)
        self.listtiles = [z for z in self.tmxdata.gidmap]  # cписок, в котором по айди объекта в pytmx можно получить его реальный айди из файла карты (хз)
        print(self.listtiles, 'huh')
        tile_obj = dict()
        for gid in atlas_pos.keys():
            properties = self.tmxdata.get_tile_properties_by_gid(gid)
            if properties is None:
                continue
            colliders = properties["colliders"]
            for i in range(len(colliders)):
                collider = colliders[i]
                collider = get_obstacle(pygame.Rect(round(collider.x), round(collider.y),
                                           round(collider.width), round(collider.height)), Player_stats.scale)
                colliders[i] = collider
            tile_obj[gid] = colliders

        Objects.set_obstacles(tile_obj)
        Objects.set_texture_poses(atlas_pos)

        textures.update_texture(objects_atlas, 2)
        Objects.source_size = objects_atlas.get_size()

        print('adding enemies')
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
                image = load_image(enemy_folder + enemy_name + "/stand.png", Player_stats.scale)
                movesets["stand"] = movesets.setdefault("stand", pygame.Rect(enemies_movesets_atlas.get_width(), 0, *image.get_size()))
                enemies_movesets_atlas = set_image(enemies_movesets_atlas, image)
                image = load_image(enemy_folder + enemy_name + "/walk.png", Player_stats.scale)
                movesets["walk"] = movesets.setdefault("walk", pygame.Rect(enemies_movesets_atlas.get_width(), 0, *image.get_size()))
                enemies[enemy_name] = propereties.copy()
                enemies_movesets_poses[enemy_name] = enemies_movesets_poses.setdefault(enemy_name, movesets)

        Enemy.source_size = enemies_movesets_atlas.get_size()
        textures.update_texture(enemies_movesets_atlas, 6)
        Enemy.movesets_poses = enemies_movesets_poses
        Enemy.property = enemies
        print("end_adding_enemies")

        for object in self.tmxdata.objects:
            if object.name is not None and object.name[:5] == "enemy":
                enemy_name = object.name.split(': ')[1].strip()
                Enemy(enemy_name, object.x * Player_stats.scale, object.y * Player_stats.scale)


        print("start characters")
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
        npc_properties = dict()  # TODO
        for i in range(len(lines)):
            if npc_find:
                line = lines[i].strip()
                if "spawn" in lines[i]:
                    pos = lines[i].strip().split('(')[1].split(')')[0].split(',')
                    npcs_poses[npc_name] = (int(pos[0]) * self.tilewidth, int(pos[1]) * self.tilewidth)
                elif "properties" in lines[i]:
                    line = lines[i].split('=')[1]
                    properties = line.split(',')
                    for i in range(len(properties)):
                        properties[i] = properties[i].strip()
                    npc_properties[npc_name] = properties
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
                    npc_name = clear_line(line_name)
                    commands.clear()
                    npc_find = True
                    npc_properties[npc_name] = []
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
                moveset_image = load_image(template_folder + moveset + ".png", 4).convert_alpha()
                templates_used_movesets[template_name][moveset] = pygame.Rect(npcs_moveset_textures.get_width(), 0, moveset_image.get_width(), moveset_image.get_height())
                npcs_moveset_textures = set_image(npcs_moveset_textures, moveset_image)
        BaseCharacter2.movesets_poses = templates_used_movesets
        BaseCharacter2.npcs_commands = npcs_commands.copy()
        BaseCharacter2.templates_by_name = templates_by_name

        textures.update_texture(npcs_moveset_textures, BaseCharacter2.source_id)
        for npc_name in npcs_commands.keys():
            BaseCharacter2(*npcs_poses[npc_name], npc_name, npc_properties[npc_name])
        print("end characters")

        print('map_painting')
        map = [[[] for i in range(self.tmxdata.width)] for i in range(self.tmxdata.height)]
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        tile = scale_image(tile, self.map_scale)
                        x_pos = x * self.tilewidth
                        y_pos = (y + 1) * self.tilewidth - tile.get_size()[1]
                        if layer.name != "objects":
                            map_image.blit(tile, (x_pos, y_pos))

                        if layer.name == 'objects':
                            object = Objects(gid, x_pos, y_pos)
                            for obj_y in range(object.rect.height // self.tilewidth):
                                if y - obj_y < 0:
                                    continue
                                for obj_x in range(object.rect.width // self.tilewidth):
                                    if x + obj_x == self.width_by_tile:
                                        break
                                    map[y - obj_y][x + obj_x].append(object)
        self.object_map = map
        print("end_map_painting")
        print('obstacles')
        for group in self.tmxdata.objectgroups:
            if group.name is not None and group.name.lower() == "obstacles":
                for obs in group:
                    if obs.gid != 0:  # если gid = 0, то обстакл не связан с объектом на карте
                        x, y = int(obs.x * self.map_scale / self.tilewidth), int(round(obs.y * self.map_scale / self.tilewidth))
                        for obj in map[y][x]:
                            if obj.get_tile_pos() == (x, y):
                                if obs.name is None:
                                    continue
                                properties = obs.name.split('; ')  # TODO
                                for i in range(len(properties)):
                                    properties[i] = properties[i].strip().split(' ')
                                for i in range(len(properties)):
                                    if properties[i][0] == "property":
                                        properties[i] = all_properties[properties[i][1]]

                                obj.set_properties(properties)
                                print(properties, 'asda')
                                ObjectObstacle(obj, properties)
                    else:
                        if obs.name is not None:
                            if obs.name[:7] == "trigger":
                                TriggerObstacle(obs)
                        Obstacle(obs)
                break
        textures.update_texture(map_image, 1)
        self.texture_pos = textures.convert_texture_pos(self.map_rect, self.source_id)
        print("end_obstacles")

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
        if 0 <= x < self.width_by_tile and 0 <= y < self.height_by_tile:  # TODO убрать проверки если, за пределы карты нельзя будет выйти
            return self.object_map[y][x]
        return []

    def get_norm_id(self, gid):
        return self.listtiles[gid - 1]


class ScreenMap:
    def __init__(self, width, height):
        self.map = [[None] for i in range(width // 64)] * (height // 64)
        self.width = width
        self.height = height

    def get_tile(self, xn, yn):
        return self.map[yn][xn]

    def scroll(self):
        pass


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.vel = (0, 0)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def apply_collide(self, collide):
        return collide.hit_rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        # limit scrolling to location_map size
        x = min(0, x)  # lef
        y = min(0, y)  # top
        x = max(-(location_map.width - width), x)  # right
        y = max(-(location_map.height - height), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)


# class Character(BaseCharacter):
#
#     def __init__(self, name, commands, moveset_positions, tilewidth):
#         spawn_found = False
#         for command in commands:
#             if command[0:5] == "spawn" and spawn_found is False:
#                 a = command.split('(')
#                 b = a[1].split(')')
#                 x, y = map(int, b[0].split(', '))
#                 spawn_found = True
#                 super().__init__(name, x * tilewidth, y * tilewidth, moveset_positions, 'walk', 'down')
#             if spawn_found:
#                 if command[0:5] == "stand":
#                     a = command.split('(')
#                     b = a[1].split(')')
#                     direction = b[0].split()[0].lower()
#                     self.stand(direction)
#                     break
#         self.commands = commands
#         self.hit_polygon = pygame.Rect(self.rect.left, int(self.rect.top + self.rect.height * 0.75), self.rect.width, int(self.rect.height * 0.25))


class Objects(ActiveSprite):
    source = None
    source_id = 2
    source_size = None
    walls_obstacles = dict()
    texture_poses = dict()

    def __init__(self, map_id, x, y):
        self.gid = map_id
        self.properties = []

        super().__init__(self.get_texture_poses_by_id(map_id), x, y, all_sprites, objects)
        self.convert_texture_pos()
        self.hit_polygon = pygame.Rect(0, 0, 0, 0)

        for collider in self.get_obstacles_by_id(map_id):
            # collider = pygame.Rect(round(collider.x, round(collider.y), )
            self.hit_polygon = pygame.Rect(x + collider.x, y + collider.y, collider.width, collider.height)

    def get_tile_pos(self):
        return self.pos[0] // Player_stats.game_tile_size, self.pos[1] // Player_stats.game_tile_size

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
                    self.hit_polygon = Polygon(collider.points, self.pos)
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


        if new_gid < tileset.firstgid + tileset.tilecount:
            for gid in range(len(location_map.listtiles)):
                if location_map.listtiles[gid] == new_gid:
                    new_gid = gid + 1
                    break
            self.texture_pos = self.texture_poses[new_gid]
            self.gid = new_gid
            self.convert_texture_pos()

    def interaction(self, target=player):
        for i in range(len(self.properties)):
            property = self.properties[i]
            if property[1] == 0:
                continue
            property_condition = property[0]
            if property_condition is not None:
                if property_condition[0][:9] == "have_item":
                    item_name = property_condition[0].split('(')[1].split(')')[0]
                    if have_item(item_name) is not property_condition[1]:
                        continue
            mini_props = []
            print(property[2])
            for mini_prop in property[2]:
                if mini_prop[0] == "replic":
                    mini_props.append([talk, all_replices[mini_prop[1]], 0])
                elif mini_prop[0] == "get_item":
                    mini_props.append([give_item, *mini_prop[1:], 0])
                elif mini_prop[0] == "door":
                    mini_props.extend(
                        [[pause_game, 0], [get_darker, 0], [load_map, *mini_prop[1:], 0], [get_lighter, 0],
                         [unpause_game, 0]])
                elif mini_prop[0] == "illusion_off":
                    mini_props.append([illusion_off, 0])
                    mini_props.append([change_sprite, self, 0])
                elif mini_prop[0] == "get_darker":
                    mini_props.append([get_darker, 0])
                elif mini_prop[0] == "kill":
                    mini_props.append([player.get_damage, 100, 0])
                elif mini_prop[0] == "get_lighter":
                    mini_props.append([get_lighter, 0])

            game_events.add_chain_events(mini_props)
            self.properties[i][1] -= 1

            break



        # for object_property in self.properties:
        #     command_name = object_property[0]
        #     params = object_property[1:]
        #     if command_name == "get":
        #         try:
        #             item = all_items[params[0]]
        #             item_count = int(params[1])
        #             get_times = int(params[2])
        #             func = None
        #             if len(params) > 3:
        #                 func = params[3]
        #             if get_times == 0:
        #                 continue
        #             object_property[3] = int(object_property[3]) - 1
        #             Player_stats.inventory.extend([item for _ in range(item_count)])
        #             self.change_to_next()
        #             DialogWindow.set_dialog_text(f"You got a {item.name}")
        #             dialog_menu.open()
        #         except KeyError:
        #             print(f"There no item {params[0]}")
        #         except ValueError:
        #             print(f"Некоторые параметры неверного формата (символы, а не числа)")
        #     if command_name == "door":
        #         door_num = params[0]
        #         location = params[1]
        #         load_location(location, door_num)


    def set_properties(self, properties):
        self.properties = properties

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


class Obstacle(pygame.sprite.Sprite):  #TODO норм скейл
    def __init__(self, object):
        self.groups = all_sprites, obstacles
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.object = object
        self.properties = object.name.split(' ')
        self.rect = get_obstacle(pygame.Rect(object.x, object.y, object.width, object.height), Player_stats.scale)

        self.pos = [self.rect.x, self.rect.y]
        # print(self.rect)
        self.hit_polygon = pygame.Rect(round(self.rect.x), round(self.rect.y), round(self.rect.width), round(self.rect.height))
        self.hit_polygon = get_obstacle(self.hit_polygon, 4)
        # self.hit_polygon = []
        # for points in self.data.points:
        #     self.hit_polygon.append([points[0], points[1]])
        # self.hit_polygon.append([self.data.points[0][0], self.data.points[0][1]])

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        self.rect.center = (x, y)

    def interaction(self, target=player):
        pass


class TriggerObstacle(pygame.sprite.Sprite):
    def __init__(self, object):
        self.groups = all_sprites, trigger_obstacles
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.object = object
        self.is_door = False
        self.door_num = None
        self.direction = None
        self.properties = object.name.split(': ')
        self.types = self.properties[0].split(' ')
        self.properties = self.properties[1]

        print(self.types, self.properties)
        for i in range(len(self.types)):
            if self.types[i] == "door":
                self.is_door = True
                self.door_num = self.types[i + 1]
                self.direction = self.types[i + 2]

        self.properties = self.properties.split('; ')  # TODO
        for i in range(len(self.properties)):
            self.properties[i] = self.properties[i].split(' ')
        for i in range(len(self.properties)):
            if self.properties[i][0] == "property":
                self.properties[i] = all_properties[self.properties[i][1]].copy()
        print(self.properties)


        self.rect = get_obstacle(pygame.Rect(object.x, object.y, object.width, object.height), Player_stats.scale)
        self.pos = [self.rect.x, self.rect.y]
        # print(self.rect)
        self.hit_polygon = pygame.Rect(round(self.rect.x), round(self.rect.y), round(self.rect.width), round(self.rect.height))
        self.hit_polygon = get_obstacle(self.hit_polygon, 4)

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        self.rect.center = (x, y)

    def interaction(self, target=player):
        pass


class ObjectObstacle(pygame.sprite.Sprite):
    def __init__(self, object, properties):
        self.groups = all_sprites, obstacles
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.object = object
        self.rect = object.hit_polygon
        self.pos = list(self.rect.topleft)
        self.properties = properties

    def update(self):
        self.rect = self.object.hit_polygon

    def interaction(self, target=player):
        for object_property in self.properties:
            command_name = object_property[0]
            params = object_property[1:]
            if command_name == "get":
                try:
                    item = all_items[params[0]]
                    item_count = int(params[1])
                    get_times = int(params[2])
                    func = None
                    if len(params) > 3:
                        func = params[3]
                    if get_times == 0:
                        continue
                    object_property[3] = int(object_property[3]) - 1
                    Player_stats.inventory.extend([item for _ in range(item_count)])
                    self.object.change_to_next()
                    DialogWindow.set_dialog_text(f"You got a {item.name}")
                    dialog_menu.open()
                except KeyError:
                    print(f"There no item {params[0]}")
                except ValueError:
                    print(f"Некоторые параметры неверного формата (символы, а не числа)")
            if command_name == "door":
                door_num = params[0]
                location = params[1]
                direction = params[2].lower()
                try:
                    if direction not in ("right", "left", "down", "up"):
                        raise CustomException(f"Theres no direction {direction}")
                    location_map.load_level(location)
                    f = False  # TODO использовать если команды после телепорта могут исполниться
                    for obj in objects:
                        for property in obj.properties:
                            if property[0] == "door" and property[1] == door_num:
                                if direction == "down":
                                    pos = obj.rect.midbottom
                                    target.stand(DOWN)
                                    target.move_by_hit_polygon(pos[0] - target.hit_polygon.width / 2,
                                                                      pos[1] + location_map.tilewidth)
                                elif direction == "up":
                                    pos = obj.rect.midtop
                                    target.stand(UP)
                                    target.move_by_hit_polygon(pos[0] - target.hit_polygon.width / 2,
                                                                      pos[1] - target.hit_polygon.height - location_map.tilewidth)
                                elif direction == "left":
                                    pos = obj.rect.midleft
                                    target.stand(LEFT)
                                    target.move_by_hit_polygon(pos[0] - target.hit_polygon.width - location_map.tilewidth,
                                                                      pos[1] - target.hit_polygon.height / 2)
                                elif direction == "right":
                                    pos = obj.rect.midright
                                    target.stand(RIGHT)
                                    target.move_by_hit_polygon(pos[0] + location_map.tilewidth,
                                                                      pos[1] - target.hit_polygon.height / 2)
                                return None

                except ValueError:
                    print("parameter Number - wrong")
                except CustomException as error:
                    print(error)
                except FileNotFoundError:
                    print(f"Theres no map with name {location}")


class ScreenGroup(pygame.sprite.Group):

    def sprites_update(self, group):
        cam = camera.camera
        self.empty()
        for spr in group:
            rect = spr.rect
            if rect[0] <= -cam[0] + cam[2] and rect[0] + rect[2] >= -cam[0] and rect[1] <= -cam[1] + cam[3] and rect[
                1] + rect[3] >= -cam[1]:
                self.add(spr)


class ScreenGroup2(pygame.sprite.Group):

    def sprites_update(self, group):
        self.empty()
        cam = camera.camera
        c = 0
        for y in range(cam.top // 64, ceil(cam.bottom / 64)):
            for x in range(cam.left // 64, ceil(cam.right / 64)):
                objects = group.get_tile(x, y)
                for object in objects:
                    if object not in self.sprites():
                        c += 1
                        self.add(object)


class CustomException(Exception):
    def __init__(self, message='Something wrong...'):
        # Call the base class constructor with the parameters it needs
        super(CustomException, self).__init__(message)


def collise_characters_sides(first: BaseCharacter2, second: BaseCharacter2):
    if first.hit_polygon.colliderect(second.hit_polygon):
        d, d2 = 0, 0
        if first.speed == 0 and second.speed == 0:
            return None
        if first.vel is DOWN:
            d = first.hit_polygon.bottom - second.hit_polygon.top
        elif first.vel is UP:
            d = second.hit_polygon.bottom - first.hit_polygon.top
        elif first.vel is RIGHT:
            d = first.hit_polygon.right - second.hit_polygon.left
        elif first.vel is LEFT:
            d = second.hit_polygon.right - first.hit_polygon.left

        if second.vel is DOWN:
            d2 = second.hit_polygon.bottom - first.hit_polygon.top
        elif second.vel is UP:
            d2 = first.hit_polygon.bottom - second.hit_polygon.top
        elif second.vel is RIGHT:
            d2 = second.hit_polygon.right - first.hit_polygon.left
        elif second.vel is LEFT:
            d2 = first.hit_polygon.right - second.hit_polygon.left

        # if 'Hero' in (first.name, second.name) and first.vel == RIGHT:
        #     print(d, d2, first.hit_polygon.bottom, second.hit_polygon.bottom, first.name, second.name)

        if d > d2:
            if second.vel is DOWN:
                second.hit_polygon.bottom = first.hit_polygon.top
            elif second.vel is UP:
                second.hit_polygon.top = first.hit_polygon.bottom
            elif second.vel is RIGHT:
                second.hit_polygon.right = first.hit_polygon.left
            elif second.vel is LEFT:
                second.hit_polygon.left = first.hit_polygon.right
            second.rect.topleft = second.hit_polygon.x - second.hit_polygon_x, second.hit_polygon.y - second.hit_polygon_y
            second.pos = list(second.rect.topleft)

        elif d < d2:
            if first.vel is DOWN:
                first.hit_polygon.bottom = second.hit_polygon.top
            elif first.vel is UP:
                first.hit_polygon.top = second.hit_polygon.bottom
            elif first.vel is RIGHT:
                first.hit_polygon.right = second.hit_polygon.left
            elif first.vel is LEFT:
                first.hit_polygon.left = second.hit_polygon.right
            first.rect.topleft = first.hit_polygon.x - first.hit_polygon_x, first.hit_polygon.y - first.hit_polygon_y
            first.pos = list(first.rect.topleft)

        elif d == d2:
            a = (first.speed / (first.speed + second.speed))
            b = (second.speed / (first.speed + second.speed))

            if first.vel is RIGHT and second.vel is LEFT:
                while first.hit_polygon.colliderect(second.hit_polygon):
                    first.move_ip(-a, 0)
                    second.move_ip(b, 0)
            elif first.vel is LEFT and second.vel is RIGHT:
                while first.hit_polygon.colliderect(second.hit_polygon):
                    first.move_ip(a, 0)
                    second.move_ip(-b, 0)
            elif first.vel is DOWN and second.vel is UP:
                while first.hit_polygon.colliderect(second.hit_polygon):
                    first.move_ip(0, -a)
                    second.move_ip(0, b)
            elif first.vel is UP and second.vel is DOWN:
                while first.hit_polygon.colliderect(second.hit_polygon):
                    first.move_ip(0, a)
                    second.move_ip(0, -b)

        # if 'Hero' in (first.name, second.name) and first.vel is RIGHT:
        #     print(d, d2, first.hit_polygon.bottom, second.hit_polygon.bottom, first.name, second.name)
        #     print("-------------------------")


def collide_with_characters(first):
    for char in characters:
        collise_characters_sides(first, char)


def collide(first: BaseCharacter2):  # столкновение с объектами на карте
    for y in range(first.hit_polygon.top // 64, first.hit_polygon.bottom // 64 + 1):
        for x in range(first.hit_polygon.left // 64, first.hit_polygon.right // 64 + 1):
            for object in location_map.get_tile_occupancy(x, y):
                # print(location_map.get_norm_id(object.gid), object.hit_polygon.left / 4, object.hit_polygon.top / 4, object.hit_polygon.width / 4, object.hit_polygon.height, 'amnam')
                collide_with_objects2(first, object)
    if first.hit_polygon.left < 0:
        first.move_ip_by_hit_polygon(-first.hit_polygon.left, 0)
    elif first.hit_polygon.right > location_map.width:
        first.move_ip_by_hit_polygon(location_map.width - first.hit_polygon.right, 0)
    if first.hit_polygon.top < 0:
        first.move_ip_by_hit_polygon(0, -first.hit_polygon.top)
    elif first.hit_polygon.bottom > location_map.height:
        first.move_ip_by_hit_polygon(0, location_map.height - first.hit_polygon.bottom)


def collision_with_triggers(target=player):
    for object in trigger_obstacles:
        if player.hit_polygon.colliderect(object.rect):
            for i in range(len(object.properties)):
                property = object.properties[i]
                if property[1] == 0:
                    continue
                property_condition = property[0]
                if property_condition is not None:
                    if property_condition[0][:9] == "have_item":
                        item_name = property_condition[0].split('(')[1].split(')')[0]
                        if have_item(item_name) is not property_condition[1]:
                            continue
                mini_props = []
                print(property)
                for mini_prop in property[2]:
                    if mini_prop[0] == "replic":
                        mini_props.append([talk, all_replices[mini_prop[1]], 0])
                    elif mini_prop[0] == "get_item":
                        mini_props.append([give_item, *mini_prop[1:], 0])
                    elif mini_prop[0] == "door":
                        mini_props.extend([[pause_game, 0], [get_darker, 0], [load_map, *mini_prop[1:], 0], [get_lighter, 0], [unpause_game, 0]])
                    elif mini_prop[0] == "get_darker":
                        mini_props.append([get_darker, 0])
                    elif mini_prop[0] == "kill":
                        mini_props.append([player.get_damage, 100, 0])
                    elif mini_prop[0] == "get_lighter":
                        mini_props.append([get_lighter, 0])
                game_events.add_chain_events(mini_props)
                object.properties[i][1] -= 1
                break
            # for property in object.properties:
            #     if property[0] == "door":
            #         load_location(property[2], property[1])

#
# def move_characters():
#
#     for first in characters:
#         first.move()
#         characters_list = characters.sprites()
#         for second in characters_list:
#             collise_characters_sides(first, second)
#         collide(first)
#
#     # characters_list = characters.sprites()
#     # for i in range(len(characters_list)):
#     #     first = characters_list[i]
#     #
#     #     if sum(first.vel) != 0:  # если спрайт стоит на месте, то по задумке, его не сдвинуть
#     #         for j in range(i + 1, len(characters_list)):
#     #             firstbox = first.hit_polygon
#     #             second = characters_list[j]
#     #             secondbox = second.hit_polygon
#     #
#     #             if secondbox.collidepoint(firstbox.topleft):
#     #
#     #             elif secondbox.collidepoint(firstbox.topright):
#     #
#     #             elif secondbox.collidepoint(firstbox.hit_polygon.bottomright):
#     #
#     #             elif secondbox.collidepoint(firstbox.hit_polygon.bottomleft):
#     #
#     #
#     #             collide_with_object(first, second)


def get_shader_program(name):
    with open(f"shaders/{name}.vert") as file:
        vertex_shader = file.read()
    with open(f"shaders/{name}.frag") as file:
        fragment_shader = file.read()
    shader_program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    return shader_program


def open_panel(panel):
    panel.open()


def load_commands(user):  # формирует список свойств предмета и отправляет в ивенты
    pass


def interaction(self, group):
    # for obj in group:
    #     if pygame.Rect.colliderect(self.get_interaction_box(), obj.hit_polygon):
    #         if obj.data.name is not None:
    #             commands = obj.data.name.split(';')
    #             for command in commands:
    #                 command = command.split(' ')
    #                 execute_command(command[0], *command[1:])
    interaction_box = self.get_interaction_box()
    for x in range(interaction_box.left // 64, interaction_box.right // 64 + 1):
        for y in range(interaction_box.top // 64, interaction_box.bottom // 64 + 1):
            for object in location_map.get_tile_occupancy(x, y):
                if interaction_box.colliderect(object.hit_polygon):
                    # print(object.properties)
                    # for command in object.properties:
                    #     execute_command(command[0], *command[1:])
                    object.interaction()


def interaction_with_charaters():
    for char in screen_characters:
        if char is not player and player.get_interaction_box().colliderect(char.hit_polygon):
            char.interaction()


def interaction2(user: SuperBaseCharacter):
    targets = []
    interaction_box = user.get_interaction_box()
    for x in range(interaction_box.left // 64, interaction_box.right // 64 + 1):
        for y in range(interaction_box.top // 64, interaction_box.bottom // 64 + 1):
            for object in location_map.get_tile_occupancy(x, y):
                if interaction_box.colliderect(object.hit_polygon):
                    targets.append(object)
    for char in screen_characters:
        if char is not player and player.get_interaction_box().colliderect(char.hit_polygon):
            targets.append(char)
    if len(targets) == 0:
        return None
    target = None

    for target in targets:
        if (len(target.properties)) > 0:
            target.interaction(user)
            return None
    # if user.vel is UP:
    #     objects = sorted(targets, key = lambda x: x.hit_polygon.bottom, reverse=True)
    #     target = objects[0]
    #     if len(target.properties) == 0:
    #         for i in range(1, len(objects)):
    #             if target.hit_polygon.bottom != objects[i].hit_polygon.bottom:
    #                 target = None
    #                 break
    #             if len(objects[i].properties) > 0:
    #                 target = objects[i]
    #                 break
    # elif user.vel is DOWN:
    #     objects = sorted(targets, key = lambda x: x.hit_polygon.top)
    #     target = objects[0]
    #     if len(target.properties) == 0:
    #         for i in range(1, len(objects)):
    #             if target.hit_polygon.top != objects[i].hit_polygon.top:
    #                 target = None
    #                 break
    #             if len(target.properties) > 0:
    #                 target = objects[i]
    #                 break
    # elif user.vel is LEFT:
    #     objects = sorted(targets, key = lambda x: x.hit_polygon.right, reverse=True)
    #     target = objects[0]
    #     if len(target.properties) == 0:
    #         for i in range(1, len(objects)):
    #             if target.hit_polygon.right != objects[i].hit_polygon.right:
    #                 target = None
    #                 break
    #             if len(target.properties) > 0:
    #                 target = objects[i]
    #                 break
    # elif user.vel is RIGHT:
    #     objects = sorted(targets, key = lambda x: x.hit_polygon.left, reverse=False)
    #     target = objects[0]
    #     if len(target.properties) == 0:
    #         for i in range(1, len(objects)):
    #             if target.hit_polygon.left != objects[i].hit_polygon.left:
    #                 target = None
    #                 break
    #             if len(target.properties) > 0:
    #                 target = objects[i]
    #                 break

    # elif user.vel is DOWN:
    #     targets = sorted(targets, key = lambda x: x.hit_polygon.top)
    #     ass_targets = [targets[0]]
    #     for i in range(1, len(targets)):
    #         if targets[i].hit_polygon.top == targets[i - 1].hit_polygon.top:
    #             ass_targets.append(targets[i])
    # elif user.vel is LEFT:
    #     targets = sorted(targets, key = lambda x: x.hit_polygon.right, reverse=True)
    #     ass_targets = [targets[0]]
    #     for i in range(1, len(targets)):
    #         if targets[i].hit_polygon.right == targets[i - 1].hit_polygon.right:
    #             ass_targets.append(targets[i])
    # else:
    #     targets = sorted(targets, key = lambda x: x.hit_polygon.left)
    #     ass_targets = [targets[0]]
    #     for i in range(1, len(targets)):
    #         if targets[i].hit_polygon.left == targets[i - 1].hit_polygon.left:
    #             ass_targets.append(targets[i])
    # for i in targets:
    #     if len(i.properties) > 0:
    #         i.interaction()
    # for target in ass_targets:
    #     if len(target.properties) > 0:
    #         target.interaction()
    #         break
    if target is not None:
        target.interaction(user)


def interaction3(user: SuperBaseCharacter):

    for obs in obstacles:
        if user.get_interaction_box().colliderect(obs.rect):

            interaction_box = user.get_interaction_box()
            objects = []
            for x in range(interaction_box.left // 64, interaction_box.right // 64 + 1):
                for y in range(interaction_box.top // 64, interaction_box.bottom // 64 + 1):
                    for object in location_map.get_tile_occupancy(x, y):
                        if interaction_box.colliderect(object.hit_polygon):
                            objects.append(object)
            f = False
            target = None
            if user.vel is UP:
                target = objects[0]
                if len(target.properties) == 0:
                    for i in range(1, len(objects)):
                        if len(objects.properties) == 0:
                            if target.hit_polygon.bottom != objects[i].hit_polygon.bottom:
                                target = None
                                break
                        else:
                            if target.hit_polygon.bottom != objects[i].hit_polygon.bottom:
                                target = None
                                break
                            else:
                                target = objects[i]
                                break
            # elif user.vel is DOWN:
            #     for object in objects:
            #         if obs.rect.top >= object.hit_polygon.top >= user.hit_polygon.bottom and object is not obs.object:
            #             f = True
            #             break
            # elif user.vel is LEFT:
            #     for object in objects:
            #         if obs.rect.right <= object.hit_polygon.right <= user.hit_polygon.left and object is not obs.object:
            #             f = True
            #             break
            # elif user.vel is RIGHT:
            #     for object in objects:
            #         if obs.rect.left >= object.hit_polygon.left >= user.hit_polygon.right and object is not obs.object:
            #             f = True
            #             break
            if target is not None:
                target.interaction(user)


def get_item(name, count=1, sound=None, state=False):
    item = all_items[name]
    Player_stats.inventory.extend([item for _ in range(count)])
    return False


def hide_map(state=False):
    events.set_map_showing(False)
    return False


def show_map(state=False):
    events.set_map_showing(True)
    return False


def set_game_event(name, state=True, state2=False):
    Player_stats.all_game_events[name] = state
    return False


def pause_game(state=False):
    Events.set_text_event(True)
    return False


def illusion_off(state=False):
    for character in characters:
        print(character.char_name, 'sda')
        if "ded" in character.char_name:
            print('ds')
            character.kill()
    return False


def unpause_game(state=False):
    Events.set_text_event(False)
    return False


def pause_game(state=False):
    Events.pause_event = True
    return False


def unpause_game(state=False):
    Events.pause_event = False
    return False


def get_darker(state=False):
    dt.raise_dark(dt.dt / 1.5)
    if dt.dark >= 1:
        dt.set_dark(1)
        return False
    return True


def get_lighter(state=False):
    dt.down_dark(dt.dt / 1.5)
    if dt.dark <= 0:
        dt.set_dark(0)
        return False
    return True


def talk(text, state=0):
    if Events.text_event is False:
        if state == 0:
            DialogWindow.set_dialog_text(*text)
            dialog_menu.open()
            return 1
        return 0
    return 1


def give_item(item_name, count=1, state=0):
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


def load_map(location, door_num, state=False):
    location_map.load_level(location)

    for obj in objects.sprites():
        for property in obj.properties:
            print(property, 's')
            if "door" in property and door_num in property:
                direction = property[3].lower()
                if direction == "down":
                    pos = obj.rect.midbottom
                    player.stand(DOWN)
                    player.move_by_hit_polygon(pos[0] - player.hit_polygon.width / 2,
                                                      pos[1] + location_map.tilewidth)
                elif direction == "up":
                    pos = obj.rect.midtop
                    player.stand(UP)
                    player.move_by_hit_polygon(pos[0] - player.hit_polygon.width / 2,
                                                      pos[1] - player.hit_polygon.height - location_map.tilewidth)
                elif direction == "left":
                    pos = obj.rect.midleft
                    player.stand(LEFT)
                    player.move_by_hit_polygon(pos[0] - player.hit_polygon.width - location_map.tilewidth,
                                                      pos[1] - player.hit_polygon.height / 2)
                elif direction == "right":
                    pos = obj.rect.midright
                    player.stand(RIGHT)
                    player.move_by_hit_polygon(pos[0] + location_map.tilewidth,
                                                      pos[1] - player.hit_polygon.height / 2)
                return False
    for obj in trigger_obstacles:
        if obj.is_door and door_num == obj.door_num:
            direction = obj.direction.lower()
            if direction == "down":
                pos = obj.rect.midbottom
                player.stand(DOWN)
                player.move_by_hit_polygon(pos[0] - player.hit_polygon.width / 2,
                                                  pos[1] + location_map.tilewidth)
            elif direction == "up":
                pos = obj.rect.midtop
                player.stand(UP)
                player.move_by_hit_polygon(pos[0] - player.hit_polygon.width / 2,
                                                  pos[1] - player.hit_polygon.height - location_map.tilewidth)
            elif direction == "left":
                pos = obj.rect.midleft
                player.stand(LEFT)
                player.move_by_hit_polygon(pos[0] - player.hit_polygon.width - location_map.tilewidth,
                                                  pos[1] - player.hit_polygon.height / 2)
            elif direction == "right":
                pos = obj.rect.midright
                player.stand(RIGHT)
                player.move_by_hit_polygon(pos[0] + location_map.tilewidth,
                                                  pos[1] - player.hit_polygon.height / 2)

    return False


def change_sprite(target, state=False):  # TODO убрать у ивентов state там где не используется
    target.change_to_next()
    return False


def have_item(item_name):
    try: all_items[item_name]
    except KeyError: print("Нет такого предмета")
    for item in Player_stats.inventory:
        if item.name == item_name:
            return True
    return False


# параметры звука перехода и анимации перехода
def load_location(filename, door_num):
    door_events = [[pause_game, 0], [get_darker, 0], [load_map, filename, door_num, 0], [get_lighter, 0], [unpause_game, 0]]
    game_events.add_chain_events(door_events)

def off_drawing(state=False):
    drawing = False
    return False


draw_black_screen = False

settings.dark = 1
print(settings.dark)
camera = Camera(width, height)
clock = pygame.time.Clock()


game_folder = os.path.dirname(__file__)
map_folder = os.path.join(game_folder, 'maps')

all_sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()  # все объекты
obstacles = pygame.sprite.Group()  # все обстаклы
trigger_obstacles = pygame.sprite.Group()

screen_sprites = ScreenGroup()  # только стены, которые на экране
# screen_sprites = ScreenGroup2()

screen_obstacles = ScreenGroup()  # объекты, которые на экране
screen_characters = ScreenGroup()

font = pygame.font.Font(font_name, font_size)

print(4)
location_map = TiledMap("first_part")
print(5)
player.stand(DOWN)


display_info()
camera.update(player)
screen_sprites.sprites_update(objects)
screen_obstacles.sprites_update(obstacles)
screen_characters.sprites_update(characters)




screen_obstacles.sprites_update(obstacles)  # TODO
screen_sprites.sprites_update(objects)
screen_characters.sprites_update(characters)
camera.update(player)

dt.set_dark(1)
light_off = get_lighter()

clock.tick_busy_loop()

DialogWindow.set_dialog_text("set_person1(player_icon)", "show_person1", "Что ж. Сегодня мне надо в цирк", "Таааак...", "...", "Блин. Не помню дорогу.", "Ладно. Прогуляюсь немного.", "hide_person1")
dialog_menu.open()

while light_off is True:
    light_off = get_lighter(light_off)
    ctx.clear(0, 0, 0, 1)
    draw_with_layers(location_map, screen_sprites, screen_characters)
    dt.set_dt(clock.tick(fps) / 1000)
    pygame.display.flip()


pygame.mixer_music.load("music/Sergey Cheremisinov - Chronos.mp3.mp3")
pygame.mixer.music.play(-1, 0.0)


print('THE END')



# test_char = characters.sprites()[1]


running = True
while running:
    input_events = pygame.event.get()

    if Events.pause_event:
        for event in input_events:
            if event.type == pygame.QUIT:
                running = False

    elif Events.text_event:
        for event in input_events:
            if event.type == pygame.QUIT:
                running = False
        dialog_menu.do_something(input_events)

    elif Events.menu_event:
        for event in input_events:
            if event.type == pygame.QUIT:
                running = False
        player_menu.do_something(input_events)

    else:
        player.timer_tick()
        for event in input_events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_o:
                    player_menu.open()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_k:
                    # interaction(player, screen_objects)
                    # interaction_with_charaters()
                    interaction2(player)
                    # interaction3(player)
                elif event.key == pygame.K_KP1:
                    player.set_speed(300)
                elif event.key == pygame.K_KP2:
                    player.set_speed(350)
                elif event.key == pygame.K_KP3:
                    player.set_speed(400)
                elif event.key == pygame.K_KP4:
                    player.set_speed(450)
                elif event.key == pygame.K_KP5:
                    player.set_speed(500)
                elif event.key == pygame.K_KP6:
                    player.set_speed(1000)
                elif event.key == pygame.K_KP7:
                    player.set_speed(2000)
                elif event.key == pygame.K_KP8:
                    player.set_speed(speed)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        player.set_player_commands(input_events)  # TODO вроде хрень. Мб сделать класс в котором ивенты ввода клавиш хранятся
        for npc in characters:
            npc.execute_commands()

        characters_list = characters.sprites()
        collision_with_triggers()
        for first in characters_list:
            for second in characters_list:
                if first is second:
                    continue
                collise_characters_sides(first, second)
            collide(first)

    game_events.work()
    screen_obstacles.sprites_update(obstacles)  # TODO
    screen_sprites.sprites_update(objects)
    screen_characters.sprites_update(characters)
    camera.update(player)
    ctx.clear(0, 0, 0, 1)
    draw_with_layers(location_map, screen_sprites, screen_characters)
    dt.set_dt(clock.tick(fps) / 1000)
    pygame.display.flip()


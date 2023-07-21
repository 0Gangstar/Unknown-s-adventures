from Sprite import ActiveSprite
import pygame


class Walls(ActiveSprite):
    source = None
    source_id = 2
    source_size = None
    walls_obstacles = dict()
    texture_poses = dict()

    def __init__(self, map_id, x, y):
        self.gid = map_id
        self.properties = []
        super().__init__(self.get_texture_poses_by_id(map_id), x, y, all_sprites, walls)
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
        Walls.walls_obstacles = sprite_obstacles

    @staticmethod
    def set_texture_poses(texture_position):
        Walls.texture_poses = texture_position

    @staticmethod
    def get_obstacles_by_id(gid):
        try:
            return Walls.walls_obstacles[gid]
        except KeyError:
            return []

    @staticmethod
    def get_texture_poses_by_id(gid):
        return Walls.texture_poses[gid]

    def set_properties(self, properties):
        self.properties = properties



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, object):
        self.groups = all_sprites, objects
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

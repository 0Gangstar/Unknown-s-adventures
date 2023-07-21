import pygame


def convert_texture_pos(texture_pos, source_size):
    vert1 = texture_pos[0] / source_size[0], 1 - texture_pos[1] / source_size[1]
    vert2 = (texture_pos[0] + texture_pos[2]) / source_size[0], 1 - (texture_pos[1] + texture_pos[3]) / source_size[1]
    return *vert1, *vert2


class ActiveSprite(pygame.sprite.Sprite):
    source = None
    source_id = None
    source_size = None

    def __init__(self, texture_pos, x, y, *group):
        super().__init__(*group)
        self.texture_pos = texture_pos
        self.sprite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.sprite_size)
        self.pos = [x, y]
        self.rect.topleft = self.pos
        self.hit_polygon = None

    def convert_texture_pos(self):
        self.texture_pos = convert_texture_pos(self.texture_pos, self.source_size)

    def update(self, target):
        self.rect.topleft = (target.rect.left, target.rect.top)

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def get_sprite_size(self):
        return self.sprite_size

    def get_rect(self):
        return self.rect


class Character:
    source_id = 3
    all_commands = dict()
    all_sprite_sets = dict()

    def __init__(self, gid, x, y):
        self.commands = self.all_commands[gid]
        self.sprite_sets = self.all_sprite_sets[gid]
        self.x = x
        self.y = y

    @staticmethod
    def set_obstacles(new_commands):
        Character.all_commands = new_commands

    @staticmethod
    def set_texture_poses(new_sprite_sets):
        Character.all_commands = new_sprite_sets

    @staticmethod
    def get_sprite_sets(gid):
        try:
            return Character.all_sprite_sets[gid]
        except KeyError:
            return []

    @staticmethod
    def get_sprite_commands(gid):
        return Character.all_commands[gid]

import pygame
from Textures import textures


class ActiveSprite(pygame.sprite.Sprite):
    source = None
    source_id = None
    source_size = None
    texture = None

    def __init__(self, texture_pos: pygame.Rect, x, y, *group):
        self.properties = []
        super().__init__(*group)
        self.image_pos = texture_pos.topleft
        self.texture_pos = texture_pos
        self.sprite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(x, y, *self.sprite_size)
        self.pos = [x, y]

    def update_texture_pos(self, texture_pos):
        self.image_pos = texture_pos.topleft
        self.sprite_size = texture_pos[2:]
        self.rect = pygame.Rect(*self.rect.topleft, *self.sprite_size)
        self.texture_pos = textures.convert_texture_pos(texture_pos, self.source_id)

    def update_pos(self, x, y):
        self.rect.topleft = (x, y)
        self.texture_pos = textures.convert_texture_pos(self.rect, self.source_id)

    def convert_texture_pos(self):
        self.texture_pos = textures.convert_texture_pos(self.texture_pos, self.source_id)

    def update_size(self):
        self.sprite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.sprite_size)
        self.rect.topleft = self.pos

    def update(self, target):
        self.rect.topleft = (target.rect.left, target.rect.top)
        self.pos = self.rect.topleft

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def get_sprite_size(self):
        return self.sprite_size

    def get_rect(self):
        return self.rect

    def set_source(self, id):
        pass

    def rewrite(self, texture_pos: pygame.Rect, x, y, *group):
        self.kill()
        self.__init__(texture_pos, x, y, *group)

    def interaction(self, target):
        pass


    #
    # def get_image_pos(self):
    #     return pygame.Rect(*self.pos, *self.sprite_size)

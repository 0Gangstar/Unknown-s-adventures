import pygame
from render_setup import ctx
from ImageTools import save_image


class Textures:
    def __init__(self, ctx):
        self.ctx = ctx
        self.map_texture = ctx.texture((0, 0), 4)
        self.objects_texture = ctx.texture((0, 0), 4)
        self.player_texture = ctx.texture((0, 0), 4)
        self.panel_texture = ctx.texture((0, 0), 4)
        self.characters_texture = ctx.texture((0, 0), 4)
        self.text_texture = ctx.texture((0, 0), 4)

        self.spare_textures = [ctx.texture((0, 0), 4), ctx.texture((0, 0), 4), ctx.texture((0, 0), 4), ctx.texture((0, 0), 4), ctx.texture((0, 0), 4), ctx.texture((0, 0), 4)]
        self.spare_textures_sizes = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        self.map_texture_size = (0, 0)
        self.objects_texture_size = (0, 0)
        self.player_texture_size = (0, 0)
        self.panel_texture_size = (0, 0)
        self.characters_texture_size = (0, 0)
        self.text_texture_size = (0, 0)

        self.textures = {1: self.map_texture, 2: self.objects_texture,
                         3: self.player_texture, 4: self.panel_texture,
                         5: self.characters_texture, 6: self.text_texture}

        self.texture_sizes = {1: self.map_texture_size, 2: self.objects_texture_size,
                              3: self.player_texture_size, 4: self.panel_texture_size,
                              5: self.characters_texture_size, 6: self.text_texture_size}

    def update_texture(self, image, source_id):
        dirt_bytes = pygame.image.tostring(image, 'RGBA', False)
        self.textures[source_id].release()
        self.textures[source_id] = self.ctx.texture(image.get_size(), 4, bytes(dirt_bytes))
        self.textures[source_id].use(source_id)
        self.texture_sizes[source_id] = image.get_size()


    def change_texture_size(self, size, source_id):
        self.texture_sizes[source_id] = size

    def convert_texture_pos(self, texture_pos, source_id):
        vert1 = texture_pos[0] / self.texture_sizes[source_id][0], 1 - texture_pos[1] / self.texture_sizes[source_id][1]
        vert2 = (texture_pos[0] + texture_pos[2]) / self.texture_sizes[source_id][0], 1 - (texture_pos[1] + texture_pos[3]) / self.texture_sizes[source_id][1]
        return *vert1, *vert2

    def clear_texture(self, source_id):
        self.textures[source_id].release()
        self.textures[source_id] = self.ctx.texture((0, 0), 4)


textures = Textures(ctx)

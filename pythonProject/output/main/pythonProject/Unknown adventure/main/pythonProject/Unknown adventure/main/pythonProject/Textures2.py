import pygame
from render_setup import ctx


class Textures:
    map_texture = ctx.texture((0, 0), 4)
    objects_texture = ctx.texture((0, 0), 4)
    player_texture = ctx.texture((0, 0), 4)
    panel_texture = ctx.texture((0, 0), 4)
    characters_texture = ctx.texture((0, 0), 4)
    text_texture = ctx.texture((0, 0), 4)

    map_texture_size = (0, 0)
    objects_texture_size = (0, 0)
    player_texture_size = (0, 0)
    panel_texture_size = (0, 0)
    characters_texture_size = (0, 0)
    text_texture_size = (0, 0)

    textures = {1: map_texture, 2: objects_texture,
                         3: player_texture, 4: panel_texture,
                         5: characters_texture, 6: text_texture}

    texture_sizes = {1: map_texture_size, 2: objects_texture_size,
                              3: player_texture_size, 4: panel_texture_size,
                              5: characters_texture_size, 6: text_texture_size}

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
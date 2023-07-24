import pygame
import Player_stats


def save_image(image):
    pygame.image.save(image, 'test.png')


def set_image(initial_image, new_change):  # adds new image to another image
    size = initial_image.get_size()
    new_image = pygame.Surface((size[0] + new_change.get_width(), max(size[1], new_change.get_height())),
                                        pygame.SRCALPHA, 32)
    new_image.blit(initial_image, (0, 0))
    new_image.blit(new_change, (size[0], 0))
    return new_image


def crop_image(initial_image, image_rect):
    a = pygame.Surface(image_rect.bottomleft)
    b = pygame.Surface((initial_image.get_width() - image_rect.right, initial_image.get_height() - image_rect.bottom))
    new_image = pygame.Surface((0, 0))
    new_image = set_image(new_image, a)
    new_image = set_image(new_image, b)
    return new_image


def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return


def load_image(filename, scale, size=16):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, (image.get_size()[0] * scale * size / Player_stats.tile_size, image.get_size()[1] * scale * size / Player_stats.tile_size)).convert_alpha()
    return image


def get_obstacle(obstacle: pygame.Rect , scale, size=16):
    return pygame.Rect(obstacle.x * scale * size / Player_stats.tile_size, obstacle.y * scale * size / Player_stats.tile_size, obstacle.width * scale * size / Player_stats.tile_size, obstacle.height * scale * size / Player_stats.tile_size)



# class Inventory:
#     def __init__(self, filename, font, x, y):
#         self.panel = TextPanel(filename, font, x, y)
#         self.selected_item = 0
#
#     def get_item_list(self):  # TODO мб список предметов перенести из класса игрока в класс инвентаря
#         return player.inventory
#
#     def get_items_count(self):
#         return len(player.inventory)
#
#     def open(self):
#         self.panel.open()
#
#     def close(self):
#         self.panel.close()
#
#     def update(self):
#         item_list = ""
#         for item in player.inventory:
#             item_list += item.name
#             item_list += ' /- '
#         self.panel.set_text([item_list])
#
#     def act(self):
#         text_panel.set_text([player.inventory[self.selected_item].info()])
#         Events.set_text_event(True)
#         pos = self.panel.x - 200, self.panel.font.get_height() * self.selected_item
#         # return ItemActions(item_actions_image_name, font, *pos, player.inventory[self.selected_item])





# class Menu:
#     def __init__(self, filename, font, x, y):
#
#         self.font = font
#         self.inventory = Inventory(filename, font, x, y)
#
#         self.active = self.inventory
#
#         self.cursor_image = pygame.Surface((32, font.get_height()))
#         pygame.draw.polygon(self.cursor_image, (255, 255, 255),
#                             ((0, self.cursor_image.get_height() / 2), (self.cursor_image.get_width(), 0),
#                              (self.cursor_image.get_width(), self.cursor_image.get_height())))
#         self.cursor_pos = [self.active.panel.image_pos.x + 300, self.active.panel.image_pos.y + self.active.panel.padding[1]]
#
#         self.route = [self.inventory]
#
#     def open(self):
#         self.active.open()
#         Events.set_menu_event(True)
#
#     def close(self):
#         self.active.close()
#         if self.active.panel.visible is False:
#             Events.set_menu_event(False)
#
#     def display_panel(self):
#         self.active.update()
#         Panel.panels_atlas.blit(self.cursor_image, (self.cursor_pos[0], self.cursor_pos[1]))
#         self.active.panel.update_texture()
#
#     def move_cursor(self, direction):
#         if direction == 1:
#             if self.active.selected_item < self.active.get_items_count() - 1:
#                 self.cursor_pos[1] += self.font.get_height()
#                 self.active.selected_item += 1
#                 self.display_panel()
#         else:
#             if self.active.selected_item > 0:
#                 self.cursor_pos[1] -= self.font.get_height()
#                 self.active.selected_item -= 1
#                 self.display_panel()
#
#     def open_new_panel(self):
#         new = self.active.act()
#         if new:
#             self.route.append(self.active)
#             self.active = new
#
#     def close_panel(self):
#         if len(self.route) == 0:
#             self.route.append(self.active)
#             self.active = None
#             Events.set_menu_event(False)
#         else:
#             self.active = self.route[-1]
#             self.route = self.route[:-1]
#
#     def get_active_visible(self):
#         return self.active.panel.visible
#
#     def open_menu(self):
#         pass

# загружает все заслуги игрока (инвентарь, уровень, прокачка, квесты и т.д.) и раздаёт эту информацию в другие файлы
# класс инвентаря


from items import all_items
import pygame

inventory = [all_items["ticket"], all_items["flower seeds"]]
current_map = ""
scale = 4
tile_size = 16
game_tile_size = 64  # размер тайлов на экране


# все ивенты игрока
all_game_events = {"talk_with_ded": False}

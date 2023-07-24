width = 1920
height = 1016
screen_size = (width, height)

map_tilewidth = 64  # TODO обойтись без этого

fps = 60
speed = 3000
test_speed = 200
sps = 2.5  # (sprites per second) количество сменяющихся спрайтов персонажей в секунду
dark = 0
#  walk speed = 200

time = 0
sec = 0

# Directions
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)
Directions = {'left': LEFT, 'right': RIGHT, 'up': UP, 'down': DOWN}

# folders
characters_folder = "characters/"
enemy_folder = characters_folder + "Enemy/"

walking_template = {'up': (0, 0),   'left': (1, 0),   'right': (2, 0),   'down': (3, 0),  # схемы, как распологается каждый спрайт на конкретном мувсете
                    'up_2': (0, 1), 'left_2': (1, 1), 'right_2': (2, 1), 'down_2': (3, 1),
                    'up_3': (0, 2), 'left_3': (1, 2), 'right_3': (2, 2), 'down_3': (3, 2)}

standing_template = {'up': (0, 0), 'left': (1, 0), 'right': (2, 0), 'down': (3, 0)}


stand_template = [(0, 0), (1, 0), (2, 0), (3, 0)]

walk_template = [(0, 0), (1, 0), (2, 0), (3, 0),
                 (0, 1), (1, 1,), (2, 1), (3, 1),
                 (0, 2), (1, 2), (2, 2), (3, 2)]

movesets_scheme_by_name = {"walk": walking_template, "stand": standing_template}


standing_template_size = (4, 1)
walking_template_size = (4, 5)

all_movesets_names = ["walk", "stand"]
movesets_size_by_name = {"walk": walking_template_size, "stand": standing_template_size}

walking_frame_rate = 3

default_character_speed = 200

font_name = "data/fonts/CodeMan38.ttf"
font_size = 36

item_actions_image_name = "data/general/item_actions_image.png"

# TODO Класс времени мб ещё и хранит таймеры для разных событий и персонажей (их кулдауны, счётчики ожидания)

class DT:
    def __init__(self):
        self.dt = 0
        self.dark = 0

    def set_dt(self, dt):
        self.dt = dt

    def get_dt(self):
        return self.dt

    def raise_dark(self, count):
        self.dark += count

    def down_dark(self, count):
        self.dark -= count

    def set_dark(self, count):
        self.dark = count
dt = DT()





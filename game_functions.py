import Player_stats
from items import all_items
from Panels import dialog_menu, DialogWindow
from Events import events, Events
import settings


def get_item(name, count=1, sound=None, ):
    item = all_items[name]
    Player_stats.inventory.extend([item for _ in range(count)])


def load_location(filename, sound=None, animation=None):
    pass


def talk(text):
    DialogWindow.set_text(text)
    dialog_menu.open()


class GameEvents():
    def __init__(self):
        self.events = []

    def work(self):  # TODO ивенты из цепи не совсем друг за другом идут

        for i in range(len(self.events)):
            # print(self.events, 'asdfwerbtrrgerfqwc')
            event = self.events[i][0]
            event[-1] = event[0](*event[1:])
            if event[-1] == 0:
                self.events[i].pop(0)
            if len(self.events[i]) == 0:
                self.events.pop(i)

    def add_event(self, event_name, *params):  # добавить одиночное событие
        self.events.append([event_name, *params])

    def add_chain_events(self, events):  # добавить цепь соыбытий, который выполнятся подряд
        self.events.append(events)


def have_item(item_name):
    try: all_items[item_name]
    except KeyError: print("Нет такого предмета")

    for item in Player_stats.inventory:
        if item.name == item_name:
            return True
    return False


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


def talk(text, state=0):
    if Events.text_event is False:
        if state == 0:
            DialogWindow.set_dialog_text(*text)
            dialog_menu.open()
            return 1
        return 0
    return 1



# def pause_game():
#     events.pause_event = True
#     return True
#
#
# def unpause_game():
#     events.pause_event = False
#     return True
#
#
# def get_darker():
#     settings.dt.raise_dark(settings.dt.dt / 4)
#     if settings.dt.dark >= 1:
#         settings.dt.set_dark(1)
#         return True
#     return False
#
#
# def get_lighter():
#     settings.dt.down_dark(settings.dt.dt / 4)
#     if settings.dt.dark <= 0:
#         settings.dt.set_dark(0)
#         return True
#     return False
#
#
# def check_event(name):
#     return Player_stats.all_game_events[name]


# def hide_map():
#     events.set_map_showing(False)
#
#
# def show_map():
#     events.set_map_showing(True)
#
#
# def set_game_event(name, state=True):
#     Player_stats.all_game_events[name] = state
#
#
# def pause_game():
#     Events.set_text_event(True)
#     return True
#
#
# def unpause_game():
#     Events.set_text_event(False)
#     return True


game_events = GameEvents()

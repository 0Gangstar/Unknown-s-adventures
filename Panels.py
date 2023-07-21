import pygame
from Textures import textures
from Sprite import ActiveSprite
from Events import Events
from settings import font_size, font_name
panels = pygame.sprite.Group()
from items import Item, all_items
from ImageTools import *
import Player_stats

basic_font = pygame.font.Font(font_name, font_size)


class Panel(ActiveSprite):
    current_active = None
    mother_image = pygame.Surface((0, 0))
    folder = "data/general"
    source_id = 4

    def __init__(self, menu, name, filename, x, y):  # TODO мб привязывать окна к меню, посылая им меню
        self.menu = menu
        self.name = name
        self.filename = filename
        self.image = None
        self.image_pos = pygame.Rect(0, 0, *pygame.image.load(self.filename).convert_alpha().get_size())
        self.texture_pos = self.image_pos.copy()
        self.visible = False
        self.locked = False
        super().__init__(self.texture_pos, x, y, panels)

    def open(self, *args):  # TODO
        if self.image is None:
            Panel.current_active = self
            self.visible = True
            image = pygame.image.load(self.filename).convert_alpha()
            self.texture_pos = pygame.Rect(Panel.mother_image.get_width(), 0, *image.get_size())
            self.image_pos = self.texture_pos.copy()
            Panel.mother_image = set_image(Panel.mother_image, image)
            textures.update_texture(Panel.mother_image, self.source_id)
        else:
            self.visible = True

    def set_image(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        Panel.mother_image.blit(image, self.image_pos)
        textures.update_texture(Panel.mother_image, self.source_id)

    def get_active_visible(self):
        return self.visible

    def get_rect(self):
        return self.image,

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    @staticmethod
    def clear_atlas():
        Panel.mother_image = pygame.Surface((0, 0))

    def close(self):
        self.kill()
        del self

    def update(self, *args):
        pass


class TextPanel(Panel):
    source_id = 4

    def __init__(self, menu, name, x, y, filename, font, color, padding, *text):
        super().__init__(menu, name, filename, x, y)
        self.font = font
        self.text = text
        self.color = color
        self.padding = padding
        self.function = None

        self.x = x / 2 - self.rect.width / 2
        self.y = y - self.rect.height
        self.id = 0
        self.text = None
        self.background = None
        self.width, self.height = self.rect.width, self.rect.height

    def render_text(self, text):  # чтобы через *args принимало текст
        Panel.mother_image.blit(self.background, self.image_pos.topleft)
        space = self.font.size(' ')[0]  # The width of a space.
        x, y = self.padding[0] + self.image_pos[0], self.padding[1] + self.image_pos[1]
        text = text.split(' ')
        word_height = self.font.get_height()
        for i in range(len(text)):
            if text[i] == '/-':  # TODO слэши нормальными сделать
                y += word_height
                x = self.padding[0] + self.image_pos[0]
                continue
            word_surface = self.font.render(text[i], False, self.color)
            word_width = word_surface.get_width()
            if x + word_width - self.image_pos[0] >= self.width:
                x = self.padding[0] + self.image_pos[0]  # Reset x.
                y += word_height  # Start on new row.
            if y + word_height >= self.height:
                new_text = " ".join(text[i:])
                self.text.insert(self.id + 1, new_text)
                break

            Panel.mother_image.blit(word_surface, (x, y))
            x += word_width + space
        textures.update_texture(Panel.mother_image, self.source_id)

    def set_text(self):
        print(self.text)
        self.visible = True
        self.id = 0
        self.render_text(self.text[self.id])

    def next(self):
        if self.id < len(self.text) - 1:
            self.id += 1
            self.render_text(self.text[self.id])
            return True
        self.menu.close_current_panel()

    def open(self, text):
        if type(text[0]).__name__ == 'function':
            self.function = text[0]
            self.text = list(text[0]())
        else:
            self.text = list(text)
        super().open()
        self.background = clip(Panel.mother_image, *self.image_pos)
        self.set_text()

    def do_something(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_k:
                    self.next()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_l:
                    self.hide()

    def update_text(self, text):
        if type(text[0]).__name__ == 'function':
            self.function = text[0]
            self.text = list(text[0]())
        else:
            self.text = list(text)
        self.set_text()

    def update(self, *args):  # TODO апдейты херня чёта
        if self.function is not None:
            self.text = list(self.function())
        self.set_text()


# class ChangingTextPanel(TextPanel):
#     source_id = 4
#     def __init__(self, menu, name, x, y, filename, font, color, padding, *text):
#         super().__init__(menu, name, filename, x, y)


class DialogWindow(TextPanel):
    text = ["asss"]
    person1 = None
    person2 = None
    person1_image = "data/general/player_icon.png"
    show_person1 = False
    show_person2 = False

    def __init__(self, menu, name, x, y, filename, font, color, padding):
        super().__init__(menu, name, x, y, filename, font, color, padding)

    def open(self, text=None, person1=False, person2=False):
        # также открыть окна иконки, если передали.
        DialogWindow.person1 = Panel(None, "person1", DialogWindow.person1_image,
                                     self.rect.right - DialogWindow.person1.rect.width,
                                     self.rect.top - DialogWindow.person1.rect.height)
        DialogWindow.person1.open()
        if DialogWindow.show_person1 is False:
            DialogWindow.person1.hide()
        else:
            DialogWindow.person1.show()

        if text is None:
            super().open(DialogWindow.text)
        else:
            super().open(text)

    def render_text(self, text):
        if text[:11] == "set_person1":
            new_icon = text.split('(')[1].split(')')[0].strip()
            DialogWindow.person1_image = "data/general/" + new_icon + ".png"
            DialogWindow.person1.set_image(DialogWindow.person1_image)
            self.next()
        elif text[:12] == "show_person1":
            print('dsdsdsdsdsww')
            DialogWindow.show_person1 = True
            DialogWindow.person1.show()
            print(DialogWindow.show_person1)
            self.next()
        elif text[:12] == "hide_person1":
            DialogWindow.show_person1 = False
            DialogWindow.person1.hide()
            self.next()
        else:
            super().render_text(text)

    @staticmethod
    def set_dialog_text(*text):
        DialogWindow.text = text

    def close(self):
        DialogWindow.person1.close()
        super().close()


class OptionPanel(TextPanel):
    def __init__(self, menu, name, x, y, filename, font=basic_font, color=(255, 255, 255), padding=(20, 20), *args):
        super().__init__(menu, name, x, y, filename, font, color, padding)
        self.options = args
        self.selected_option = 0
        self.image_copy = None

    def blit_cursor(self):
        x, y = self.image_pos[0] - self.padding[1] + self.width, self.padding[1] + self.image_pos[1]
        Panel.mother_image.blit(self.image_copy, self.image_pos.topleft)
        Panel.mother_image.blit(cursor, (x - cursor.get_width(), y + self.font.get_height() * self.selected_option))
        textures.update_texture(Panel.mother_image, self.source_id)

    def open(self, *args):
        super().open(self.get_options_name())
        self.image_copy = clip(Panel.mother_image, *self.image_pos)
        self.blit_cursor()

    def get_options_name(self):
        text = ""
        for option in self.options:
            text += option[0]
            text += ' /- '
        return [text]

    def scroll_down(self):
        if self.selected_option < len(self.options) - 1:
            self.selected_option += 1
            self.blit_cursor()

    def scroll_up(self):
        if self.selected_option > 0:
            self.selected_option -= 1
            self.blit_cursor()

    def do_selected(self):
        self.visible = True
        if len(self.options) != 0:
            if self.options[self.selected_option][1] == "open_panel":
                self.menu.open_panel(*self.options[self.selected_option][2:])
            else:
                return self.options[self.selected_option][1](*self.options[self.selected_option][2:])

    def do_something(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.scroll_up()
                elif event.key == pygame.K_s:
                    self.scroll_down()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_k:
                    return self.do_selected()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_l:
                    self.hide()

    def open_panel(self, panel_name):
        self.menu.open_panel(panel_name)

    def update(self, *args):
        self.blit_cursor()


class Inventory(OptionPanel):
    selected_item = None

    def __init__(self, menu, name, x, y, filename, font, color, padding):
        options = []
        for item in Player_stats.inventory:
            options.append([item.name])
        super().__init__(menu, name, x, y, filename, font, color, padding, *options)

    def open(self):
        Inventory.selected_item = 0
        options = []
        for item in Player_stats.inventory:
            options.append([item.name])
        self.options = options
        super().open()

    def scroll_up(self):
        super().scroll_up()
        Inventory.selected_item = self.selected_option

    def scroll_down(self):
        super().scroll_down()
        Inventory.selected_item = self.selected_option

    def update(self, *args):
        options = []
        for item in Player_stats.inventory:
            options.append([item.name])
        self.options = options
        self.update_text(self.get_options_name())
        self.set_text()
        self.image_copy = clip(Panel.mother_image, *self.image_pos)
        self.blit_cursor()

    def do_selected(self):
        if len(self.options) != 0:
            self.menu.open_panel("item_actions")


class ItemActions(OptionPanel):
    def __init__(self, menu, name, x, y, filename, font, color, padding):
        self.item = None
        self.item_description = ""

        options = [("description", "open_panel", "itemText"), ("drop", self.drop_item)]
        super().__init__(menu, name, x, y, filename, font, color, padding, *options)

    def hide(self):
        super().hide()
        self.selected_option = 0

    def open(self):
        super().open()
        self.item = Inventory.selected_item
        self.item_description = Player_stats.inventory[self.item].get_description()

    def drop_item(self):
        Player_stats.inventory.pop(Inventory.selected_item)
        self.menu.close_current_panel()

    def update(self, *args):
        self.item = Player_stats.inventory[Inventory.selected_item]
        if self.item is not None:
            self.item_description = self.item.get_description()
        else:
            self.item_description = "Haha monke"
        self.blit_cursor()


class Menu:
    panel_types = {1: OptionPanel, 2: TextPanel, 3: DialogWindow, 4: Inventory, 5: ItemActions}

    def __init__(self, event=None):
        self.event = event
        self.types = {}
        self.panels = dict()
        self.opened_panels = dict()
        self.font = basic_font
        self.route = dict()
        self.current_panel = None
        self.last_panel = None
        self.first_panel_name = None
        self.locked = False

    def lock(self):
        self.locked = True

    def unlock(self):
        print('dsadafwwefwrere')
        self.locked = False

    def set_current_panel(self, panel):
        self.current_panel = panel

    def back(self):  # обновлять предыдущую панель при переходе назад
        if self.current_panel.last_panel is None:
            self.close()
        else:
            self.current_panel.hide()
            self.current_panel = self.current_panel.last_panel
            self.current_panel.show()

    def add_option_panel(self, name, template_name, x, y, previous, *options):
        if len(self.panels.keys()) == 0:
            self.first_panel_name = name
        self.panels[name] = {"type": 1, "template": template_name, "previous": previous, "pos": (x, y), "options": options}
        self.route[name] = self.route.setdefault(name, previous)

    def add_text_panel(self, name, template_name, x, y, previous, *text):
        if len(self.panels.keys()) == 0:
            self.first_panel_name = name
        self.panels[name] = {"type": 2, "template": template_name, "previous": previous, "pos": (x, y), "text": text}
        self.route[name] = previous

    def add_dialog_window(self, name, template_name, x, y, previous):
        if len(self.panels.keys()) == 0:
            self.first_panel_name = name
        self.panels[name] = {"type": 3, "template": template_name, "previous": previous, "pos": (x, y)}
        self.route[name] = previous

    def add_inventory_panel(self, name, template_name, x, y, previous):
        if len(self.panels.keys()) == 0:
            self.first_panel_name = name
        self.panels[name] = {"type": 4, "template": template_name, "previous": previous, "pos": (x, y)}
        self.route[name] = previous

    def add_item_actions_panel(self, name, template_name, x, y, previous):
        if len(self.panels.keys()) == 0:
            self.first_panel_name = name
        self.panels[name] = {"type": 5, "template": template_name, "previous": previous, "pos": (x, y)}
        self.route[name] = previous

    def add_panel(self, type, name, template_name, x, y, previous, *args):
        if len(self.panels.keys()) == 0:
            self.first_panel_name = name
        self.panels[name] = {"type": type, "template": template_name, "previous": previous, "pos": (x, y)}
        self.route[name] = previous

    def open_panel(self, panel_name):  # имя панели которое есть в системе данного меню
        if self.current_panel is not None:
            self.current_panel.hide()
        panel_args = self.panels[panel_name]
        template = templates[panel_args["template"]]
        try:
            self.opened_panels[panel_name].show()
            self.opened_panels[panel_name].update()
        except KeyError:
            if panel_args["type"] == 1:
                self.opened_panels[panel_name] = self.opened_panels.setdefault(panel_name, OptionPanel(self, panel_name, *panel_args["pos"], *template[1:], *panel_args["options"]))
                self.opened_panels[panel_name].open()
            elif panel_args["type"] == 2:
                self.opened_panels[panel_name] = self.opened_panels.setdefault(panel_name, TextPanel(self, panel_name, *panel_args["pos"], *template[1:]))
                self.opened_panels[panel_name].open(panel_args["text"])
            elif panel_args["type"] == 3:
                self.opened_panels[panel_name] = self.opened_panels.setdefault(panel_name, DialogWindow(self, panel_name, *panel_args["pos"], *template[1:]))
                self.opened_panels[panel_name].open()
            elif panel_args["type"] == 4:
                self.opened_panels[panel_name] = self.opened_panels.setdefault(panel_name, Inventory(self, panel_name, *panel_args["pos"], *template[1:]))
                self.opened_panels[panel_name].open()
            elif panel_args["type"] == 5:
                self.opened_panels[panel_name] = self.opened_panels.setdefault(panel_name, ItemActions(self, panel_name, *panel_args["pos"], *template[1:]))
                self.opened_panels[panel_name].open()
        self.current_panel = self.opened_panels[panel_name]

    def close_current_panel(self):
        if self.current_panel is not None:
            self.current_panel.hide()
            panel_name = self.route[self.current_panel.name]
            if panel_name is not None:
                self.current_panel = self.opened_panels[panel_name]
                self.current_panel.update()
                self.current_panel.show()
            else:
                self.close()

    def open(self):
        self.event(True)
        self.open_panel(self.first_panel_name)

    def set_first_panel(self, name):
        self.first_panel_name = name

    # def close(self):
    #     self.event(False)
    #     self.current_panel = None
    #     for panel in self.opened_panels.values():
    #         panel.hide()

    # def set_current_panel(self, name, previous, x, y, *options):
    #     self.current_panel = self.panels[name]

    def get_panel(self, panel_name):
        try:
            return self.opened_panels[panel_name]
        except KeyError:
            print("No")

    def do_something(self, events):
        if self.locked is False:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.close_current_panel()
                    elif event.key == pygame.K_UP:
                        self.close()
                    else:
                        if self.current_panel is not None:
                            self.current_panel.do_something(events)

    def close(self):
        self.event(False)
        self.current_panel = None
        for panel in self.opened_panels.values():
            panel.close()
        self.opened_panels.clear()
        Panel.clear_atlas()

    @staticmethod
    def add_new_panel_type(self, panel_class):
        pass


def item_text():
    return [Player_stats.inventory[Inventory.selected_item].get_description()]


def add_panel(name, filename):
    templates[name] = (0, filename)


def add_text_panel_template(name, filename, font=basic_font, color=(255, 255, 255), padding=(20, 20)):
    templates[name] = (2, filename, font, color, padding)


def add_option_panel_template(name, filename, font=basic_font, color=(255, 255, 255), padding=(20, 20)):
    templates[name] = (1, filename, font, color, padding)


# text_panel.hide()

templates = dict()
add_text_panel_template("textPanel1", "data/general/dialog_window.png")
add_option_panel_template("optionPanel1", "data/general/panel.png")
add_option_panel_template("itemActions", "data/general/item_actions_image.png")

# text_panel = DialogWindow(200, 700, "data/general/dialog_window.png")

player_menu = Menu(Events.set_menu_event)
dialog_menu = Menu(Events.set_text_event)


cursor = pygame.Surface((font_size, font_size))
cursor_rect = cursor.get_rect()
pygame.draw.polygon(cursor, (255, 255, 255), (cursor_rect.midleft, cursor_rect.topright, cursor_rect.bottomright))

start_panel_name = "Start"
inventory_name = "Inventory"

player_menu.add_option_panel(start_panel_name, "optionPanel1", 1520, 0, None, ("inventory", "open_panel", inventory_name))

player_menu.add_inventory_panel(inventory_name, "optionPanel1", 1520, 0, start_panel_name)
player_menu.add_item_actions_panel("item_actions", "itemActions", 1000 - 400, 0, inventory_name)

player_menu.add_text_panel("itemText", "textPanel1", 656, 296, "item_actions", item_text)


dialog_menu.add_dialog_window("Dialog window", "textPanel1", 200, 700, None)

player_icon_panel = Panel(None, "player_icon", "data/general/player_icon.png", 0, 0)

DialogWindow.person1 = player_icon_panel

# player_menu.open_panel("text")
# player_menu.open_panel("inventory")


#
# item_actions = ItemActions(basic_font, 1000 - 200, 0)
# #
# inventory = Inventory(basic_font, 1000, 0)

# last_panel = None
# current_panel = None

# text_panel.open(None, "W A S D - move  |  Right - leaf through text panel/interaction | Up - open/close Inventory. "
#                       "This game about common peoples and psychics who are struggle with hard destiny and try to survive in cruel world. "
#                       "You may encounter anything. From aliens to devils. /- From homeless people to secret organizations."
#                       "From drug dealers to ancient cults. From peaceful and funny situations to incredibly creepy and hopeless",
#                       "wow next text sign", "-Sign Painter")

# menu = Menu()
#
# menu.set_current_panel(inventory)

# text_panel2 = TextPanel2("data/general/dialog_window.png", basic_font)
# text_panel2.open(200, 300, ["ass"])


# item_actions.last_panel = inventory


# panel = Panel2("data/general/dialog_window.png")
# panel.open(200, 200)

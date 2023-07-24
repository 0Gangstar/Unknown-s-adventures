from Player_stats import inventory

class Events:
    text_event = False
    saving_event = False
    transition_event = False
    pause_event = False
    menu_event = False
    option_event = False
    map_showing = True

    @staticmethod
    def set_text_event(condition: bool):
        Events.text_event = condition

    @staticmethod
    def set_saving_event(condition: bool):
        Events.saving_event = condition

    @staticmethod
    def set_transition_event(condition: bool):
        Events.transition_event = condition

    @staticmethod
    def set_pause_event(condition: bool):
        Events.pause_event = condition

    @staticmethod
    def set_menu_event(condition: bool):
        Events.menu_event = condition

    @staticmethod
    def set_option_event(condition: bool):
        Events.menu_event = condition


class Events2:
    def __init__(self):
        self.text_event = False
        self.saving_event = False
        self.transition_event = False
        self.pause_event = False
        self.menu_event = False
        self.option_event = False
        self.names = {"text_event": self.text_event, "saving_event": self.saving_event,
                      "transition_event": self.text_event, "pause_event": self.saving_event,
                      "menu_event": self.text_event, "options_event": self.saving_event}
        self.map_showing = True
        self.game_events = {"ded_psycho_talk": False}

    def set_game_event(self, name, condition: bool):
        self.game_events[name] = condition

    def get_game_event(self, name):
        return self.game_events[name]

    def set_event(self, name, condition: bool):
        self.names[name] = condition

    def set_text_event(self, condition: bool):
        self.text_event = condition

    def set_saving_event(self, condition: bool):
        self.saving_event = condition

    def set_transition_event(self, condition: bool):
        self.transition_event = condition

    def set_pause_event(self, condition: bool):
        self.pause_event = condition

    def set_menu_event(self, condition: bool):
        self.menu_event = condition

    def set_option_event(self, condition: bool):
        self.menu_event = condition

    def set_map_showing(self, condition):
        self.map_showing = condition

    @staticmethod
    def have_item(name):
        for item in inventory:
            if item.name == name:
                return True
        return False

    def check_function(self, name, params):
        for func in self.__dict__.keys():
            if func == name:
                self.__dict__[name](params)


events = Events2()

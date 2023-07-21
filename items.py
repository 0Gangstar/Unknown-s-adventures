all_items = dict()


class Item:

    def __init__(self, name, size, description, image, droppable=True):
        self.name = name
        self.size = size
        self.description = description
        self.image = image
        self.droppable = droppable
        all_items[self.name] = self

    def info(self):
        return "name: " + self.name + " size: " + str(self.size) + self.description

    def get_description(self):
        return self.description


class UseableItem(Item):
    def __init__(self, name, size, description):
        super().__init__(name, size, description, None)

    def use(self):
        pass


class Equipment(Item):
    def __init__(self, name, size, description, offence=0, defense=0):
        super().__init__(name, size, description, None)
        self.attack_bonus = offence
        self.defense_bonus = defense

    def info(self):
        return "name: " + self.name + " size: " + str(self.size) + " attack: " + str(self.attack_bonus) + " defense: " + str(self.defense_bonus) + ' /- ' \
               + self.description

apple = UseableItem('apple', 2, "Обычное белое яблоко...")
bat = Equipment('bat', 5, "Для разбивания чьих-нубудь арбузов", 5, 0)
shovel = Item('shovel', 2, "Единственная, кто подарит крышу над головой", None, False)
ticket = Item('ticket', 1, "Сегодня состоится выступление в приезжем цирке! Приходите на поле рядом с кладбищем в 23.00! Вроде грустно, а вроде и смешно.", None, False)
seeds = Item("flower seeds", 2, "То что надо, чтобы наполнить жизнью даже самое мёртвое место", None, False)
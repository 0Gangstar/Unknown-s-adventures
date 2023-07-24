class Menu:
    def __init__(self, filename, font, x, y):

        self.font = font
        self.inventory = Inventory(filename, font, x, y)

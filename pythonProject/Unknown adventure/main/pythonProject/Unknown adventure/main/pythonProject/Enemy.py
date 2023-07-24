from settings import *
from Player import player
from BaseCharacter import SuperBaseCharacter
from math import sqrt


class Enemy(SuperBaseCharacter):
    folder = enemy_folder
    property = dict()
    source_id = 6

    def __init__(self, template_name, x, y, name=None):
        super().__init__(template_name, x, y, name)
        self.own_speed = self.property[template_name]["speed"]
        self.vision = self.property[template_name]["vision"] * 64  # TODO
        self.type = self.property[template_name]["type"]
        print(self.hit_polygon, self.rect, 'aass')

    def execute_commands(self):
        # TODO чекать перед этим, находится ли игрок в квадратном радиусе
        if (self.hit_polygon.centerx - player.hit_polygon.centerx) <= self.vision and (self.hit_polygon.centery - player.hit_polygon.centery) and \
                sqrt((self.hit_polygon.centerx - player.hit_polygon.centerx)**2 + (self.hit_polygon.centery - player.hit_polygon.centery) ** 2) <= self.vision:
            if player.hit_polygon.left > self.hit_polygon.centerx:
                self.set_sight_side(RIGHT)
            elif player.hit_polygon.right < self.hit_polygon.centerx:
                self.set_sight_side(LEFT)
            elif player.hit_polygon.bottom > self.hit_polygon.centery:
                self.set_sight_side(DOWN)
            elif player.hit_polygon.top < self.hit_polygon.centery:
                self.set_sight_side(UP)
            self.speed = self.own_speed
            self.move()
        else:
            self.speed = 0
        # if self.hit_polygon.colliderect(player.hit_polygon):
        #     player.get_damage(30)

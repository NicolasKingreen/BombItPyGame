import pygame
from random import randint

from unit import Unit
from fraction import Fraction


class Level:
    def __init__(self):

        self.units = []
        for _ in range(50):
            x = randint(0, 640)
            y = randint(0, 480)
            self.units.append(Unit(self, (x, y), Fraction.RED))

        for _ in range(50):
            x = randint(0, 640)
            y = randint(0, 480)
            self.units.append(Unit(self, (x, y), Fraction.GREEN))

    def update(self, frame_time_s):
        for unit in self.units:
            unit.update(frame_time_s)

    def draw(self, surface):
        for unit in self.units:
            unit.draw(surface)

    def get_units_around(self, pos):
        DETECTION_RANGE = 100
        units = []
        for unit in self.units:
            if unit.pos.distance_to(pos) < DETECTION_RANGE:
                units.append(unit)
        return units

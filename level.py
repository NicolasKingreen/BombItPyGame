import pygame
from random import randint

from unit import Unit


class Level:
    def __init__(self):

        self.units = []
        for _ in range(50):
            x = randint(0, 640)
            y = randint(0, 480)
            self.units.append(Unit((x, y)))

    def update(self, frame_time_s):
        for unit in self.units:
            unit.update(frame_time_s)

    def draw(self, surface):
        for unit in self.units:
            unit.draw(surface)

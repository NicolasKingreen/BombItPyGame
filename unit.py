import pygame
from pygame.math import Vector2
from random import randint

from state_machine import StateMachine, State


class UnitStateExploring(State):

    def __init__(self, unit):
        super().__init__("exploring")
        self.unit = unit

    def do_actions(self):
        if randint(1, 300) == 1:
            self.unit.set_random_destination()

    def check_conditions(self):
        pass

    def entry_actions(self):
        self.unit.speed = 200 + randint(-50, 50)


class Unit:

    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.speed = 200
        self.destination = None

        self.brain = StateMachine()

    def update(self, frame_time_s):
        self.brain.think()
        if self.destination:
            move_dir_vector = (self.destination - self.pos).normalized()
            self.pos += move_dir_vector * self.speed * frame_time_s
            if (self.destination - self.pos).magnitude() < 5:
                self.destination = None

    def draw(self, surface):
        pygame.draw.circle(surface, (241, 89, 82), self.pos, 2)

    def set_random_destination(self):
        dx = randint(-150, 150)
        dy = randint(-150, 150)
        self.destination = self.pos + Vector2(dx, dy)


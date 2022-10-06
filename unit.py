import pygame
from pygame.math import Vector2
from random import randint

from state_machine import StateMachine, State

from fraction import Fraction
from colors import *

DEFAULT_SPEED = 50


class UnitStateIdling(State):

    def __init__(self, unit):
        super().__init__("idling")
        self.unit = unit

    def do_actions(self):
        pass

    def check_conditions(self):
        if randint(1, 100) <= 3:
            return "exploring"

    def entry_actions(self):
        self.unit.destination = None


class UnitStateExploring(State):

    def __init__(self, unit):
        super().__init__("exploring")
        self.unit = unit

    def do_actions(self):
        if randint(1, 500) <= 1:
            self.unit.set_random_destination()

    def check_conditions(self):
        # if sees an enemy
        for unit in self.unit.level.get_units_around(self.unit.pos):
            if unit.team_tag != self.unit.team_tag:
                self.unit.target = unit
                return "seeking"

        # randomly becomes idle
        if randint(1, 1000) <= 3:
            return "idling"

    def entry_actions(self):
        self.unit.speed = DEFAULT_SPEED + randint(-50, 50)


class UnitStateSeeking(State):

    def __init__(self, unit):
        super().__init__("seeking")
        self.unit = unit

    def do_actions(self):
        self.unit.destination = self.unit.target.pos
        target_vector = self.unit.destination - self.unit.pos
        move_dir = target_vector.normalize() if target_vector else target_vector

    def check_conditions(self):
        SEEKING_RANGE = 100
        if (self.unit.destination - self.unit.pos).magnitude() > SEEKING_RANGE:
            return "idling"

        if (self.unit.destination - self.unit.pos).magnitude() < 5:
            # fighting state
            pass

    def entry_actions(self):
        self.unit.speed = DEFAULT_SPEED + randint(25, 50)


class Unit:

    def __init__(self, level, pos, team_tag=Fraction.RED):
        self.level = level
        self.pos = Vector2(pos)
        self.speed = DEFAULT_SPEED
        self.destination = None

        self.brain = StateMachine()
        self.brain.add_state(UnitStateExploring(self))
        self.brain.add_state(UnitStateIdling(self))
        self.brain.add_state(UnitStateSeeking(self))
        self.brain.set_state("idling")

        self.team_tag = team_tag
        self.target = None

    def update(self, frame_time_s):
        self.brain.think()
        if self.destination is not None:
            move_dir = self.destination - self.pos
            move_dir and move_dir.normalize_ip()
            self.pos += move_dir * self.speed * frame_time_s
            if (self.destination - self.pos).magnitude() < 5:
                self.destination = None

    def draw(self, surface):
        color = (0, 0, 0)
        if self.team_tag == Fraction.RED:
            color = CINNABAR
        elif self.team_tag == Fraction.GREEN:
            color = DODGER_BLUE
        pygame.draw.circle(surface, color, self.pos, 2)

    def set_random_destination(self):
        dx = randint(-150, 150)
        dy = randint(-150, 150)
        destination = self.pos + Vector2(dx, dy)
        while destination.x < 0 or \
                destination.x > 640 or \
                destination.y < 0 \
                or destination.y > 480:
            dx = randint(-150, 150)
            dy = randint(-150, 150)
            destination = self.pos + Vector2(dx, dy)
        self.destination = destination


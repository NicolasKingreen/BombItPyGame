import pygame
from pygame.locals import *

from level import Level


WIN_SIZE = 640, 480


class Game:
    def __init__(self):
        pygame.display.set_caption("Bomb It")
        self.surface = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.is_running = False

        self.level = Level()

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick()
            frame_time_s = frame_time_ms / 1000.

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()

            # updates
            self.level.update(frame_time_s)

            # drawings
            self.surface.fill((232, 232, 232))
            self.level.draw(self.surface)
            pygame.display.update()

    def terminate(self):
        self.is_running = False


if __name__ == '__main__':
    Game().run()

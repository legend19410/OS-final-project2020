import pygame
from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

class RR:

    def __init__(self, window):
        self.window = window

        # Configuring surface
        self.background = pygame.Surface(window.get_size())
        self.background.fill((255, 255, 255))

        # Blit everything to the window
        window.blit(self.background, (0, 0))
        pygame.display.flip()

    def run(self):
        pass

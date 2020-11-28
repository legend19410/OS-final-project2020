import pygame
from libs.OsObj import OsObj

class CPU(OsObj):
    def __init__(self):
        img = pygame.image.load("resources/images/cpu.png")
        super().__init__(img, pygame.font.SysFont(None, 30), (0, 0, 255))
        self.currentProcess = None
        self.setTopLeft(840, 0)

    def draw(self, window):
        # Draw cpu image
        self.rect = window.blit(self.img, self.topLeft())

        # Draw text
        txt = self.font.render("CPU", True, self.color)
        topLeft = self.computeTopLeft(self.center(), txt.get_size())
        window.blit(txt, topLeft)

import pygame
from libs.OsObj import OsObj

class CPU(OsObj):
    def __init__(self):
        img = pygame.image.load("resources/images/cpu.png")
        super().__init__(img, pygame.font.SysFont(None, 30), (0, 0, 255))
        self.currentProcess = None
        self.setTopLeft(840, 0)
        self.lock = False

    def draw(self, window):
        # Draw cpu image
        self.rect = window.blit(self.img, self.topLeft())

        # Draw text
        txt = self.font.render("CPU", True, self.color)
        topLeft = self.computeTopLeft(self.center(), txt.get_size())
        window.blit(txt, topLeft)

    def execute(self, window, updateWindow):
        """ Decrements the burst time. If the process finishes, \
            lock is set to False """
        self.lock = not self.currentProcess.execute()
        self.currentProcess.draw(window, updateWindow)

    def getProcess(self):
        """ Returns the currently executing process """
        return self.currentProcess

    def setProcess(self, process):
        """ Set the currently executing process """
        self.currentProcess = process

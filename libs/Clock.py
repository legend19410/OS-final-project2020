import pygame
import time
from libs.OsObj import OsObj

class Clock(OsObj):
    def __init__(self, mode="normal"):
        super().__init__(pygame.Rect((900, 700), (100, 100)), \
            pygame.font.SysFont(None, 30))
        self.VALID_MODES = ("normal", "step", "paused")
        self.mode = mode
        self.txt = "Elapsed Time: "
        self.cycles = 0

    def draw(self, window):
        t = self.txt + str(self.cycles) + " ms"
        t = self.font.render(t, True, self.txtColor)
        width, height = window.get_size()
        x = width - t.get_width() - 10
        y = height - t.get_height() - 10
        window.blit(t, (x, y))

        if (self.mode == "step"):
            t = "Mode: " + self.mode
            t = self.font.render(t, True, self.txtColor)
            y -= (t.get_height() + 10)
            window.blit(t, (x, y))
    
    def getMode(self):
        """ Returns the current mode of the clock """
        return self.mode

    def setMode(self, mode):
        """ Sets the mode of the clock """

        if (mode in self.VALID_MODES):
            self.mode = mode
        else:
            raise Exception("Not a valid clock mode: " + str(mode))

    def increment(self):
        """ Increments the cycle by 1. If mode is set to 'step', 
            the user must press space to continue """

        if (self.mode == "step"):
            i = None
            while(i == None):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        i = event.unicode
                time.sleep(0.1)
        self.cycles += 1

    def getTime(self):
        """ Returns the number of cycles elapsed """
        return self.cycles

import pygame
from libs.OsObj import OsObj

class Clock(OsObj):
    def __init__(self, mode):
        super().__init__(pygame.Rect((900, 700), (100, 100)), \
            pygame.font.SysFont(None, 30))
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

    def increment(self):
        """ Increments the cycle by 1. If mode is set to 'step', 
            the user must press space to continue """

        if (self.mode == "step"):
            i = None
            while(i == None):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        i = event.unicode

        self.cycles += 1

    def getTime(self):
        """ Returns the number of cycles elapsed """
        return self.cycles

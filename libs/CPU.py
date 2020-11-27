import pygame

class CPU:

    def __init__(self):
        self.currentProcess = None
        self.color = (255, 255, 255)  # red color
        self.x_pos = 840
        self.y_pos = 0
        self.width = 120
        self.height = 400
        self.font = pygame.font.SysFont(None, 30)
        self.cpu_image = pygame.image.load("resources/images/cpu.png")

    def draw(self, window):
        """ Draw an outline of the cpu and make it invisible by making the color white
            Also draw the cpu image """

        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)
        txt = self.font.render("CPU", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 35, self.y_pos + 200])

        # Draw cpu image
        window.blit(self.cpu_image, (825, 0))
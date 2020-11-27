import pygame

class Queue:

    def __init__(self):
        self.queue = []
        self.color = (255, 0, 0)  # red color
        self.x_pos = 300
        self.y_pos = 40
        self.width = 420
        self.height = 60
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, window):
        """ Draw the queue on the screen """

        # Draw the rectangle to hold 7 processes
        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)

        # Draw the vertical lines for each cell of the queue. 60 is the diameter of a process
        t = self.width//60
        for i in range(1, t+1):
            pygame.draw.line(window, self.color, (self.x_pos+(60*i), self.y_pos),(self.x_pos+(60*i), self.y_pos+self.height))

        # Draw label 'Queue' at the top of the queue
        txt = self.font.render("Queue", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 180, self.y_pos - 25])

    def end_x(self):
        return self.x_pos + self.width

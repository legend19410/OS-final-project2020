import pygame
from libs.OsObj import OsObj

class Queue(OsObj):
    def __init__(self):
        super().__init__(pygame.Rect((300, 40), (420, 60)), \
            pygame.font.SysFont(None, 30), (255, 0, 0))
        self.queue = []
        self.cellWidth = 60

    def draw(self, window):
        """ Draw the queue on the screen """

        # Centering queue relative to window
        self.setCenterX(window.get_width()//2)

        # Draw the rectangle to hold 7 processes
        pygame.draw.rect(window, self.bgColor, self.rect,3)

        # Draw the vertical lines for each cell of the queue
        t = self.width()//self.cellWidth
        for i in range(1, t+1):
            pygame.draw.line(window, self.bgColor, \
                (self.backX() + (self.cellWidth*i), self.topY()), \
                (self.backX() + (self.cellWidth*i), self.topY()+self.height()))

        # Draw label 'Queue' at the top of the queue
        txt = self.font.render("Queue", True, self.txtColor)
        window.blit(txt, self.computeTopLeft(self.center(), txt.get_size(), \
            0, -self.height()//2 - 10))

    def getEndPtr(self):
        """ Returns the x-coordinate of the end of the queue """
        return self.frontX() - self.getLen()*self.cellWidth

    def getLen(self):
        """ Returns the length of the queue """
        return len(self.queue)

    def enqueue(self, process):
        """ Adds a process to the back of the queue """
        self.queue.append(process)

    def dequeue(self, window):
        """ Removes a process from the front of the queue and returns it.
            Returns None if queue is empty """
        try:
            for p in self.queue:
                p.moveRight(self.cellWidth)
            return self.queue.pop(0)
        except IndexError:
            return None

    def shuffleFrom(self, index):
        """ Removes the last process in the queue and places it at the
            index given. Also shuffles down th processes down visually
            leaving room for the end process to be moved in """

        end = self.queue.pop(-1)
        self.queue.insert(index, end)
        for i in range(self.getLen()-1, index, -1):
            p = self.queue[i]
            p.moveLeft(self.cellWidth)

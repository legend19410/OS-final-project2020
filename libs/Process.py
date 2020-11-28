import pygame
from libs.OsObj import OsObj

class Process(OsObj):
    def __init__(self, CPU, queue, id, burstTime):
        img = pygame.image.load("resources/images/exe.png")
        img = pygame.transform.scale(img, (60, 60))
        super().__init__(img, pygame.font.SysFont(None,30), (0, 0, 255))

        self.setTopLeft(30, 70)
        self.CPU = CPU
        self.burstTime = burstTime
        self.queue = queue
        self.stepSize = 30
        self.id = id
        self.label = self.font.render("P" + str(self.id), True, self.color)
        self.inQueue = False
        self.inCPU = False

    def draw(self, window):
        """ Draw all processes on the screen along with their respective
            labels and time remaining on cpu """

        # Draw the image that represents the process
        self.rect = window.blit(self.img, self.topLeft())

        # Draw the label on the process eg 'P1'
        #txt = self.font.render(self.label, True, self.color)
        txt = self.label
        window.blit(txt, self.computeTopLeft(self.center(), txt.get_size()))

        # If the process is in the cpu draw the label just below the cpu
        # otherwise draw it just below the process
        if self.inCPU:
            txt = self.font.render(str(self.burstTime)+"ms", True, self.color)
            window.blit(txt, self.computeTopLeft(self.center(), \
                self.getDims(), 0, self.CPU.height()))
        else:
            txt = self.font.render(str(self.burstTime)+"ms", True, self.color)
            window.blit(txt, self.computeTopLeft(self.center(), \
                self.getDims(), 0, self.height() + 5))

    def advance(self):
        """ Move the process and make it aware if it is in the cpu or queue """

        x, y = self.topLeft()
        x += self.stepSize
        self.setTopLeft(x, y)

        self.isInQueue()
        self.isInCPU()

    def isInQueue(self):
        """ If process is within the bounds of the queue then set it as inQueue. if not
            set inQueue to false and if it was marked as in the queue before, remove it. """

        if (self.queue.rect.collidepoint(self.center())):
            self.inQueue = True
            self.queue.queue.append(self)
        else:
            self.inQueue = False
            self.queue.remove(self)

    def isInCPU(self):
        """ If process is within the bounds of the CPU then set it as inCPU. if not
            set inCPU to false """

        if (self.CPU.rect.collidepoint(self.center())):
            self.inCPU = True
            self.CPU.currentProcess = self
            
            # Centers the process in the CPU
            x, y = self.computeTopLeft(self.CPU.center(), self.getDims())
            self.setTopLeft(x, y)
        else:
            self.inCPU = False
            self.CPU.currentProcess = None

    def moveUp(self, wondow, stepSize):
        self.setY(self.topY() - stepSize)
        self.draw(window)

    def moveDown(self, wondow, stepSize):
        self.setY(self.topY() + stepSize)
        self.draw(window)

    def moveLeft(self, wondow, stepSize):
        self.setX(self.backX() - stepSize)
        self.draw(window)

    def moveRight(self, wondow, stepSize):
        self.setX(self.backX() + stepSize)
        self.draw(window)
    
import pygame
from libs.OsObj import OsObj

class Process(OsObj):
    def __init__(self, ID, aTime, burstTime):
        img = pygame.image.load("resources/images/exe.png")
        img = pygame.transform.scale(img, (60, 60))
        super().__init__(img, pygame.font.SysFont(None,30), (0, 0, 255))

        self.id = ID
        self.arrivalTime = aTime
        self.burstTime = burstTime

        self.setTopLeft(70, 40)
        self.inCPU = False
        self.label = self.font.render("P" + str(self.id), True, self.color)
    
    def execute(self):
        """ Decrements the burst time and returns True if process is complete """
        self.burstTime -= 1
        return self.burstTime == 0

    def draw(self, window, updateWindow):
        """ Draw all processes on the screen along with their respective
            labels and time remaining on cpu """

        # Redraws all the other elements in the window
        updateWindow()

        # Draw the image that represents the process
        self.rect = window.blit(self.img, self.topLeft())

        # Draw the label on the process eg 'P1'
        window.blit(self.label, self.computeTopLeft(self.center(), \
            self.label.get_size()))

        # If the process is in the cpu draw the label just below the cpu
        # otherwise draw it just below the process
        if self.inCPU:
            txt = self.font.render(str(self.burstTime)+"ms", True, self.color)
            window.blit(txt, self.computeTopLeft(self.center(), \
                self.getDims(), 0, 100))
        else:
            txt = self.font.render(str(self.burstTime)+"ms", True, self.color)
            window.blit(txt, self.computeTopLeft(self.center(), \
                self.getDims(), 0, 100))
        pygame.display.update()

    def moveUp(self, stepSize):
        """ Moves the process up by the number of pixels specified """
        self.setY(self.topY() - stepSize)

    def moveDown(self, stepSize):
        """ Moves the process down by the number of pixels specified """
        self.setY(self.topY() + stepSize)

    def moveLeft(self, stepSize):
        """ Moves the process left by the number of pixels specified """
        self.setX(self.backX() - stepSize)

    def moveRight(self, stepSize):
        """ Moves the process right by the number of pixels specified """
        self.setX(self.backX() + stepSize)

    def moveTo(self, window, coord, stepSize, updateWindow):
        """ Moves the process in a straight line to the coordinates specified """
        startX = self.backX()
        startY = self.topY()
        endX, endY = coord
        move = {"x": None, "y": None}

        distX = abs(startX - endX)
        distY = abs(startY - endY)
        stepsX = distX//stepSize
        stepsY = distY//stepSize

        # Ensure an even number of steps are taken
        if (stepsX > stepsY):
            try:
                stepSizeY = distY//stepsX
            except ZeroDivisionError:
                stepSizeY = 0

            stepSizeX = stepSize
            numSteps = stepsX
        elif (stepsX < stepsY):
            try:
                stepSizeX = distX//stepsY
            except ZeroDivisionError:
                stepSizeX = 0

            stepSizeY = stepSize
            numSteps = stepsY
        else:
            stepSizeX = stepSize
            stepSizeY = stepSizeX
            numSteps = stepsX

        try:
            lastStepX = distX%stepSizeX
        except ZeroDivisionError:
            lastStepX = distX

        try:
            lastStepY = distY%stepSizeY
        except ZeroDivisionError:
            lastStepY = distY

        # Ensures that steps go in the right direction
        if (endX > startX):
            move["x"] = self.moveRight
        else:
            move["x"] = self.moveLeft

        if (endY > startY):
            move["y"] = self.moveDown
        else:
            move["y"] = self.moveUp

        # Moves the process
        while (numSteps >= 0):
            move["x"](stepSizeX)
            move["y"](stepSizeY)
            self.draw(window, updateWindow)
            numSteps -= 1
        move["x"](lastStepX)
        move["y"](lastStepY)
        self.draw(window, updateWindow)

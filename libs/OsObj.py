import pygame

class OsObj:
    def __init__(self, body, font, color=(255, 255, 255)):
        if (type(body) == pygame.Surface):
            self.img = body
            self.rect = self.img.get_rect()
        elif (type(body) == pygame.Rect):
            self.rect = body

        self.color = color
        self.font = font

    def frontX(self):
        """ Returns the front x coordinate """
        return self.rect.right

    def backX(self):
        """ Returns the back x coordinate """
        return self.rect.left
    
    def topY(self):
        """ Returns the top y coordinate """
        return self.rect.top

    def bottomY(self):
        """ Returns the bottom y coordinate """
        return self.rect.bottom

    def center(self):
        """ Returns the coordinates of the center """
        return self.rect.center

    def centerX(self):
        """ Returns the x-coordinates of the center """
        return self.rect.centerx

    def centerY(self):
        """ Returns the y-coordinates of the center """
        return self.rect.centery

    def topLeft(self):
        """ Returns the coordinates of the top left corner """
        return self.rect.topleft
    
    def width(self):
        """ Returns the width of the object """
        return self.rect.w

    def height(self):
        """ Returns the height of the object """
        return self.rect.h

    def getDims(self):
        """ Returns the dimensions of the object """
        return self.rect.size



    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y

    def setTopLeft(self, x, y):
        self.rect.topleft = (x,y)

    def setCenterX(self, x):
        self.rect.centerx = x

    def setCenterY(self, y):
        self.rect.centery = y

    def setCenter(self, x, y):
        self.rect.center = (x, y)

    def computeTopLeft(self, center, dimensions, xOff=0, yOff=0):
        """ Computes the top left corner relative to the center given """
        x, y = center
        width, height = dimensions
        x = x - width//2 + xOff
        y = y - height//2 + yOff
        return (x, y)

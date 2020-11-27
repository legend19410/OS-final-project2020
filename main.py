#import sys
import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

from libs.FCFS import FCFS
from libs.RR import RR
#from libs.<> import <>
#from libs.<> import <>

def closeGameOnQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

if __name__ == '__main__':
    #args = sys.argv[1:]
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    run = True

    pygame.init()
    icon = pygame.image.load("resources/images/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Scheduler Simulator")
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    fcfs = FCFS(window)
    rr = RR(window)

    while run:
        pygame.time.Clock().tick(5)  # frame rate 5 frames per second
        run = closeGameOnQuit()  # exit on click the quit button
        fcfs.run()

    pygame.quit()

import sys
import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

from libs.FCFS import FCFS
from libs.RR import RR
from libs.SPN import SPN
#from libs.<> import <>

def closeGameOnQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

if __name__ == '__main__':
    args = sys.argv[1:]
    if (len(args) == 2):
        mode= args[0]
        speed = float(args[1])
    elif (len(args) == 1):
        mode = args[0]
        speed = 0.25
    else:
        mode = "normal"
        speed = 0.25

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    run = True

    pygame.init()
    icon = pygame.image.load("resources/images/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Scheduler Simulator")
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    window.fill((255, 255, 255))

    fcfs = FCFS(window, [(1, 3, 2), (2, 5, 7), (3, 7, 10), (4, 10, 23), \
            (5, 15, 15), (6, 20, 28), (7, 25, 30)])
    rr = RR(window, [(1, 3, 2), (2, 5, 7), (3, 7, 10), (4, 10, 23), \
            (5, 15, 15), (6, 20, 28), (7, 25, 30)])
    spn = SPN(window, [(1, 3, 2), (2, 5, 7), (3, 7, 10), (4, 10, 23), \
            (5, 15, 15), (6, 20, 28), (7, 25, 30)])

    while run:
        pygame.time.Clock().tick(5)  # frame rate 5 frames per second

        fcfs.run(mode, speed)
        rr.run(mode, speed)
        spn.run(mode, speed)

        run = closeGameOnQuit()  # exit on click the quit button
    pygame.quit()

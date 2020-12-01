import sys
import pygame
import time

from libs.menu import menu

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

from libs.FCFS import FCFS
from libs.RR import RR
from libs.SPN import SPN
from libs.SRT import SRT

def closeGameonQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    

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
        speed = 0.15

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    run = True
    text_input2 = ""

    pygame.init()
    icon = pygame.image.load("resources/images/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Scheduler Simulator")
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    window.fill((255, 255, 255))

    default_processes = [(1, 3, 2), (2, 5, 7), (3, 7, 10), (4, 10, 23), \
            (5, 15, 15), (6, 20, 28), (7, 25, 30)]

    fcfs = FCFS(window, default_processes)
    rr = RR(window, default_processes)
    spn = SPN(window, default_processes)
    
    srt = SRT(window, default_processes)
    
    algorithms = {"fcfs":fcfs, "rr":rr, "spn":spn, "srt":srt}
    al_classes = {"fcfs":FCFS, "rr":RR, "spn":SPN, "srt":SRT}
    menu = menu(window)#create menu
    while run:
        pygame.display.set_caption("Scheduler Simulator")
        pygame.time.Clock().tick(10)  # frame rate 5 frames per second

        btn = menu.run()
        if(btn):
            algorithms[btn].run(speed,mode)
            algorithms[btn]=al_classes[btn](window, default_processes) #reinitialize algorithm so if chosen again
                                                                       #it starts fresh
            time.sleep(3)
        closeGameonQuit()  # exit on click the quit button
    # pygame.quit()

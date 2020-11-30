import pygame
import time

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table
from libs.Clock import Clock

class Scheduler:
    def __init__(self, window,processes):
        # Dictionary of processes indexed on arrival time
        self.options_color = (0,0,255)       #blue
        self.hover_color = (0,255,00)
        self.heading_font = pygame.font.Font('freesansbold.ttf',25)
        self.window = window
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_window_size()
        self.speed=0.25
        self.speeds = [1, 0.5, 0.25, 0.15, 0.1, 0.05]

        self.processes = {}
        for id, arrivalTime, burstTime in processes:
            proc = Process(id, burstTime)
            try:
                self.processes[arrivalTime].append(proc)
            except KeyError:
                self.processes[arrivalTime] = [proc]

        self.CPU = CPU()
        self.queue = Queue()
        self.table = Table(processes)
        self.clock = Clock()
        self.window = window

        self.nextProcess = 0
        self.numProcesses = len(processes)
        self.processList = [] # Stores all active processes
        self.finishedProcesses = 0

        self.mode = ""

        self.state = "waiting"
        self.prevState = ""
        self.STATE_DICT = {"waiting": self.waiting, \
            "dequeue": self.dequeue, \
            "enqueue": self.invalidState, \
            "requeue": self.invalidState, \
            "sort": self.invalidState, \
            "execute": self.invalidState}

    def run(self, mode="normal"):
        """ Simulates scheduler using the processes given """

        self.clock.setMode(mode)
        self.updateWindow()
        # Run until all processes have been executed
        while (self.finishedProcesses < self.numProcesses):
            self.stepModeWait()
            self.STATE_DICT[self.state]()
            self.updateWindow()
            self.closeGameOnQuit()
            time.sleep(self.speed)

    def spawnProcess(self):
        """ Spawns a newly arrived process. Sets state to enqueue if successful """

        try:
            new = self.processes[self.clock.getTime()]
            self.processList.extend(new)
            self.state = "enqueue"
        except KeyError:
            return 0

    def waiting(self):
        """ Checks for newly arrived processes and increments the clock """
        self.clock.increment()
        self.spawnProcess()

    def dequeue(self):
        """ Removes a process from the queue and adds it to the CPU for execution """

        # If the CPU isn't busy send a process to be executed
        if (self.CPU.lock):
            self.state = "execute"
        else:
            # Checks if cpu has been updated with the next process
            p = self.CPU.getProcess()
            if ((p == None) or (p.burstTime == 0)):
                if (p != None):      # Catches case where a process arrives as the current one finishes
                    self.processList.remove(self.CPU.getProcess())
                    self.nextProcess -= 1
                    self.finishedProcesses += 1
                p = self.queue.dequeue(self.window)
                if (p == None):     # Returns to waiting state if queue is empty
                    self.state = "waiting"
                    return None
                self.CPU.setProcess(p)

            dist = self.CPU.centerX() - p.centerX()
            if (dist > p.stepSize):
                if (dist <= (self.CPU.width() + p.width())//2):
                    p.inCPU = True
                p.moveRight()
            else:
                x, y = self.CPU.center()
                p.setCenter(x, y)
                self.CPU.lock = True
                self.state = "execute"

    def closeGameOnQuit(self):
        """ Manages closing of the simulator """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def updateWindow(self):
        """ Redraws all the elements on the screen and updates the display """

        self.window.fill((255, 255, 255))
        self.CPU.draw(self.window)
        self.table.draw(self.window)
        self.queue.draw(self.window)
        self.clock.draw(self.window)
        self.generateControlButtons()
        for p in self.processList:
            p.draw(self.window)
        pygame.display.update()
    
    def stepModeWait(self):
        """ Waits on user input before changing state if in the scheduler is in 'step' mode """

        if (self.clock.getMode() == "step"):
            if (self.prevState != self.state):
                print("State: " + self.state)
                print("Time: " + str(self.clock.getTime()))
            while (self.prevState != self.state):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        self.prevState = self.state
                time.sleep(0.1)

    def invalidState(self):
        """ Placeholder method """
        msg = "Plese reassign the method of this state...\n"
        msg += "Current State: " + self.state
        raise Exception(msg)


    def generateControlButtons(self):
        # options_box1 = pygame.Rect((0, 0), (420, 30))
        # options_box1.center = ((self.SCREEN_WIDTH/2),(self.SCREEN_HEIGHT/4))
        options_box2 = pygame.Rect((0, self.SCREEN_HEIGHT-30), (100, 30))
        # options_box2.center = ((self.SCREEN_WIDTH/2),(options_box1.bottom+40))
        options_box3 = pygame.Rect((options_box2.right+20, self.SCREEN_HEIGHT-30), (100, 30))
        # options_box3.center = ((self.SCREEN_WIDTH/2),(options_box2.bottom+40))
        # options_box4 = pygame.Rect((0, 0), (100, 30))
        # options_box4.center = ((self.SCREEN_WIDTH/2),(options_box3.bottom+40))

        # print(options_box1.right)
        

        #display the words in the rectangles
        options_font = pygame.font.Font(None,24)
        speedbtn=self.createButton("SPEED " + str(self.speed), options_box2, options_font,\
            self.hover_color,self.options_color, 3)
        
        pausebtn=self.createButton("PAUSE", options_box3, options_font,\
        self.hover_color,self.options_color, 3)
        
        if (speedbtn):
            cur = self.speeds.index(self.speed)
            if cur == (len(self.speeds)-1):
                self.speed = self.speeds[0]
            else:
                self.speed = self.speeds[cur+1]
        
        if (pausebtn):
            pausebtn=False
            while not pausebtn:
                for event in pygame.event.get():
                    continue
                pausebtn=self.createButton("PAUSE", options_box3, options_font,\
                    self.hover_color,self.options_color, 3)
                pygame.time.Clock().tick(10)  # frame rate 5 frames per second
            

    def createText(self,words, font, colour):
        text = font.render(words, True, colour)
        return text, text.get_rect()

    def createButton(self, words, box, font,color, color2, size):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        event = False
        if box.right > mouse_pos[0] > box.left and box.bottom > mouse_pos[1] > box.top:
                pygame.draw.rect(self.window, color,box,size)
                if clicked[0] == 1:
                    event = True
        else:
            pygame.draw.rect(self.window, color2, box,3)

        box_text, box_surf = self.createText(words, font, color2)
        box_surf.center = box.center
        self.window.blit(box_text, box_surf)
        return event
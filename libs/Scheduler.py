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
        self.input_font = pygame.font.Font('freesansbold.ttf',15)
        self.window = window
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_window_size()
        self.speed=0.15
        self.speeds = [0.5, 0.25, 0.15, 0.1, 0.05, 0.01]
        self.input_text = ""
        self.input_text2 = ""
        self.options_box4 = None
        self.options_box5 = None
        self.playbtntext = "PAUSE"
        self.box4_color = (0,0,255)  
        self.box5_color = (0,0,255) 
        self.input=False
        self.input2=False
        self.lpid = processes[-1][0]+1

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

    def run(self,speed,mode="normal"):
        """ Simulates scheduler using the processes given """
        self.speed = speed
        self.clock.setMode(mode)
        self.updateWindow()
        # Run until all processes have been executed
        
        while (self.finishedProcesses < self.numProcesses):
            # print(self.finishedProcesses, self.numProcesses)
            if not self.clock.getMode()=="paused":
                self.stepModeWait()
                self.STATE_DICT[self.state]()
                self.updateWindow()
                self.getEvents()
                time.sleep(self.speed)
            else:
                self.updateWindow()
                self.getEvents()

    def spawnProcess(self):
        """ Spawns a newly arrived process. Sets state to enqueue if successful """

        try:
            new = self.processes[self.clock.getTime()]
            self.processList.extend(new)
            self.state = "enqueue"
        except KeyError:
            # wait_queue_size = len(self.processesList) - self.finishedProcesses
            wait_queue = self.processList[self.queue.getLen()+1:]
            wait_queue_size = self.finishedProcesses - self.numProcesses
            if (self.queue.isSpaceAvailable() and wait_queue):
                self.state = "enqueue"
                return 1
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
        options_box1 = pygame.Rect((50, self.SCREEN_HEIGHT-230), (180, 30))
        # options_box1.center = ((self.SCREEN_WIDTH/2),(self.SCREEN_HEIGHT/4))
        options_box2 = pygame.Rect((5, self.SCREEN_HEIGHT-30), (102, 30))
        # options_box2.center = ((self.SCREEN_WIDTH/2),(options_box1.bottom+40))
        options_box3 = pygame.Rect((options_box2.right+20, self.SCREEN_HEIGHT-30), (100, 30))
        # options_box3.center = ((self.SCREEN_WIDTH/2),(options_box2.bottom+40))
        self.options_box4 = pygame.Rect((options_box3.left+20,options_box3.top-250), (80, 30))
        self.options_box5 = pygame.Rect((self.options_box4.left-90,self.options_box4.top), (80, 30))

        if self.input:
            self.box4_color = (0,255,0)
        else:
            self.box4_color = (0,0,255)

        if self.input2:
            self.box5_color = (0,255,0)
        else:
            self.box5_color = (0,0,255)

        pygame.draw.rect(self.window, self.box4_color, self.options_box4,1)
        pygame.draw.rect(self.window, self.box5_color, self.options_box5,1)
        # options_box4.center = ((self.SCREEN_WIDTH/2),(options_box3.bottom+40))
        text = self.input_font.render(self.input_text, True, (0,0,0))
        self.window.blit(text, (self.options_box4.left+5,self.options_box4.top+5))

        text2 = self.input_font.render(self.input_text2, True, (0,0,0))
        self.window.blit(text2, (self.options_box5.left+5,self.options_box5.top+5))

        ihf = pygame.font.Font('freesansbold.ttf',15)
        input_heading = ihf.render("Burst Time", True, (0,0,255))
        self.window.blit(input_heading, (self.options_box4.left,self.options_box4.top-20) )
        input_heading = ihf.render("Arrive Time", True, (0,0,255))
        self.window.blit(input_heading, (self.options_box5.left,self.options_box5.top-20) )

        pidl = pygame.font.Font('freesansbold.ttf',20)
        input_label = pidl.render("P"+str(self.lpid), True, (0,0,255))
        self.window.blit(input_label, (self.options_box5.left-40,self.options_box5.top+5) )
        
        ihf2 = pygame.font.Font('freesansbold.ttf',23)
        ih2 = ihf2.render("Add Processes", True, (0,0,255))
        self.window.blit(ih2, (self.options_box5.left,self.options_box4.top-50) )
    
        # self.options_box4.width = max(2, text.get_width()+5)

        # print(options_box1.right)
        

        #display the words in the rectangles
        options_font = pygame.font.Font(None,24)
        speedbtn=self.createButton("SPEEDx" + str(round(0.15/self.speed,2)), options_box2, options_font,\
            self.hover_color,self.options_color, 3)
        
        pausebtn=self.createButton(self.playbtntext, options_box3, options_font,\
        self.hover_color,self.options_color, 3)

        okbtn=self.createButton("OK", options_box1, options_font,\
        self.hover_color,self.options_color, 3)        
        
        if (speedbtn):     #if speed button is pressed
            cur = self.speeds.index(self.speed)
            if cur == (len(self.speeds)-1):
                self.speed = self.speeds[0]
            else:
                self.speed = self.speeds[cur+1]
        
        if (pausebtn):         #if paused button is pressed
            pausebtn=False
            if not self.clock.getMode() == "paused":
                self.clock.setMode("paused")
                self.playbtntext = "PLAY"
            else:
                self.clock.setMode("normal")
                self.playbtntext = "PAUSE"
        
        if (okbtn):    #if ok btn is pressed
            try:
                arrive_time = int(self.input_text2)
                burst_time = int(self.input_text)
                # arrive_time = self.clock.getTime()+1
                if(arrive_time and burst_time):
                    if arrive_time > self.clock.getTime():
                        new = Process(self.lpid, burst_time)
                        try:
                            self.processes[arrive_time].append(new)
                        except KeyError:
                            self.processes[arrive_time] = [new]

                        self.numProcesses = self.calculateNumProcesses()
                        # print(self.numProcesses)
                        self.table.updateProcessTable((self.lpid,arrive_time, burst_time))
                        self.lpid+=1
                        self.input_text = ""
                        self.input_text2 = ""
            except:
                pass
    def calculateNumProcesses(self):
        """Calculate the number of processes remaining"""
        total = 0
        for processList in self.processes.values():
            total+=len(processList)
        return total

    def createText(self,words, font, colour):
        """create text"""
        text = font.render(words, True, colour)
        return text, text.get_rect()

    def createButton(self, words, box, font,color, color2, size):
        """create buttons for input"""
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
    
    def getEvents(self):
        """Gets all events and updates parameters"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.options_box4.collidepoint(event.pos):
                    self.input = True
                else:
                    self.input = False
                
                if self.options_box5.collidepoint(event.pos):
                    self.input2 = True
                else:
                    self.input2 = False
                
                time.sleep(0.1)

            if event.type == pygame.KEYDOWN:
                if self.input:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    self.input_text+=event.unicode

                if self.input2:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text2 = self.input_text2[:-1]
                    self.input_text2+=event.unicode
        time.sleep(0.05)

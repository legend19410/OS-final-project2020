import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table
from libs.Clock import Clock

class Scheduler:
    def __init__(self, window, mode, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        #(process ID, arrival time, burst time)

        # Dictionary of processes indexed on arrival time
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
        self.clock = Clock(mode)
        self.window = window

        self.nextProcess = 0
        self.numProcesses = len(processes)
        self.processList = [] # Stores all active processes
        self.finishedProcesses = 0

        self.state = "waiting"
        self.STATE_DICT = {"waiting": self.waiting, \
            "dequeue": self.dequeue, \
            "enqueue": self.inValidState, \
            "requeue": self.inValidState, \
            "sort": self.inValidState, \
            "execute": self.inValidState}

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
        for p in self.processList:
            p.draw(self.window)
        pygame.display.update()
    
    def spawnProcess(self):
        """ Spawns a newly arrived process. Sets state to enqueue if successful """

        try:
            print(self.clock.getTime())
            new = self.processes[self.clock.getTime()]
            self.processList.extend(new)
            self.state = "enqueue"
        except KeyError:
            pass

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
            if (p == None):
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

    def inValidState(self):
        """ Placeholder method """
        msg = "Plese reassign the method of this state...\n"
        msg += "Current State: " + self.state
        raise Exception(msg)

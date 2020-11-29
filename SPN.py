from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table
from libs.Clock import Clock
from libs.Scheduler import Scheduler

class RR(Scheduler):
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        super().__init__(window, processes)
        self.STATE_DICT.update({"enqueue": self.enqueue,\
            "execute": self.execute})
        self.movingUp = False               #these are for the requeue functions
        self.movingRight = False            #these are for the requeue functions

    def enqueue(self):
        """ Adds a newly spaawned process to the queue """

        p = self.processList[self.nextProcess]
        back = self.queue.getEndPtr()
        if (p.frontX() < back):
            dist = back - p.frontX()
            if (dist > p.stepSize):
                p.moveRight()
            else:
                p.moveRight(dist)
                self.queue.enqueue(p)
                self.nextProcess += 1
                if (self.nextProcess == len(self.processList)):
                    self.state = "dequeue"

    def execute(self):
        """ Decrements the burst time of the current process and interrupts
            execution if the time slice has been exhausted"""

        if (not self.CPU.lock):                 # The process finished before the time slice
            self.processList.remove(self.CPU.getProcess())
            self.nextProcess -= 1
            self.CPU.setProcess(None)
            self.finishedProcesses += 1
            self.state = "dequeue"
        elif (self.timeBeforeInterrupt == 0):   # The time slice finished before the process
            self.state = "requeue"
        else:                                   # The process still has time to execute
            self.CPU.execute()
            self.clock.increment()
            self.timeBeforeInterrupt -= 1
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
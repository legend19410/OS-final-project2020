import time
import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table
from libs.Scheduler import Scheduler

class FCFS(Scheduler):
    def __init__(self, window, mode="normal"):
        super().__init__(window, mode)
        self.STATE_DICT.update({"enqueue": self.enqueue, \
            "execute": self.execute})

    def run(self):
        """ Simulates scheduler using the processes given """

        # Run until all processes have been executed
        while (self.finishedProcesses < self.numProcesses):
            print(self.state)
            self.STATE_DICT[self.state]()
            self.updateWindow()
            self.closeGameOnQuit()
            time.sleep(0.1)

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
        """ Executes the current process to completion before removing
            the process from the cpu and releasing the lock """

        if (self.CPU.lock):
            self.CPU.execute()
            self.clock.increment()
            self.spawnProcess()
        else:
            self.processList.remove(self.CPU.getProcess())
            self.CPU.setProcess(None)
            self.finishedProcesses += 1
            print("\t\tFin count: " + str(self.finishedProcesses) + \
                "\t" + str(self.clock.getTime()))
            self.state = "dequeue"

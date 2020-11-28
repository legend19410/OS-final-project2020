import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table
from libs.Scheduler import Scheduler

class FCFS(Scheduler):
    def __init__(self, window):
        super().__init__(window)
        self.processList = []       # store all created processes
        self.lock = False

    def run(self):
        self.updateWindow()

        self.createProcess()
        self.drawAllProcesses()
        self.moveProcesses()
        self.executeProcess()

        pygame.display.update()
        self.time += 0.25

    def createProcess(self):
        """ Check the arrival time of each process and create it if arrival
            time match current time """

        for process in self.processes:
            if process[1] == self.time:
                p = Process(self.CPU, self.queue, process[0],process[2])
                self.processList.append(p)

    def drawAllProcesses(self):
        """ Draw all processes on the screen """
        for process in self.processList:
            process.draw(self.window)

    def executeProcess(self):
        """ If lock is true and there is a current process assigned to the
            cpu then decrease that process burst time until it becomes zero
            before removingthe process from the cpu and releasing the lock """

        if self.lock and self.CPU.getProcess():
            self.CPU.getProcess().burstTime -= 1
            if self.CPU.getProcess().burstTime == 0:
                self.processList.remove(self.CPU.getProcess())
                self.lock = False

    def moveProcesses(self):
        """ Iterate over all processes in the process list to determine if
            they can move """

        for i, proc in enumerate(self.processList):
            if proc.frontX() > self.CPU.backX() + 60:  # this stops the process from moving pass the cpu
                continue                            # once pass cpu start pos + the diameter of the process
                                                    # then never move that process again.
            if proc.frontX() == self.queue.frontX():  # if process at the front of the queue
                if not self.lock:                   # if lock not on move process beyond front and set lock to true
                    proc.advance()
                    self.lock = True
                else:
                    pass                           # else dont move
            else:                                  # else process not at front of the queue; worry about process infront
                                                   # this checks if there is a process directly infront. If not move
                if not(self.processList[i-1].backX()-self.processList[i-1].width()//2 == proc.backX()+proc.width()//2):
                    proc.advance()

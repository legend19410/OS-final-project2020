import time
import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table
from libs.Scheduler import Scheduler

class RR(Scheduler):
    def __init__(self, window):
        super().__init__(window)
        self.TIME_QUANTUM = 15
        self.timeBeforeInterrupt = self.TIME_QUANTUM
        self.newProcesses = []
        self.finishedProcesses = []

    def run(self):
        self.updateWindow()
        i = 0
        process = self.processes[i]

        # Run until all processes have been executed
        while (len(self.finishedProcesses) != len(self.processes)):
            pygame.time.Clock().tick(5)  # frame rate 5 frames per second
            print("time: " + str(self.time))

            # Moves process back into the queue if it's time slice is up but
            # it still needs more CPU time
            if (self.timeBeforeInterrupt == 0):
                print("Switch")
                self.timeBeforeInterrupt = self.TIME_QUANTUM

                p = self.CPU.getProcess()
                x, y = p.topLeft()
                y += self.CPU.height()//2
                p.inCPU = False
                p.moveTo(self.window, (x, y), 30, self.updateWindow)

                x = self.queue.backX() - 90
                p.moveTo(self.window, (x, y), 30, self.updateWindow)

                y = self.queue.topY()
                p.moveTo(self.window, (x, y), 30, self.updateWindow)

                x = self.queue.getEndPtr()
                p.moveTo(self.window, (x, y), 30, self.updateWindow)

            # Create the process and move it into the queue
            if (process[1] == self.time):
                print("Process ID: " + str(i))
                p = Process(process[0], process[1], process[2])
                self.newProcesses.append(p)
                p.draw(self.window, self.updateWindow)

                """
                start = p.frontX()
                stop = self.queue.getEndPtr()
                lastStep = (stop - start)%30
                while (p.frontX() < (stop-lastStep)):
                    p.moveRight(30)
                    p.draw(self.window, self.updateWindow)
                p.moveRight(lastStep)
                """

                x = self.queue.getEndPtr()
                y = p.topY()
                p.moveTo(self.window, (x, y), 90, self.updateWindow)

                self.queue.enqueue(p)
                i += 1
                process = self.processes[i]

            # Execute the current process if the CPU is locked otherwise
            # add the current process to the finished queue and move a 
            # new process into the CPU if one is waiting in the queue
            if (self.CPU.lock):
                print("Execute")
                self.CPU.execute(self.window, self.updateWindow)
                self.time += 1
                self.timeBeforeInterrupt -= 1
            else:
                if (self.CPU.getProcess() != None):
                    self.finishedProcesses.append(self.CPU.getProcess())
                    self.CPU.setProcess(None)

                nextProcess = self.queue.dequeue(self.window, self.updateWindow)
                print("Moving to cpu: " + str(nextProcess))
                if (nextProcess != None):
                    while (nextProcess.frontX() < self.CPU.centerX()):
                        if ((not nextProcess.inCPU) and \
                            (nextProcess.frontX() >= self.CPU.backX())):

                            nextProcess.inCPU = True
                        nextProcess.moveRight(30)
                        nextProcess.draw(self.window, self.updateWindow)
                    c = self.CPU.center()
                    nextProcess.setCenter(c[0], c[1])
                    self.CPU.setProcess(nextProcess)
                    self.CPU.lock = True
                    nextProcess.draw(self.window, self.updateWindow)
                print("End Lock")

            # Increment the time if the processor is idle and no new
            # processes have been created
            if ((len(self.newProcesses) == 0) and not self.CPU.lock):
                self.time += 1
            time.sleep(1)
            #window.fill((255, 255, 255))
            pygame.display.update()

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
        self.state = "waiting"
        self.STATE_DICT = {"waiting": self.waiting, \
            "enqueue": self.enqueue, \
            "requeue": self.requeue, \
            "dequeue": self.dequeue, \
            "execute": self.execute}

    def run(self):
        """ Simulates scheduler using the processes given """

        prevState = ""
        # Run until all processes have been executed
        while (self.finishedProcesses < len(self.processes)):
            if (self.state != prevState):
                print("State: " + self.state)
                print("Time: " + str(self.time))
                prevState = self.state

            self.STATE_DICT[self.state]()
            self.updateWindow()
            time.sleep(0.1)

    def spawnProcess(self):
        """ Spawns a newly arrived process """

        try:
            new = self.processes[self.time]
            self.processList.extend(new)
            self.state = "enqueue"
            return 1
        except KeyError:
            return 0

    def waiting(self):
        """ Checks for newly arrived processes and increments the clock """
        self.spawnProcess()
        self.time += 1

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

    def execute(self):
        """ Decrements the burst time of the current process and interrupts
            execution if the time slice has been exhausted"""

        if (not self.CPU.lock):                 # The process finished before the time slice
            self.processList.remove(self.CPU.getProcess())
            self.CPU.setProcess(None)
            self.state = "dequeue"
        elif (self.timeBeforeInterrupt == 0):   # The time slice finished before the process
            self.state = "requeue"
        else:                                   # The process still has time to execute
            self.CPU.execute()
            self.time += 1
            self.timeBeforeInterrupt -= 1
            self.spawnProcess()

    def requeue(self):
        """ Moves the current process back into the queue and updates the CPU """

        p = self.CPU.getProcess()
        down = self.CPU.bottomY() + 10
        left = self.queue.backX() - 90
        up = self.queue.topY()
        right = self.queue.getEndPtr()

        # Move the process down out of the CPU
        if (p.topY() < down):
            if (p.bottomY() >= self.CPU.bottomY()):
                p.inCPU = False
            p.moveDown()

        # Move the process to the left after it has been removed from the queue
        if (p.topY() >= down):
            if (p.backX() > left):
                p.moveLeft()

        # Move process up inline with queue after moving it behind the queue
        print("left: " + str(p.backX() <= left))
        if (p.backX() <= left):
            dist = p.topY() - up

            print("p: " + str(p) + " " + str(self.CPU.getProcess()))
            print("step check: " + str(dist > p.stepSize))
            if (dist > p.stepSize):
                p.moveUp()
            else:
                p.moveUp(dist)

        # Enqueue the process
        print("top: " + str(p.topY() == up))
        if (p.topY() == up):
            dist = right - p.frontX()
            if (dist > p.stepSize):
                p.moveRight()
            else:
                p.moveRight(dist)
                self.queue.enqueue(p)
                self.CPU.setProcess(None)
                self.CPU.lock = False
                if (self.spawnProcess() == 0):
                    self.state = "dequeue"

    """
            print("Len: " + str(len(self.finishedProcesses)))
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
                self.processList.append(p)
                p.draw(self.window, self.updateWindow)

                " " "
                start = p.frontX()
                stop = self.queue.getEndPtr()
                lastStep = (stop - start)%30
                while (p.frontX() < (stop-lastStep)):
                    p.moveRight(30)
                    p.draw(self.window, self.updateWindow)
                p.moveRight(lastStep)
                " " "

                x = self.queue.getEndPtr()
                y = p.topY()
                p.moveTo(self.window, (x, y), 30, self.updateWindow)

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
                        #time.sleep(0.25)
                    c = self.CPU.center()
                    nextProcess.setCenter(c[0], c[1])
                    self.CPU.setProcess(nextProcess)
                    self.CPU.lock = True
                    nextProcess.draw(self.window, self.updateWindow)
                print("End Lock")

            # Increment the time if the processor is idle and no new
            # processes have been created
            if ((len(self.processList) == 0) and not self.CPU.lock):
                self.time += 1
            time.sleep(0.25)
            #window.fill((255, 255, 255))
            pygame.display.update()
    """

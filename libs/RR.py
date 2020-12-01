from libs.Scheduler import Scheduler

class RR(Scheduler):
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        super().__init__(window, processes)
        self.algorithm = "rr"
        self.TIME_QUANTUM = 15
        self.timeBeforeInterrupt = self.TIME_QUANTUM
        self.STATE_DICT.update({"enqueue": self.enqueue, \
            "dequeue": self.dequeue, \
            "requeue": self.requeue, \
            "execute": self.execute})

        # Atributes to save the stte of the requeue operation
        self.movingUp = False
        self.movingRight = False
    
    def setTimeQuantum(self, num):
        """sets the time quantum for round robin"""
        self.TIME_QUANTUM = num

    def enqueue(self):
        """ Adds a newly spaawned process to the queue """
        if self.queue.isSpaceAvailable():
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
        elif self.CPU.lock:
            self.state = "execute"
        else:
            self.state = "dequeue"

    def dequeue(self):
        """ Removes a process from the queue and adds it to the CPU for execution """

        # If the CPU isn't busy send a process to be executed
        if (self.CPU.lock):
            self.state = "execute"
        else:
            # Checks if cpu has been updated with the next process
            p = self.CPU.getProcess()
            if ((p == None) or (p.burstTime == 0)):
                self.timeBeforeInterrupt = self.TIME_QUANTUM
                if (p != None):      # Catches case where a process arrives as the current one finishes
                    self.processList.remove(self.CPU.getProcess())
                    self.nextProcess -= 1
                    self.finishedProcesses += 1
                    self.TT += self.clock.getTime() - p.getArrivalTime()
                    # print()
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

    def execute(self):
        """ Decrements the burst time of the current process and interrupts
            execution if the time slice has been exhausted """

        if (not self.CPU.lock):                 # The process finished before the time slice
            self.TT += self.clock.getTime() - (self.CPU.getProcess()).getArrivalTime()
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

    def requeue(self):
        """ Moves the current process back into the queue and updates the CPU """

        p = self.CPU.getProcess()
        down = self.CPU.bottomY()-20
        left = self.queue.backX() - 90
        up = self.queue.topY()
        right = self.queue.getEndPtr()

        # Move the process down out of the CPU
        if ((p.topY() < down) and (not self.movingUp)):
            if (p.bottomY() >= self.CPU.bottomY()):
                p.inCPU = False
            p.moveDown()

        # Move the process to the left after it has been removed from the queue
        if ((p.topY() >= down) and (not self.movingUp)):
            if (p.backX() > left):
                p.moveLeft()

        # Move process up inline with queue after moving it behind the queue
        if ((p.backX() <= left) and (not self.movingRight)):
            self.movingUp=True
            dist = p.topY() - up
            if (dist > p.stepSize):
                p.moveUp()
            else:
                p.moveUp(dist)

        if (p.topY() == up):
            self.movingRight = True
            dist = right - p.frontX()
            if (dist > p.stepSize):
                p.moveRight()
            else:
                p.moveRight(dist)
                self.queue.enqueue(p)
                self.CPU.setProcess(None)
                self.CPU.lock = False
                self.movingRight = False
                self.movingUp = False                
                if (self.spawnProcess() == 0):
                    self.state = "dequeue"

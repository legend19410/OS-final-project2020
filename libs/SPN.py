from libs.Scheduler import Scheduler

class SPN(Scheduler):
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        super().__init__(window, processes)
        self.STATE_DICT.update({"enqueue": self.enqueue, \
            "execute": self.execute})
        self.target = None
        self.newProcess = None

    def enqueue(self):
        """ Adds a newly spaawned process to the queue """

        if (self.nextProcess == len(self.processList)):
            self.state = "dequeue"
        else:
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
                    self.newProcess = p
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
                if (p != None):      # Catches case where a process arrives as the current one finishes
                    self.processList.remove(self.CPU.getProcess())
                    self.nextProcess -= 1
                    self.finishedProcesses += 1
                p = self.queue.dequeue(self.window, "spn")
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
        """ Executes the current process to completion before removing
            the process from the cpu and releasing the lock """

        if (self.CPU.lock):
            self.CPU.execute()
            self.clock.increment()
            self.spawnProcess()
        else:
            self.processList.remove(self.CPU.getProcess())
            self.nextProcess -= 1
            self.CPU.setProcess(None)
            self.finishedProcesses += 1
            self.state = "dequeue"

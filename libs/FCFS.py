from libs.Scheduler import Scheduler

class FCFS(Scheduler):
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        super().__init__(window, processes)
        self.STATE_DICT.update({"enqueue": self.enqueue, \
            "execute": self.execute})

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
            self.nextProcess -= 1
            self.CPU.setProcess(None)
            self.finishedProcesses += 1
            self.state = "dequeue"

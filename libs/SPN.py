from libs.Scheduler import Scheduler

class SPN(Scheduler):
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        super().__init__(window, processes)
        self.STATE_DICT.update({"enqueue": self.enqueue, \
            "swap": self.swap, \
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
                    self.state = "swap"

    def swap(self):
        """ Sorts the processes in the queue based on burst time """

        p = self.newProcess

        # Search for the appropriate spot for the newly added process
        if (self.target == None):
            self.target = 0
            for q in self.queue.queue:
                if (p.burstTime < q.burstTime):
                    break
                self.target += 1

            # If process is in the right spot, proceed with simulation else reorder the queue
            end = self.queue.getLen()
            if (self.target == end):
                self.target = None
                self.state = "dequeue"
        else:
            down = self.queue.bottomY() + 20
            right = self.queue.frontX() - self.queue.cellWidth * self.target
            up = self.queue.topY()

            # Moves the new process down below the queue
            if ((p.topY() < down) and \
                    (p.frontX() != right)):
                p.moveDown()

            # Moves the new process to the right until it is below the correct cell
            # and shuffle other processes down by one cell
            if ((p.topY() >= down) and \
                    (p.frontX() < right)):
                dist = right - p.frontX()
                if (dist > p.stepSize):
                    p.moveRight()
                else:
                    p.moveRight(dist)
                    self.queue.shuffleFrom(self.target)

            # Move the new process up into the new cell
            if ((p.frontX() == right)):
                dist = p.topY() - up
                if (dist > p.stepSize):
                    p.moveUp()
                else:
                    p.moveUp(dist)
                    self.state = "enqueue"

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

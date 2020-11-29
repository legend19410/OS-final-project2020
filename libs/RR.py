from libs.Scheduler import Scheduler

class RR(Scheduler):
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        super().__init__(window, processes)
        self.TIME_QUANTUM = 15
        self.timeBeforeInterrupt = self.TIME_QUANTUM
        self.STATE_DICT.update({"enqueue": self.enqueue, \
            "requeue": self.requeue, \
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
            execution if the time slice has been exhausted """

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

    def requeue(self):
        """ Moves the current process back into the queue and updates the CPU """

        p = self.CPU.getProcess()
        down = self.CPU.bottomY() + 10
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
        # print("left: " + str(p.backX() <= left))
        if ((p.backX() <= left) and (not self.movingRight)):
            self.movingUp=True
            dist = p.topY() - up

            # print("p: " + str(p) + " " + str(self.CPU.getProcess()))
            # print("p in processList: " + str(p in self.processList))
            # print("step check: " + str(dist > p.stepSize))
            if (dist > p.stepSize):
                print("Moving...")
                p.moveUp()
                print("Moved")
            else:
                # print("Moving 2")
                p.moveUp(dist)
                # print("Moved 2")

        # Enqueue the process
        # print("top process:",p.topY(), "      top q:", up)
        # print("top: " + str(p.topY() == up))
        if (p.topY() == up):
            # print("HEEEEE")
            self.movingRight = True
            dist = right - p.frontX()
            # print("Distance to next queue slot:", dist)
            if (dist > p.stepSize):
                p.moveRight()
                # print("moving right")
            else:
                # print("moving right 2")
                p.moveRight(dist)
                self.queue.enqueue(p)
                self.CPU.setProcess(None)
                self.CPU.lock = False
                self.movingRight = False
                self.movingUp = False                
                if (self.spawnProcess() == 0):
                    self.state = "dequeue"
                    self.timeBeforeInterrupt = self.TIME_QUANTUM

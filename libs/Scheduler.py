from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

class Scheduler:
    def __init__(self, window):
        #(process ID, arrival time, burst time)
        self.processes = [(2,2,32), (3,3,44), (1,5,33), (4,9,27), \
            (5,10,58), (6,20,34), (7,30, 80)]
        self.CPU = CPU()
        self.queue = Queue()
        self.table = Table(self.processes)
        self.window = window
        self.time = 1

    def updateWindow(self):
        self.window.fill((255, 255, 255))
        self.CPU.draw(self.window)
        self.table.draw(self.window)
        self.queue.draw(self.window)

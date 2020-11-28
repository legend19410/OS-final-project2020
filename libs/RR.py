import pygame
from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

class RR:
    def __init__(self, window):
        self.window = window
        self.time = 0
        self.CPU = CPU()
        self.queue = Queue()
        self.lock = False

        #(process ID, arrival time, burst time)
        self.processes = [(1, 3, 2), (2, 5, 7), (3, 7, 10), (4, 10, 23), \
            (5, 15, 15), (6, 20, 28), (7, 25, 30)]
        self.table = Table(self.processes)

        self.newProcesses = []
        self.finishedProcesses = []

    def run(self):
        self.queue.draw(self.window)
        self.CPU.draw(self.window)
        self.table.draw(self.window)
        i = 0
        process = self.processes[i]
        while (len(self.finishedProcesses) != len(self.processes)):
            if (process[1] == self.time):
                print("i: " + str(i))
                print("time: " + str(self.time))
                p = Process(self.CPU, self.queue, process[0], process[2])
                self.newProcesses.append(p)
                p.draw(self.window)
                i += 1
                process = self.processes[i]

            for p in self.newProcesses:
                p.advance()

            if ((len(self.newProcesses) == 0) and not self.lock):
                self.time += 0.25
            pygame.display.update()

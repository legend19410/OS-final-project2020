import pygame

from libs.CPU import CPU
from libs.Process import Process
from libs.Queue import Queue
from libs.Table import Table

class Scheduler:
    def __init__(self, window, processes=[(1,5,33), (2,2,32), \
            (3,3,44), (4,9,27), (5,10,58), (6,20,34), (7,30, 80)]):
        #(process ID, arrival time, burst time)

        # Dictionary of processes indexed on arrival time
        self.processes = {}
        for id, arrivalTime, burstTime in processes:
            proc = Process(id, burstTime)
            try:
                self.processes[arrivalTime].append(proc)
            except KeyError:
                self.processes[arrivalTime] = [proc]

        self.CPU = CPU()
        self.queue = Queue()
        self.table = Table(processes)
        self.window = window
        self.time = 0

        self.nextProcess = 0
        self.processList = [] # Stores all active processes
        self.finishedProcesses = 0

    def updateWindow(self):
        self.window.fill((255, 255, 255))
        self.CPU.draw(self.window)
        self.table.draw(self.window)
        self.queue.draw(self.window)
        for p in self.processList:
            p.draw(self.window)
        pygame.display.update()
